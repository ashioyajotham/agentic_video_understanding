from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time
from typing import Any


@dataclass
class ProviderResult:
    text: str
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    thought_tokens: int | None
    strategy_trace: str | None
    raw_metadata: dict[str, Any]


class GeminiEAPProvider:
    """Thin adapter kept deliberately isolated because the unreleased SDK may change."""

    def __init__(self, poll_seconds: int = 10):
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("Install the EAP google-genai wheel before running API experiments") from exc
        self.client = genai.Client()
        self.poll_seconds = poll_seconds
        self._cache: dict[Path, Any] = {}

    def _upload(self, path: Path):
        path = path.resolve()
        if path in self._cache:
            return self._cache[path]
        uploaded = self.client.files.upload(file=str(path))
        while str(getattr(uploaded, "state", "")).endswith("PROCESSING"):
            time.sleep(self.poll_seconds)
            uploaded = self.client.files.get(name=uploaded.name)
        if str(getattr(uploaded, "state", "")).endswith("FAILED"):
            raise RuntimeError(f"Video processing failed for {path.name}")
        self._cache[path] = uploaded
        return uploaded

    def ask(self, *, model: str, video: Path, question: str, processing: str) -> ProviderResult:
        uploaded = self._upload(video)
        interaction = self.client.interactions.create(
            model=model,
            input=[
                {"type": "video", "uri": uploaded.uri, "mime_type": uploaded.mime_type, "processing": processing},
                {"type": "text", "text": question},
            ],
        )
        # Exact names used by the EAP notebook's Interactions API.
        usage = getattr(interaction, "usage", None)
        input_tokens = getattr(usage, "total_input_tokens", None)
        output_tokens = getattr(usage, "total_output_tokens", None)
        total_tokens = getattr(usage, "total_tokens", None)
        thought_tokens = getattr(usage, "total_thought_tokens", None)
        modality_usage = []
        for item in (getattr(usage, "input_tokens_by_modality", None) or []):
            modality_usage.append({
                "modality": str(getattr(item, "modality", "unknown")),
                "tokens": getattr(item, "tokens", None),
            })
        trace = getattr(interaction, "video_processing_strategy", None)
        if trace is None:
            trace = getattr(interaction, "thoughts", None)
        return ProviderResult(
            text=interaction.output_text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            thought_tokens=thought_tokens,
            strategy_trace=str(trace) if trace else None,
            raw_metadata={
                "total_tokens": total_tokens,
                "thought_tokens": thought_tokens,
                "input_tokens_by_modality": modality_usage,
            },
        )
