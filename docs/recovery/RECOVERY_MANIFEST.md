# AVU evaluation recovery manifest

Reconstructed on 2026-09-02 after the local working directory was deleted.

## Recovered source state

- Original two-commit Git history from the last source bundle.
- Complete Phase 2 harness and task suites.
- Corrected cross-model reporter and its regression test.
- Phase 3 discrimination suite, seven-task replication suite, and model configurations.
- Phase 4 tracking-ablation generator, suite, methodology, and tests.
- Updated Gemini 3.6-versus-3.7 evaluation report document.

## Recovered experimental records

- Phase 1 synthetic-core runs.
- Phase 2 priority, post-backend, and 600-second diagnostic runs.
- Gemini 3.6 and 3.7 AVU model-comparison runs.
- Phase 3 one-shot, fully replicated, combined 92-record, and balanced 84-record cohorts.
- Regenerated Markdown and CSV reports from the recovered JSONL sources.

## Important limitations

- Generated videos were omitted because every synthetic stimulus can be reproduced from its checked-in task specification.
- Any local run or hand-edited file that was never uploaded cannot be independently recovered here.
- API credentials and virtual environments were intentionally not recovered or bundled.

The authoritative Phase 3 comparison input is:

`artifacts/runs/phase3-validation/gemini-3.6-vs-3.7-phase3-balanced.jsonl`

It contains 84 records: seven tasks × two models × two processing modes × three repetitions.
