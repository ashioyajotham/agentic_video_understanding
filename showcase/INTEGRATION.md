# Canonical benchmark integration

The showcase is now the parent repository's visual front door. It deliberately
retains two distinct stimulus paths:

- `data/tasks/phase4_tracking_ablation.jsonl` and `src/avu_eval/synthetic.py`
  define the canonical, claim-bearing benchmark.
- `showcase/rapid_crossing/variants_hard.json` and `generate_variants.py`
  define a 960×540 seeded visual demo. Its results cannot be attributed to
  Phase 4 because its renderer, dimensions, trajectories, and ground truth differ.

## Export exact canonical stimuli

From the repository root:

```bash
avu-eval showcase-export \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --output showcase/generated_canonical_phase4

avu-eval showcase-verify \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --input showcase/generated_canonical_phase4
```

The export copies exact canonical video bytes, writes per-task ground truth,
records suite/task/video hashes, and marks the export as stimuli-only until a
registered model run exists. Verification fails on suite drift, task drift,
ground-truth drift, clip modification, or a non-exact source copy.

Do not recolor, resize, re-encode, or otherwise restyle these exported videos
and then describe them as the evaluated Phase 4 artifacts. Polished 960×540
renders remain useful illustrations, but are `demo_suite` artifacts.

## Preserve one source of truth

1. Keep original evaluation JSONL under the parent `artifacts/runs/` tree.
2. Treat the export manifest and canonical task JSONL as the stimulus provenance
   record; add model-run provenance separately after execution.
3. Do not copy or manually edit original responses inside the showcase.
4. Generate launch-safe summaries from source rows with a deterministic export
   script.
5. Keep primary 180-second attempts separate from 600-second diagnostic retries.

## Historical standalone adapter

`run_demo.py` remains available for historical or exploratory showcase runs.
New claim-bearing Phase 4 runs must use `avu-eval run`, preserving paired modes,
counterbalancing, timeouts, telemetry, resumability, and the canonical grader.

```bash
python showcase/rapid_crossing/run_demo.py \
  --adapter command \
  --command 'python YOUR_EXISTING_RUNNER.py --video {clip} --prompt-file {prompt} --mode {mode}' \
  --clips-dir showcase/assets/clips \
  --prompt showcase/rapid_crossing/prompt.txt \
  --mode agentic \
  --attempts 3 \
  --output showcase/generated/agentic.jsonl
```

The existing runner must print the model's response text to standard output and
return a non-zero exit code on request failure. Extend the adapter record with
the parent telemetry fields if the existing runner already exposes provider
latency, input tokens, output tokens, thought tokens, termination reason, and
selection strategy.

## Before publishing

- Run both modes against all eight canonical Phase 4 tasks with registered repetition counts.
- Confirm every clip hash against its ground-truth file.
- Score without removing failed attempts or malformed responses.
- Report the exact Phase 4 denominators separately from historical showcase suites.
- Select the strongest representative clip only after reporting the aggregate.
- Keep the complete package private until Google explicitly clears it.
