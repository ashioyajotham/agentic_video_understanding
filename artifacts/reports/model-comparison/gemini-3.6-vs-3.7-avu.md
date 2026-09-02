# Evaluation report

Attempts: 72
Models: 2

## Model × family × mode summary

| Model | Family | Mode | n | Completion | Semantic | Exact | Strict | Input tokens | Total tokens | Provider mean (s) | Provider median (s) | Provider CV | Provider max (s) | Errors |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.6-flash-video-understanding-eap | fine_motion | agentic | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 9639.333 | 10925.000 | 13.592 | 14.293 | 0.096 | 14.395 | 0 |
| gemini-3.6-flash-video-understanding-eap | fine_motion | static | 3 | 1.000 | 0.600 | 0.000 | 0.000 | 1208.000 | 6236.667 | 34.243 | 36.122 | 0.252 | 41.795 | 0 |
| gemini-3.6-flash-video-understanding-eap | incomplete_action | agentic | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 5235.000 | 6338.667 | 14.956 | 13.893 | 0.348 | 20.612 | 0 |
| gemini-3.6-flash-video-understanding-eap | incomplete_action | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 11897.000 | 12892.000 | 9.378 | 9.227 | 0.038 | 9.785 | 0 |
| gemini-3.6-flash-video-understanding-eap | reversible_state | agentic | 6 | 1.000 | 1.000 | 1.000 | 0.500 | 18059.000 | 21044.500 | 28.753 | 28.405 | 0.126 | 35.619 | 0 |
| gemini-3.6-flash-video-understanding-eap | reversible_state | static | 6 | 1.000 | 1.000 | 1.000 | 0.500 | 11914.000 | 13304.333 | 11.739 | 11.052 | 0.212 | 16.215 | 0 |
| gemini-3.6-flash-video-understanding-eap | sparse_event | agentic | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 71802.333 | 75039.333 | 49.408 | 25.709 | 1.074 | 110.210 | 0 |
| gemini-3.6-flash-video-understanding-eap | sparse_event | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 19820.000 | 19963.667 | 5.670 | 5.673 | 0.095 | 6.208 | 0 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | agentic | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 28033.667 | 31894.000 | 38.202 | 24.308 | 0.634 | 66.161 | 0 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 19819.000 | 20198.333 | 6.378 | 6.386 | 0.194 | 7.609 | 0 |
| gemini-3.7-flash-video-understanding-eap | fine_motion | agentic | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 8348.667 | 9017.333 | 12.135 | 11.019 | 0.160 | 14.378 | 0 |
| gemini-3.7-flash-video-understanding-eap | fine_motion | static | 3 | 1.000 | 0.000 | 0.000 | 0.000 | 1208.000 | 2651.000 | 8.902 | 8.640 | 0.068 | 9.595 | 0 |
| gemini-3.7-flash-video-understanding-eap | incomplete_action | agentic | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 5845.333 | 6260.333 | 9.797 | 8.457 | 0.339 | 13.582 | 0 |
| gemini-3.7-flash-video-understanding-eap | incomplete_action | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 11897.000 | 12304.667 | 5.128 | 5.042 | 0.060 | 5.471 | 0 |
| gemini-3.7-flash-video-understanding-eap | reversible_state | agentic | 6 | 1.000 | 1.000 | 1.000 | 0.500 | 14074.500 | 15184.500 | 14.216 | 13.319 | 0.408 | 21.422 | 0 |
| gemini-3.7-flash-video-understanding-eap | reversible_state | static | 6 | 1.000 | 1.000 | 1.000 | 0.500 | 11914.000 | 12629.833 | 5.867 | 5.626 | 0.089 | 6.525 | 0 |
| gemini-3.7-flash-video-understanding-eap | sparse_event | agentic | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 20100.333 | 20660.333 | 14.258 | 17.048 | 0.391 | 17.884 | 0 |
| gemini-3.7-flash-video-understanding-eap | sparse_event | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 19820.000 | 19904.000 | 5.522 | 5.343 | 0.171 | 6.544 | 0 |
| gemini-3.7-flash-video-understanding-eap | temporal_localization | agentic | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 16007.667 | 16613.667 | 12.982 | 12.167 | 0.365 | 18.072 | 0 |
| gemini-3.7-flash-video-understanding-eap | temporal_localization | static | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 19819.000 | 20041.000 | 4.332 | 4.269 | 0.114 | 4.856 | 0 |

