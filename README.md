# Agentic Video Understanding (AVU) Showcase

> 🔒 **Confidential — Gemini API EAP Material**  
> *Embargo lifts today at **8:00 PM** (local time). Maintain repository privacy until Google explicitly lifts the embargo.*

---

## Layman's Guide: Static vs. Agentic Video Understanding

Most AI video models today use **Static Video Understanding**. When you feed an AI a 1-minute or 10-minute video, it acts like a human watching on 10× fast-forward: it samples a few frames per second (or downscales image resolution) to fit the whole video into its memory. 

* **The Static Limitation**: If a critical event occurs in a 0.1-second flash—or if solving the problem requires reading a tiny number on a moving object—static downsampling misses it completely.
* **The Agentic Solution (AVU)**: Instead of passively watching a downsampled stream, an **Agentic Video Understanding** system acts like an **expert video investigator with a remote control and magnifying glass**. It:
  1. **Scans** the long overview to detect where the action happens (*"Anomalous crossing detected between 00:21.0s and 00:24.0s"*).
  2. **Invokes active tools** (like `ffmpeg` temporal frame slicing) to extract uncompressed, full-framerate frames for that exact 3-second window.
  3. **Zooms into micro-details** at native pixel resolution to read micro-IDs and resolve observable frame-level ordering.
  4. **Allocates more visual detail to the decisive window** instead of processing the entire video at high FPS.

---

## Poised Real-World Use Cases for AVU

| Industry | The Challenge for Static AI | The Agentic (AVU) Advantage |
|---|---|---|
| **Security & CCTV Forensics** | Sifting through 24 hours of surveillance footage misses a 2-second license plate crossing. | Agent scans for motion, requests high-FPS zoom on the vehicle, and extracts the plate number. |
| **Sports Adjudication & VAR** | Millisecond photo-finishes or rapid ball deflections blur across standard frame sampling. | Agent identifies the play window, pulls 60 FPS sub-second crops, and accurately determines the winner. |
| **Industrial QC & Manufacturing** | High-speed conveyor belts produce micro-defects that appear for a fraction of a second. | Agent monitors overall flow, inspects high-speed frame bursts on anomalies, and logs defect IDs. |
| **Autonomous Systems & Robotics** | Fine-grained state transitions and fast-moving obstacles require targeted spatial-temporal focus. | Agent selectively allocates perception compute to dynamic interaction zones. |

---

## Showcase Overview & Benchmark Suites

This repository provides deterministic, mathematically verifiable benchmarks to evaluate and demonstrate temporal video understanding on `models/gemini-3.6-flash-video-understanding-eap`.

```text
├── rapid_crossing/
│   ├── generate_variants.py         # Suite A: 8s Rapid Crossing generator
│   ├── generate_needle_variants.py  # Suite B: 60-90s Needle-in-a-Haystack generator
│   ├── needle_variants.json         # Needle benchmark spec (micro-IDs, ambient decoys)
│   ├── variants_hard.json           # Stress test spec (0.08s gaps, variable speeds, no labels)
│   ├── tools/
│   │   └── video_tools.py           # High-FPS frame extraction and spatial crop tools
│   ├── agentic_runner.py            # Multi-turn agent loop with active tool calling
│   ├── static_runner.py             # Single-pass static baseline runner
│   ├── run_demo.py                  # Standard CLI test harness
│   ├── score_results.py             # Scorer for Suite A
│   └── score_needle.py              # Scorer for Suite B (evaluates sequence + micro-IDs)
├── assets/                          # Standard registered test clips
├── generated_needle/                # 60s-90s Needle benchmark clips & results
├── generated_hard/                  # Stress-test clips & results
└── submission/
    ├── gde-demo-brief.md            # GDE launch demo narrative
    └── email-to-zviad.md            # Partner launch summary
```

---

## Benchmark Results

Treat these as controlled synthetic results, not production-readiness claims. The
registered easy variants are useful as pipeline controls, while the hard variants
are intentionally failure-finding probes.

