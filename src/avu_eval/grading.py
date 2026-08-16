from __future__ import annotations

import json
import math
import re
from typing import Any


def normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def _extract_json(text: str) -> Any:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*(.*?)```", text, re.S | re.I)
        if match:
            return json.loads(match.group(1))
        raise


def grade(answer_type: str, expected: Any, output: str, tolerance: float | None = None) -> float:
    kind = answer_type.lower()
    if kind == "exact":
        return float(normalize(str(expected)) == normalize(output))
    if kind == "contains":
        values = expected if isinstance(expected, list) else [expected]
        normalized = normalize(output)
        return sum(normalize(str(v)) in normalized for v in values) / len(values)
    if kind == "choice":
        target = normalize(str(expected))
        tokens = normalize(output).split()
        return float(target in tokens[:8])
    if kind == "number":
        numbers = re.findall(r"-?\d+(?:\.\d+)?", output.replace(",", ""))
        if not numbers:
            return 0.0
        tol = 0.0 if tolerance is None else tolerance
        return float(any(math.isclose(float(n), float(expected), abs_tol=tol) for n in numbers))
    if kind == "ordered_list":
        try:
            value = _extract_json(output)
        except (json.JSONDecodeError, TypeError):
            return 0.0
        if isinstance(value, dict):
            value = value.get("answer", value.get("events"))
        if not isinstance(value, list):
            return 0.0
        target = [normalize(str(x)) for x in expected]
        actual = [normalize(str(x)) for x in value]
        return sum(a == b for a, b in zip(actual, target)) / max(len(target), len(actual), 1)
    if kind == "set":
        try:
            value = _extract_json(output)
        except (json.JSONDecodeError, TypeError):
            return 0.0
        if isinstance(value, dict):
            value = value.get("answer", value.get("items"))
        if not isinstance(value, list):
            return 0.0
        target, actual = {normalize(str(x)) for x in expected}, {normalize(str(x)) for x in value}
        return len(target & actual) / len(target | actual) if target | actual else 1.0
    raise ValueError(f"Unsupported answer_type: {answer_type}")

