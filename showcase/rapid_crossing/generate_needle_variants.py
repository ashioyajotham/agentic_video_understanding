#!/usr/bin/env python3
"""Generate long-duration needle-in-a-haystack videos with micro-IDs and ambient motion."""

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
}


@dataclass(frozen=True)
class CrossingObject:
    color: str
    digit_id: str
    crossing_time: float
    lane_y: float
    amplitude: float
    phase: float
    direction: float  # +1 left-to-right, -1 right-to-left


@dataclass(frozen=True)
class AmbientDecoy:
    color: str
    center_x: float
    center_y: float
    radius_x: float
    radius_y: float
    speed_factor: float
    phase: float


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                continue
    return ImageFont.load_default()


def build_needle_plan(variant: dict, video: dict) -> dict:
    rng = random.Random(int(variant["seed"]))
    count = int(variant["object_count"])
    colors = rng.sample(list(PALETTE), count)
    rng.shuffle(colors)

    # 2-digit unique numbers
    digits_pool = list(range(10, 99))
    rng.shuffle(digits_pool)
    digit_ids = [str(digits_pool[i]) for i in range(count)]

    width = int(video["width"])
    height = int(video["height"])
    line_x = int(width * 0.5)

    event_start = float(variant["event_start_seconds"])
    gap = float(variant["crossing_gap_seconds"])
    crossing_times = [event_start + i * gap for i in range(count)]

    # Y lanes with slight jitter
    lanes = [height * (0.22 + 0.56 * i / max(1, count - 1)) for i in range(count)]
    rng.shuffle(lanes)

    dir_mult = 1.0 if variant["direction"] == "left_to_right" else -1.0
    crossing_objects = [
        CrossingObject(
            color=color,
            digit_id=digit_ids[i],
            crossing_time=crossing_times[i],
            lane_y=lanes[i],
            amplitude=rng.uniform(6.0, 14.0),
            phase=rng.uniform(0.0, math.tau),
            direction=dir_mult,
        )
        for i, color in enumerate(colors)
    ]

    # Ambient decoys wandering around on either side without crossing the center line
    n_decoys = int(variant.get("ambient_decoys", 4))
    ambient_decoys = []
    for i in range(n_decoys):
        side = -1 if (i % 2 == 0) else 1  # left vs right side
        cx = width * 0.25 if side < 0 else width * 0.75
        cy = height * (0.2 + 0.6 * rng.random())
        rx = width * 0.15 * rng.uniform(0.6, 1.0)
        ry = height * 0.25 * rng.uniform(0.5, 1.0)
        color = rng.choice(list(PALETTE))
        ambient_decoys.append(
            AmbientDecoy(
                color=color,
                center_x=cx,
                center_y=cy,
                radius_x=rx,
                radius_y=ry,
                speed_factor=rng.uniform(0.8, 1.8),
                phase=rng.uniform(0.0, math.tau),
            )
        )

    expected_order = [
        {"color": obj.color, "id": obj.digit_id, "time": round(obj.crossing_time, 3)}
        for obj in crossing_objects
    ]
    simple_color_order = [obj.color for obj in crossing_objects]
    simple_id_order = [obj.digit_id for obj in crossing_objects]

    return {
        "variant_id": variant["id"],
        "seed": int(variant["seed"]),
        "duration_seconds": float(variant["duration_seconds"]),
        "direction": variant["direction"],
        "line_x": line_x,
        "event_start_seconds": event_start,
        "crossing_gap_seconds": gap,
        "crossing_objects": [asdict(obj) for obj in crossing_objects],
        "ambient_decoys": [asdict(decoy) for decoy in ambient_decoys],
        "expected_order": expected_order,
        "expected_colors": simple_color_order,
        "expected_ids": simple_id_order,
        "video": video,
        "background": variant["background"],
    }


