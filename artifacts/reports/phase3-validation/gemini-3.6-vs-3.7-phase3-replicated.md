# Evaluation report

Attempts: 92
Models: 2

## Model × family × mode summary

| Model | Family | Mode | n | Completion | Semantic | Exact | Strict | Input tokens | Total tokens | Provider mean (s) | Provider median (s) | Provider CV | Provider max (s) | Errors |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.6-flash-video-understanding-eap | fine_motion | agentic | 6 | 1.000 | 1.000 | 1.000 | 0.167 | 11059.667 | 12343.167 | 14.041 | 14.528 | 0.223 | 17.941 | 0 |
| gemini-3.6-flash-video-understanding-eap | fine_motion | static | 6 | 1.000 | 0.100 | 0.000 | 0.000 | 1472.000 | 6138.167 | 32.027 | 33.003 | 0.245 | 41.895 | 0 |
| gemini-3.6-flash-video-understanding-eap | incomplete_action | agentic | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 16449.000 | 19078.000 | 29.086 | 29.086 | 0.000 | 29.086 | 0 |
| gemini-3.6-flash-video-understanding-eap | incomplete_action | static | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 19823.000 | 20801.000 | 9.592 | 9.592 | 0.000 | 9.592 | 0 |
| gemini-3.6-flash-video-understanding-eap | reversible_state | agentic | 4 | 1.000 | 1.000 | 1.000 | 0.250 | 22140.250 | 26006.500 | 41.949 | 42.540 | 0.150 | 47.388 | 0 |
| gemini-3.6-flash-video-understanding-eap | reversible_state | static | 4 | 1.000 | 1.000 | 1.000 | 0.250 | 19836.500 | 21654.500 | 13.734 | 13.000 | 0.231 | 18.214 | 0 |
| gemini-3.6-flash-video-understanding-eap | sparse_event | agentic | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 69432.000 | 72348.667 | 38.179 | 42.954 | 0.443 | 54.565 | 0 |
| gemini-3.6-flash-video-understanding-eap | sparse_event | static | 6 | 1.000 | 0.167 | 0.167 | 0.167 | 19820.000 | 29158.833 | 50.039 | 51.517 | 0.339 | 74.776 | 0 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | agentic | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 44056.500 | 49486.667 | 53.219 | 56.986 | 0.358 | 71.534 | 0 |
| gemini-3.6-flash-video-understanding-eap | temporal_localization | static | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 19819.000 | 24484.000 | 29.529 | 25.554 | 0.517 | 49.181 | 0 |
| gemini-3.7-flash-video-understanding-eap | fine_motion | agentic | 6 | 1.000 | 1.000 | 1.000 | 0.000 | 9064.000 | 9883.833 | 14.045 | 13.538 | 0.206 | 19.132 | 0 |
| gemini-3.7-flash-video-understanding-eap | fine_motion | static | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 1472.000 | 2452.833 | 9.563 | 8.401 | 0.373 | 16.754 | 0 |
| gemini-3.7-flash-video-understanding-eap | incomplete_action | agentic | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 16108.000 | 16713.000 | 14.122 | 14.122 | 0.000 | 14.122 | 0 |
| gemini-3.7-flash-video-understanding-eap | incomplete_action | static | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 19823.000 | 20285.000 | 8.325 | 8.325 | 0.000 | 8.325 | 0 |
| gemini-3.7-flash-video-understanding-eap | reversible_state | agentic | 4 | 1.000 | 1.000 | 1.000 | 0.250 | 23352.250 | 24797.500 | 24.579 | 26.416 | 0.162 | 26.880 | 0 |
| gemini-3.7-flash-video-understanding-eap | reversible_state | static | 4 | 1.000 | 1.000 | 1.000 | 0.250 | 19836.500 | 20844.000 | 10.383 | 9.459 | 0.258 | 14.311 | 0 |
| gemini-3.7-flash-video-understanding-eap | sparse_event | agentic | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 65661.667 | 67917.667 | 48.017 | 39.277 | 0.545 | 99.496 | 0 |
| gemini-3.7-flash-video-understanding-eap | sparse_event | static | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 19820.000 | 22969.333 | 16.946 | 17.518 | 0.234 | 21.085 | 0 |
| gemini-3.7-flash-video-understanding-eap | temporal_localization | agentic | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 44985.000 | 46519.667 | 56.944 | 41.246 | 0.794 | 144.070 | 0 |
| gemini-3.7-flash-video-understanding-eap | temporal_localization | static | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 19819.000 | 21586.667 | 13.215 | 10.622 | 0.413 | 21.024 | 0 |

