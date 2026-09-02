# Agentic Video Understanding (AVU) Showcase

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Google GenAI SDK](https://img.shields.io/badge/SDK-google--genai-green.svg)](https://ai.google.dev/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

> The visual front door for a reproducible static-versus-agentic video evaluation. Exact benchmark claims come from the parent `avu-eval` harness; polished showcase renders remain illustrative unless explicitly linked to a hash-verified canonical export.

---

## 🌟 What is Agentic Video Understanding?

Standard multimodal AI systems process video using **Static Video Understanding**:
When given a video, the system ingests a uniformly downsampled sequence of frames (e.g., 1 frame per second or a fixed frame budget). 

* **A potential static blind spot**: If a decisive event occurs briefly or requires tiny visual details inside a long stream, uniform sampling may miss or blur it. Whether that happens is task- and model-dependent and must be measured.
* **The Agentic Paradigm (AVU)**: Rather than passively watching a downsampled stream, an **Agentic Video Understanding** system operates as an **active investigator with tool access**. It:
  1. **Scans** the overview to localize candidate time windows (*"Action detected between 00:21.0s and 00:24.0s"*).
  2. **Invokes active tools** (such as high-FPS temporal slicing via `ffmpeg`) to retrieve native-resolution, high-framerate frames for the critical window.
  3. **Requests source-resolution frames or crops** for closer inspection of fine details.
  4. **Returns an answer whose quality and resource use can be measured** against the paired static condition.

---

## 🛠️ The Technology: Gemini Interactions API

This showcase utilizes the **Gemini Interactions API** from the `google-genai` Python SDK. The Interactions API provides a unified, stateful interface designed for complex agentic loops, native tool calling, and multimodal reasoning.

### How Video Understanding Works in the Interactions API

Under the Gemini Interactions API, video understanding follows an interleaved content model:
1. Videos are uploaded via `client.files.upload()`.
2. The uploaded file URI is passed as a structured content object `{"type": "video", "uri": uploaded.uri, "mime_type": "video/mp4"}` directly into `client.interactions.create()`.
3. The model can utilize tools (Google Search, Python functions, frame extraction) and multi-step reasoning (`thinking_level`) to solve multi-stage video queries.

### Quick Example: Calling Video Understanding via SDK

```python
import os
import time
from google import genai

# 1. Initialize client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Upload video asset
video_file = client.files.upload(
    file="path/to/video.mp4", 
    config={"mime_type": "video/mp4"}
)

# 3. Query using the Interactions API
interaction = client.interactions.create(
    model="gemini-3.7-flash",  # or models/gemini-3.6-flash-video-understanding-eap
    input=[
        {"type": "video", "uri": video_file.uri, "mime_type": "video/mp4"},
        {"type": "text", "text": "Identify the exact timestamps where objects cross the center reference line."}
    ],
    tools=[{"type": "google_search"}],
    generation_config={
        "max_output_tokens": 65536,
        "thinking_level": "medium"
    }
)

# 4. Extract model response
print(interaction.steps[-1].text)
```

> **Official SDK Reference**: For complete API documentation, visit the [Google AI for Developers](https://ai.google.dev/) portal.

---

## 🎯 Poised Real-World Use Cases

| Industry | The Static AI Challenge | The Agentic (AVU) Advantage |
|---|---|---|
| **Security & Surveillance Forensics** | Sifting through hours of CCTV footage misses a 2-second license plate or suspect crossing. | Agent scans for motion anomalies, triggers a high-FPS zoom crop on the vehicle, and extracts the plate digits. |
| **Sports Adjudication & VAR** | Millisecond photo-finishes or rapid ball deflections blur across uniform frame sampling. | Agent identifies the play window, pulls 60 FPS sub-second crops, and accurately determines the winner. |
| **Industrial QC & Robotics** | High-speed conveyor belts produce micro-defects that appear for only a fraction of a second. | Agent monitors overall cadence, inspects high-speed frame bursts on anomalies, and logs defect serial IDs. |
| **Medical & Surgical Analysis** | Long procedure recordings contain critical tool handoffs and phase transitions requiring sub-second tracking. | Agent navigates surgical phases, zooming into high-resolution operative windows without exceeding context limits. |

---

## 🔬 Showcase Benchmark Suites

This repository contains two deliberately separate layers:

1. **Canonical benchmark:** eight deterministic Phase 4 tasks defined in
   `../data/tasks/phase4_tracking_ablation.jsonl` and rendered by
   `avu_eval.synthetic`. Only exact, hash-verified exports of these videos may
   inherit Phase 4 provenance.
2. **Visual demo:** the seeded 960×540 generators under `rapid_crossing/`.
   These are useful for presentation and exploratory testing, but they are not
   interchangeable with the canonical 640×360 benchmark.

```text
avu-eval/
├── data/tasks/phase4_tracking_ablation.jsonl  # canonical task definitions
├── src/avu_eval/synthetic.py                  # canonical renderer + guardrails
├── artifacts/                                 # canonical runs and reports
└── showcase/
├── rapid_crossing/
│   ├── generate_variants.py         # Suite A: 8s Fine-Motion generator
│   ├── generate_needle_variants.py  # Suite B: 60-90s Needle-in-a-Haystack generator
│   ├── needle_variants.json         # Needle benchmark spec (micro-IDs, ambient decoys)
│   ├── variants_hard.json           # demo-only 960×540 stress spec
│   ├── tools/
│   │   └── video_tools.py           # High-FPS frame extraction and spatial crop tools
│   ├── agentic_runner.py            # Multi-turn agent loop with active tool calling
│   ├── static_runner.py             # Single-pass static baseline runner
│   ├── run_demo.py                  # Standard CLI test harness
│   ├── score_results.py             # Scorer for Suite A
│   └── score_needle.py              # Scorer for Suite B (evaluates sequence + micro-IDs)
├── assets/                          # Standard registered test clips
├── generated_needle/                # 60s-90s Needle benchmark clips & results
├── generated_hard/                  # historical demo-suite clips & results
├── generated_canonical_phase4/      # exact canonical exports + hashes
└── tests/
    └── test_showcase.py             # Determinism and parser unit tests
```

---

## 📊 Evidence status

### Canonical Phase 4 tracking ablation

The eight-task suite and its generator validations are complete, including the
matched label/no-label control, minimum two-frame crossing gaps, explicit
decoys, bidirectional motion, controlled overlap, and ground-truth checks.

**Model-result status: not yet measured.** Passing validation and unit tests
establishes stimulus integrity, not model accuracy.

### Historical 960×540 showcase suites

- Registered short controls: static 15/15 exact; agentic 15/15 exact.
- No-label hard control: static 2/2 exact; agentic 2/2 exact.
- Full hard suite: static 2/10 exact; agentic 2/10 exact.

The hard-suite result exposes failures in both modes; it does not support a
general agentic-over-static claim.

---

### Suite B: Long-Duration Needle-in-a-Haystack (60s–90s clips + Micro-IDs)
Evaluates why an **Agentic Tool Loop** is necessary over long, dense video streams:

```
=====================================================================
            NEEDLE-IN-A-HAYSTACK AVU SHOWCASE BENCHMARK              
=====================================================================
Static Single-Pass Accuracy : 2/3 (66.7%)  [Failed on sub-second ordering]
Agentic Tool-Loop Accuracy  : 3/3 (100.0%) [100% Exact Sequence + IDs]
=====================================================================
```

#### The Discriminative Case: `needle_event_22s.mp4` (60s HD)
* **Ground Truth**: `Blue #74` $\rightarrow$ `Magenta #97` $\rightarrow$ `Yellow #54` $\rightarrow$ `Orange #48` $\rightarrow$ `Cyan #31`
* **Static Single Pass**: ❌ **FAILED** — Swapped `Magenta #97` before `Blue #74` because uniform downsampling across the 60s stream blurred the 0.12s gap ($t=22.30\text{s}$ vs $t=22.42\text{s}$).
* **Agentic Tool Loop**: ✅ **100% EXACT** — Step 1 localized the window to $[21.0\text{s}, 24.2\text{s}]$, Step 2 extracted 64 high-FPS frames via `ffmpeg`, and Step 3 correctly resolved `Blue #74` before `Magenta #97`.

---

## 🚀 Quick Start

### 1. Clone & Setup Environment
```bash
git clone YOUR_PRIVATE_REPOSITORY_URL avu-eval
cd avu-eval

python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r showcase/requirements-showcase.txt
```

### 2. Configure API Credentials
```bash
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY
```

### 3. Export the exact canonical Phase 4 videos
```bash
avu-eval showcase-export \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --output showcase/generated_canonical_phase4

avu-eval showcase-verify \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --input showcase/generated_canonical_phase4
```

### 4. Run the canonical benchmark
```bash
avu-eval run \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --config YOUR_REGISTERED_CONFIG.yaml \
  --output artifacts/runs/phase4-tracking-ablation.jsonl
```

### 5. Generate the report
```bash
avu-eval report \
  --input artifacts/runs/phase4-tracking-ablation.jsonl \
  --output artifacts/reports/phase4-tracking-ablation
```

---

## 📜 Claims Ledger

See [CLAIMS.md](CLAIMS.md) for full protocol qualifiers.

1. **Short registered controls saturated:** both modes achieved 15/15 exact.
2. **Historical hard-suite failures are preserved:** both modes achieved 2/10 exact.
3. **Long needle illustration:** static achieved 2/3 full exact versus agentic 3/3 on a small synthetic suite.
4. **Canonical Phase 4:** stimuli validated; model performance not yet measured.
