# GDE launch demo brief — rapid-crossing event order

## One-line concept

Agentic inspection identifies the decisive moments in a rapidly changing video
and reconstructs an event order that a static pass can miss.

## Demonstration

Several colored circles cross a white reference line within a narrow time
window. The clip generator changes their ordering, trajectories, direction,
timing gaps, and appearance across deterministic variants. The model must return
the chronological order of crossing events.

## Why it matters

Video questions often hinge on a few high-information frames rather than uniform
processing of the complete clip. Fine-motion ordering is a simple visual proxy
for state transitions, sports adjudication, industrial monitoring, and anomaly
analysis.

## Evidence available now

- Original controlled task: agentic exact in 3/3 primary attempts.
- Static comparison: not exact in the three primary attempts.
- Agentic provider latency: 55.7% lower on this specific task.

## Evidence to add before launch copy

- Exactness over all generated variants and three repetitions per mode.
- Completion, timeout, latency, and token distributions.
- At least one mirrored-motion and one narrow-gap success.
- Clear accounting of any failed seeds or retries.

## Intended output

A 30–45 second narrated screen recording showing the clip, the question, the
inspection path, the answer, and the narrow capability claim. The technical
evaluation remains a separate confidential attachment.

