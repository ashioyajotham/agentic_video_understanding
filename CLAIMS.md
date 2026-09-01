# Capability-claim ledger

This ledger prevents launch copy from getting ahead of the evidence.

## Observed in the original controlled evaluation

| Claim | Status | Required qualifier |
|---|---|---|
| Agentic was exact on the original rapid-crossing task in 3/3 primary attempts. | Observed | One synthetic task; three repetitions. |
| Static was not exact in the three primary attempts. | Observed | Primary attempts used the evaluation timeout; diagnostic retries are separate. |
| Agentic provider latency was 55.7% lower on this task. | Observed | Task-specific, not the suite-wide latency result. |
| Selective frame inspection can resolve fine-motion ordering missed by a static pass. | Supported illustration | Phrase as a demonstrated mechanism/use case, not a universal guarantee. |

## Claims this showcase is designed to test

| Claim | Status before variant runs | Promotion criterion |
|---|---|---|
| The behavior persists when the input clip changes. | Unvalidated | Report exactness over all registered variants and repetitions. |
| The model follows the temporal event rather than a fixed color sequence. | Unvalidated | Use different color orders and mirrored motion; score against per-clip ground truth. |
| Agentic outperforms static across the variant family. | Unvalidated | Same prompt, timeout, repetitions, and counterbalanced execution; report both denominators. |
| The latency trade-off is acceptable for fine-motion queries. | Unvalidated | Report distribution and tail latency, not a single average. |

## Explicitly prohibited claims

- “Agentic video understanding is always more accurate.”
- “Agentic mode is faster” without naming the exact task and measurement.
- “The system generalizes to real-world video” from this synthetic suite alone.
- “The benchmark proves production readiness.”
- Any claim based on a cherry-picked successful seed while omitting registered
  variants, timeouts, retries, or failures.

## Claim template after validation

> Across **N** preregistered synthetic rapid-crossing variants and **R** repeated
> attempts per mode, **MODEL** achieved **A/B** exact agentic responses versus
> **C/D** static responses under a **T-second** timeout. These results support
> selective agentic inspection for fine-grained temporal ordering in this
> controlled setting; they do not establish universal video-understanding gains.

