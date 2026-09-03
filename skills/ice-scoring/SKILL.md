---
name: ice-scoring
description: Procedure for scoring and ranking hypotheses or actions using Impact × Confidence / Effort. Use after hypotheses are drafted, or to re-rank actions.
---

# ICE Scoring

## When to use

- In Phase 1, **after `signal-mapping` has written `signals-map.md`** — not immediately after hypotheses are drafted. ICE runs last in the Phase 1 sequence because Impact anchors on the business KPIs in `signals-map.md` and Step 0 reads its "Instrumentation gaps" section. If `signals-map.md` does not yet exist, stop and run `signal-mapping` first.
- After new evidence arrives that materially changes Confidence or Status on one or more hypotheses.
- In Phase 2, to re-rank the opportunity set after the persona panel — recalibrating the Phase 1 scores into Phase 2 terms (see "Recalibration when re-ranking for Phase 2" below).

The ICE formula is:

```
ICE = (Impact × Confidence) / Effort
```

All dimensions scored 1–10. Higher ICE = higher priority. Use the ranking as a starting point for prioritization conversations, not as an automatic decision rule.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session. The agent fixes it once — when Phase 0 (`context-framing`) creates the engagement folder, or when a paused/active engagement is resumed — and holds it in working context for the rest of the session. There is **no shared pointer file** to read; nothing depends on a global "active" file a second concurrent session could overwrite.
2. If no engagement is established yet (a fresh session picking up earlier work), resolve it with the resume procedure in `skills/investigation-reset/SKILL.md`: scan `memory/clients/*/engagements/*/current-context.md` for a `state:` of `active` or `paused`, present the matches, and have the user pick one. If none, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = the established/selected path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`). CLIENT_NAME = the segment between `memory/clients/` and `/engagements/`.
4. All phase file reads/writes use ENGAGEMENT_PATH as the base — e.g., `<ENGAGEMENT_PATH>/hypotheses.md`.

Then read these files:

- `<ENGAGEMENT_PATH>/hypotheses.md` — the items to score.
- `memory/long-term/frameworks.md` — for the calibration definitions of Impact, Confidence, and Effort. Apply consistently within a single scoring pass.
- `<ENGAGEMENT_PATH>/signals-map.md` — for the business KPI mappings that anchor Impact scores.
- `<ENGAGEMENT_PATH>/current-context.md` — for the **Out-of-scope exclusions**. An item whose confirmation or execution depends on an excluded capability is not scored — remove it from the scoring list, note the removal, and report it in part 4 of the gate summary block. Paste the exclusions verbatim into the ICE-lens dispatch prompt (CLAUDE.md dispatch rule).

## Steps

0. **Check measurability before scoring Impact.** For each item, read its Status in `hypotheses.md` and cross-reference the "Instrumentation gaps" section of `signals-map.md`. If validation depends on a gap that is not yet closed — i.e. the hypothesis is `blocked: instrumentation`, or its KPI link cannot be measured today — adjust the scores accordingly:
   - **Raise Effort** to fold in the instrumentation work required before the item can even be validated or executed.
   - **Lower Confidence** — confirmation is currently impossible, so Confidence cannot reflect strong belief regardless of how plausible the claim feels.
   - **Lower Impact** if the KPI link cannot be quantified with today's telemetry; an unquantifiable impact cannot anchor a high score.
   - **Note the adjustment in the justification cell**, naming the specific gap (e.g., "Effort raised + C lowered: no RUM error attribution by route until SDK 4.13 ships").
   Calibration reminder: Impact and Effort must reflect **measurability**, not just the underlying engineering merit. A high-merit item the team cannot yet measure or validate ranks below one it can act on now.
1. **Score Impact (1–10)** for each item based on the magnitude of the business outcome if the hypothesis is confirmed or the action is executed. Anchor the score to the business KPI in `signals-map.md`. State the KPI and the directional effect in the justification cell.
2. **Score Confidence (1–10)** based on the strength of prior evidence. Confidence is a function of *independent* signals. Three dashboards drawing from the same telemetry source = one signal. State which signals are supporting the Confidence score.
3. **Score Effort (1–10)** based on the engineering and analytics cost to validate the hypothesis or execute the action. Include cross-team coordination cost, not just developer-hours. State the rough timeline (hours / days / weeks / quarters).
4. **Compute ICE** = (Impact × Confidence) / Effort. Round to two decimals.
5. **Rank descending.** Sort the table by ICE.
6. **Flag items where one dimension is doing most of the work.** A very low Effort score can inflate ICE for a low-impact item. A very high Confidence score on a single-signal Hypothesis can inflate ICE artificially. Flag these in the justification column so the team scrutinizes them.
7. **Invoke the ICE lens** (`.claude/agents/ice-lens.md`) for a sanity-check pass on the scoring. Capture any rescoring suggestions.
8. **Update the table** in `<ENGAGEMENT_PATH>/hypotheses.md` with the scores and the ICE column. Preserve prior scores in a brief annotation if a score has materially changed (e.g., "C: 4 → 7, raised after A-02 confirmed latency regression").

## Output

Updates `<ENGAGEMENT_PATH>/hypotheses.md` with Impact, Confidence, Effort, and ICE columns populated for every row.

## Phase 1 gate

ICE scoring is the last Phase 1 step, so this skill closes the phase. After updating `hypotheses.md`, present the **Phase 1 gate summary block** (per CLAUDE.md "Gate summary block") with the full ranked table:

1. **Conclusion** — the highest-ICE hypothesis and what it implies for the investigation, in one sentence.
2. **What changed** — what Phase 1 produced since the Phase 0 gate: the issue tree (and what the MECE lens changed), the hypothesis set (and what the Consultative framing pass reworded), the signals map, and which hypotheses rose or fell in the ranking and why.
3. **Assumptions and confidence gaps** — every hypothesis whose score was adjusted for an instrumentation gap (raised Effort, lowered Confidence, lowered Impact) with the gap named; every business-KPI linkage in `signals-map.md` that is qualitative rather than measured; any ICE-lens rescoring suggestion the agent declined and why.
4. **Out-of-scope cost** — any hypothesis or signal excluded because confirming it would require an out-of-scope capability; otherwise "No out-of-scope items arose this phase."
5. **Approve / Redirect / Iterate** — "**Approve** to proceed to Phase 2 (action planning), **Redirect** [scope or framing change], or **Iterate** [lens to re-run on the scored hypotheses]."

Record the gate decision in `<ENGAGEMENT_PATH>/decisions-log.md`; on approval, set `phase: 2` and today's `last-touched:` in `<ENGAGEMENT_PATH>/current-context.md`. Do not begin Phase 2 until the user explicitly approves.

## Calibration reminders

- **Impact** is anchored to business KPI magnitude, not to engineering interest.
- **Confidence** is anchored to independent supporting signals, not to how confident the author feels.
- **Effort** includes cross-team coordination, not just engineering hours.
- An ICE score is a **ranking tool, not a verdict**. The team makes the final call.

## Recalibration when re-ranking for Phase 2

Phase 1 and Phase 2 score the same dimensions against different questions. Do not carry Phase 1 numbers over unchanged when re-ranking the opportunity set in Phase 2 — recalibrate:

- **Confidence.** Phase 1 Confidence = likelihood the hypothesis is **validated by telemetry**. Phase 2 Confidence = likelihood the action **executes given coordination and risk**. A hypothesis the data strongly supports may still face hard cross-team or rollout risk as an action.
- **Impact.** Phase 1 Impact = magnitude **if the hypothesis is confirmed**. Phase 2 Impact = magnitude **if the mitigation is executed** — so a partial fix scores *below* the problem it addresses, because it only recovers part of the at-stake KPI.

Worked example: H-01 enters Phase 1 with Confidence 7 (telemetry strongly supports the latency-regression hypothesis). Its mitigation A-01 carries real coordination risk across two teams and a release-train dependency, so its Phase 2 Confidence drops to 5 — the evidence is solid, but executing the fix is less certain. Annotate the change in the justification cell (e.g., "C: 7 → 5, recalibrated for Phase 2 coordination risk across platform + payments") rather than silently overwriting it.
