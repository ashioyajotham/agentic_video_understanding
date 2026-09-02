# Evaluation report

Attempts: 30
Models: 1

## Model × family × mode summary

| Model | Family | Mode | n | Completion | Semantic | Exact | Strict | Input tokens | Total tokens | Provider mean (s) | Provider median (s) | Provider CV | Provider max (s) | Errors |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.6-flash-video-understanding-eap | cumulative_state | agentic | 6 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.153 | 0.156 | 0.082 | 0.166 | 6 |
| gemini-3.6-flash-video-understanding-eap | cumulative_state | static | 6 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.733 | 0.144 | 1.968 | 3.676 | 6 |
| gemini-3.6-flash-video-understanding-eap | hallucination_negative | agentic | 3 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.160 | 0.166 | 0.106 | 0.172 | 3 |
| gemini-3.6-flash-video-understanding-eap | hallucination_negative | static | 3 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.155 | 0.162 | 0.148 | 0.174 | 3 |
| gemini-3.6-flash-video-understanding-eap | identity_tracking | agentic | 3 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.147 | 0.155 | 0.160 | 0.166 | 3 |
| gemini-3.6-flash-video-understanding-eap | identity_tracking | static | 3 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.158 | 0.152 | 0.062 | 0.169 | 3 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | agentic | 3 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.168 | 0.168 | 0.036 | 0.175 | 3 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | static | 3 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.169 | 0.170 | 0.059 | 0.179 | 3 |

## Static versus agentic within each model

### gemini-3.6-flash-video-understanding-eap

Completed pairs: 15

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| semantic_score | 0.000 | 0.000 | — |
| strict_score | 0.000 | 0.000 | — |
| input_tokens | — | — | — |
| total_tokens | — | — | — |
| thought_tokens | — | — | — |
| provider_latency_seconds | 0.390 | 0.156 | -59.9% |
| wall_latency_seconds | 0.390 | 0.156 | -59.9% |
