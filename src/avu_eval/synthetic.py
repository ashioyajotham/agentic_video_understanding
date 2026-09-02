from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Callable

from PIL import Image, ImageDraw, ImageFont

from .schema import Task


WIDTH, HEIGHT, FPS = 960, 540, 12
COLORS = {
    "red": "#dc3545",
    "orange": "#ed6a2c",
    "magenta": "#cf3f8f",
    "blue": "#2474ff",
    "green": "#23a455",
    "yellow": "#f2c94c",
    "purple": "#8844cc",
    "cyan": "#24a9b8",
}


def _font(size: int):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _snake_frame(t: float, events: list[dict], duration: float) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), "#f5f1e8")
    draw = ImageDraw.Draw(image)
    completed = [e for e in events if t >= float(e["time"])]
    active = next((e for e in events if abs(t - float(e["time"])) < 0.55), None)
    # Snake body grows after each swallowed object; bulges retain ordered state.
    body_start, body_end, y = 130, 770, 290
    draw.line((body_start, y, body_end, y), fill="#3a9d5d", width=62)
    draw.ellipse((735, 245, 825, 335), fill="#3a9d5d", outline="#164d2b", width=4)
    draw.ellipse((790, 270, 802, 282), fill="black")
    for i, event in enumerate(completed):
        x = 650 - i * 105
        radius = 30 + int(event.get("size", 1)) * 5
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=COLORS[event["color"]], outline="#163a24", width=4)
    if active:
        progress = max(0.0, min(1.0, (t - float(active["time"]) + .55) / 1.1))
        x = int(900 - progress * 115)
        r = 18 + int(active.get("size", 1)) * 4
        draw.ellipse((x-r, y-r, x+r, y+r), fill=COLORS[active["color"]], outline="black", width=3)
    draw.text((30, 25), f"Elapsed {t:05.1f}s", fill="#333", font=_font(28))
    draw.text((30, 475), "Objects already swallowed remain visible as body bulges", fill="#444", font=_font(24))
    return image


def _render_snake(output: Path, spec: dict) -> None:
    duration = float(spec.get("duration", 16))
    events = list(spec["events"])
    with tempfile.TemporaryDirectory(prefix="avu-frames-") as tmp:
        tmp_path = Path(tmp)
        for idx in range(round(duration * FPS)):
            _snake_frame(idx / FPS, events, duration).save(tmp_path / f"{idx:06d}.png")
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
            "-i", str(tmp_path / "%06d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(output)
        ], check=True)


def _stream_video(output: Path, duration: float, fps: int, frame_fn: Callable[[float], Image.Image], size=(640, 360)) -> None:
    """Stream frames directly into ffmpeg so multi-minute stimuli do not fill disk."""
    staging = output.with_name(f".{output.stem}.rendering{output.suffix}")
    staging.unlink(missing_ok=True)
    process = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{size[0]}x{size[1]}", "-r", str(fps), "-i", "-", "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", str(staging),
    ], stdin=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for index in range(round(duration * fps)):
            process.stdin.write(frame_fn(index / fps).convert("RGB").tobytes())
    finally:
        process.stdin.close()
    if process.wait() != 0:
        staging.unlink(missing_ok=True)
        raise RuntimeError(f"ffmpeg failed while creating {output}")
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(staging),
    ], capture_output=True, text=True)
    try:
        rendered_duration = float(probe.stdout.strip())
    except ValueError:
        rendered_duration = 0.0
    if probe.returncode != 0 or rendered_duration < duration - (1 / fps):
        staging.unlink(missing_ok=True)
        raise RuntimeError(f"ffmpeg produced an invalid or incomplete video for {output}")
    staging.replace(output)


