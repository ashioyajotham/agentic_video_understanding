# AVU Eval recovered repository

This repository consolidates the last recoverable AVU evaluation state through Phase 4. It includes Git history, source code, task specifications, tests, configurations, recovered JSONL records, regenerated reports, and the updated evaluation document.

## Restore locally

Extract the ZIP into a new directory; do not overwrite a copy recovered from the Recycle Bin until the two trees have been compared.

```powershell
Set-Location C:\Users\HomePC\avu-eval-recovered-2026-09-02

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .

python -m unittest discover -s tests -v
```

Expected: 12 tests pass.

Validate the restored suites:

```powershell
avu-eval validate --suite data/tasks/phase2_priority.jsonl
avu-eval validate --suite data/tasks/phase3_discrimination.jsonl
avu-eval validate --suite data/tasks/phase3_replication_priority.jsonl
avu-eval validate --suite data/tasks/phase4_tracking_ablation.jsonl
```

Expected task counts: 6, 9, 7, and 8.

The primary publication-quality comparison is:

```text
artifacts/runs/phase3-validation/gemini-3.6-vs-3.7-phase3-balanced.jsonl
```

See `docs/recovery/RECOVERY_MANIFEST.md` for the complete recovery inventory and limitations.