## Static versus agentic within each model

### gemini-3.6-flash-video-understanding-eap

Completed pairs: 23

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| semantic_score | 0.287 | 1.000 | +248.5% |
| strict_score | 0.130 | 0.652 | +400.0% |
| input_tokens | 15036.304 | 37056.478 | +146.4% |
| total_tokens | 20265.435 | 40355.435 | +99.1% |
| thought_tokens | 5210.565 | 2914.957 | -44.1% |
| provider_latency_seconds | 31.917 | 36.066 | +13.0% |
| wall_latency_seconds | 34.908 | 38.988 | +11.7% |

### gemini-3.7-flash-video-understanding-eap

Completed pairs: 23

| Metric | Static mean | Agentic mean | Agentic change |
|---|---:|---:|---:|
| semantic_score | 0.217 | 1.000 | +360.0% |
| strict_score | 0.087 | 0.609 | +600.0% |
| input_tokens | 15036.304 | 35990.478 | +139.4% |
| total_tokens | 16770.174 | 37470.870 | +123.4% |
| thought_tokens | 1720.609 | 1160.304 | -32.6% |
| provider_latency_seconds | 12.531 | 35.934 | +186.8% |
| wall_latency_seconds | 15.318 | 38.831 | +153.5% |

## Model-to-model paired comparison

Baseline: gemini-3.6-flash-video-understanding-eap

| Candidate | Task | Mode | n | Semantic A | Semantic B | Input change | Total change | Thought change | Provider change | Wall change | Quality regression |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.7-flash-video-understanding-eap | phase3_ledger_actions | agentic | 3 | 1.000 | 1.000 | +2.5% | -7.1% | -65.8% | -39.8% | -37.1% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_ledger_purple_feint | agentic | 1 | 1.000 | 1.000 | -2.1% | -12.4% | -80.4% | -51.4% | -47.0% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_ledger_red_count | agentic | 1 | 1.000 | 1.000 | +15.1% | +3.5% | -66.8% | -47.3% | -42.8% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_rapid_dense | agentic | 3 | 1.000 | 1.000 | +24.6% | +16.2% | -39.8% | +21.9% | +16.9% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_rapid_offset | agentic | 3 | 1.000 | 1.000 | -37.1% | -37.4% | -42.3% | -16.7% | -15.1% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_early_color | agentic | 3 | 1.000 | 1.000 | -24.9% | -25.6% | -37.2% | -3.5% | -3.7% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_early_timestamp | agentic | 3 | 1.000 | 1.000 | -7.2% | -15.2% | -78.4% | -32.5% | -30.8% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_late_color | agentic | 3 | 1.000 | 1.000 | +6.8% | +6.6% | -11.3% | +65.5% | +60.3% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_late_timestamp | agentic | 3 | 1.000 | 1.000 | +10.6% | +2.5% | -75.6% | +51.4% | +48.5% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_ledger_actions | static | 3 | 1.000 | 1.000 | +0.0% | -3.4% | -40.6% | -21.1% | -17.6% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_ledger_purple_feint | static | 1 | 1.000 | 1.000 | +0.0% | -2.5% | -52.8% | -13.2% | -11.8% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_ledger_red_count | static | 1 | 1.000 | 1.000 | +0.0% | -4.9% | -63.5% | -35.3% | -29.0% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_rapid_dense | static | 3 | 0.133 | 0.000 | +0.0% | -55.9% | -75.6% | -69.6% | -64.0% | YES |
| gemini-3.7-flash-video-understanding-eap | phase3_rapid_offset | static | 3 | 0.067 | 0.000 | +0.0% | -63.0% | -81.5% | -70.5% | -65.5% | YES |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_early_color | static | 3 | 0.000 | 0.000 | +0.0% | -14.4% | -51.6% | -57.0% | -54.0% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_early_timestamp | static | 3 | 0.000 | 0.000 | +0.0% | -10.5% | -56.7% | -54.2% | -49.5% | no |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_late_color | static | 3 | 0.333 | 0.000 | +0.0% | -27.3% | -76.5% | -73.1% | -69.8% | YES |
| gemini-3.7-flash-video-understanding-eap | phase3_sparse_late_timestamp | static | 3 | 0.000 | 0.000 | +0.0% | -13.2% | -67.2% | -56.2% | -51.7% | no |
