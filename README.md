# Agentic Video Understanding Eval

A reproducible, paired evaluation of **static** versus **agentic** video processing. The harness runs the same model, video, prompt, and thinking configuration in both modes and records quality, input-token use, latency, strategy traces, and failure modes.

> Keep this repository and all EAP details, outputs, screenshots, and results private until the program owner explicitly lifts confidentiality.

## Core question

Does query-adaptive video inspection preserve or improve answer quality while using fewer input tokens—and when does its chosen viewing strategy fail?

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
```

## Quick start

The supplied notebook requires the unreleased SDK wheel below. This is the exact wheel named in the EAP materials—not a separate SDK:

```bash
python -m venv .venv
source .venv/bin/activate
gsutil cp gs://gemini-api-eap/VideoUnderstanding/google_genai-2.14.2-py3-none-any.whl .
pip uninstall -y google-genai
pip install ./google_genai-2.14.2-py3-none-any.whl
pip install -e .
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

The adapter follows the supplied Colab's Interactions API request shape and usage fields. The Colab does not demonstrate a thinking-level request parameter, so the harness does not invent one. Strategy traces are captured only if an installed SDK response actually exposes them.

## Evaluation ladder

1. Short-video smoke tests: recognition, spatial relations, order, counting.
2. Fine motion: brief events requiring selective high-FPS inspection.
3. Cumulative state: the `snake_state` family tracks a progressively changing hidden state.
4. Sparse-event search: a decisive event embedded among distractors.
5. Transcript routing: transcript-sufficient, visual-only, and audio/visual-conflict cases.
6. Long-form retrieval and summarization.
7. Adversarial negatives: expected-but-absent events and false premises.

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for hypotheses and grading rules.

## Phase 2 priority run

Phase 2 moves beyond the saturated short-video baseline. It adds reversible state, incomplete-action negatives, a sub-second event hidden in five minutes, timestamp localization, and a five-event order compressed into under one second.

```bash
avu-eval generate --suite data/tasks/phase2_priority.jsonl
avu-eval validate --suite data/tasks/phase2_priority.jsonl
avu-eval run --suite data/tasks/phase2_priority.jsonl --config configs/phase2_priority.yaml --output artifacts/runs/phase2-priority.jsonl
avu-eval report --input artifacts/runs/phase2-priority.jsonl --output artifacts/reports/phase2-priority
```

The priority matrix is 36 attempts. Videos are uploaded before request timing, condition order is counterbalanced, each attempt has a hard timeout, timeouts are written as results, and rerunning the same command resumes missing jobs instead of duplicating completed rows. See [docs/PHASE2.md](docs/PHASE2.md).
