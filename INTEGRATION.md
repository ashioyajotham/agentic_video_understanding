# Integrating into the parent AVU evaluation repository

The package is intended to become the parent repository's `showcase/`
directory. Copy the contents of this package—not the outer folder—into that
location.

## Preserve one source of truth

1. Keep original evaluation JSONL under the parent `artifacts/runs/` tree.
2. Add the exact original rapid-crossing run IDs and hashes to `manifest.yaml`
   after integration.
3. Do not copy or manually edit original responses inside the showcase.
4. Generate launch-safe summaries from source rows with a deterministic export
   script.
5. Keep primary 180-second attempts separate from 600-second diagnostic retries.

## Reusing the existing backend

The preferred integration is to retain the parent repository's request wrapper
and call it through the command adapter:

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

## Before sending the launch demo

- Run both modes against all five registered variants.
- Confirm every clip hash against its ground-truth file.
- Score without removing failed attempts or malformed responses.
- Add exact denominators to the GDE brief.
- Select the strongest representative clip only after reporting the aggregate.
- Keep the complete package private until Google explicitly clears it.

