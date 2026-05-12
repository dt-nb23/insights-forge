---
name: ice-scoring
description: Procedure for scoring and ranking hypotheses or actions using Impact × Confidence / Effort. Use after hypotheses are drafted, or to re-rank actions.
---

# ICE Scoring

## When to use

- After new hypotheses are drafted in `memory/project-space/hypotheses.md` and the table needs ranking.
- After new evidence arrives that materially changes Confidence on one or more hypotheses.
- When the Phase 2 action plan needs prioritization across recommended actions.

The ICE formula is:

```
ICE = (Impact × Confidence) / Effort
```

All dimensions scored 1–10. Higher ICE = higher priority. Use the ranking as a starting point for prioritization conversations, not as an automatic decision rule.

## Inputs

Read these files before starting:

- `memory/project-space/hypotheses.md` — the items to score.
- `memory/long-term/frameworks.md` — for the calibration definitions of Impact, Confidence, and Effort. Apply consistently within a single scoring pass.
- `memory/project-space/signals-map.md` — for the business KPI mappings that anchor Impact scores.

## Steps

1. **Score Impact (1–10)** for each item based on the magnitude of the business outcome if the hypothesis is confirmed or the action is executed. Anchor the score to the business KPI in `signals-map.md`. State the KPI and the directional effect in the justification cell.
2. **Score Confidence (1–10)** based on the strength of prior evidence. Confidence is a function of *independent* signals. Three dashboards drawing from the same telemetry source = one signal. State which signals are supporting the Confidence score.
3. **Score Effort (1–10)** based on the engineering and analytics cost to validate the hypothesis or execute the action. Include cross-team coordination cost, not just developer-hours. State the rough timeline (hours / days / weeks / quarters).
4. **Compute ICE** = (Impact × Confidence) / Effort. Round to two decimals.
5. **Rank descending.** Sort the table by ICE.
6. **Flag items where one dimension is doing most of the work.** A very low Effort score can inflate ICE for a low-impact item. A very high Confidence score on a single-signal Hypothesis can inflate ICE artificially. Flag these in the justification column so the team scrutinizes them.
7. **Invoke the ICE lens** (`.claude/agents/ice-lens.md`) for a sanity-check pass on the scoring. Capture any rescoring suggestions.
8. **Update the table** in `memory/project-space/hypotheses.md` with the scores and the ICE column. Preserve prior scores in a brief annotation if a score has materially changed (e.g., "C: 4 → 7, raised after A-02 confirmed latency regression").

## Output

Updates `memory/project-space/hypotheses.md` with Impact, Confidence, Effort, and ICE columns populated for every row.

## Calibration reminders

- **Impact** is anchored to business KPI magnitude, not to engineering interest.
- **Confidence** is anchored to independent supporting signals, not to how confident the author feels.
- **Effort** includes cross-team coordination, not just engineering hours.
- An ICE score is a **ranking tool, not a verdict**. The team makes the final call.
