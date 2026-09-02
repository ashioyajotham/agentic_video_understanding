from __future__ import annotations

import argparse
from pathlib import Path
import yaml

from .report import build
from .runner import run
from .schema import load_tasks
from .showcase import export_showcase, verify_showcase
from .synthetic import ensure_ffmpeg, generate_task_video, validate_generator_spec


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="avu-eval")
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("generate", "validate"):
        cmd = commands.add_parser(name)
        cmd.add_argument("--suite", required=True)
    cmd = commands.add_parser("run")
    cmd.add_argument("--suite", required=True); cmd.add_argument("--config", required=True)
    cmd.add_argument("--output", required=True); cmd.add_argument("--dry-run", action="store_true")
    cmd = commands.add_parser("report")
    cmd.add_argument("--input", required=True); cmd.add_argument("--output", required=True)
    cmd = commands.add_parser("showcase-export")
    cmd.add_argument("--suite", required=True); cmd.add_argument("--output", required=True)
    cmd.add_argument("--skip-generate", action="store_true")
    cmd = commands.add_parser("showcase-verify")
    cmd.add_argument("--suite", required=True); cmd.add_argument("--input", required=True)
    return root


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    cwd = Path.cwd()
    if args.command == "validate":
        tasks = load_tasks(args.suite)
        for task in tasks:
            validate_generator_spec(task)
        print(f"Validated {len(tasks)} unique tasks")
        return 0
    if args.command == "generate":
        ensure_ffmpeg(); tasks = load_tasks(args.suite)
        generated = {}
        for task in tasks:
            if task.generator and task.video not in generated:
                generated[task.video] = generate_task_video(task, cwd)
        for path in generated.values(): print(path)
        return 0
    if args.command == "run":
        tasks = load_tasks(args.suite)
        config = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
        return run(tasks, config, cwd, Path(args.output), args.dry_run)
    if args.command == "report":
        build(Path(args.input), Path(args.output)); return 0
    if args.command == "showcase-export":
        if not args.skip_generate:
            ensure_ffmpeg()
        result = export_showcase(
            root=cwd, suite_path=Path(args.suite), output_dir=Path(args.output),
            generate=not args.skip_generate,
        )
        print(f"Exported {result['task_count']} canonical tasks across {result['unique_video_count']} exact videos")
        return 0
    if args.command == "showcase-verify":
        result = verify_showcase(root=cwd, suite_path=Path(args.suite), input_dir=Path(args.input))
        print(f"Verified {result['tasks']} canonical tasks across {result['videos']} exact videos")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
