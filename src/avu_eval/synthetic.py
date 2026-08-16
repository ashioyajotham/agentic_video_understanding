from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

from .schema import Task


WIDTH, HEIGHT, FPS = 960, 540, 12
COLORS = {"red": "#dc3545", "blue": "#2474ff", "green": "#23a455", "yellow": "#f2c94c", "purple": "#8844cc"}


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


def generate_task_video(task: Task, root: Path) -> Path:
    if not task.generator:
        return root / task.video
    output = root / task.video
    output.parent.mkdir(parents=True, exist_ok=True)
    kind = task.generator.get("type")
    if kind == "snake_state":
        _render_snake(output, task.generator)
    else:
        raise ValueError(f"Unknown generator type: {kind}")
    return output


def ensure_ffmpeg() -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required to generate synthetic MP4 files")

