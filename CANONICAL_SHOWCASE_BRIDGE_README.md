# Canonical Phase 4 showcase bridge

Copy this patch over the merged `avu-eval` repository root. It does not delete,
rename, or modify historical `showcase/generated*` results.

## What changes

- Adds `avu-eval showcase-export` and `avu-eval showcase-verify`.
- Exports exact canonical Phase 4 video bytes into the visual showcase.
- Records suite, task, and clip hashes plus per-task provenance.
- Detects specification, ground-truth, source-video, and exported-video drift.
- Marks the independent 960×540 seeded suite as demo-only.
- Corrects showcase claims to preserve reported failures and denominators.

## Install and verify

```bash
cp -R avu-canonical-showcase-bridge-patch/. .
python -m pip install -e .
python -m unittest discover -s tests -v
python -m unittest discover -s showcase/tests -v

avu-eval showcase-export \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --output showcase/generated_canonical_phase4

avu-eval showcase-verify \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --input showcase/generated_canonical_phase4
```

Expected: 15 evaluator tests, 4 showcase tests, and 8 canonical videos verified.
The exported directory is ignored by default because it is reproducible.