## Static versus agentic within each model

### gemini-3.6-flash-video-understanding-eap

Completed pairs: 18

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| semantic_score | 0.933 | 1.000 | +7.1% |
| strict_score | 0.667 | 0.667 | +0.0% |
| input_tokens | 12762.000 | 25138.056 | +97.0% |
| total_tokens | 14316.556 | 27714.333 | +93.6% |
| thought_tokens | 1540.944 | 2265.778 | +47.0% |
| provider_latency_seconds | 13.191 | 28.944 | +119.4% |
| wall_latency_seconds | 16.073 | 31.820 | +98.0% |

### gemini-3.7-flash-video-understanding-eap

Completed pairs: 18

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| semantic_score | 0.833 | 1.000 | +20.0% |
| strict_score | 0.667 | 0.667 | +0.0% |
| input_tokens | 12762.000 | 13075.167 | +2.5% |
| total_tokens | 13360.056 | 13820.111 | +3.4% |
| thought_tokens | 586.889 | 554.944 | -5.4% |
| provider_latency_seconds | 5.936 | 12.934 | +117.9% |
| wall_latency_seconds | 8.747 | 15.697 | +79.4% |

## Model-to-model paired comparison

Baseline: gemini-3.6-flash-video-understanding-eap

| Candidate | Task | Mode | n | Semantic A | Semantic B | Input change | Total change | Thought change | Provider change | Wall change | Quality regression |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.7-flash-video-understanding-eap | ledger_completed_actions | agentic | 3 | 1.000 | 1.000 | -26.1% | -32.3% | -71.0% | -58.8% | -54.0% | no |
| gemini-3.7-flash-video-understanding-eap | ledger_feint_negative | agentic | 3 | 1.000 | 1.000 | +11.7% | -1.2% | -69.4% | -34.5% | -28.6% | no |
| gemini-3.7-flash-video-understanding-eap | ledger_red_swallow_count | agentic | 3 | 1.000 | 1.000 | -17.6% | -22.9% | -62.5% | -41.0% | -37.1% | no |
| gemini-3.7-flash-video-understanding-eap | needle_color | agentic | 3 | 1.000 | 1.000 | -72.0% | -72.5% | -86.9% | -71.1% | -67.9% | no |
| gemini-3.7-flash-video-understanding-eap | needle_timestamp | agentic | 3 | 1.000 | 1.000 | -42.9% | -47.9% | -87.9% | -66.0% | -61.7% | no |
| gemini-3.7-flash-video-understanding-eap | rapid_crossing_order | agentic | 3 | 1.000 | 1.000 | -13.4% | -17.5% | -53.6% | -10.7% | -8.9% | no |
| gemini-3.7-flash-video-understanding-eap | ledger_completed_actions | static | 3 | 1.000 | 1.000 | +0.0% | -1.8% | -21.0% | -42.8% | -33.0% | no |
| gemini-3.7-flash-video-understanding-eap | ledger_feint_negative | static | 3 | 1.000 | 1.000 | +0.0% | -4.6% | -59.1% | -45.3% | -34.9% | no |
| gemini-3.7-flash-video-understanding-eap | ledger_red_swallow_count | static | 3 | 1.000 | 1.000 | +0.0% | -8.2% | -68.7% | -55.7% | -46.7% | no |
| gemini-3.7-flash-video-understanding-eap | needle_color | static | 3 | 1.000 | 1.000 | +0.0% | -0.3% | -41.8% | -2.6% | -6.7% | no |
| gemini-3.7-flash-video-understanding-eap | needle_timestamp | static | 3 | 1.000 | 1.000 | +0.0% | -0.8% | -41.9% | -32.1% | -20.8% | no |
| gemini-3.7-flash-video-understanding-eap | rapid_crossing_order | static | 3 | 0.600 | 0.000 | +0.0% | -57.5% | -71.5% | -74.0% | -68.4% | YES |
