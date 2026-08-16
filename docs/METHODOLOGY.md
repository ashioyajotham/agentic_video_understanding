# Methodology

## Experimental question

For a fixed model and query, does query-adaptive video processing outperform fixed-rate processing on the joint objective of quality, token use, and latency?

The primary unit is a paired `(task, repetition)` comparison. Never compare agentic and static modes on different prompts, different encodes, or different model versions.

## Hypotheses

1. **Sparse evidence:** Agentic mode should spend fewer tokens while retaining accuracy when a long video contains a short decisive interval.
2. **Transcript sufficiency:** It should prefer transcript extraction when visual frames add no evidence.
3. **Fine motion:** It should selectively increase sampling around rapid actions and improve motion accuracy.
4. **Cumulative state:** It should recover multiple separated state transitions rather than answering from the final frame or narrative priors.
5. **Short-video overhead:** It may add latency or tokens without quality gains when exhaustive static inspection is already cheap.

## The cumulative-state challenge

The synthetic snake sequence is a video analogue of long-horizon state tracking in agents. Each swallowing event updates a latent state:

`S_t = S_(t-1) + [(object_id, attribute, event_time)]`

Questions probe distinct failure surfaces:

- final count: cumulative retention;
- chronological list: ordering;
- second event: targeted retrieval;
- repeated colors: identity versus set-based shortcuts;
- absent color: hallucination resistance;
- later variants: occlusion, expulsion/reversal, swaps, and distractor near-events.

The videos are synthetic because exact ground truth, event boundaries, and controlled counterfactual pairs matter more here than visual realism. Natural-video suites complement them for external validity.

## Task families

| Family | Manipulation | Intended strategy | Principal failure |
|---|---|---|---|
| Short smoke | <1 minute, dense evidence | Static may suffice | Agentic overhead |
| Sparse event | Brief event in 5–30 minutes | Scan, then focus | Skipped decisive interval |
| Fine motion | Fast action or brief text | Selective high FPS | Temporal aliasing |
| Transcript sufficient | Static visuals, informative speech | Transcript first | Wasteful frame processing |
| Visual contradiction | Speech conflicts with pixels | Inspect visuals | Transcript over-reliance |
| Cumulative state | Separated irreversible updates | Revisit event windows | Final-frame shortcut |
| Reversible state | Add/remove/swap events | Track current state | Monotonicity assumption |
| Long retrieval | 1+ hour with distractors | Progressive search | Context loss or repeated scans |
| Negative premise | Expected event is absent | Verify evidence | Sequential-inference hallucination |

## Metrics

- **Quality:** exact accuracy or partial-credit structured score.
- **Input-token delta:** `(agentic - static) / static` for paired runs.
- **Latency delta:** identical calculation on wall-clock latency.
- **Reliability:** mean score plus per-task variance across repetitions.
- **Strategy appropriateness:** human label of trace: appropriate, under-watch, over-watch, repeated/non-convergent, transcript error.
- **Pareto outcome:** agentic wins only if quality improves without unreasonable cost, or cost falls without meaningful quality loss.

Report accuracy and cost separately; do not collapse them into one arbitrary scalar. Token counts in an EAP may not match public-launch accounting.

## Grading

Prefer constrained outputs: one number, one label, JSON arrays, or timestamp intervals. Avoid LLM-as-judge for the core synthetic suite. Human review is reserved for free-form summaries and surfaced strategy traces.

Run at least three repetitions per mode. Preserve raw outputs even when deterministic graders assign zero so errors can be regraded without rerunning the model.

## Threats to validity

- Synthetic simplicity may encourage end-frame shortcuts; include questions unanswerable from the final frame.
- Generated clips may contain rendering artifacts; visually inspect every canonical stimulus.
- Prompt wording can alter strategy; freeze prompts before comparison.
- Upload/transcoding and cache effects can affect latency; randomize or alternate condition order in a fuller study.
- The supplied Colab does not show a thinking-level parameter or a stable machine-readable strategy-trace field. Do not invent either; store them only if a subsequently validated SDK response exposes them.