def _ledger_frame(t: float, spec: dict) -> Image.Image:
    image = Image.new("RGB", (640, 360), "#f3efe5")
    draw = ImageDraw.Draw(image)
    events = sorted(spec["events"], key=lambda x: x["time"])
    state: list[str] = []
    for event in events:
        completion_time = float(event["time"]) + float(event.get("window", 0.8))
        if t < completion_time:
            break
        action, color = event["action"], event["color"]
        if action == "swallow": state.append(color)
        elif action == "expel" and color in state: state.remove(color)
    draw.line((70, 190, 510, 190), fill="#3a9d5d", width=50)
    draw.ellipse((485, 150, 565, 230), fill="#3a9d5d", outline="#164d2b", width=4)
    draw.ellipse((535, 174, 546, 185), fill="black")
    for idx, color in enumerate(state):
        x = 440 - idx * 72
        draw.ellipse((x-25, 165, x+25, 215), fill=COLORS[color], outline="#163a24", width=3)
    # Animate the current event without writing its action or color as text.
    active = next((e for e in events if abs(t - e["time"]) <= float(e.get("window", 0.8))), None)
    if active:
        window = float(active.get("window", 0.8))
        phase = (t - active["time"] + window) / (2 * window)
        if active["action"] == "swallow": x = int(620 - min(max(phase, 0), 1) * 90)
        elif active["action"] == "expel": x = int(530 + min(max(phase, 0), 1) * 90)
        else:  # feint: approach and retreat while remaining clearly outside the head.
            x = int(625 - 35 * (1 - abs(2 * min(max(phase, 0), 1) - 1)))
        draw.ellipse((x-18, 172, x+18, 208), fill=COLORS[active["color"]], outline="black", width=3)
    draw.text((22, 18), f"T+{int(t):03d}s", fill="#333", font=_font(22))
    draw.text((22, 320), "Track completed entries and exits; approaches may be incomplete.", fill="#444", font=_font(18))
    return image


def _render_state_ledger(output: Path, spec: dict) -> None:
    duration, fps = float(spec.get("duration", 180)), int(spec.get("fps", 6))
    _stream_video(output, duration, fps, lambda t: _ledger_frame(t, spec))


def _needle_frame(t: float, spec: dict) -> Image.Image:
    image = Image.new("RGB", (640, 360), "#10151c")
    draw = ImageDraw.Draw(image)
    target_time = float(spec["target_time"]); window = float(spec.get("window", 0.45))
    # Slow distractor motion ensures the video is not a static card.
    x = int(40 + (t * 17) % 540)
    draw.rectangle((x, 145, x+55, 200), fill="#657786")
    if target_time <= t < target_time + window:
        draw.polygon([(320, 75), (370, 180), (320, 285), (270, 180)], fill=COLORS[spec["target_color"]])
    draw.text((20, 20), f"T+{t:06.1f}s", fill="#d4d9df", font=_font(22))
    return image


def _render_sparse_needle(output: Path, spec: dict) -> None:
    duration, fps = float(spec.get("duration", 300)), int(spec.get("fps", 6))
    _stream_video(output, duration, fps, lambda t: _needle_frame(t, spec))


def _rapid_event_y(event: dict, index: int, count: int, overlap: bool) -> int:
    if "y" in event:
        return int(event["y"])
    if overlap:
        # Controlled convergence prevents lane identity from being a shortcut while
        # retaining a small vertical offset so the stimulus remains recoverable.
        offsets = (-12, 0, 12, -6, 6)
        return 180 + offsets[index % len(offsets)]
    if count <= 1:
        return 180
    return int(65 + index * (230 / (count - 1)))


def _draw_rapid_background(draw: ImageDraw.ImageDraw, t: float, noise: str) -> None:
    if noise not in {"grid", "moving_grid"}:
        return
    offset = int((t * 18) % 40) if noise == "moving_grid" else 0
    for x in range(-40 + offset, 681, 40):
        draw.line((x, 0, x, 360), fill="#d9dde2", width=1)
    for y in range(0, 361, 40):
        draw.line((0, y, 640, y), fill="#d9dde2", width=1)


def _rapid_x(t: float, event: dict, gate_x: int, default_speed: float) -> float:
    event_time = float(event["time"])
    speed = float(event.get("speed", default_speed))
    direction = event.get("direction", "ltr")
    sign = 1 if direction == "ltr" else -1
    dt = t - event_time
    if event.get("crosses", True):
        return gate_x + sign * dt * speed

    # A decoy reaches its closest point at `time` and reverses without touching
    # the gate. It always remains on its approach side.
    closest = float(event.get("closest_offset", 10))
    return gate_x - sign * (closest + abs(dt) * speed)


