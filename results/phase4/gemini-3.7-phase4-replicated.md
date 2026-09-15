# Evaluation report

Attempts: 48
Models: 1

## Model × family × mode summary

| Model | Family | Mode | n | Completion | Semantic | Exact | Strict | Input tokens | Total tokens | Provider mean (s) | Provider median (s) | Provider CV | Provider max (s) | Errors |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.7-flash | fine_motion_ablation | agentic | 24 | 1.000 | 0.893 | 0.583 | 0.000 | 327.833 | 9071.250 | 15.376 | 14.305 | 0.367 | 29.533 | 0 |
| gemini-3.7-flash | fine_motion_ablation | static | 24 | 1.000 | 0.320 | 0.125 | 0.000 | 557.000 | 2470.375 | 11.452 | 11.257 | 0.366 | 21.329 | 0 |

## Static versus agentic within each model

### gemini-3.7-flash

Completed pairs: 24

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| semantic_score | 0.320 | 0.893 | +179.2% |
| strict_score | 0.000 | 0.000 | — |
| input_tokens | 557.000 | 327.833 | -41.1% |
| total_tokens | 2470.375 | 9071.250 | +267.2% |
| thought_tokens | 1876.083 | 1992.375 | +6.2% |
| provider_latency_seconds | 11.452 | 15.376 | +34.3% |
| wall_latency_seconds | 11.773 | 15.700 | +33.4% |
