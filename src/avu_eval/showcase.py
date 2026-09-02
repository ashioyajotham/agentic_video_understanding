from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any
import hashlib
import json
import shutil

from .schema import Task, load_tasks
from .synthetic import generate_task_video, validate_generator_spec


EXPORT_SCHEMA = "avu-showcase-export/v1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def task_sha256(task: Task) -> str:
    payload = json.dumps(asdict(task), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    staging = path.with_name(f".{path.name}.writing")
    staging.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    staging.replace(path)


def _copy_exact(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.with_name(f".{destination.name}.copying")
    shutil.copyfile(source, staging)
    staging.replace(destination)


def export_showcase(
    *,
    root: Path,
    suite_path: Path,
    output_dir: Path,
    generate: bool = True,
) -> dict[str, Any]:
    root = root.resolve()
    suite_path = suite_path.resolve()
    output_dir = output_dir.resolve()
    tasks = load_tasks(suite_path)
    for task in tasks:
        validate_generator_spec(task)

    clips_dir = output_dir / "clips"
    truth_dir = output_dir / "ground_truth"
    exported_videos: dict[str, dict[str, str]] = {}
    entries = []

    for task in tasks:
        source_video = root / task.video
        if generate and task.video not in exported_videos:
            generate_task_video(task, root)
        if not source_video.is_file():
            raise FileNotFoundError(
                f"Canonical video is missing for {task.id}: {source_video}. "
                "Run without --skip-generate or generate the suite first."
            )

        clip_name = Path(task.video).name
        exported_clip = clips_dir / clip_name
        if task.video not in exported_videos:
            _copy_exact(source_video, exported_clip)
            source_hash = sha256(source_video)
            exported_hash = sha256(exported_clip)
            if exported_hash != source_hash:
                raise RuntimeError(f"Exact-copy verification failed for {task.video}")
            exported_videos[task.video] = {
                "clip": str(exported_clip.relative_to(output_dir).as_posix()),
                "clip_sha256": exported_hash,
                "source_video": task.video,
            }

        video_record = exported_videos[task.video]
        entry = {
            "task_id": task.id,
            "family": task.family,
            "question": task.question,
            "answer_type": task.answer_type,
            "expected": task.expected,
            "tolerance": task.tolerance,
            "tags": task.tags,
            "rationale": task.rationale,
            "generator": task.generator,
            "task_spec_sha256": task_sha256(task),
            **video_record,
            "provenance": {
                "kind": "canonical_benchmark",
                "exact_canonical_render": True,
                "claim_status": "eligible_after_registered_model_run",
            },
        }
        _write_json(truth_dir / f"{task.id}.json", entry)
        entries.append(entry)

    manifest = {
        "schema": EXPORT_SCHEMA,
        "suite": str(suite_path.relative_to(root).as_posix()) if suite_path.is_relative_to(root) else str(suite_path),
        "suite_sha256": sha256(suite_path),
        "exact_canonical_render": True,
        "claim_status": "stimuli_only_no_model_results",
        "task_count": len(tasks),
        "unique_video_count": len(exported_videos),
        "tasks": entries,
    }
    _write_json(output_dir / "manifest.json", manifest)
    return manifest


def verify_showcase(*, root: Path, suite_path: Path, input_dir: Path) -> dict[str, int]:
    root = root.resolve()
    suite_path = suite_path.resolve()
    input_dir = input_dir.resolve()
    manifest_path = input_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != EXPORT_SCHEMA:
        raise ValueError(f"Unsupported showcase export schema: {manifest.get('schema')!r}")
    if manifest.get("suite_sha256") != sha256(suite_path):
        raise ValueError("Canonical suite hash has changed since this showcase export")

    tasks = load_tasks(suite_path)
    expected_by_id = {task.id: task for task in tasks}
    entries = manifest.get("tasks", [])
    if {entry.get("task_id") for entry in entries} != set(expected_by_id):
        raise ValueError("Exported task IDs do not match the canonical suite")

    verified_videos = set()
    for entry in entries:
        task = expected_by_id[entry["task_id"]]
        validate_generator_spec(task)
        if entry.get("task_spec_sha256") != task_sha256(task):
            raise ValueError(f"Task specification drift detected for {task.id}")
        if entry.get("expected") != task.expected:
            raise ValueError(f"Ground truth drift detected for {task.id}")
        if entry.get("provenance", {}).get("exact_canonical_render") is not True:
            raise ValueError(f"Missing exact-render provenance for {task.id}")

        clip = input_dir / entry["clip"]
        if sha256(clip) != entry["clip_sha256"]:
            raise ValueError(f"Clip hash mismatch for {task.id}")
        source = root / entry["source_video"]
        if not source.is_file() or sha256(source) != entry["clip_sha256"]:
            raise ValueError(f"Exported clip is not an exact copy of the canonical render for {task.id}")
        truth = json.loads((input_dir / "ground_truth" / f"{task.id}.json").read_text(encoding="utf-8"))
        if truth != entry:
            raise ValueError(f"Ground-truth record mismatch for {task.id}")
        verified_videos.add(entry["clip"])

    return {"tasks": len(tasks), "videos": len(verified_videos)}
