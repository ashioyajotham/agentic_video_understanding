# Research basis

Primary sources informing the suite:

1. **Video-MME** — Fu et al., 2024. A full-spectrum benchmark spanning 11-second to one-hour videos, multiple visual domains, subtitles, and audio. It motivates duration-stratified and modality-stratified evaluation. <https://arxiv.org/abs/2405.21075>
2. **HourVideo** — Chandrasegaran et al., NeurIPS 2024. Its hour-long suite covers recall, tracking, spatial/temporal/predictive/causal/counterfactual reasoning, and navigation. It motivates long-horizon state tracking and targeted retrieval. <https://arxiv.org/abs/2411.04998>
3. **1H-VideoQA** — Google DeepMind. A compact frontier-model probe with 101 five-choice questions over 21 videos lasting 40–90 minutes. It motivates a small but high-signal long-form subset under a tight evaluation deadline. <https://github.com/google-deepmind/1h-videoqa>
4. **MotionBench** — Hong et al., CVPR 2025. Fine-grained motion remains difficult, and higher-frame-rate inputs improve motion understanding. It directly motivates selective-resampling tests. <https://arxiv.org/abs/2501.02955>
5. **TemporalBench** — dedicated fine-grained temporal evaluation; it argues that many video benchmarks can be solved like static-image tasks. It motivates questions that cannot be answered from a single frame. <https://temporalbench.github.io/>
6. **MoHallBench** — Li et al., 2026. It studies motion hallucination from co-occurrence priors, sequential inference, and similarity confusion, and reports particularly severe sequential-inference hallucination. It motivates matched negative questions and expected-but-absent events. <https://arxiv.org/abs/2607.01117>

## Mapping from evidence to tests

| Test | Supporting idea |
|---|---|
| Duration buckets | Video-MME; HourVideo |
| Long-horizon state and retrieval | HourVideo; 1H-VideoQA |
| Selective high-FPS windows | MotionBench |
| Non-single-frame questions | TemporalBench |
| Negative and counterfactual pairs | MoHallBench; HourVideo |
| Audio/transcript/visual ablations | Video-MME |

These papers motivate capability dimensions, not claims that the local suite reproduces their published benchmark scores.

