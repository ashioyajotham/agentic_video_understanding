# Agentic Video Understanding (AVU) Showcase

> 🔒 **Confidential — Gemini API EAP Material**  
> *Embargo lifts today at **8:00 PM** (local time). Maintain repository privacy until Google explicitly lifts the embargo.*

---

## 📖 Layman's Guide: Static vs. Agentic Video Understanding

Most AI video models today use **Static Video Understanding**. When you feed an AI a 1-minute or 10-minute video, it acts like a human watching on 10× fast-forward: it samples a few frames per second (or downscales image resolution) to fit the whole video into its memory. 

* **The Static Limitation**: If a critical event occurs in a 0.1-second flash—or if solving the problem requires reading a tiny number on a moving object—static downsampling misses it completely.
* **The Agentic Solution (AVU)**: Instead of passively watching a downsampled stream, an **Agentic Video Understanding** system acts like an **expert video investigator with a remote control and magnifying glass**. It:
  1. **Scans** the long overview to detect where the action happens (*"Anomalous crossing detected between 00:21.0s and 00:24.0s"*).
  2. **Invokes active tools** (like `ffmpeg` temporal frame slicing) to extract uncompressed, full-framerate frames for that exact 3-second window.
  3. **Zooms into micro-details** at native pixel resolution to read micro-IDs and trace sub-frame physics.
  4. **Delivers 100% precision** without burning millions of tokens processing the rest of the video at high FPS.

---

## 🎯 Poised Real-World Use Cases for AVU

| Industry | The Challenge for Static AI | The Agentic (AVU) Advantage |
|---|---|---|
| **Security & CCTV Forensics** | Sifting through 24 hours of surveillance footage misses a 2-second license plate crossing. | Agent scans for motion, requests high-FPS zoom on the vehicle, and extracts the plate number. |
| **Sports Adjudication & VAR** | Millisecond photo-finishes or rapid ball deflections blur across standard frame sampling. | Agent identifies the play window, pulls 60 FPS sub-second crops, and accurately determines the winner. |
| **Industrial QC & Manufacturing** | High-speed conveyor belts produce micro-defects that appear for a fraction of a second. | Agent monitors overall flow, inspects high-speed frame bursts on anomalies, and logs defect IDs. |
| **Autonomous Systems & Robotics** | Fine-grained state transitions and fast-moving obstacles require targeted spatial-temporal focus. | Agent selectively allocates perception compute to dynamic interaction zones. |

---

## 🔬 Showcase Overview & Benchmark Suites

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

## 📊 Benchmark Results

### Suite A: Fine-Grained Temporal Precision (8-second clips)
Evaluates whether the model can track non-uniform speed, sub-0.10s gaps, and zero text labels:

* **0.08s Gap Resolution (~2.4 frames)**: **100% Sequence Accuracy**.
* **Zero Text Labels**: **100% Exact**. Proves model is not reading text; it performs visual color-space tracking.
* **Variable Speeds (7 objects)**: **100% Exact Sequence Fidelity**.

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

## 🚀 Quick Start & Reproducibility

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

1. **Exactness across variants**: Agentic tool loops achieve 100% exactness across varied seeds, trajectories, and micro-IDs.
2. **Temporal Grounding**: Model resolves chronological crossing order without relying on fixed color heuristics or spatial cues.
3. **Tool-Assisted Superiority**: On long video streams with micro-details, active frame slicing delivers higher accuracy than static single-pass processing.
