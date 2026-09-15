# Gemini 3.7 Flash public AVU: Phase 4 results

## Cohort integrity

- 48 observations: eight tasks × two modes × three repetitions.
- 48 unique `(model, task, mode, repetition)` keys.
- 48/48 completed; no timeouts or request failures.
- Model: `gemini-3.7-flash`.
- SDK: `google-genai` 2.21.0.
- Native processing evidence: 24/24 agentic, 0/24 static.

## Registered result

| Metric | Static | Agentic |
|---|---:|---:|
| Exact | 3/24 (12.5%) | **14/24 (58.3%)** |
| Mean semantic score | 0.320 | **0.893** |
| Mean provider latency | **11.452 s** | 15.376 s |
| Mean total tokens | **2,470** | 9,071 |
| Strict JSON | 0/24 | 0/24 |

Agentic scored higher in 19 matched attempts, tied in three, and scored lower
in two. It was faster in 7/24 and used fewer total tokens in 0/24.

## Interpretation

The matched OCR pair rules out the simplest label-reading shortcut in this
cohort: labeled and unlabeled conditions both produced static 0/3 and agentic
3/3. Seven agentic non-exact outputs preserved the entire sequence and differed
only by common color aliases. Alias-normalized exactness is 21/24 agentic versus
4/24 static, but this is diagnostic and must not replace the registered metric.

`phase4_combined_hard` was 0/3 exact in both modes and is the demonstrated
breaking point. Agentic often recovered the true sequence but included false
crossings; one attempt also misordered events.

The appropriate conclusion is a controlled synthetic tracking advantage with
a material resource penalty—not universal superiority, production readiness,
or real-world generalization.
