from __future__ import annotations

from pathlib import Path
import json
import subprocess
import time
from typing import Any

from .grading import grade, grade_format
from .provider import GeminiProvider
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
        for repetition in range(1, int(config["repetitions"]) + 1):
            modes = list(config["processing_modes"])
            if config.get("order_strategy") == "counterbalanced" and repetition % 2 == 0:
                modes.reverse()
            for mode in modes:
                yield task, mode, repetition


def completed_keys(output: Path) -> set[tuple[str, str, int]]:
    keys = set()
    if not output.exists():
        return keys
    for line in output.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        keys.add((row["task_id"], row["processing"], int(row["repetition"])))
    return keys


def run(tasks: list[Task], config: dict[str, Any], root: Path, output: Path, dry_run: bool = False) -> int:
    jobs = list(matrix(tasks, config))
    if dry_run:
        for task, mode, repetition in jobs:
            print(json.dumps({"task": task.id, "mode": mode, "repetition": repetition, "video": task.video}))
        return 0
    provider = GeminiProvider(
        poll_seconds=int(config.get("poll_seconds", 10)),
        timeout_seconds=int(config.get("timeout_seconds", 180)),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    uploads = {}
    for idx, video in enumerate(dict.fromkeys(root / task.video for task in tasks), 1):
        print(f"[upload {idx}] Preparing {video.name}...", flush=True)
        started = time.perf_counter(); provider.prepare(video)
        uploads[str(video)] = time.perf_counter() - started
        print(f"[upload {idx}] Ready in {uploads[str(video)]:.2f}s", flush=True)
    done = completed_keys(output) if config.get("resume", True) else set()
    jobs = [job for job in jobs if (job[0].id, job[1], job[2]) not in done]
    print(f"Running {len(jobs)} jobs; skipping {len(done)} existing records.", flush=True)
    with output.open("a", encoding="utf-8") as handle:
        for index, (task, mode, repetition) in enumerate(jobs, 1):
            video = root / task.video
            print(f"[{index}/{len(jobs)}] {task.id} | {mode} | repetition {repetition}", flush=True)
            started = time.perf_counter()
            try:
                result = provider.ask(
                    model=config["model"], video=video, question=task.question,
                    processing=mode,
                )
                score = grade(task.answer_type, task.expected, result.text, task.tolerance)
                format_score = grade_format(task.answer_type, result.text)
                result.raw_metadata["upload_seconds"] = uploads[str(video)]
                observation = Observation(
                    task_id=task.id, family=task.family, processing=mode, repetition=repetition,
                    model=config["model"], video_duration_seconds=duration_seconds(video),
                    question=task.question, expected=task.expected, output_text=result.text,
                    score=score, correct=score >= 0.999, input_tokens=result.input_tokens,
                    output_tokens=result.output_tokens, latency_seconds=time.perf_counter() - started,
                    format_score=format_score, strict_correct=score >= 0.999 and format_score >= 0.999,
                    attempt_status="completed", strategy_trace=result.strategy_trace, metadata=result.raw_metadata,
                )
            except Exception as exc:
                status = "timeout" if isinstance(exc, TimeoutError) else "error"
                observation = Observation(
                    task_id=task.id, family=task.family, processing=mode, repetition=repetition,
                    model=config["model"], video_duration_seconds=duration_seconds(video),
                    question=task.question, expected=task.expected, output_text="", score=0, correct=False,
                    input_tokens=None, output_tokens=None, latency_seconds=time.perf_counter() - started,
                    attempt_status=status, error=f"{type(exc).__name__}: {exc}",
                    metadata={"upload_seconds": uploads[str(video)]},
                )
            handle.write(observation.to_json() + "\n")
            handle.flush()
            print(f"[{index}/{len(jobs)}] {observation.attempt_status} in {observation.latency_seconds:.2f}s", flush=True)
    return 0
