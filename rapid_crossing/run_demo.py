#!/usr/bin/env python3
"""Run the showcase via Gemini or an existing repository adapter command."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import time
from pathlib import Path


def run_command(template: str, clip: Path, prompt_path: Path, mode: str) -> dict:
    command = template.format(
        clip=shlex.quote(str(clip)),
        prompt=shlex.quote(str(prompt_path)),
        mode=shlex.quote(mode),
    )
    started = time.perf_counter()
    completed = subprocess.run(command, shell=True, text=True, capture_output=True)
    latency = time.perf_counter() - started
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"adapter exited {completed.returncode}")
    return {"response_text": completed.stdout.strip(), "latency_seconds": latency}


def run_gemini(model: str, clip: Path, prompt: str) -> dict:
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Install the google-genai SDK first: pip install google-genai") from exc

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    uploaded = client.files.upload(file=str(clip))

    tools = [{"type": "google_search"}]
    generation_config = {
        "max_output_tokens": 65536,
        "thinking_level": "medium",
    }

    # Interleaved typed input content format
    input_content = [
        {"type": "video", "uri": uploaded.uri, "mime_type": "video/mp4"},
        {"type": "text", "text": prompt},
    ]

    started = time.perf_counter()
    interaction = client.interactions.create(
        model=model,
        input=input_content,
        tools=tools,
        generation_config=generation_config,
    )
    latency = time.perf_counter() - started

    # Extract response text using official output_text or final step text
    response_text = interaction.output_text or ""
    if not response_text and interaction.steps:
        last_step = interaction.steps[-1]
        response_text = getattr(last_step, "text", str(last_step))

    usage = getattr(interaction, "usage", None)
    return {
        "response_text": response_text,
        "latency_seconds": latency,
        "usage": str(usage) if usage is not None else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clips-dir", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=("static", "agentic"), required=True)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--adapter", choices=("gemini", "command"), default="gemini")
    parser.add_argument("--model")
    parser.add_argument(
        "--command",
        help="Shell template producing response text; placeholders: {clip}, {prompt}, {mode}",
    )
    args = parser.parse_args()

    if args.adapter == "gemini" and not args.model:
        parser.error("--model is required for the gemini adapter")
    if args.adapter == "command" and not args.command:
        parser.error("--command is required for the command adapter")

    prompt = args.prompt.read_text(encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    clips = sorted(args.clips_dir.glob("*.mp4"))
    if not clips:
        raise SystemExit(f"no MP4 clips found in {args.clips_dir}")

    with args.output.open("a", encoding="utf-8") as handle:
        for attempt in range(1, args.attempts + 1):
            ordered_clips = clips if attempt % 2 else list(reversed(clips))
            for clip in ordered_clips:
                started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                try:
                    if args.adapter == "gemini":
                        result = run_gemini(args.model, clip, prompt)
                    else:
                        result = run_command(args.command, clip, args.prompt, args.mode)
                    record = {
                        "variant_id": clip.stem,
                        "clip": str(clip),
                        "mode": args.mode,
                        "attempt": attempt,
                        "started_at": started_at,
                        "status": "completed",
                        **result,
                    }
                except Exception as exc:
                    record = {
                        "variant_id": clip.stem,
                        "clip": str(clip),
                        "mode": args.mode,
                        "attempt": attempt,
                        "started_at": started_at,
                        "status": "error",
                        "error": str(exc),
                    }
                handle.write(json.dumps(record) + "\n")
                handle.flush()
                print(json.dumps(record))


if __name__ == "__main__":
    main()