def render_needle(plan: dict, clip_path: Path) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required to encode MP4 clips")

    video = plan["video"]
    width, height = int(video["width"]), int(video["height"])
    fps = int(video["fps"])
    duration = float(plan["duration_seconds"])
    frame_count = round(duration * fps)
    radius = int(video["object_radius"])
    line_x = int(plan["line_x"])
    travel_seconds = 1.8
    span = width + 4 * radius
    velocity = span / travel_seconds

    font_id = load_font(13)
    font_ref = load_font(20)
    font_clock = load_font(16)

    temporary = Path(tempfile.mkdtemp(prefix=f"{plan['variant_id']}-"))
    try:
        for frame_index in range(frame_count):
            t = frame_index / fps
            image = Image.new("RGB", (width, height), plan["background"])
            draw = ImageDraw.Draw(image)

            # Draw center reference line
            draw.line((line_x, 50, line_x, height - 35), fill="#e2e8f0", width=4)
            draw.text((line_x - 85, 18), "REFERENCE LINE", fill="#e2e8f0", font=font_ref)

            # Draw on-screen timestamp (helps visual verification)
            mins = int(t // 60)
            secs = t % 60
            clock_str = f"TIME: {mins:02d}:{secs:05.2f}"
            draw.text((30, 20), clock_str, fill="#94a3b8", font=font_clock)

            # 1. Render ambient decoys
            for decoy in plan["ambient_decoys"]:
                dx = decoy["center_x"] + decoy["radius_x"] * math.sin(decoy["speed_factor"] * t + decoy["phase"])
                dy = decoy["center_y"] + decoy["radius_y"] * math.cos(0.8 * decoy["speed_factor"] * t + decoy["phase"])
                color_hex = PALETTE.get(decoy["color"], "#888888")
                draw.ellipse(
                    (dx - radius * 0.8, dy - radius * 0.8, dx + radius * 0.8, dy + radius * 0.8),
                    fill=color_hex,
                    outline="#64748b",
                    width=1,
                )

            # 2. Render rapid crossing objects during their active window
            for obj in plan["crossing_objects"]:
                t_cross = float(obj["crossing_time"])
                dt = t - t_cross
                # Only visible while traversing the screen
                if abs(dt) <= (travel_seconds / 2.0 + 0.2):
                    direction = float(obj["direction"])
                    x = line_x + direction * velocity * dt
                    y = float(obj["lane_y"]) + float(obj["amplitude"]) * math.sin(3.0 * t + float(obj["phase"]))
                    color_hex = PALETTE.get(obj["color"], "#ffffff")

                    # Draw outer circle
                    draw.ellipse(
                        (x - radius, y - radius, x + radius, y + radius),
                        fill=color_hex,
                        outline="#ffffff",
                        width=2,
                    )
                    # Draw micro 2-digit ID inside
                    digit_text = str(obj["digit_id"])
                    bbox = draw.textbbox((0, 0), digit_text, font=font_id)
                    tw = bbox[2] - bbox[0]
                    th = bbox[3] - bbox[1]
                    draw.text(
                        (x - tw / 2, y - th / 2 - 1),
                        digit_text,
                        fill="#000000",
                        font=font_id,
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
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def generate(spec_path: Path, output_dir: Path) -> list[dict]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    clips = output_dir / "clips"
    truth = output_dir / "ground_truth"
    clips.mkdir(parents=True, exist_ok=True)
    truth.mkdir(parents=True, exist_ok=True)
    records = []

    for variant in spec["variants"]:
        plan = build_needle_plan(variant, spec["video"])
        clip_path = clips / f"{variant['id']}.mp4"
        print(f"Rendering {variant['id']} ({plan['duration_seconds']}s, event at {plan['event_start_seconds']}s)...")
        render_needle(plan, clip_path)
        record = {
            **plan,
            "clip": str(clip_path.relative_to(output_dir.parent)),
            "clip_sha256": sha256(clip_path),
        }
        truth_path = truth / f"{variant['id']}.json"
        truth_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        records.append(record)
        print(f"Generated {clip_path}: Expected colors={plan['expected_colors']}, IDs={plan['expected_ids']}")
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, default=Path("rapid_crossing/needle_variants.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("generated_needle"))
    args = parser.parse_args()
    generate(args.spec, args.output_dir)


if __name__ == "__main__":
    main()
