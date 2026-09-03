---
name: drill
description: |
  Chat-native intake skill. Runs the Phase 0 clarifying questions in-chat
  without a pre-filled seed-prompt brief. Produces a brief in the exact
  format defined by docs/brief-contract.md — the same format the browser
  Seed Prompt Generator emits — so both paths converge at context-framing.
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

Both paths produce the same output: a brief in the `docs/brief-contract.md` format that `context-framing` reads as its Phase A, Phase B, and Phase C inputs. Calibration *routing* (drill depth, council size, gate verbosity, ambition ceiling) is computed by `context-framing` from the scores this skill records — `/drill` collects the dial, it does not turn it.

## Partial drill — skip known fields

If the consultant provides a partial brief along with `/drill`, read the brief first and identify which MUST-HAVE fields are already populated with real values. Skip those fields. Ask only for the unfilled MUST-HAVEs plus the SHOULD-HAVEs that pass the marginal-value test in `skills/context-framing/SKILL.md` Step 9 (could a plausible answer change the issue tree, the hypothesis set, or the deliverable's framing?). The same skip rule applies to anything the consultant supplies up front in prose — never re-ask what has already been answered.

Start with: "I see [N] fields already filled. Let me collect the missing pieces."

## Procedure

Run the three-phase structure from `context-framing`:

**Phase A — Narrative funnel (Q1–Q3, C.S.I.R.):**

Ask conversationally, one question at a time, building on each answer:
1. Q1 — Customer and what they do → the brief's `Name` and `What they do` lines.
2. Q2 — Vertical → the `Vertical(s)` line.
3. Q3 — C.S.I.R. sub-sequence, one dimension at a time:
   - **Context** → the `Relationship & context` line (relationship history, mood, recent milestones or incidents).
   - **Specific Information** → the `## Pain & constraints` section (day-to-day pain plus constraints: commitments, prior outcomes, regulated data, contract phase).
   - **Intent** → the `## Goals & success criteria` section, both halves: what *Dynatrace* wants (`Dynatrace intent:`) and what the *customer* would call success (`Customer success:`).
   - **Response format** → `Additional formats` (which presentation formats to build on top of the always-produced customer action plan: Executive one-pager, PowerPoint deck, Execution guides — required; "none, action plan only" is a valid answer) and each stakeholder's communication level.

Allow the consultant's answers to flow naturally. A short crisp answer wraps a dimension. Follow up only if a dimension is genuinely unclear.

**Phase B — Closed drill block:**

Once C.S.I.R. is confirmed, present the remaining factual fields in one message, skipping anything already answered:

> "To anchor the plan, I need a few factual details:
>
> - **Your role:** Insights Analytics Consultant, CSM, SE, Consultant, or other?
> - **Calibration (all three optional — pick the statement that fits):**
>   - *Your experience with Dynatrace consulting:* New to Dynatrace consulting / A few engagements delivered / Comfortable across the common patterns / Deep experience across verticals / Expert — the person others ask
>   - *Account familiarity:* First touch — no history with this account / Read the notes, never worked it / A few working sessions in / Know the environment and the players / Deep history — multi-year relationship
>   - *Customer's Dynatrace maturity:* Just onboarding — basics only / Core APM in place, little else / Several capabilities in active use / Broad adoption with SLOs and some automation / Advanced — full-stack, Grail, automation at scale
> - **Customer size (ACV band), tenant type (SaaS or Managed), and region(s)** (NORAM / LATAM / EMEA / APAC)?
> - **Active capabilities:** [present the Q5 checklist — Davis AI is always on; at least one beyond Davis, or "unsure"]
> - **Out of scope:** anything the plan must not suggest, even if the capability is active?
> - **Stakeholders:** for each — name, role archetype (required), communication level (Technical / Executive / Mixed), and what they care about most?
> - **Focus applications:** each app in scope with RUM and Session Replay status (Yes / No / Unsure)?
> - **Engagement trigger:** QBR, New Customer, Renewal, Expansion, Client Conversation, Incident follow-up, or something else?"

The calibration questions are **behavioral picks**, not numeric ratings: the consultant picks the anchor statement (or clearly implies one), and you record its position as N/5. The anchor labels above are the same five per scale that the form presents — copy them exactly from `docs/brief-contract.md`. Any subset of the three may be answered; there is no rate-one-rate-all rule.

Focus applications follow the contract's rule: optional, but required (at least one app with name, RUM, and Session Replay status) when the goals text signals digital-experience intent (phrase set in `docs/brief-contract.md`).

**Phase C — Vertical drill sheet:**

Once the closed block is answered, open the drill sheet for the vertical from Phase A (`memory/long-term/drill-sheets/README.md` maps each Q2 vertical to its file). Prune it: drop any question whose capability dependency is not in the Active capabilities just collected, and any whose topic is on the Out of scope list. Skip the whole phase only when the Specific Information answer already covers the sheet's questions — a targeted probe gets a better answer than the generic "what does the technical team care about?", so the default is to ask. Ask the surviving questions in **one message**, in the sheet's fixed order, using the consultant-facing phrasings. Record the answers inside the brief's `## Pain & constraints` block as a trailing `Technical team priorities:` paragraph, each answer tagged `[sheet Qn]`, so context-framing can trace which probe produced which fact. Name any pruned question when you hand off, so the consultant can override.

## Output

Emit the brief in the exact format defined by `docs/brief-contract.md` — the same format the Seed Prompt Generator produces (`tools/conformance-check.py` verifies the two stay in sync). The template below is embedded so this skill is self-contained; if it ever disagrees with the contract, the contract wins.

Fill every line; write `not provided` for anything the consultant declined or could not answer — a gap is shown, not hidden. Emit the preamble blockquote verbatim as written here. `Generated:` is today's date.

```markdown
# Insights Forge intake brief

> **For the agent — read first.** This is a seeded Phase 0 engagement intake, captured with Insights Forge and aligned to skills/context-framing/SKILL.md. The **baseline deliverable is always a customer action plan**; "Requested outputs" below are the presentation formats to produce on top of it.
>
> **How the inputs are categorized:**
> - **Required context** — Requested outputs, Customer (name / what-they-do / vertical), Relationship & context, Pain & constraints, Dynatrace intent + customer success, Active capabilities, and at least one Stakeholder (role archetype required; a named person strongly preferred). Framing is not complete without these.
> - **Recommended context** — Analyst calibration (1–5) + role, Tenant, Customer region(s), per-stakeholder communication level & priorities, and Trigger. These sharpen tone, depth and KPI selection.
> - **Active capabilities are the boundary** of what insight you can surface — do not propose value that depends on a capability not listed. Davis AI is always on.
> - **Out of scope is a hard exclusion** — do not suggest or reference anything the customer has flagged as out of scope, even if the underlying capability is active.
> - Any value shown as "not provided" is a genuine gap.
>
> **Before you build the plan:** ask the consultant **1–3 rounds of clarifying questions**, one topic at a time, until you have enough substantial context to move forward confidently. Start with any Required item marked "not provided", then tighten Intent, capability scope, and what each stakeholder cares about. Do not advance past the Phase 0 gate until the consultant approves your framing.

## Requested outputs & trigger
- Baseline (always): Customer action plan
- Additional formats: [comma list, or "none (action plan only)"]
- Trigger(s): [comma list, or "not provided"]
- Analyst: role [role]; experience [N/5 — "anchor" or "not provided"], account familiarity [N/5 — "anchor" or "not provided"], customer Dynatrace maturity [N/5 — "anchor" or "not provided"]
- Generated: [YYYY-MM-DD]

## Customer context
- Name: [customer name]
- What they do: [one line]
- Vertical(s): [comma list]
- Customer size (ACV): [band, or "not provided"]
- Tenant type: [SaaS / Managed, or "not provided"]
- Region(s): [comma list, or "not provided"]
- Relationship & context: [relationship history and mood]

## Stakeholders & audience
- [name or "(unnamed)"] · [archetype] · communication level: [Technical / Executive / Mixed] — cares about: [priorities, or "not provided"]

## Goals & success criteria
Dynatrace intent: [what Dynatrace wants from the engagement]
Customer success: [what the customer would call success]

## Pain & constraints
[day-to-day pain plus constraints, one block]
Technical team priorities: [sheet Q1] [answer]; [sheet Q2] [answer]; … — or omit this line when Phase C was skipped

## Active capabilities
- Davis AI (problem detection) (always on)
- [capability label — generation if stated]
[if unconfirmed: "- Capabilities unconfirmed — analyst requests help confirming during framing"]

## Out of scope / do not suggest
- [excluded capability, or the whole section is "not provided"]
- Notes: [free text, if any]

## Focus applications
- [app name] — RUM: [Yes / No / Unsure / "not provided"]; Session Replay: [Yes / No / Unsure / "not provided"]
```

After producing the brief, hand off to `context-framing`:

> "Brief complete. Type **approve** to proceed with Phase 0, or tell me anything you want to adjust."

On approval, context-framing takes over, reads the brief using the brief-complete fast path (if all MUSTs are filled), and creates the engagement folder.
