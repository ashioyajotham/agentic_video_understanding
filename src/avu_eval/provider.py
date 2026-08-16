from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import multiprocessing as mp
import os
import queue
import time
from typing import Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # Allows offline unit tests before dependencies are installed.
    pass


@dataclass
class ProviderResult:
    text: str
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    thought_tokens: int | None
    strategy_trace: str | None
    raw_metadata: dict[str, Any]


def _interaction_worker(result_queue, payload: dict[str, Any]) -> None:
    """Run one request in a killable process; required for hard timeouts on Windows."""
    try:
        from google import genai
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        client = genai.Client(api_key=api_key)
        started = time.perf_counter()
        interaction = client.interactions.create(
            model=payload["model"],
            input=[
                {
                    "type": "video",
                    "uri": payload["uri"],
                    "mime_type": payload["mime_type"],
                    "processing": payload["processing"],
                },
                {"type": "text", "text": payload["question"]},
            ],
        )
        usage = getattr(interaction, "usage", None)
        modality_usage = [
            {"modality": str(getattr(item, "modality", "unknown")), "tokens": getattr(item, "tokens", None)}
            for item in (getattr(usage, "input_tokens_by_modality", None) or [])
        ]
        trace = getattr(interaction, "video_processing_strategy", None)
        if trace is None:
            trace = getattr(interaction, "thoughts", None)
        result_queue.put({
            "ok": True,
            "text": interaction.output_text,
            "input_tokens": getattr(usage, "total_input_tokens", None),
            "output_tokens": getattr(usage, "total_output_tokens", None),
            "total_tokens": getattr(usage, "total_tokens", None),
            "thought_tokens": getattr(usage, "total_thought_tokens", None),
            "strategy_trace": str(trace) if trace else None,
            "modality_usage": modality_usage,
            "provider_latency_seconds": time.perf_counter() - started,
        })
    except BaseException as exc:
        result_queue.put({"ok": False, "error": f"{type(exc).__name__}: {exc}"})


class GeminiEAPProvider:
    """Thin adapter kept deliberately isolated because the unreleased SDK may change."""

    def __init__(self, poll_seconds: int = 10, timeout_seconds: int = 180):
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("Install the EAP google-genai wheel before running API experiments") from exc
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        self.client = genai.Client(api_key=api_key)
        self.poll_seconds = poll_seconds
        self.timeout_seconds = timeout_seconds
        self._cache: dict[Path, Any] = {}

    def _upload(self, path: Path):
        path = path.resolve()
        if path in self._cache:
            return self._cache[path]
        uploaded = self.client.files.upload(file=str(path))
        started = time.perf_counter()
        while str(getattr(uploaded, "state", "")).endswith("PROCESSING"):
            if time.perf_counter() - started > self.timeout_seconds:
                raise TimeoutError(f"Video preparation exceeded {self.timeout_seconds} seconds for {path.name}")
            time.sleep(self.poll_seconds)
            uploaded = self.client.files.get(name=uploaded.name)
        if str(getattr(uploaded, "state", "")).endswith("FAILED"):
            raise RuntimeError(f"Video processing failed for {path.name}")
        self._cache[path] = uploaded
        return uploaded

    def prepare(self, path: Path):
        return self._upload(path)

    def ask(self, *, model: str, video: Path, question: str, processing: str) -> ProviderResult:
        uploaded = self._upload(video)
        ctx = mp.get_context("spawn")
        result_queue = ctx.Queue()
        process = ctx.Process(target=_interaction_worker, args=(result_queue, {
            "model": model, "uri": uploaded.uri, "mime_type": uploaded.mime_type,
            "processing": processing, "question": question,
        }))
        process.start()
        process.join(self.timeout_seconds)
        if process.is_alive():
            process.terminate(); process.join(10)
            raise TimeoutError(f"Request exceeded {self.timeout_seconds} seconds")
        try:
            payload = result_queue.get(timeout=5)
        except queue.Empty as exc:
            raise RuntimeError(f"Request worker exited with code {process.exitcode} without a result") from exc
        if not payload["ok"]:
            raise RuntimeError(payload["error"])
        return ProviderResult(
            text=payload["text"],
            input_tokens=payload["input_tokens"],
            output_tokens=payload["output_tokens"],
            total_tokens=payload["total_tokens"],
            thought_tokens=payload["thought_tokens"],
            strategy_trace=payload["strategy_trace"],
            raw_metadata={
                "total_tokens": payload["total_tokens"],
                "thought_tokens": payload["thought_tokens"],
                "input_tokens_by_modality": payload["modality_usage"],
                "provider_latency_seconds": payload["provider_latency_seconds"],
            },
        )
