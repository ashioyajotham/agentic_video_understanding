# Capability-claim ledger

This ledger prevents launch copy from getting ahead of the evidence.

## Evidence boundary after repository integration

| Artifact | Role | Claim eligibility |
|---|---|---|
| `data/tasks/phase4_tracking_ablation.jsonl` rendered by `avu_eval.synthetic` | Canonical eight-task ablation benchmark | Eligible only after registered model runs on the exact exported bytes. |
| `showcase/generated_canonical_phase4/` | Hash-verified copies of canonical stimuli and ground truth | Inherits Phase 4 provenance; the export itself contains no model result. |
| `showcase/rapid_crossing/variants_hard.json` rendered at 960×540 | Seeded visual demo and historical exploratory suite | Demo-specific results only; never relabel as Phase 4 evidence. |
| `showcase/generated_hard/` | Historical showcase outputs | Preserve with original denominators and failures. |
| `results/phase4/gemini-3.7-phase4-replicated.jsonl` | Exact 48-row registered public run | Primary model-result evidence; reports must be reproducible from these rows. |

Changing resolution, renderer, trajectories, labels, or encoding creates a new
stimulus. Results do not transfer between the 960×540 showcase and the 640×360
canonical benchmark merely because their concepts map to one another.

## Observed in the original controlled evaluation

| Claim | Status | Required qualifier |
|---|---|---|
| Agentic was exact on the original rapid-crossing task in 3/3 primary attempts. | Observed | One synthetic task; three repetitions. |
| Static was not exact in the three primary attempts. | Observed | Primary attempts used the evaluation timeout; diagnostic retries are separate. |
| Agentic provider latency was 55.7% lower on this task. | Observed | Task-specific, not the suite-wide latency result. |
| Selective frame inspection can resolve fine-motion ordering missed by a static pass. | Supported illustration | Phrase as a demonstrated mechanism/use case, not a universal guarantee. |

## Observed in this showcase repository

| Claim | Status | Required qualifier |
|---|---|---|
| The registered short rapid-crossing variants saturated both modes. | Observed | Static: 15/15 exact. Agentic: 15/15 exact. This is a control result, not evidence of agentic superiority. |
| The no-label hard control was exact in both modes. | Observed | Static: 2/2 exact. Agentic: 2/2 exact on `hard_no_labels_01`; this supports "not only label reading" for that control. |
| The current hard suite exposes failures in both modes. | Observed | Static: 2/10 exact. Agentic: 2/10 exact. Preserve failures when reporting. |
| Long needle clips showed an agentic advantage. | Observed | Static: 2/3 full exact. Agentic: 3/3 full exact. Small synthetic sample with one static miss. |
| Hard-suite failures include color aliasing and decoy/order errors. | Observed | Several responses use `purple` for expected `magenta`; decoy/bidirectional runs can include non-crossing objects. |

## Claims this showcase is designed to test

| Claim | Status before variant runs | Promotion criterion |
|---|---|---|
| The behavior persists when the input clip changes. | Partially supported | Registered controls pass; hard variants fail. Report per-suite denominators. |
| The model follows the temporal event rather than a fixed color sequence. | Partially supported | Registered controls and the no-label hard control pass; hard decoy/overlap variants need stronger analysis. |
| Agentic outperforms static across the variant family. | Supported on canonical Phase 4; not supported by the historical short/hard demo suites | Canonical: agentic scored higher in 19/24 matched cells, tied three, and lost two. Keep renderer-specific results separate. |
| Agentic improves quality without a resource penalty. | Refuted on canonical Phase 4 | Agentic was 34.3% slower by mean provider latency and used 3.67× mean total tokens. |

## Canonical Phase 4 result: Gemini 3.7 Flash

The registered public-API run is complete: eight deterministic tasks, two
processing modes, and three repetitions produced 48/48 completed attempts.
All results below come from the canonical 640×360 renders and must not be
attributed to the separate 960×540 demo suite.

| Metric | Static | Agentic |
|---|---:|---:|
| Attempts completed | 24/24 | 24/24 |
| Registered exact | 3/24 (12.5%) | **14/24 (58.3%)** |
| Mean semantic score | 0.320 | **0.893** |
| Strict JSON | 0/24 | 0/24 |
| Mean provider latency | **11.452 s** | 15.376 s |
| Mean total tokens | **2,470** | 9,071 |
| Native processing steps observed | 0/24 | **24/24** |

Agentic scored higher in 19/24 matched cells, tied in three, and scored lower
in two. It was faster in 7/24 cells and used fewer total tokens in 0/24.

The matched OCR ablation reproduced across all attempts: static was exact in
0/3 unlabeled and 0/3 labeled attempts, while agentic was exact in 3/3 for each
condition. Visible labels therefore did not explain the observed separation.

Seven of the ten non-exact agentic responses preserved the complete expected
order and differed only by `teal`/`cyan` or `pink`/`magenta`. Treating these as
aliases yields a diagnostic—not registered—exact result of 21/24 agentic versus
4/24 static. The three remaining agentic failures were all on
`phase4_combined_hard`; this is the demonstrated breaking point.

The result supports a controlled fine-motion tracking advantage. It does not
support universal accuracy, speed, cost, or real-world generalization claims.

## Explicitly prohibited claims

- “Agentic video understanding is always more accurate.”
- “Agentic mode is faster” without naming the exact task and measurement.
- “The system generalizes to real-world video” from this synthetic suite alone.
- “The benchmark proves production readiness.”
- “Hard variants were solved at 100% exactness.”
- “Phase 4 achieved X%” when X was measured on the separate 960×540 demo renderer.
- “Removing labels proves identity tracking” without reporting the paired labeled control.
- “The model resolves sub-frame ordering.”
- Any claim based on a cherry-picked successful seed while omitting registered
  variants, timeouts, retries, or failures.

## Approved Phase 4 claim

> Across 24 matched attempts on eight registered deterministic tracking
> ablations, Gemini 3.7 Flash agentic video processing achieved 14/24 registered
> exact responses versus 3/24 for static processing, with mean semantic scores
> of 0.893 versus 0.320. The separation persisted with and without visible
> labels. Agentic mean provider latency was 34.3% higher and mean total-token
> usage was 3.67× static. Both modes failed the combined-hard condition in all
> three repetitions. These synthetic results do not establish universal or
> real-world video-understanding gains.
