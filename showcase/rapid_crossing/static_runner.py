#!/usr/bin/env python3
"""Static single-pass baseline for Needle-in-a-Haystack video understanding."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from google import genai

PROMPT_NEEDLE = """Watch the video carefully. In this video, there is a rapid crossing event where colored circles (each containing a 2-digit ID number) cross the center vertical reference line in quick succession.

Task:
1. Identify the timestamp when the rapid crossing event occurs.
2. Determine the exact chronological order in which the circles cross the vertical reference line.
3. For each crossing circle, report both its lowercase color name and its 2-digit ID number.

Return ONLY a JSON object with this exact schema:
{
  "event_timestamp_seconds": 0.0,
  "order": [
    {"color": "color_name", "id": "12"},
    {"color": "color_name", "id": "34"}
  ]
}
"""


def run_static(model: str, clip: Path) -> dict:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    uploaded = client.files.upload(file=str(clip))

    tools = [{"type": "google_search"}]
    generation_config = {
        "max_output_tokens": 65536,
        "thinking_level": "medium",
    }

    input_content = [
        {"type": "video", "uri": uploaded.uri, "mime_type": "video/mp4"},
        {"type": "text", "text": PROMPT_NEEDLE},
    ]

    started = time.perf_counter()
    interaction = client.interactions.create(
        model=model,
        input=input_content,
        tools=tools,
        generation_config=generation_config,
    )
    latency = time.perf_counter() - started

    response_text = interaction.output_text or ""
    if not response_text and interaction.steps:
        last_step = interaction.steps[-1]
        response_text = getattr(last_step, "text", str(last_step))

    return {
        "response_text": response_text,
        "latency_seconds": latency,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clips-dir", type=Path, default=Path("generated_needle/clips"))
    parser.add_argument("--output", type=Path, default=Path("generated_needle/static_results.jsonl"))
    parser.add_argument("--model", default="models/gemini-3.6-flash-video-understanding-eap")
    args = parser.parse_args()

    clips = sorted(args.clips_dir.glob("*.mp4"))
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", encoding="utf-8") as out:
        for clip in clips:
            print(f"Running static on {clip.name}...")
            try:
                res = run_static(args.model, clip)
                record = {
                    "variant_id": clip.stem,
                    "clip": str(clip),
                    "mode": "static_single_pass",
                    "status": "completed",
                    **res,
                }
            except Exception as exc:
                record = {
                    "variant_id": clip.stem,
                    "clip": str(clip),
                    "mode": "static_single_pass",
                    "status": "error",
                    "error": str(exc),
                }
            out.write(json.dumps(record) + "\n")
            out.flush()
            print(f"Completed {clip.name} (latency: {record.get('latency_seconds', 0):.1f}s)")


if __name__ == "__main__":
    main()
