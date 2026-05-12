# Frameworks

The agent's procedural reference for the structured analysis techniques used in every investigation. Updated only on explicit user approval.

## MECE (Mutually Exclusive, Collectively Exhaustive)

A structuring discipline borrowed from management consulting. A set of branches is **MECE** if every relevant cause fits into exactly one branch and no real cause is missing from the set.

### Definition

- **Mutually exclusive**: no two branches overlap. Any given cause belongs in one branch only.
- **Collectively exhaustive**: every plausible cause is captured by some branch in the set.

A MECE tree is a tool for thinking, not a deliverable in its own right. Its value is that it forces the team to confront where they have not yet looked.

### Common pitfalls

- **Overlap.** "Backend" and "Database" branches placed at the same level — but database queries are part of backend behavior. Resolve by making "database" a child of "backend" or by renaming "backend" to "application logic".
- **Gaps.** Missing third-party branch, missing instrumentation-gap branch, missing business-process branch (deploy events, feature flag rollouts, A/B tests, pricing changes). These hide in plain sight because they are not always owned by the engineering team.
- **Mixed abstraction levels.** "iOS" and "the API" cannot be siblings — one is a platform, one is a service. Either rephrase as a platform/service decomposition or as a stack-layer decomposition; do not mix them.
- **Solution-shaped branches.** "Add caching" is a solution. The problem-space form is "Cache behavior" or "Request load characteristics".
- **Conclusion-shaped branches.** "Backend is slow" presupposes the answer. Use "Backend behavior" so the tree can do its work.

### Template question set for testing a tree

Before approving a tree, run these questions against it:

1. For each pair of branches, can you name a cause that could plausibly live in both? If yes, you have overlap.
2. Imagine a cause that has hit your system before that does not fit in any branch. Where does it go? If nowhere, you have a gap.
3. Are all branches at the same level of abstraction? Read them out loud — if one sounds like a category and another sounds like a specific component, abstraction is mixed.
4. Is any branch phrased as a solution, an action, or a conclusion? If yes, rephrase as a problem space.
5. Does the tree include third-party dependencies, business process changes, and instrumentation gaps? These three are the most commonly missed.

## ICE Scoring

A prioritization formula for ranking hypotheses or actions.

### Formula

```
ICE = (Impact × Confidence) / Effort
```

All three dimensions are scored on a 1–10 scale. Higher ICE = higher priority. Use as a ranking tool, not as an absolute decision rule — a high-ICE item with weak supporting evidence still deserves a second look.

### Calibration guidance

- **Impact (1–10)** — the magnitude of the business outcome if the hypothesis is confirmed or the action is executed.
  - 1–3: marginal effect, narrow surface area, single workflow.
  - 4–6: meaningful effect on a single team, product surface, or workflow.
  - 7–8: meaningful effect on a product line, revenue stream, or top-line KPI.
  - 9–10: company-level outcome — revenue, churn, market position, regulatory.
- **Confidence (1–10)** — strength of prior evidence that the hypothesis is true or the action will work.
  - 1–3: hunch. No telemetry, no precedent, no analogous case.
  - 4–6: indirect signals or relevant precedent elsewhere in the org.
  - 7–8: direct signals from this system pointing the same direction.
  - 9–10: confirmed by multiple independent signals; what remains is sizing, not validation.
- **Effort (1–10)** — the engineering and analytics cost to validate the hypothesis or execute the action.
  - 1–3: hours of work for one person.
  - 4–6: days; coordination across one team.
  - 7–8: weeks; cross-team coordination.
  - 9–10: multi-quarter; significant headcount, platform change, or vendor coordination.

### Worked example

> Hypothesis: A backend latency regression after the 2026-05-04 deploy is causing cart abandonment.
>
> - **Impact**: 7 — cart abandonment is a direct lever on revenue; a regression affects every checkout session.
> - **Confidence**: 7 — funnel data shows a step-function drop in cart→payment conversion at the deploy timestamp; latency dashboards show a correlated rise.
> - **Effort**: 4 — a few days of focused analytics work to confirm cleanly, plus coordination with the cart-service team.
> - **ICE**: (7 × 7) / 4 = **12.25**

### Watch-outs

- **Effort doing too much work.** A very low Effort score can inflate ICE for a low-impact item. When this happens, flag it in the justification column.
- **Confidence inflated by a single signal.** Confidence is a function of *independent* signals. Three dashboards drawing from the same telemetry source = one signal, not three.
- **Impact stated without a denominator.** "High impact" is not a number. State Impact in terms of the KPI it touches.

## Issue tree → hypothesis mapping

A MECE branch is a problem space. A hypothesis is a specific, testable claim about what is happening inside that problem space.

- One branch may yield 2–4 hypotheses.
- Each hypothesis must be **testable** — there must be a signal that would confirm it and a signal that would rule it out.
- Each hypothesis must specify the **expected signals**, the **validation approach**, and the **required metrics** (kinds of data, not raw queries).
- If a branch yields no testable hypothesis, that is a finding in itself: the branch is real but invisible without new instrumentation, and the instrumentation gap belongs in the action plan.

## Exit criteria

"Confirmed" and "ruled out" are not vibes. Each hypothesis must carry exit criteria that the team agrees on **before** the investigation starts, so the result is not adjudicated after the fact.

- **Confirmed** — the expected signals are present at the predicted magnitude in the predicted window, and no alternate hypothesis fits the same signal pattern equally well.
- **Ruled out** — the expected signals are absent, or are present but do not correlate with the outcome the hypothesis claims to explain, or an alternate hypothesis explains the same signals more parsimoniously.
- **Inconclusive** — the data needed to apply either criterion does not exist. This is a legitimate outcome and surfaces an instrumentation gap, not a failure of the investigation.
