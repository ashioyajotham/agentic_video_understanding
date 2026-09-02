# Evaluation report

Attempts: 36
Models: 1

## Model × family × mode summary

| Model | Family | Mode | n | Completion | Semantic | Exact | Strict | Input tokens | Total tokens | Provider mean (s) | Provider median (s) | Provider CV | Provider max (s) | Errors |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.6-flash-video-understanding-eap | fine_motion | agentic | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 10982.667 | 12221.333 | 14.999 | 14.295 | 0.201 | 18.307 | 0 |
| gemini-3.6-flash-video-understanding-eap | fine_motion | static | 3 | 0.000 | 0.000 | 0.000 | 0.000 | — | — | 180.109 | 180.110 | 0.000 | 180.115 | 3 |
| gemini-3.6-flash-video-understanding-eap | incomplete_action | agentic | 3 | 0.667 | 0.667 | 0.667 | 0.667 | 6459.000 | 7318.500 | 123.976 | 14.354 | 1.547 | 345.468 | 1 |
| gemini-3.6-flash-video-understanding-eap | incomplete_action | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 11897.000 | 12836.000 | 9.516 | 9.397 | 0.059 | 10.124 | 0 |
| gemini-3.6-flash-video-understanding-eap | reversible_state | agentic | 6 | 0.000 | 0.000 | 0.000 | 0.000 | — | — | 180.172 | 180.168 | 0.000 | 180.250 | 6 |
| gemini-3.6-flash-video-understanding-eap | reversible_state | static | 6 | 0.500 | 0.500 | 0.500 | 0.500 | 11909.000 | 13327.667 | 97.043 | 97.269 | 0.947 | 182.180 | 3 |
| gemini-3.6-flash-video-understanding-eap | sparse_event | agentic | 3 | 0.000 | 0.000 | 0.000 | 0.000 | — | — | 180.285 | 180.111 | 0.002 | 180.640 | 3 |
| gemini-3.6-flash-video-understanding-eap | sparse_event | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 19820.000 | 19951.000 | 7.332 | 8.314 | 0.260 | 8.550 | 0 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | agentic | 3 | 0.333 | 0.333 | 0.333 | 0.333 | 5627.000 | 6378.000 | 123.921 | 180.100 | 0.785 | 180.111 | 2 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 19819.000 | 20146.000 | 6.166 | 5.843 | 0.107 | 6.926 | 0 |

## Static versus agentic within each model

### gemini-3.6-flash-video-understanding-eap

Completed pairs: 3

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| semantic_score | 1.000 | 1.000 | +0.0% |
| strict_score | 1.000 | 1.000 | +0.0% |
| input_tokens | 14537.667 | 6181.667 | -57.5% |
| total_tokens | 15259.667 | 7005.000 | -54.1% |
| thought_tokens | 720.333 | 671.667 | -6.8% |
| provider_latency_seconds | 8.816 | 12.671 | +43.7% |
| wall_latency_seconds | 13.408 | 18.471 | +37.8% |
