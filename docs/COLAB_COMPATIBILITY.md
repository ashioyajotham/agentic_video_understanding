# Supplied Colab compatibility

Validated against the private notebook `[External] Agentic_video_understanding.ipynb`, modified 2026-08-13.

## Canonical details used by this harness

- Wheel: `google_genai-2.14.2-py3-none-any.whl`
- Model: `models/gemini-3.6-flash-video-understanding-eap`
- Client: `genai.Client(api_key=GEMINI_API_KEY)`
- Upload: `client.files.upload(file=...)`, followed by polling `client.files.get(...)`
- Request: `client.interactions.create(...)`
- Per-video mode: `"processing": "agentic"` or `"processing": "static"`
- Static extraction: described as fixed-rate 1 FPS
- Usage:
  - `result.usage.total_input_tokens`
  - `result.usage.total_output_tokens`
  - `result.usage.total_tokens`
  - `result.usage.total_thought_tokens`
  - `result.usage.input_tokens_by_modality`

Agentic mode is the default for supported 3.5+ models, but this evaluation always sets both modes explicitly to preserve experimental control.

The notebook does not demonstrate an explicit thinking-level parameter or a concrete response field for processing-strategy traces. The harness therefore does not claim to configure thinking level and treats traces as optional response metadata.
