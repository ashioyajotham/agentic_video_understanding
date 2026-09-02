# Phase 4: Tracking Ablation

This suite tests whether rapid-order performance depends on OCR labels, separate lanes, uniform motion, or proximity shortcuts. It is an ablation ladder, not eight interchangeable benchmark items.

## Experimental order

1. Run `phase4_control_unlabeled` and `phase4_ocr_positive_control` first.
2. Run the four isolated stressors: small/many, tight timing, overlap, and bidirectional/variable speed.
3. Run decoys/grid.
4. Run `phase4_combined_hard` only after visually verifying every earlier stimulus.

Do not pool the eight items into one headline number without also reporting each task. The paired control is specifically designed to measure label dependence.

## Validity guardrails

- True crossing gaps are never below two source frames.
- The validator rejects sub-frame ordering.
- Decoy centers remain farther from the gate than their radius, so they cannot touch or cross it.
- Ground-truth ordered lists are checked against rendered crossing times.
- Partial occlusion uses small vertical offsets rather than perfectly coincident, unrecoverable trajectories.
- The original generator default is unlabeled; labels are enabled only for the matched OCR-positive control.

## Commands

```powershell
python -m pip install -e .

python -m unittest discover -s tests -v

avu-eval validate `
    --suite data/tasks/phase4_tracking_ablation.jsonl

avu-eval generate `
    --suite data/tasks/phase4_tracking_ablation.jsonl
```

Inspect every generated MP4 at native resolution before any paid run. In particular, confirm that:

- The two control videos differ only by printed labels.
- Each decoy visibly reverses before touching the gate.
- Bidirectional objects start on the correct side.
- The combined-hard ordering is recoverable at normal playback and frame-by-frame.

Then create one-repetition model configurations and run static and agentic modes exactly as in Phase 3. Treat the first pass as stimulus validation, not as a publishable denominator. Use three repetitions only after the videos and grader outputs pass review.

## Claim gate

Do not claim general temporal-tracking superiority from this suite unless:

- the unlabeled control rules out dependence on text labels;
- at least one isolated stressor reproducibly separates modes;
- the separation survives three repetitions;
- every reported failure is checked against human-solvability;
- denominators, failed requests, semantic scoring, and strict-format scoring are reported separately.

## Registered Gemini 3.7 Flash result

The claim gate was executed with the public `gemini-3.7-flash` model through
`google-genai` 2.21.0. The matrix contained eight tasks, static and agentic
processing, and three repetitions: 48 unique observations with no request
failures or duplicate keys.

| Task | Static exact | Static semantic | Agentic exact | Agentic semantic |
|---|---:|---:|---:|---:|
| Unlabeled control | 0/3 | 0.000 | **3/3** | **1.000** |
| OCR-positive control | 0/3 | 0.000 | **3/3** | **1.000** |
| Small/many | 0/3 | 0.000 | **1/3** | **0.875** |
| Tight timing | 0/3 | 0.000 | **1/3** | **0.917** |
| Overlap | 2/3 | 0.952 | **3/3** | **1.000** |
| Bidirectional/variable | 1/3 | 0.667 | **3/3** | **1.000** |
| Decoys/grid | 0/3 | 0.421 | 0/3 | **0.833** |
| Combined hard | 0/3 | 0.519 | 0/3 | 0.519 |
| **All registered attempts** | **3/24** | **0.320** | **14/24** | **0.893** |

All 24 agentic responses exposed at least one matched `processing_call` and
`processing_result`; none of the static responses did. Thus the treatment was
observed in the public response, not inferred solely from the request config.

### Failure analysis

- Seven agentic failures were color-vocabulary mismatches while preserving the
  complete sequence: `teal` for `cyan` or `pink` for `magenta`.
- Alias normalization would produce 21/24 agentic exact versus 4/24 static, but
  this is diagnostic only. The registered exact metric remains 14/24.
- All three remaining agentic failures occurred on `combined_hard`. Two added
  false crossings while retaining the true sequence; one also misordered true
  events. This is evidence of a decoy/identity limit.
- Every response was fenced as Markdown, so strict JSON compliance was 0/48.

### Resource trade-off

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| Provider latency | 11.452 s | 15.376 s | +34.3% |
| Wall latency | 11.773 s | 15.700 s | +33.4% |
| Reported input tokens | 557 | 328 | −41.1% |
| Total tokens | 2,470 | 9,071 | +267.2% (3.67×) |
| Thought tokens | 1,876 | 1,992 | +6.2% |

Agentic had a mean 6,598-token residual after subtracting reported input,
output, and thought tokens from total tokens. Because this residual appears
only with processing calls, lower reported input tokens must not be presented
as lower total usage or cost. Agentic used fewer total tokens in none of the 24
matched cells.

## Reproduction

```bash
avu-eval run \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --config configs/models/gemini-3.7-phase4-replication.yaml \
  --output artifacts/runs/phase4-validation/gemini-3.7-phase4-replicated.jsonl

avu-eval report \
  --input artifacts/runs/phase4-validation/gemini-3.7-phase4-replicated.jsonl \
  --output artifacts/reports/phase4-validation/gemini-3.7-phase4-replicated
```
