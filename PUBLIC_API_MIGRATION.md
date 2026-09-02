# Public Gemini API migration

Agentic video understanding is public. The canonical evaluator now uses:

- Python package: `google-genai`
- Model: `gemini-3.7-flash`
- API surface: `client.interactions.create(...)`
- Mode control: `processing: static` or `processing: agentic` on the video input

Historical EAP model identifiers, wheel locations, and raw private traces are not
needed for new runs and should not be included in public releases.

## Upgrade an existing checkout

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -c "from google import genai; print('public google-genai import OK')"
```

Confirm the public model configuration:

```bash
cat configs/models/gemini-3.7-phase4-validation.yaml
```

Then inspect the 16-job matrix before making requests:

```bash
avu-eval run \
  --suite data/tasks/phase4_tracking_ablation.jsonl \
  --config configs/models/gemini-3.7-phase4-validation.yaml \
  --output artifacts/runs/phase4-validation/gemini-3.7-phase4.jsonl \
  --dry-run
```

Remove `--dry-run` to run the validation cohort. Each completed agentic record
includes `metadata.agentic_processing_observed`; it is true only when the public
response exposes both `processing_call` and `processing_result` steps.
