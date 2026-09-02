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
