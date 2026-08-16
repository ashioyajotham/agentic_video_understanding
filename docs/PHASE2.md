# Phase 2: discriminative agentic-video evaluation

## Baseline findings that determine this phase

The short 18–24 second baseline saturated at 100% semantic accuracy among returned requests. Agentic mode used 85% more input tokens and 65% more total tokens across completed pairs, showed large repeated-run token variance, and failed to return once. Because the baseline lies in the documented static-friendly regime, Phase 2 treats it as a control rather than a general verdict.

The strongest baseline tasks were repeated-color identity tracking, the expected-but-absent negative, and chronological ordering. Phase 2 extends those dimensions rather than adding more trivial recognition questions.

## Priority hypotheses

| Priority | Task | Static weakness | Expected agentic advantage | Main metric |
|---|---|---|---|---|
| 1 | Five-minute sparse needle | Fixed 1 FPS can miss a 0.45 s event | Search then locally resample | Quality and tokens |
| 2 | Sub-second five-event order | One frame cannot recover the sequence | High-FPS inspection of a narrow window | Exact order accuracy |
| 3 | Three-minute reversible ledger | Final-frame and monotonic-state shortcuts fail | Retrieve multiple separated windows | Ledger accuracy |
| 4 | Incomplete yellow approach | Sequential prior encourages false completion | Verify whether the action finishes | Negative accuracy |
| 5 | Event-history counting | Final state differs from event count | Aggregate non-monotonic history | Count accuracy |

## Measurement fixes

- Every unique video is uploaded and processed before condition timing begins.
- `provider_latency_seconds` measures the API interaction itself; `upload_seconds` is stored separately.
- Odd repetitions run static then agentic; even repetitions reverse the order.
- A spawned request process is terminated after `timeout_seconds`, including on Windows.
- Timeout and error attempts are written to JSONL and count against completion.
- Existing `(task_id, mode, repetition)` records are skipped on rerun.
- Semantic correctness and strict response-format compliance are separate fields.
- Console progress identifies the exact active job.

## Run sequence

Use an API key associated with the EAP-enabled project:

```powershell
$env:GEMINI_API_KEY = Read-Host -MaskInput "Gemini API key"
```

Generate and inspect the videos:

```powershell
avu-eval generate --suite data/tasks/phase2_priority.jsonl
```

The canonical files are:

- `phase2_state_ledger.mp4` — 180 seconds
- `phase2_sparse_needle.mp4` — 300 seconds
- `phase2_rapid_order.mp4` — 18 seconds at 30 FPS

Dry-run the 36-attempt matrix:

```powershell
avu-eval run `
  --suite data/tasks/phase2_priority.jsonl `
  --config configs/phase2_priority.yaml `
  --output artifacts/runs/phase2-priority.jsonl `
  --dry-run
```

Run it:

```powershell
avu-eval run `
  --suite data/tasks/phase2_priority.jsonl `
  --config configs/phase2_priority.yaml `
  --output artifacts/runs/phase2-priority.jsonl
```

If interrupted, run the identical command again. Completed keys are skipped. A recorded timeout is intentionally not retried in the same result file; use a new output file for a clean reliability replication.

Generate the paired report:

```powershell
avu-eval report `
  --input artifacts/runs/phase2-priority.jsonl `
  --output artifacts/reports/phase2-priority
```

## Decision rules

Agentic mode earns a clear win only when it improves semantic quality, or materially reduces tokens without lowering quality or completion. A correct answer that requires substantially more tokens is not an efficiency win. A timeout counts as an end-to-end failure even if all returned answers are correct.

The key comparison is task-specific. Sparse needle and rapid order are intended agentic-win regimes; the reversible ledger tests whether selective navigation can integrate distributed evidence. Do not average them into one score before inspecting each mechanism separately.

## Extended controls

After the priority results are inspected, run `data/tasks/phase2_extended.jsonl` for final-frame inventory, long-video absence verification, and rapid-event counting. These are controls and should not delay the priority feedback.
