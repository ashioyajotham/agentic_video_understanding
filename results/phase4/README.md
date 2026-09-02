# Phase 4 public evidence

This directory freezes the exact source rows and deterministic reports used for
the public Gemini 3.7 Flash Phase 4 claim.

## Files

- `gemini-3.7-phase4-replicated.jsonl`: 48 unedited observations.
- `gemini-3.7-phase4-replicated.md`: generated aggregate report.
- `gemini-3.7-phase4-replicated.csv`: generated aggregate table.

The cohort contains eight tasks, static and agentic processing, and three
repetitions. It has 48 unique observation keys and 48 completed attempts.

## SHA-256

```text
887257826e9f19e33dc725b6c0705c6d3937e669423ebc0af0fa57dc7336b243  gemini-3.7-phase4-replicated.jsonl
e1a6dad34c5d57750e4204ec3ce156710fc00bb525a60a7a1a3cad9a0b333d5c  gemini-3.7-phase4-replicated.md
9c42b9981bf2e66b52005672666ea1dc9686f5664d0f2d769b5c72d04747230b  gemini-3.7-phase4-replicated.csv
```

## Reproduce the reports

```bash
avu-eval report \
  --input results/phase4/gemini-3.7-phase4-replicated.jsonl \
  --output /tmp/gemini-3.7-phase4-replicated

shasum -a 256 /tmp/gemini-3.7-phase4-replicated.md
shasum -a 256 /tmp/gemini-3.7-phase4-replicated.csv
```

The generated model-comparison CSV is intentionally omitted because this
directory contains one model; it has only a header and provides no evidence.
