from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json


@dataclass(frozen=True)
class Task:
    id: str
    family: str
    video: str
    question: str
    answer_type: str
    expected: Any
    generator: dict[str, Any] | None = None
    tolerance: float | None = None
    tags: list[str] = field(default_factory=list)
    rationale: str = ""

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Task":
        required = {"id", "family", "video", "question", "answer_type", "expected"}
        missing = sorted(required - value.keys())
        if missing:
            raise ValueError(f"Task missing keys: {missing}")
        return cls(**value)


@dataclass
class Observation:
    task_id: str
    family: str
    processing: str
    repetition: int
    model: str
    video_duration_seconds: float | None
    question: str
    expected: Any
    output_text: str
    score: float
    correct: bool
    input_tokens: int | None
    output_tokens: int | None
    latency_seconds: float
    format_score: float = 0.0
    strict_correct: bool = False
    attempt_status: str = "completed"
    strategy_trace: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


def load_tasks(path: str | Path) -> list[Task]:
    tasks: list[Task] = []
    seen: set[str] = set()
    with Path(path).open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            task = Task.from_dict(json.loads(line))
            if task.id in seen:
                raise ValueError(f"Duplicate task id {task.id!r} at line {line_no}")
            seen.add(task.id)
            tasks.append(task)
    return tasks
