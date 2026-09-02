# X launch copy

## Recommended short thread

### Post 1

Was my Gemini AVU showcase too easy? Honestly, yes: labels, separate lanes and a
clean background.

So I rebuilt it as 8 deterministic tracking ablations × 3 runs: no labels,
tight timing, overlap, bidirectional motion, decoys and noise. Gemini 3.7 Flash
results 🧵

### Post 2

Across 24 matched attempts:

- Agentic: 14/24 exact
- Static: 3/24 exact
- Mean semantic: .893 vs .320

Agentic scored higher in 19 pairs, tied 3 and lost 2.

The public API exposed processing calls/results in all 24 agentic runs and 0
static runs.

### Post 3

The label-reading shortcut did not explain it.

Unlabeled control: agentic 3/3, static 0/3.

Same clip with labels: agentic 3/3, static 0/3.

Most agentic misses preserved the full order but called cyan “teal” or magenta
“pink.”

### Post 4

Not a free win—and not bulletproof.

Agentic was 34% slower and used 3.67× more total tokens. The combined overlap +
decoy + noise + fine-timing task broke both modes in all 3 runs.

Code, exact denominators, raw results and failures: [REPOSITORY LINK]

## Single-post alternative

Gemini 3.7 Flash AVU, 8 tracking ablations × 3 runs: agentic 14/24 exact vs
static 3/24; semantic .893 vs .320. But it was 34% slower, used 3.67× total
tokens, and combined-hard broke both. Code, denominators + failures: [LINK]
