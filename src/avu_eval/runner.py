from __future__ import annotations

from pathlib import Path
import json
import subprocess
import time
from typing import Any

from .grading import grade
from .provider import GeminiEAPProvider
from .schema import Observation, Task


def duration_seconds(video: Path) -> float | None:
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(video)
        ], capture_output=True, text=True, check=True)
        return round(float(result.stdout.strip()), 3)
    except (OSError, ValueError, subprocess.CalledProcessError):
        return None


def matrix(tasks: list[Task], config: dict[str, Any]):
    for task in tasks:
        for mode in config["processing_modes"]:
            for repetition in range(1, int(config["repetitions"]) + 1):
                yield task, mode, repetition


def run(tasks: list[Task], config: dict[str, Any], root: Path, output: Path, dry_run: bool = False) -> int:
    jobs = list(matrix(tasks, config))
    if dry_run:
        for task, mode, repetition in jobs:
            print(json.dumps({"task": task.id, "mode": mode, "repetition": repetition, "video": task.video}))
        return 0
    provider = GeminiEAPProvider(poll_seconds=int(config.get("poll_seconds", 10)))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as handle:
        for task, mode, repetition in jobs:
            video = root / task.video
            started = time.perf_counter()
            try:
                result = provider.ask(
                    model=config["model"], video=video, question=task.question,
                    processing=mode,
                )
                score = grade(task.answer_type, task.expected, result.text, task.tolerance)
                observation = Observation(
                    task_id=task.id, family=task.family, processing=mode, repetition=repetition,
                    model=config["model"], video_duration_seconds=duration_seconds(video),
                    question=task.question, expected=task.expected, output_text=result.text,
                    score=score, correct=score >= 0.999, input_tokens=result.input_tokens,
                    output_tokens=result.output_tokens, latency_seconds=time.perf_counter() - started,
                    strategy_trace=result.strategy_trace, metadata=result.raw_metadata,
                )
            except Exception as exc:
                observation = Observation(
                    task_id=task.id, family=task.family, processing=mode, repetition=repetition,
                    model=config["model"], video_duration_seconds=duration_seconds(video),
                    question=task.question, expected=task.expected, output_text="", score=0, correct=False,
                    input_tokens=None, output_tokens=None, latency_seconds=time.perf_counter() - started,
                    error=f"{type(exc).__name__}: {exc}",
                )
            handle.write(observation.to_json() + "\n")
            handle.flush()
    return 0
