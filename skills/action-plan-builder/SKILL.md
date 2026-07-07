---
name: action-plan-builder
description: Procedure for building the Phase 2 action plan from confirmed and open hypotheses. Use when the team is ready to translate the diagnosis into investigation and recommended actions.
---

# Action Plan Builder

## When to use

The **Phase 2 deliverable**. Use after Phase 1 has been approved — that is, after the user has signed off on the issue tree, the ranked hypotheses, and the signals map.

Use this skill when:

- Phase 1 is approved and the team is ready to plan how to validate the remaining hypotheses and what to do once they are validated.
- New evidence has materially changed Phase 1 conclusions and the action plan needs to be revised.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session. The agent fixes it once — when Phase 0 (`context-framing`) creates the engagement folder, or when a paused/active engagement is resumed — and holds it in working context for the rest of the session. There is **no shared pointer file** to read; nothing depends on a global "active" file a second concurrent session could overwrite.
2. If no engagement is established yet (a fresh session picking up earlier work), resolve it with the resume procedure in `skills/investigation-reset/SKILL.md`: scan `memory/clients/*/engagements/*/current-context.md` for a `state:` of `active` or `paused`, present the matches, and have the user pick one. If none, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = the established/selected path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`). CLIENT_NAME = the segment between `memory/clients/` and `/engagements/`.
4. All phase file reads/writes use ENGAGEMENT_PATH as the base — e.g., `<ENGAGEMENT_PATH>/action-plan.md`.

Then read these files:

- `<ENGAGEMENT_PATH>/hypotheses.md` — confirmed, open, and validating hypotheses with ICE scores.
- `<ENGAGEMENT_PATH>/signals-map.md` — for the business KPIs that anchor recommended actions.
- `<ENGAGEMENT_PATH>/current-context.md` — for stakeholders, owners, and decision deadlines.
- `memory/long-term/dynatrace-playbooks.md` — the playbook matched to each hypothesis at Phase 1 supplies the investigation sequence. The numbered steps in that playbook become the candidate investigation-action rows; the "confirmed" / "ruled out" sections become the exit criteria.
- `memory/long-term/frameworks.md` — for the exit-criteria standard.
- `memory/long-term/stakeholder-profiles.md` — for the leaders whose decisions will be asked.
- `memory/clients/<CLIENT_NAME>/environment.md` — **the client's actual Dynatrace instrumentation** (Management Zones, defined SLOs, synthetic monitors, RUM / Session Replay coverage, business events, log management, instrumentation gaps, DPS headroom). Every investigation and recommended action must be grounded in what this client can actually observe — see Step 2a. If the file does not exist, note that the plan's instrumentation assumptions are unverified and flag `environment-intake` as a follow-on.

**Preserve citations.** Any URL + retrieval-date citation already attached to a hypothesis or signal row (from `skills/external-research/SKILL.md` or from a playbook in `dynatrace-playbooks.md`) must flow through into the investigation-action row that consumes it. If an investigation action depends on a Dynatrace feature behavior not already cited upstream, fetch and cite it now rather than asserting it. Allowlist remains `docs.dynatrace.com` and `community.dynatrace.com`.

## Steps

The Phase 2 plan is built by a **deliberating panel of perspectives**, in a deliberate order: MECE lays out the opportunity space, the plan is drafted against it **and against the client's real instrumentation**, four perspectives critique it over **at least three rounds** (independent positions → cross-examination → convergence), the agent reconciles, and ICE re-ranks once the critique is in. Run the steps in order — the sequence is the point.

1. **Break down the opportunity space — MECE lens.** Before drafting, lay out the full set of opportunities and levers the plan could pull, then invoke the **MECE lens** (`.claude/agents/mece-lens.md`) on that breakdown. Its job here is the same as in Phase 1, applied to the opportunity set instead of an issue tree: confirm the set is **collectively exhaustive** (no viable opportunity missed) and **mutually exclusive** (no two overlap). Apply its fixes. A rough first-cut priority is fine at this point — ICE does the rigorous ranking in step 7. This breakdown is the candidate pool the recommended actions are drawn from.
1a. **Direction check (default ON).** Before building the full plan, draft a one-screen skeleton: the headline framing, the wave/phase structure, and the candidate action list as titles only — no owners, no exit criteria, no detail. Present it per the CLAUDE.md communication protocol (confirm direction / redirect) and wait. Only after confirmation do steps 2–9 run. A redirect here costs minutes; a redirect after the council costs a rebuilt plan.
2. **Define investigation actions for every open and validating hypothesis.** Each investigation action specifies:
   - What the team will look at (telemetry, dashboard, analysis).
   - The data source(s) — RUM, APM, business events, third-party.
   - Who is involved (which team or named owner).
   - **Exit criteria for confirmed** and **exit criteria for ruled out**, written before the investigation starts so the outcome is not adjudicated after the fact.
   - Target completion date.
2a. **Ground every action in the client's instrumentation (`environment.md`).** Before any investigation or recommended action is allowed to name a data source, confirm that source exists in the client's `environment.md`. If an action depends on a capability the client does not have — e.g., "read the SLO burn rate" when no SLOs are defined, "pull synthetic results" with no synthetic monitors, "segment by business event" without Business Analytics — do **not** silently recommend it. Either (a) rewrite it as an **instrumentation work item** ("stand up an availability SLO on checkout, then measure its burn"), or (b) flag the dependency explicitly in the action's Notes as `requires instrumentation: <capability>`. This is the Phase 2 enforcement of the CLAUDE.md rule against inventing instrumentation the client lacks. If `environment.md` does not exist, say the instrumentation assumptions are unverified rather than asserting them.
3. **Draft recommended actions from the opportunity set, ranked by impact vs effort.** For each confirmed hypothesis (or each high-Impact open hypothesis where a contingent plan makes sense), name:
   - The action.
   - The hypothesis or evidence it is conditional on (if any).
   - The owner.
   - The timeframe.
   - Notes — including any coordination, sequencing, or vendor dependencies.
4. **Surface decision asks for leadership.** Distill the recommended actions into the **specific decisions a named leader needs to make** before work can proceed. Each ask is one sentence: "Approval to roll back iOS SDK to 4.11 within 24h of H-01 confirmation — VP of Engineering owns this decision."
5. **Document risks and tradeoffs.** Every recommendation has a cost. Pair each high-impact recommendation with its risk and a mitigation in the same line. The Consultative lens (step 6) and the Phase 3 one-pager both depend on this — surface it now rather than leaving it to be invented downstream.
6. **Convene the deliberating panel — Skeptic, Optimist, Customer, Consultative — over at least three rounds.** This is an AI council, not a relay. Hand every panelist the draft plan **and** the client's `environment.md` (or the environment facts) so critiques are grounded in what this client can actually observe, not generic product capability.

   - **Round 1 — Independent positions (parallel, blind).** Dispatch all four lenses at once, each critiquing the draft *only* from its own vantage, none seeing the others' output. Collect four independent position statements.
     - **Skeptic** (`.claude/agents/skeptic-lens.md`) — fragile assumptions, weak evidence, instrumentation the plan needs but the client lacks, the questions a leader will ask.
     - **Optimist** (`.claude/agents/optimist-lens.md`) — unclaimed upside, higher ambition, capabilities the client already owns but underuses, actions that could run in parallel.
     - **Customer** (`.claude/agents/customer-lens.md`) — whether the plan targets what users actually experience, given the client's real RUM / Session Replay footprint.
     - **Consultative** (`.claude/agents/consultative-lens.md`) — whether it reads as decisions for the named senior leader, with each tradeoff surfaced honestly.
   - **Round 2 — Cross-examination (parallel).** Give each panelist the other three Round-1 positions. Each responds: where it agrees, where it contradicts another lens and why, what it concedes, what it holds firm on.
   - **Round 3 — Convergence (parallel).** Give each panelist the Round-2 reactions. Each states its **final position** — the strongest version of its view after the debate — and flags explicitly any tension it cannot concede.
   - **Continue if needed.** Three rounds is the floor. If panelists are still moving positions or a material tension is unresolved, run another round; stop when positions stabilize.
   - **Round checkpoints (always).** After each round completes, pause and present per the CLAUDE.md communication protocol: 2–3 bullets per lens on its material position or what shifted this round, where the live tensions stand, and what the next round will do. The user chooses: **continue** (run the next round as planned), **steer** (their guidance is injected verbatim into every lens's briefing for the next round), or — after the final round — **proceed** to reconciliation and ICE re-ranking. Checkpoints add visibility and steering, never skipping: the ≥3-round minimum and the full four-lens set always run.

   **Reconciliation — the agent decides (after the rounds).** Read every panelist's final position. For **each material disagreement** — not only the two recurring pairs below — record in a **"Tensions resolved"** subsection of `action-plan.md`: (a) the claim in dispute, (b) each side's logic, and (c) the agent's ruling and why. Resolve each explicitly in the revised plan rather than splitting the difference or averaging it away. **Default tie-break** when no specific rule applies: weight the evidence, and escalate any unresolved high-severity Skeptic risk into the decision-asks section so leadership rules on it. Two conflicts recur and have set tie-breaks:
   - **Optimist vs Skeptic** — ambition against caution. Decide how much upside the plan claims given the evidence, and say which way you ruled.
   - **Customer vs Consultative** — do **not** pick one. The Customer grounds the user need; the Consultative reframes the corrected plan to *serve* that need in leadership terms. The tie-break is to keep the Customer's grounding and let the Consultative reframe on top of it, so the plan stays user-anchored while reading as decisions for a senior leader.

   Fold the Skeptic's "questions a leader will ask" into the decision-asks section so the plan answers them up front. Present the **"Tensions resolved"** subsection at the Phase 2 gate.
7. **Re-rank the opportunities — ICE lens.** After the panel, invoke the **ICE lens** (`.claude/agents/ice-lens.md`) to re-score and re-rank the opportunities in light of what the critique surfaced — Impact, Confidence, and Effort all move once the perspectives have weighed in. Scores must be **recalibrated to Phase 2 action-execution semantics** (per ice-scoring's recalibration note: Confidence = likelihood the action executes given coordination/risk; Impact = magnitude if the mitigation is executed, with a partial fix scoring below its target problem) — not carried over from Phase 1 unchanged. The ranking that lands in the plan is this post-panel ranking, not the first-cut order from step 1.
8. **Revise** based on the panel and the re-ranking.
9. **Write to `<ENGAGEMENT_PATH>/action-plan.md`.** All five sections — investigation actions, recommended actions, decision asks, risks and tradeoffs, and **"Tensions resolved"** (the panel conflicts and their resolutions from step 6) — must be populated. No placeholders in the live file.

## Output

`<ENGAGEMENT_PATH>/action-plan.md`, fully populated and ready for the Phase 2 gate. The **"Tensions resolved"** subsection is a required section, not optional: each panel conflict appears as claim, each side's logic, and the agent's decision.

## Common pitfalls

- **Investigation actions without exit criteria.** "Look at the data" is not a plan. Specify the comparison, the time window, and what constitutes confirmed vs ruled out.
- **Recommended actions without owners or timeframes.** An action without an owner is a wish.
- **Decision asks framed as updates instead of asks.** "We will be rolling back" is a statement; "We need approval to roll back" is an ask. Leadership reads asks differently from updates.
- **Risks hidden in an appendix.** Pair risks with the recommendation they belong to. If a leader has to flip between sections to find the cost of a recommendation, the plan is hiding the cost.
- **Collapsing the panel into one pass.** The council is at least three rounds — independent positions, then cross-examination, then convergence — not a single relay. Round 1 must be blind (no panelist sees another's output) or the independent positions are contaminated. The value is in resolving where the lenses disagree *after* they have actually engaged each other; surface the tension and rule on it, do not average it away.
- **Re-ranking before the critique instead of after.** ICE runs last (step 7). Ranking the opportunities before the panel has weighed in bakes in the pre-critique view and wastes the panel.
- **Skipping the panel to save time.** This is the moment to catch what a hostile reviewer will find in Phase 3. Cheaper to fix now than in front of the VP.
- **Recommending instrumentation the client does not have.** An action that names a data source — SLO burn, synthetics, business events, Session Replay — without confirming it in `environment.md` is fabricated grounding (Step 2a). Convert it to an instrumentation work item or flag the dependency; never present it as a ready action.
- **Running the council as a black box.** The user sees a round summary after every round and can steer the next one. Skipping the checkpoints hides exactly the deliberation the user most needs visibility into — and steering arrives too late to matter.