### Suite A: Registered rapid-crossing controls (8-second clips)
Evaluates whether the model can follow deterministic color-order changes across
short synthetic clips:

```
Static single-pass accuracy : 15/15 (100.0%)
Agentic tool-loop accuracy  : 15/15 (100.0%)
```

This suite saturates both modes. It confirms that the harness, ground truth, and
scoring path work, but it does not by itself prove agentic superiority.

### Suite A-hard: Stress variants (8-second clips)
Evaluates smaller objects, no text labels, tighter gaps, overlapping lanes,
variable speeds, bidirectional motion, and decoys:

```
Static single-pass accuracy : 2/10 (20.0%)
Agentic tool-loop accuracy  : 2/10 (20.0%)
```

The no-label control succeeded in both modes, so the showcase is not merely
reading printed labels. The harder variants also expose current failure modes:
both modes confuse `magenta` with `purple` on several runs, and the decoy /
bidirectional setting can add non-crossing objects to the predicted sequence.
These failures should remain visible in any public write-up.

### Suite B: Long-Duration Needle-in-a-Haystack (60s–90s clips + Micro-IDs)
Evaluates why an **Agentic Tool Loop** is necessary over long video streams:

```
=====================================================================
            NEEDLE-IN-A-HAYSTACK AVU SHOWCASE BENCHMARK              
=====================================================================
Static Single-Pass Accuracy : 2/3 (66.7%)  [Failed on sub-second ordering]
Agentic Tool-Loop Accuracy  : 3/3 (100.0%) [100% Exact Sequence + IDs]
=====================================================================
```

#### Why Static Failed on `needle_event_22s.mp4`:
In a 60-second video stream, static downsampling inverted two near-simultaneous crossing events occurring 0.12s apart ($t=22.30\text{s}$ and $t=22.42\text{s}$).  
**The Agentic Loop won** by localizing the window to $[21.0\text{s}, 24.2\text{s}]$, extracting 64 high-res frames at 20 FPS, and reading both the exact chronological order and the micro-digit IDs (`#74`, `#97`, `#54`, `#48`, `#31`).

---

## Quick Start & Reproducibility

### 1. Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-showcase.txt google-genai
```

### 2. Configure Environment
```bash
cp .env.example .env
# Add your GEMINI_API_KEY in .env
```

### 3. Generate Needle-in-a-Haystack Benchmark Clips
```bash
python rapid_crossing/generate_needle_variants.py \
  --spec rapid_crossing/needle_variants.json \
  --output-dir generated_needle
```

### 4. Run Static vs. Agentic Benchmarks
```bash
# Run Static Baseline
export $(cat .env | xargs) && python rapid_crossing/static_runner.py

# Run Agentic Tool Loop
export $(cat .env | xargs) && PYTHONPATH=. python rapid_crossing/agentic_runner.py
```

### 5. Score Exact Accuracy
```bash
python rapid_crossing/score_needle.py \
  --results generated_needle/agentic_results.jsonl \
  --truth-dir generated_needle/ground_truth
```

---

## 📜 Capability Claims Ledger

See [CLAIMS.md](CLAIMS.md) for full protocol qualifiers.

1. **Short control variants saturated**: both static and agentic achieved 15/15 exact on the registered short clips.
2. **Hard variants expose limits**: both static and agentic achieved 2/10 exact on the current hard suite, mainly due to color-name confusion and decoy/order errors.
3. **Needle benchmark shows tool-assisted gain**: on the long clips with micro-IDs, agentic achieved 3/3 exact versus 2/3 for static single-pass processing.
4. **No-label ablation passed**: the current hard no-label variant was exact in both modes, so the observed success is not solely OCR over printed color names.

## Security Note

Do not commit or share `.env`. The file is ignored by git, but local zip exports
can still include it if the archive command is too broad. Use `.env.example` for
configuration instructions and rotate any key that has been sent outside the
private development environment.
