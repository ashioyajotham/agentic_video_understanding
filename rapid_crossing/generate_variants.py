#!/usr/bin/env python3
"""Generate deterministic rapid-crossing videos and exact ground truth."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import shutil
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PALETTE = {
    "red": "#ef4444",
    "green": "#22c55e",
    "blue": "#3b82f6",
    "yellow": "#facc15",
    "magenta": "#d946ef",
    "cyan": "#06b6d4",
    "orange": "#f97316",
    "white": "#f8fafc",
}


@dataclass(frozen=True)
class MovingObject:
    color: str
    crossing_time: float
    lane_y: float
    amplitude: float
    phase: float
    velocity_scale: float = 1.0
    obj_direction: float = 1.0  # +1 left-to-right, -1 right-to-left
    is_decoy: bool = False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_plan(variant: dict, video: dict) -> dict:
    rng = random.Random(int(variant["seed"]))
    count = int(variant["object_count"])
    colors = rng.sample(list(PALETTE)[:-1], count)
    rng.shuffle(colors)

    width = int(video["width"])
    height = int(video["height"])
    line_x = rng.randint(int(width * 0.44), int(width * 0.56))
    gap = float(variant["crossing_gap_seconds"])
    first_crossing = 3.0 + rng.uniform(-0.15, 0.15)
    crossing_times = [first_crossing + i * gap for i in range(count)]

    # --- New difficulty knobs (backward-compatible defaults) ---
    show_labels = variant.get("show_labels", True)
    obj_radius = int(variant.get("object_radius", video["object_radius"]))
    lane_overlap = variant.get("lane_overlap", False)
    variable_speed = variant.get("variable_speed", False)
    bidirectional = variant.get("bidirectional", False)
    decoy_count = int(variant.get("decoy_count", 0))

    # Lane positions: overlapping or separated
    if lane_overlap:
        # Cluster objects into 2-3 Y bands so they share vertical space
        n_bands = max(2, count // 3)
        band_ys = [height * (0.25 + 0.50 * i / max(1, n_bands - 1)) for i in range(n_bands)]
        lanes = [band_ys[i % n_bands] + rng.uniform(-15, 15) for i in range(count)]
    else:
        lanes = [height * (0.18 + 0.64 * i / max(1, count - 1)) for i in range(count)]
    rng.shuffle(lanes)

    # Per-object velocity and direction
    base_direction = 1.0 if variant["direction"] == "left_to_right" else -1.0
    objects = []
    for index, color in enumerate(colors):
        v_scale = rng.uniform(0.6, 1.4) if variable_speed else 1.0
        obj_dir = base_direction
        if bidirectional:
            obj_dir = rng.choice([1.0, -1.0])
        objects.append(
            MovingObject(
                color=color,
                crossing_time=crossing_times[index],
                lane_y=lanes[index],
                amplitude=rng.uniform(7.0, 17.0),
                phase=rng.uniform(0.0, math.tau),
                velocity_scale=v_scale,
                obj_direction=obj_dir,
            )
        )

    # Decoy objects: approach the line but reverse before crossing
    decoy_colors_pool = [c for c in PALETTE if c != "white" and c not in colors]
    decoys = []
    for i in range(decoy_count):
        d_color = decoy_colors_pool[i % len(decoy_colors_pool)] if decoy_colors_pool else "white"
        d_time = first_crossing + rng.uniform(-0.5, (count - 1) * gap + 0.5)
        d_lane = rng.uniform(height * 0.15, height * 0.85)
        decoys.append(
            MovingObject(
                color=d_color,
                crossing_time=d_time,
                lane_y=d_lane,
                amplitude=rng.uniform(5.0, 12.0),
                phase=rng.uniform(0.0, math.tau),
                velocity_scale=rng.uniform(0.7, 1.0),
                obj_direction=base_direction,
                is_decoy=True,
            )
        )

    all_objects = objects + decoys

    return {
        "variant_id": variant["id"],
        "seed": int(variant["seed"]),
        "direction": variant["direction"],
        "line_x": line_x,
        "crossing_gap_seconds": gap,
        "objects": [asdict(obj) for obj in all_objects],
        "expected_order": colors,  # decoys excluded from expected order
        "video": video,
        "background": variant["background"],
        "show_labels": show_labels,
        "object_radius": obj_radius,
    }


def position(obj: dict, t: float, plan: dict) -> tuple[float, float]:
    video = plan["video"]
    radius = float(plan.get("object_radius", video["object_radius"]))
    width = float(video["width"])
    line_x = float(plan["line_x"])
    travel_seconds = 2.1
    span = width + 4 * radius
    base_velocity = span / travel_seconds
    velocity = base_velocity * float(obj.get("velocity_scale", 1.0))
    direction = float(obj.get("obj_direction", 1.0 if plan["direction"] == "left_to_right" else -1.0))

    dt = t - float(obj["crossing_time"])

    if obj.get("is_decoy", False):
        # Decoys approach the line but reverse at ~80% of the way
        reversal_point = 0.8 * (line_x / (velocity if direction > 0 else velocity))
        if abs(dt) < 0.3:
            # Near the crossing time, reverse direction
            dt = -abs(dt) * 0.6
        x = line_x + direction * velocity * dt
    else:
        x = line_x + direction * velocity * dt

    y = float(obj["lane_y"]) + float(obj["amplitude"]) * math.sin(2.2 * t + float(obj["phase"]))
    return x, y


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def render(plan: dict, clip_path: Path, keep_frames: bool = False) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required to encode MP4 clips")

    video = plan["video"]
    width, height = int(video["width"]), int(video["height"])
    fps = int(video["fps"])
    frame_count = round(float(video["duration_seconds"]) * fps)
    radius = int(plan.get("object_radius", video["object_radius"]))
    show_labels = plan.get("show_labels", True)
    font = load_font(max(12, min(22, radius)))

    temporary = Path(tempfile.mkdtemp(prefix=f"{plan['variant_id']}-"))
    try:
        for frame_index in range(frame_count):
            t = frame_index / fps
            image = Image.new("RGB", (width, height), plan["background"])
            draw = ImageDraw.Draw(image)
            line_x = int(plan["line_x"])
            draw.line((line_x, 42, line_x, height - 28), fill="#f8fafc", width=3)
            draw.text((line_x - 70, 10), "REFERENCE", fill="#f8fafc", font=font)

            for obj in plan["objects"]:
                x, y = position(obj, t, plan)
                color_hex = PALETTE.get(obj["color"], "#888888")
                # Decoys get a dashed outline to subtly distinguish them
                outline_color = "#888888" if obj.get("is_decoy", False) else "#ffffff"
                draw.ellipse(
                    (x - radius, y - radius, x + radius, y + radius),
                    fill=color_hex,
                    outline=outline_color,
                    width=2,
                )
                if show_labels:
                    label = obj["color"]
                    box = draw.textbbox((0, 0), label, font=font)
                    draw.text(
                        (x - (box[2] - box[0]) / 2, y + radius + 5),
                        label,
                        fill="#f8fafc",
                        font=font,
                    )

            image.save(temporary / f"frame-{frame_index:05d}.png")

        clip_path.parent.mkdir(parents=True, exist_ok=True)
        command = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-framerate", str(fps),
            "-i", str(temporary / "frame-%05d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(clip_path),
        ]
        subprocess.run(command, check=True)
        if keep_frames:
            frame_dir = clip_path.with_suffix("")
            if frame_dir.exists():
                shutil.rmtree(frame_dir)
            shutil.copytree(temporary, frame_dir)
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def generate(spec_path: Path, output_dir: Path, keep_frames: bool = False) -> list[dict]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    clips = output_dir / "clips"
    truth = output_dir / "ground_truth"
    clips.mkdir(parents=True, exist_ok=True)
    truth.mkdir(parents=True, exist_ok=True)
    records = []

    for variant in spec["variants"]:
        plan = build_plan(variant, spec["video"])
        clip_path = clips / f"{variant['id']}.mp4"
        render(plan, clip_path, keep_frames=keep_frames)
        record = {
            **plan,
            "clip": str(clip_path.relative_to(output_dir.parent)),
            "clip_sha256": sha256(clip_path),
        }
        truth_path = truth / f"{variant['id']}.json"
        truth_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        records.append(record)
        print(f"generated {clip_path} order={plan['expected_order']}")
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--keep-frames", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate(args.spec, args.output_dir, keep_frames=args.keep_frames)

