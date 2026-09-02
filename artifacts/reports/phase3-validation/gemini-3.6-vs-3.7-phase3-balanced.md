# Evaluation report

Attempts: 84
Models: 2

## Model × family × mode summary

| Model | Family | Mode | n | Completion | Semantic | Exact | Strict | Input tokens | Total tokens | Provider mean (s) | Provider median (s) | Provider CV | Provider max (s) | Errors |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.6-flash-video-understanding-eap | fine_motion | agentic | 6 | 1.000 | 1.000 | 1.000 | 0.167 | 11059.667 | 12343.167 | 14.041 | 14.528 | 0.223 | 17.941 | 0 |
| gemini-3.6-flash-video-understanding-eap | fine_motion | static | 6 | 1.000 | 0.100 | 0.000 | 0.000 | 1472.000 | 6138.167 | 32.027 | 33.003 | 0.245 | 41.895 | 0 |
| gemini-3.6-flash-video-understanding-eap | reversible_state | agentic | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 22650.000 | 26597.000 | 44.156 | 47.229 | 0.124 | 47.388 | 0 |
| gemini-3.6-flash-video-understanding-eap | reversible_state | static | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 19839.000 | 21711.000 | 14.031 | 13.161 | 0.272 | 18.214 | 0 |
| gemini-3.6-flash-video-understanding-eap | sparse_event | agentic | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 69432.000 | 72348.667 | 38.179 | 42.954 | 0.443 | 54.565 | 0 |
| gemini-3.6-flash-video-understanding-eap | sparse_event | static | 6 | 1.000 | 0.167 | 0.167 | 0.167 | 19820.000 | 29158.833 | 50.039 | 51.517 | 0.339 | 74.776 | 0 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | agentic | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 44056.500 | 49486.667 | 53.219 | 56.986 | 0.358 | 71.534 | 0 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | static | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 19819.000 | 24484.000 | 29.529 | 25.554 | 0.517 | 49.181 | 0 |
| gemini-3.7-flash-video-understanding-eap | fine_motion | agentic | 6 | 1.000 | 1.000 | 1.000 | 0.000 | 9064.000 | 9883.833 | 14.045 | 13.538 | 0.206 | 19.132 | 0 |
| gemini-3.7-flash-video-understanding-eap | fine_motion | static | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 1472.000 | 2452.833 | 9.563 | 8.401 | 0.373 | 16.754 | 0 |
| gemini-3.7-flash-video-understanding-eap | reversible_state | agentic | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 23227.000 | 24704.333 | 26.571 | 26.549 | 0.011 | 26.880 | 0 |
| gemini-3.7-flash-video-understanding-eap | reversible_state | static | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 19839.000 | 20980.667 | 11.077 | 9.515 | 0.253 | 14.311 | 0 |
| gemini-3.7-flash-video-understanding-eap | sparse_event | agentic | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 65661.667 | 67917.667 | 48.017 | 39.277 | 0.545 | 99.496 | 0 |
| gemini-3.7-flash-video-understanding-eap | sparse_event | static | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 19820.000 | 22969.333 | 16.946 | 17.518 | 0.234 | 21.085 | 0 |
| gemini-3.7-flash-video-understanding-eap | temporal_localization | agentic | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 44985.000 | 46519.667 | 56.944 | 41.246 | 0.794 | 144.070 | 0 |
| gemini-3.7-flash-video-understanding-eap | temporal_localization | static | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 19819.000 | 21586.667 | 13.215 | 10.622 | 0.413 | 21.024 | 0 |

## Static versus agentic within each model

### gemini-3.6-flash-video-understanding-eap

Completed pairs: 21

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| semantic_score | 0.219 | 1.000 | +356.5% |
| strict_score | 0.048 | 0.619 | +1200.0% |
| input_tokens | 14580.143 | 38820.905 | +166.3% |
| total_tokens | 20181.857 | 42136.286 | +108.8% |
| thought_tokens | 5581.476 | 2924.381 | -47.6% |
| provider_latency_seconds | 33.889 | 36.434 | +7.5% |
| wall_latency_seconds | 36.881 | 39.356 | +6.7% |

### gemini-3.7-flash-video-understanding-eap

Completed pairs: 21

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| semantic_score | 0.143 | 1.000 | +600.0% |
| strict_score | 0.000 | 0.571 | — |
| input_tokens | 14580.143 | 37521.190 | +157.3% |
| total_tokens | 16428.333 | 39049.524 | +137.7% |
| thought_tokens | 1833.762 | 1196.857 | -34.7% |
| provider_latency_seconds | 12.932 | 37.797 | +192.3% |
| wall_latency_seconds | 15.713 | 40.679 | +158.9% |

## Model-to-model paired comparison

Baseline: gemini-3.6-flash-video-understanding-eap

| Candidate | Task | Mode | n | Semantic A | Semantic B | Input change | Total change | Thought change | Provider change | Wall change | Quality regression |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.7-flash-video-understanding-eap | phase3_ledger_actions | agentic | 3 | 1.000 | 1.000 | +2.5% | -7.1% | -65.8% | -39.8% | -37.1% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_rapid_dense | agentic | 3 | 1.000 | 1.000 | +24.6% | +16.2% | -39.8% | +21.9% | +16.9% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_rapid_offset | agentic | 3 | 1.000 | 1.000 | -37.1% | -37.4% | -42.3% | -16.7% | -15.1% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_early_color | agentic | 3 | 1.000 | 1.000 | -24.9% | -25.6% | -37.2% | -3.5% | -3.7% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_early_timestamp | agentic | 3 | 1.000 | 1.000 | -7.2% | -15.2% | -78.4% | -32.5% | -30.8% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_late_color | agentic | 3 | 1.000 | 1.000 | +6.8% | +6.6% | -11.3% | +65.5% | +60.3% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_late_timestamp | agentic | 3 | 1.000 | 1.000 | +10.6% | +2.5% | -75.6% | +51.4% | +48.5% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_ledger_actions | static | 3 | 1.000 | 1.000 | +0.0% | -3.4% | -40.6% | -21.1% | -17.6% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_rapid_dense | static | 3 | 0.133 | 0.000 | +0.0% | -55.9% | -75.6% | -69.6% | -64.0% | YES |
| gemini-3.7-flash-video-understanding-eap | phase3_rapid_offset | static | 3 | 0.067 | 0.000 | +0.0% | -63.0% | -81.5% | -70.5% | -65.5% | YES |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_early_color | static | 3 | 0.000 | 0.000 | +0.0% | -14.4% | -51.6% | -57.0% | -54.0% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_early_timestamp | static | 3 | 0.000 | 0.000 | +0.0% | -10.5% | -56.7% | -54.2% | -49.5% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_late_color | static | 3 | 0.333 | 0.000 | +0.0% | -27.3% | -76.5% | -73.1% | -69.8% | YES |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_late_timestamp | static | 3 | 0.000 | 0.000 | +0.0% | -13.2% | -67.2% | -56.2% | -51.7% | no |
