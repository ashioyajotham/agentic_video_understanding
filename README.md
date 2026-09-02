# Agentic Video Understanding Eval

A reproducible, paired evaluation of **static** versus **agentic** video processing. The harness runs the same model, video, prompt, and thinking configuration in both modes and records quality, input-token use, latency, strategy traces, and failure modes.

Agentic video understanding is now available through the public Gemini API. Historical EAP artifacts and private service traces should still be reviewed before publication.

## Core question

Does query-adaptive video inspection preserve or improve answer quality while using fewer input tokens—and when does its chosen viewing strategy fail?

## Phase 4 headline result

On eight registered deterministic tracking ablations with three repetitions,
Gemini 3.7 Flash agentic processing achieved **14/24 exact** responses versus
**3/24 static**, with mean semantic scores of **0.893 versus 0.320**. The
label/no-label pair produced the same separation, weakening the OCR-shortcut
explanation. Native processing calls/results were observed in all 24 agentic
attempts and none of the static attempts.

This quality gain was not free: agentic mean provider latency was 34.3% higher
and mean total-token usage was 3.67× static. Both modes failed the combined
overlap + decoy + noise + fine-timing condition in all three repetitions. See
[the Phase 4 methodology and results](docs/PHASE4_TRACKING_ABLATION.md) and the
[claim ledger](showcase/CLAIMS.md) for denominators and failure analysis. The
exact public JSONL and generated reports are versioned under
[`results/phase4/`](results/phase4/README.md).

## Design

- **Paired conditions:** `static` and `agentic` for every case.
- **Controlled synthetic tests:** exact event times and state transitions enable deterministic grading.
- **Natural-video tests:** transcript-heavy, sparse-event, and long-form cases test ecological validity.
- **Strategy auditing:** retain surfaced processing traces to diagnose missed windows, needless rescans, and transcript failures.
- **Repeated runs:** separate systematic capability gaps from stochastic variance.

## Repository map

```text
configs/                 Experiment configuration
data/tasks/              Versioned JSONL task manifests
docs/                    Methodology, references, feedback template
src/avu_eval/            Generator, runner, graders, reporting
artifacts/videos/        Generated/local videos (gitignored)
artifacts/runs/          Raw JSONL observations (gitignored)
artifacts/reports/       Aggregate CSV/Markdown reports (gitignored)
tests/                   Offline unit tests
showcase/                Visual front door and historical demo suites
```

## Quick start

Install the public Gemini SDK through the project dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
cp .env.example .env
```

Put only `GEMINI_API_KEY=...` in `.env`, or set that variable in the active shell. This harness does not enable Vertex AI.

Generate deterministic synthetic videos and validate their manifests:

```bash
avu-eval generate --suite data/tasks/synthetic_core.jsonl
avu-eval validate --suite data/tasks/synthetic_core.jsonl
```

Run the paired experiment:

```bash
avu-eval run \
  --suite data/tasks/synthetic_core.jsonl \
  --config configs/eval.yaml \
  --output artifacts/runs/synthetic_core.jsonl
```

Aggregate results:

```bash
avu-eval report \
  --input artifacts/runs/synthetic_core.jsonl \
  --output artifacts/reports/synthetic_core
```

Use `--dry-run` on `run` to inspect the full experiment matrix without calling the API.

The adapter uses the public Interactions API. Public model configurations use `gemini-3.7-flash`; the paired condition is selected with `processing: static` or `processing: agentic` on the video input. The harness records public processing step types and marks whether both a `processing_call` and `processing_result` were observed. It does not persist model thoughts.

## Evaluation ladder

1. Short-video smoke tests: recognition, spatial relations, order, counting.
2. Fine motion: brief events requiring selective high-FPS inspection.
3. Cumulative state: the `snake_state` family tracks a progressively changing hidden state.
4. Sparse-event search: a decisive event embedded among distractors.
5. Transcript routing: transcript-sufficient, visual-only, and audio/visual-conflict cases.
6. Long-form retrieval and summarization.
7. Adversarial negatives: expected-but-absent events and false premises.

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for hypotheses and grading rules.

## Showcase and canonical Phase 4 export

The showcase is integrated as a visual front door, not a second source of
benchmark truth. Its seeded 960×540 generators remain demo-specific. Export
exact canonical Phase 4 renders—with task, suite, and video hashes—using:

```bash
avu-eval showcase-export \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --output showcase/generated_canonical_phase4

avu-eval showcase-verify \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --input showcase/generated_canonical_phase4
```

See `showcase/CLAIMS.md` for the evidence boundary. A conceptual mapping between
a demo variant and a Phase 4 task does not transfer results across renderers.

## Phase 2 priority run

Phase 2 moves beyond the saturated short-video baseline. It adds reversible state, incomplete-action negatives, a sub-second event hidden in five minutes, timestamp localization, and a five-event order compressed into under one second.

```bash
avu-eval generate --suite data/tasks/phase2_priority.jsonl
avu-eval validate --suite data/tasks/phase2_priority.jsonl
avu-eval run --suite data/tasks/phase2_priority.jsonl --config configs/phase2_priority.yaml --output artifacts/runs/phase2-priority.jsonl
avu-eval report --input artifacts/runs/phase2-priority.jsonl --output artifacts/reports/phase2-priority
```

The priority matrix is 36 attempts. Videos are uploaded before request timing, condition order is counterbalanced, each attempt has a hard timeout, timeouts are written as results, and rerunning the same command resumes missing jobs instead of duplicating completed rows. See [docs/PHASE2.md](docs/PHASE2.md).
