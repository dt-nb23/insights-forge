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

Read these files before starting:

- `memory/project-space/hypotheses.md` — confirmed, open, and validating hypotheses with ICE scores.
- `memory/project-space/signals-map.md` — for the business KPIs that anchor recommended actions.
- `memory/project-space/current-context.md` — for stakeholders, owners, and decision deadlines.
- `memory/long-term/dynatrace-playbooks.md` — the playbook matched to each hypothesis at Phase 1 supplies the investigation sequence. The numbered steps in that playbook become the candidate investigation-action rows; the "confirmed" / "ruled out" sections become the exit criteria.
- `memory/long-term/frameworks.md` — for the exit-criteria standard.
- `memory/long-term/stakeholder-profiles.md` — for the leaders whose decisions will be asked.

**Preserve citations.** Any URL + retrieval-date citation already attached to a hypothesis or signal row (from `skills/external-research/SKILL.md` or from a playbook in `dynatrace-playbooks.md`) must flow through into the investigation-action row that consumes it. If an investigation action depends on a Dynatrace feature behavior not already cited upstream, fetch and cite it now rather than asserting it. Allowlist remains `docs.dynatrace.com` and `community.dynatrace.com`.

## Steps

1. **Define investigation actions for every open and validating hypothesis.** Each investigation action specifies:
   - What the team will look at (telemetry, dashboard, analysis).
   - The data source(s) — RUM, APM, business events, third-party.
   - Who is involved (which team or named owner).
   - **Exit criteria for confirmed** and **exit criteria for ruled out**, written before the investigation starts so the outcome is not adjudicated after the fact.
   - Target completion date.
2. **Draft recommended actions, ranked by impact vs effort.** For each confirmed hypothesis (or each high-Impact open hypothesis where a contingent plan makes sense), name:
   - The action.
   - The hypothesis or evidence it is conditional on (if any).
   - The owner.
   - The timeframe.
   - Notes — including any coordination, sequencing, or vendor dependencies.
3. **Surface decision asks for leadership.** Distill the recommended actions into the **specific decisions a named leader needs to make** before work can proceed. Each ask is one sentence: "Approval to roll back iOS SDK to 4.11 within 24h of H-01 confirmation — VP of Engineering owns this decision."
4. **Document risks and tradeoffs.** Every recommendation has a cost. Pair each high-impact recommendation with its risk and a mitigation in the same line. This is what the Consultative lens will look for in Phase 3 — surface it now so the one-pager does not have to invent it.
5. **Invoke the Skeptic lens** (`.claude/agents/skeptic-lens.md`) on the draft plan. Capture risks, severity, and mitigations. Incorporate the "questions a leader will ask" into the decision-asks section so the plan answers them up front.
6. **Revise** based on the lens output.
7. **Write to `memory/project-space/action-plan.md`.** All four sections — investigation actions, recommended actions, decision asks, risks and tradeoffs — must be populated. No placeholders in the live file.

## Output

`memory/project-space/action-plan.md`, fully populated and ready for the Phase 2 gate.

## Common pitfalls

- **Investigation actions without exit criteria.** "Look at the data" is not a plan. Specify the comparison, the time window, and what constitutes confirmed vs ruled out.
- **Recommended actions without owners or timeframes.** An action without an owner is a wish.
- **Decision asks framed as updates instead of asks.** "We will be rolling back" is a statement; "We need approval to roll back" is an ask. Leadership reads asks differently from updates.
- **Risks hidden in an appendix.** Pair risks with the recommendation they belong to. If a leader has to flip between sections to find the cost of a recommendation, the plan is hiding the cost.
- **Skipping the Skeptic lens.** This is the moment to catch what a hostile reviewer will find in Phase 3. Cheaper to fix now than in front of the VP.
