# Evaluation report

Attempts: 36
Models: 1

## Model × family × mode summary

| Model | Family | Mode | n | Completion | Semantic | Exact | Strict | Input tokens | Total tokens | Provider mean (s) | Provider median (s) | Provider CV | Provider max (s) | Errors |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.6-flash-video-understanding-eap | fine_motion | agentic | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 10532.667 | 11638.000 | 13.244 | 13.324 | 0.032 | 13.619 | 0 |
| gemini-3.6-flash-video-understanding-eap | fine_motion | static | 3 | 1.000 | 0.467 | 0.000 | 0.000 | 1208.000 | 5378.333 | 29.923 | 32.311 | 0.234 | 35.433 | 0 |
| gemini-3.6-flash-video-understanding-eap | incomplete_action | agentic | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 5525.333 | 6335.000 | 12.704 | 10.955 | 0.278 | 16.763 | 0 |
| gemini-3.6-flash-video-understanding-eap | incomplete_action | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 11897.000 | 12579.000 | 9.158 | 9.241 | 0.090 | 9.940 | 0 |
| gemini-3.6-flash-video-understanding-eap | reversible_state | agentic | 6 | 1.000 | 1.000 | 1.000 | 0.500 | 20417.333 | 23139.500 | 31.471 | 30.232 | 0.204 | 42.187 | 0 |
| gemini-3.6-flash-video-understanding-eap | reversible_state | static | 6 | 1.000 | 1.000 | 1.000 | 0.500 | 11914.000 | 13118.167 | 10.821 | 10.652 | 0.091 | 12.691 | 0 |
| gemini-3.6-flash-video-understanding-eap | sparse_event | agentic | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 38608.333 | 40192.000 | 26.844 | 14.936 | 0.938 | 55.774 | 0 |
| gemini-3.6-flash-video-understanding-eap | sparse_event | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 19820.000 | 19949.000 | 6.369 | 6.266 | 0.045 | 6.692 | 0 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | agentic | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 18467.000 | 19939.000 | 22.235 | 26.455 | 0.406 | 28.390 | 0 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 19819.000 | 20175.667 | 6.026 | 5.854 | 0.128 | 6.869 | 0 |

## Static versus agentic within each model

### gemini-3.6-flash-video-understanding-eap

Completed pairs: 18

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| semantic_score | 0.911 | 1.000 | +9.8% |
| strict_score | 0.667 | 0.667 | +0.0% |
| input_tokens | 12762.000 | 18994.667 | +48.8% |
| total_tokens | 14053.056 | 20730.500 | +47.5% |
| thought_tokens | 1277.500 | 1463.111 | +14.5% |
| provider_latency_seconds | 12.186 | 22.995 | +88.7% |
| wall_latency_seconds | 15.689 | 26.357 | +68.0% |
