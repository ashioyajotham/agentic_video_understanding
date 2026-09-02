# Capability-claim ledger

This ledger prevents launch copy from getting ahead of the evidence.

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
| Agentic outperforms static across the variant family. | Not supported by the short/hard showcase suites | Supported only by the long needle suite in this repo; broader claims require the parent eval harness. |
| The latency trade-off is acceptable for fine-motion queries. | Not established here | Report latency distributions from the parent harness or add telemetry to this showcase. |

## Explicitly prohibited claims

- “Agentic video understanding is always more accurate.”
- “Agentic mode is faster” without naming the exact task and measurement.
- “The system generalizes to real-world video” from this synthetic suite alone.
- “The benchmark proves production readiness.”
- “Hard variants were solved at 100% exactness.”
- “The model resolves sub-frame ordering.”
- Any claim based on a cherry-picked successful seed while omitting registered
  variants, timeouts, retries, or failures.

## Claim template after validation

> Across **N** preregistered synthetic rapid-crossing variants and **R** repeated
> attempts per mode, **MODEL** achieved **A/B** exact agentic responses versus
> **C/D** static responses under a **T-second** timeout. These results support
> selective agentic inspection for fine-grained temporal ordering in this
> controlled setting; they do not establish universal video-understanding gains.