def _rapid_frame(t: float, spec: dict) -> Image.Image:
    background = spec.get("background_color", "#f7f7f7")
    image = Image.new("RGB", (640, 360), background)
    draw = ImageDraw.Draw(image)
    _draw_rapid_background(draw, t, spec.get("background_noise", "none"))
    gate_x = int(spec.get("gate_x", 320))
    draw.line((gate_x, 45, gate_x, 315), fill="#222", width=5)
    events = list(spec["events"])
    radius = int(spec.get("object_radius", 16))
    default_speed = float(spec.get("speed", 600))
    visible_window = float(spec.get("visible_window", 0.45))
    overlap = bool(spec.get("lane_overlap", False))
    show_labels = bool(spec.get("show_labels", False))
    for idx, event in enumerate(events):
        dt = t - float(event["time"])
        if abs(dt) <= visible_window:
            x = int(_rapid_x(t, event, gate_x, default_speed))
            y = _rapid_event_y(event, idx, len(events), overlap)
            color = event["color"]
            draw.ellipse(
                (x-radius, y-radius, x+radius, y+radius),
                fill=COLORS[color], outline="#111", width=max(1, radius // 6),
            )
            if show_labels:
                label_font = _font(max(10, radius))
                box = draw.textbbox((0, 0), color, font=label_font)
                label_width = box[2] - box[0]
                draw.text((x-label_width/2, y+radius+3), color, fill="#222", font=label_font)
    if spec.get("show_instruction", True):
        draw.text((20, 20), "Which objects cross the gate, and in what order?", fill="#333", font=_font(20))
    return image


def _render_rapid_order(output: Path, spec: dict) -> None:
    duration, fps = float(spec.get("duration", 18)), int(spec.get("fps", 30))
    _stream_video(output, duration, fps, lambda t: _rapid_frame(t, spec))


def validate_generator_spec(task: Task) -> None:
    """Reject misleading or unobservable synthetic rapid-order tasks."""
    spec = task.generator
    if not spec or spec.get("type") != "rapid_order":
        return
    fps = int(spec.get("fps", 30))
    if fps <= 0:
        raise ValueError(f"{task.id}: fps must be positive")
    radius = int(spec.get("object_radius", 16))
    if radius < 6:
        raise ValueError(f"{task.id}: object_radius below 6px is not reliably visible")
    events = list(spec.get("events", []))
    crossings = sorted((e for e in events if e.get("crosses", True)), key=lambda e: float(e["time"]))
    if not crossings:
        raise ValueError(f"{task.id}: rapid_order requires at least one crossing")
    for event in events:
        if event.get("direction", "ltr") not in {"ltr", "rtl"}:
            raise ValueError(f"{task.id}: direction must be 'ltr' or 'rtl'")
        if event["color"] not in COLORS:
            raise ValueError(f"{task.id}: unknown color {event['color']!r}")
        if float(event.get("speed", spec.get("speed", 600))) <= 0:
            raise ValueError(f"{task.id}: speed must be positive")
        if not event.get("crosses", True) and float(event.get("closest_offset", 10)) <= radius:
            raise ValueError(
                f"{task.id}: decoy closest_offset must exceed object_radius so it cannot touch the gate"
            )

    minimum_gap_frames = float(spec.get("minimum_gap_frames", 2))
    for first, second in zip(crossings, crossings[1:]):
        gap_frames = (float(second["time"]) - float(first["time"])) * fps
        if gap_frames + 1e-9 < minimum_gap_frames:
            raise ValueError(
                f"{task.id}: crossings {first['color']}->{second['color']} are only "
                f"{gap_frames:.2f} frames apart; require >= {minimum_gap_frames:g}"
            )

    if task.answer_type == "ordered_list":
        derived = [event["color"] for event in crossings]
        if task.expected != derived:
            raise ValueError(f"{task.id}: expected order {task.expected!r} does not match rendered crossings {derived!r}")


def generate_task_video(task: Task, root: Path) -> Path:
    if not task.generator:
        return root / task.video
    validate_generator_spec(task)
    output = root / task.video
    output.parent.mkdir(parents=True, exist_ok=True)
    kind = task.generator.get("type")
    if kind == "snake_state":
        _render_snake(output, task.generator)
    elif kind == "state_ledger":
        _render_state_ledger(output, task.generator)
    elif kind == "sparse_needle":
        _render_sparse_needle(output, task.generator)
    elif kind == "rapid_order":
        _render_rapid_order(output, task.generator)
    else:
        raise ValueError(f"Unknown generator type: {kind}")
    return output


def ensure_ffmpeg() -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required to generate synthetic MP4 files")
