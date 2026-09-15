"""Video inspection tools for the Agentic Video Understanding loop."""

from __future__ import annotations

import base64
import subprocess
import tempfile
from pathlib import Path
from PIL import Image


def extract_high_fps_window(
    clip_path: str,
    start_seconds: float,
    end_seconds: float,
    output_fps: int = 25,
) -> list[dict]:
    """Extract full-resolution frame images within a specific time window.
    
    Returns a list of dicts with:
      - 'timestamp': float
      - 'image_path': str
    """
    duration = end_seconds - start_seconds
    if duration <= 0:
        raise ValueError("end_seconds must be greater than start_seconds")
    if duration > 10.0:
        # Cap window length to prevent token overflow
        duration = 10.0

    temp_dir = Path(tempfile.mkdtemp(prefix="agent_frame_window_"))
    out_pattern = str(temp_dir / "frame_%04d.png")

    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{start_seconds:.3f}",
        "-t", f"{duration:.3f}",
        "-i", clip_path,
        "-vf", f"fps={output_fps}",
        out_pattern,
    ]
    subprocess.run(cmd, check=True)

    extracted = []
    frame_files = sorted(temp_dir.glob("frame_*.png"))
    for idx, f in enumerate(frame_files):
        ts = start_seconds + (idx / float(output_fps))
        extracted.append({
            "timestamp": round(ts, 3),
            "image_path": str(f),
        })
    return extracted


def crop_region_at_timestamp(
    clip_path: str,
    timestamp_sec: float,
    x: int,
    y: int,
    crop_width: int = 200,
    crop_height: int = 200,
) -> str:
    """Extract a cropped zoom of a specific region at a specific timestamp.
    
    Returns the path to the high-resolution crop image.
    """
    temp_dir = Path(tempfile.mkdtemp(prefix="agent_crop_"))
    full_frame = str(temp_dir / "full_frame.png")
    crop_frame = str(temp_dir / "crop.png")

    # Extract 1 frame at timestamp
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{timestamp_sec:.3f}",
        "-i", clip_path,
        "-vframes", "1",
        full_frame,
    ]
    subprocess.run(cmd, check=True)

    # Crop with PIL
    img = Image.open(full_frame)
    left = max(0, x - crop_width // 2)
    top = max(0, y - crop_height // 2)
    right = min(img.width, left + crop_width)
    bottom = min(img.height, top + crop_height)

    cropped = img.crop((left, top, right, bottom))
    cropped.save(crop_frame)
    return crop_frame
