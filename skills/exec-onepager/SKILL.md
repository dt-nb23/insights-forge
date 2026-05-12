---
name: exec-onepager
description: Procedure for producing the Phase 3 exec-ready one-page written deliverable. Use after the action plan has been approved.
---

# Exec One-Pager

## When to use

The **Phase 3 written deliverable**. Use after the Phase 2 action plan has been approved by the user and the team is ready to package the findings for a named senior technical leader (VP of Engineering, Director of Reliability, Head of Data Analytics, or similar).

Use this skill when:

- The action plan is approved and the deliverable is destined for a specific named leader.
- The team has been asked for a written brief ahead of a leadership review.
- A previous one-pager needs revision after new evidence or a redirected scope.

## Inputs

Read these files before starting:

- `memory/project-space/action-plan.md` — the approved action plan.
- `memory/project-space/signals-map.md` — for the business impact numbers and the SLI/SLO grounding.
- `memory/project-space/hypotheses.md` — for the confirmed/open/ruled-out status of each hypothesis.
- `memory/long-term/stakeholder-profiles.md` — for the profile of the intended reader. If no matching profile exists, ask the user which profile to use or whether to create one.
- `memory/long-term/terminology.md` — to ensure first-use definitions for any acronym the reader's profile says they expect.

## Structure

A one-pager has five sections, in this order, and fits on a single page.

1. **Problem summary (2–3 sentences).** What is the problem? What is the urgency? What is the audience being asked to decide? Lead with what changed in the business, not with what was observed in telemetry.
2. **Business impact.** Quantify where possible. "Conversion on iOS checkout has declined 8% week-over-week. At current volume, this is approximately $X/week in revenue at risk." If the numbers carry confidence intervals or assumptions, name them in one short clause. Avoid false precision.
3. **Top findings (3–5 bullets).** The confirmed hypotheses, the open ones with high ICE, and the instrumentation gaps that matter. Each finding is a sentence — what was found and what evidence supports it. No more than five bullets.
4. **Recommended actions.** Each with an **owner** and a **timeframe**. Pair every recommendation with the cost or risk in the same line. "Roll back iOS payment SDK to 4.11 — Mobile platform lead, within 24h of H-01 confirmation. Cost: reintroduces a known checkout bug fixed in 4.12; mitigation is targeted patch if vendor can ship in <72h."
5. **Risks and decision asks.** One short paragraph or three bullets. Surface the questions the leader needs to answer. End with the specific decision being requested.

## Style rules

- **Lead with business impact, not technical detail.** The opening sentence should mean something to a non-engineer reading the document for the first time.
- **No acronyms without first-use definition.** Even if the reader knows SLO, write "Service Level Objective (SLO)" on first use, then SLO thereafter — unless the stakeholder profile says otherwise.
- **One page maximum.** If it doesn't fit, the findings are not yet sharp enough.
- **Match the tone to the named stakeholder profile.** A Director of Reliability tolerates more technical depth than a VP of Engineering; a Head of Data Analytics expects time windows and segmentations stated explicitly. Read the profile first.
- **Tradeoffs in the same paragraph as recommendations.** Never put the cost of an action in a separate "appendix" section. If it costs something, say so where you say what to do.
- **No hedging language.** "May possibly indicate" is noise. State the finding; state the confidence; let the reader decide.

## Quality gates

Before finalizing, run three lenses in this order:

1. **Consultative lens** (`.claude/agents/consultative-lens.md`) — verifies the voice matches the named stakeholder. Apply suggested rewrites.
2. **Customer lens** (`.claude/agents/customer-lens.md`) — verifies the document actually addresses what users experience, not just what the systems team measured. Apply suggested edits.
3. **Skeptic lens** (`.claude/agents/skeptic-lens.md`) — surfaces the "questions a leader will ask" that the current draft does not answer. For each, either incorporate the answer into the one-pager or surface it as a decision ask.

After the lenses, do a final read for the one-page constraint. Cut, don't compress.

## Output

The agent writes a `one-pager.md` file in `memory/project-space/` (filename: `one-pager-YYYY-MM-DD.md` if multiple drafts are expected). The agent then **prompts the user to approve PPTX generation** — it does not automatically invoke the pptx skill. The Phase 3 gate is between the one-pager and the deck.

## Common pitfalls

- **Opening with telemetry instead of business impact.** "p95 latency on cart-service rose 200ms" buries the lede. Start with "checkout conversion dropped 8% week-over-week; here is what's driving it."
- **Burying tradeoffs in a risks-appendix.** Pair them with the recommendations they belong to.
- **Skipping the stakeholder profile.** Every leader reads differently. Read the profile before drafting, not after.
- **Treating the lens passes as optional.** They are the quality gate. Skipping them is how good drafts become bad final documents.
- **Auto-generating the PPTX.** The Phase 3 gate is the one-pager. Wait for explicit user approval before invoking the pptx skill.
