#!/usr/bin/env python3
"""Agentic multi-turn runner with active frame inspection tools."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from google import genai
from rapid_crossing.tools.video_tools import extract_high_fps_window


PROMPT_LOCALIZE = """Scan this video. At some point in this video, there is a rapid crossing event where colored circles cross the center vertical reference line.
Identify the approximate time window (start second and end second) when this crossing happens.

Return ONLY a JSON object:
{"event_detected": true, "start_seconds": 21.5, "end_seconds": 24.5}
"""

PROMPT_INSPECT = """You are analyzing high-framerate extracted frames from the crossing window of the video.
Determine the EXACT chronological order in which the colored circles cross the vertical reference line.
For each circle, read its lowercase color name and its 2-digit ID number printed on it.

Return ONLY a JSON object:
{
  "order": [
    {"color": "color_name", "id": "12"},
    {"color": "color_name", "id": "34"}
  ]
}
"""


def parse_json_response(text: str) -> dict | None:
    # If wrapped inside TextContent string representation:
    m = re.search(r"text='(.*?)'(?:,\s*annotations=|\s*\))", text, re.DOTALL)
    if m:
        try:
            text = m.group(1).encode("utf-8").decode("unicode_escape")
        except Exception:
            text = m.group(1)

    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except Exception:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
    return None


def run_agentic_pipeline(model: str, clip: Path) -> dict:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    started_total = time.perf_counter()

    # --- Step 1: Temporal Localization Scan ---
    print(f"  [Agent Step 1] Scanning {clip.name} for event window...")
    uploaded_video = client.files.upload(file=str(clip))
    
    t0 = time.perf_counter()
    interaction_scan = client.interactions.create(
        model=model,
        input=[
            {"type": "video", "uri": uploaded_video.uri, "mime_type": "video/mp4"},
            {"type": "text", "text": PROMPT_LOCALIZE},
        ],
        tools=[{"type": "google_search"}],
        generation_config={"max_output_tokens": 8192, "thinking_level": "medium"},
    )
    t_scan = time.perf_counter() - t0

    step_text = interaction_scan.output_text or ""
    if not step_text and interaction_scan.steps:
        last_s = interaction_scan.steps[-1]
        step_text = getattr(last_s, "text", str(last_s))
    parsed_loc = parse_json_response(step_text)
    
    start_sec = 0.0
    end_sec = 10.0
    if parsed_loc and "start_seconds" in parsed_loc and "end_seconds" in parsed_loc:
        start_sec = max(0.0, float(parsed_loc["start_seconds"]) - 0.5)
        end_sec = float(parsed_loc["end_seconds"]) + 0.5
        print(f"  [Agent Step 1] Found window: {start_sec:.2f}s - {end_sec:.2f}s")
    else:
        print(f"  [Agent Step 1 Warning] Could not parse window, using default fallback: {step_text[:100]}")

    # --- Step 2: Tool Execution (extract high-FPS window) ---
    print(f"  [Agent Step 2] Calling tool: extract_high_fps_window({start_sec:.2f}s to {end_sec:.2f}s @ 20fps)...")
    frames = extract_high_fps_window(str(clip), start_sec, end_sec, output_fps=20)
    print(f"  [Agent Step 2] Extracted {len(frames)} high-resolution frames.")

    # Encode a subset of representative frames for the inspection step (e.g. 10 evenly spaced frames)
    step_frames = frames
    if len(frames) > 12:
        stride = max(1, len(frames) // 10)
        step_frames = frames[::stride][:12]

    # --- Step 3: High-Resolution Sequence Inspection ---
    print(f"  [Agent Step 3] Inspecting {len(step_frames)} high-res frames for micro-IDs and order...")
    image_contents = []
    for f in step_frames:
        up_img = client.files.upload(file=f["image_path"])
        image_contents.append({"type": "image", "uri": up_img.uri, "mime_type": "image/png"})

    t1 = time.perf_counter()
    interaction_inspect = client.interactions.create(
        model=model,
        input=image_contents + [{"type": "text", "text": PROMPT_INSPECT}],
        tools=[{"type": "google_search"}],
        generation_config={"max_output_tokens": 16384, "thinking_level": "medium"},
    )
    t_inspect = time.perf_counter() - t1

    final_text = interaction_inspect.output_text or ""
    if not final_text and interaction_inspect.steps:
        last_s = interaction_inspect.steps[-1]
        final_text = getattr(last_s, "text", str(last_s))

    total_latency = time.perf_counter() - started_total

    return {
        "response_text": final_text,
        "localization_result": parsed_loc,
        "frames_inspected": len(step_frames),
        "scan_latency_seconds": t_scan,
        "inspect_latency_seconds": t_inspect,
        "total_latency_seconds": total_latency,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clips-dir", type=Path, default=Path("generated_needle/clips"))
    parser.add_argument("--output", type=Path, default=Path("generated_needle/agentic_results.jsonl"))
    parser.add_argument("--model", default="models/gemini-3.6-flash-video-understanding-eap")
    args = parser.parse_args()

    clips = sorted(args.clips_dir.glob("*.mp4"))
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", encoding="utf-8") as out:
        for clip in clips:
            print(f"\nRunning Agentic Loop on {clip.name}...")
            try:
                res = run_agentic_pipeline(args.model, clip)
                record = {
                    "variant_id": clip.stem,
                    "clip": str(clip),
                    "mode": "agentic_tool_loop",
                    "status": "completed",
                    **res,
                }
            except Exception as exc:
                record = {
                    "variant_id": clip.stem,
                    "clip": str(clip),
                    "mode": "agentic_tool_loop",
                    "status": "error",
                    "error": str(exc),
                }
            out.write(json.dumps(record) + "\n")
            out.flush()
            print(f"Completed {clip.name} (total latency: {record.get('total_latency_seconds', 0):.1f}s)")


if __name__ == "__main__":
    main()
