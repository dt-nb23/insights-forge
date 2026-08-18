---
name: drill
description: |
  Chat-native intake skill. Runs the Phase 0 clarifying questions in-chat
  without a pre-filled seed-prompt brief. Produces the same brief format as
  the browser Seed Prompt Generator so both paths converge at context-framing.
  Use when the consultant starts cold (no form output) or needs to fill
  gaps from a partial brief. Invoke with /drill.
---

# /drill — Chat-Native Intake

## When to use

Use when:
- The consultant types `/drill` or asks to start the intake without a form.
- A seed-prompt brief was pasted but some MUST-HAVE fields are empty.
- The consultant wants to update a specific section of an existing brief.

**Do not use** if a complete brief (all MUST-HAVEs filled) is already present — use the brief-complete fast path in `skills/context-framing/SKILL.md` instead.

## How this differs from context-framing

`/drill` is pure intake — it collects fields and produces a brief. It does **not** create an engagement folder, write `current-context.md`, or advance to Phase 0's orientation hypotheses. Those steps happen in `context-framing` after the brief is complete.

Both paths produce the same output: a structured brief that `context-framing` reads as its Phase A and Phase B inputs.

## Partial drill — skip known fields

If the consultant provides a partial brief along with `/drill`, read the brief first and identify which MUST-HAVE fields are already populated with real values. Skip those fields. Ask only for the unfilled MUST-HAVEs plus any SHOULD-HAVEs that would add clear framing value.

Start with: "I see [N] fields already filled. Let me collect the missing pieces."

## Procedure

Run the two-phase structure from `context-framing`:

**Phase A — Narrative funnel (Q1–Q3, C.S.I.R.):**

Ask conversationally, building on each answer. Work through:
1. Q1 — Customer and what they do
2. Q2 — Vertical
3. Q3 — C.S.I.R. sub-sequence (Context → Specific Information → Intent → Response Format), one dimension at a time

Allow the consultant's answers to flow naturally. A short crisp answer wraps a dimension. Follow up only if a dimension is genuinely unclear.

**Phase B — Closed drill block (Q4–Q9):**

Once C.S.I.R. is confirmed, present Q4–Q9 in one message:

> "To anchor the plan, I need a few factual details:
>
> - **Tenant type:** SaaS or Managed?
> - **Active capabilities:** [present the Q5 checklist]
> - **RUM on the app in question:** enabled? Session Replay on?
> - **Primary stakeholder:** who will consume the deliverable and what do they care about most?
> - **Technical team's day-to-day priorities:** main pain points or frustrations?
> - **Engagement trigger:** QBR, renewal, expansion, or something else?"

Skip any question the consultant has already answered.

## Output

A structured brief in the exact format the Seed Prompt Generator produces:

```markdown
# Insights Forge intake brief

> **For the agent — read first.**
> This brief was produced by the /drill skill. Treat all populated fields as answers to the Phase 0 clarifying questions. Proceed with the brief-complete fast path if all MUST-HAVEs are filled; otherwise continue with the standard two-phase intake for any missing fields.

## Customer
- **Company:** [name or anonymized label]
- **Business description:** [what they sell/do]
- **Industry vertical:** [vertical]
- **Size (ACV band):** [if known]
- **Region(s):** [if known]

## Engagement framing (C.S.I.R.)
- **Context (C):** [relationship history, consultant role]
- **Specific Information (S):** [constraints, prior outcomes, contract phase]
- **Intent (I):** [consultant's goal, customer's expected outcome]
- **Response format (R):** [format, audience, tone/length]

## Environment
- **Tenant type:** [SaaS / Managed]
- **Active capabilities:** [checked list]
- **RUM on app in question:** [enabled / not enabled; Session Replay on/off]
- **Environment file exists:** [yes / no]

## Stakeholder
- **Primary contact:** [role / name if provided]
- **Key KPIs / priorities:** [named KPIs]
- **Archetype match:** [from stakeholder-profiles.md]

## Technical team
- **Day-to-day priorities:** [pain points, frustrations]

## Engagement trigger
- **Trigger:** [QBR / renewal / expansion / touchpoint / other]

## Analyst calibration
- **Consultant experience (1–5):** [if stated or inferred]
- **Account familiarity (1–5):** [if stated or inferred]
- **Customer DT maturity (1–5):** [if stated or inferred]

## Out-of-scope exclusions
[Capabilities or topics ruled out. Write "None stated" if no exclusions named.]
```

After producing the brief, hand off to `context-framing`:

> "Brief complete. Type **approve** to proceed with Phase 0, or tell me anything you want to adjust."

On approval, context-framing takes over, reads the brief using the brief-complete fast path (if all MUSTs are filled), and creates the engagement folder.
