---
name: value-highlight
description: Produces a backward-looking "Dynatrace value delivered" brief for renewal and QBR engagements. Reads past investigation archives for the same client and synthesizes confirmed findings, resolved hypotheses, and actions taken into a written summary that a CSM can use as the value-surfacing section of a QBR deck. Requires at least one archived investigation for the target client. Medium priority — build value after investigation-reset has run 2+ times for a client.
---

# Engagement Value Highlight

## When to use

- The engagement trigger (Q9) is a QBR, renewal, or expansion conversation.
- The consultant asks for "what Dynatrace found for this client" or "a value summary" for the period.
- Phase 3 deliverable needs a backward-looking "here's what we surfaced" section before the current-engagement findings.

**Pre-requisite:** At least one prior completed investigation must exist in `memory/long-term/past-investigations/<date-name>/` for this client. If none exist, inform the consultant and offer to run Phase 0 → Phase 3 for the current engagement, then use this skill on the next renewal cycle.

## Inputs

Read before starting:

- `memory/project-space/active-engagement.md` — to get the active client name (all prior-engagement reads scope to this client's folder only).
- `memory/clients/<active-client-name>/README.md` — the engagement history index for this client.
- `memory/clients/<active-client-name>/past-investigations/<date-name>/hypotheses.md` — confirmed, ruled-out, and open hypotheses with ICE scores.
- `memory/clients/<active-client-name>/past-investigations/<date-name>/action-plan.md` — recommended actions and any stated outcomes.
- `memory/clients/<active-client-name>/past-investigations/<date-name>/current-context.md` — consulting objective and engagement trigger.
- `memory/clients/<active-client-name>/past-investigations/<date-name>/lessons-learned.md` — "What worked / new knowledge."
- `memory/clients/<active-client-name>/environment.md` — for environment context (if the file exists).
- `memory/project-space/current-context.md` — for the current engagement's scope and named stakeholder.

## Procedure

### Step 1 — Find prior engagements for this client

Read `memory/project-space/active-engagement.md` to get the active client name. Then read `memory/clients/<active-client-name>/README.md` and find the engagement history table.

List the prior engagements to the consultant:

> "I found [N] prior engagement(s) for [client]:
> - [Date] — [Problem one-liner] — [status: complete / incomplete]
> - [Date] — [Problem one-liner] — [status]"

Ask the consultant: "Which engagements should be included in the value summary? (Default: all completed ones.)"

If `memory/clients/<active-client-name>/past-investigations/` is empty or the folder does not exist, inform the consultant and stop:

> "No prior completed engagements found for [client] in their workspace archive. This skill requires at least one archived investigation. Once this engagement completes and is archived, the value summary will be available for the next renewal cycle."

### Step 2 — Extract value evidence

For each selected prior engagement, read the archive folder and extract:

**From `hypotheses.md`:**
- Confirmed hypotheses: what was found, and what was the business impact (from signals-map or action-plan).
- High-ICE open hypotheses that were surfaced as important even if not yet validated.

**From `action-plan.md`:**
- Recommended actions: what the team was advised to do. If any are measurably completed, note that.
- Decision asks: what leadership was asked to decide.

**From `lessons-learned.md`:**
- New knowledge entries that are client-relevant (new signal patterns found in this environment, failure modes unique to this vertical).

**From `current-context.md`:**
- The consulting objective for that engagement — what was the consultant trying to accomplish.

Build a raw evidence list organized by engagement date. Do not write prose yet — just collect the facts.

### Step 3 — Identify the value narrative thread

Look across the evidence for 2–4 themes that make a compelling value story:

- **Discovery themes:** "We surfaced that your [system] had a problem you didn't know about."
- **Improvement themes:** "These actions we recommended have reduced [metric] by [X]." (Only if the action-plan included measurable targets and the lessons-learned confirms outcome.)
- **Risk mitigation themes:** "We identified and helped resolve a risk to [KPI] before it became a customer-visible incident."
- **Strategic insight themes:** "Findings from the [engagement] shaped how you approached [initiative]."
- **Instrumentation progress themes:** "We identified capability gaps in [area] — since then, [monitoring / SLOs / RUM] have been added."

If the evidence does not support a compelling theme, name what is missing honestly: "We have confirmed findings but no evidence of outcomes yet — this brief will be forward-leaning rather than backward-looking."

### Step 4 — Draft the value brief

Produce a one-to-two-page written brief in this structure:

---

**[Client Name] — Dynatrace Value Summary**
*Prepared for [stakeholder name and title, from current-context.md]*
*Period: [earliest engagement date] – [today's date]*

**Summary** (2–3 sentences)
What Dynatrace surfaced for [client] over this period, and what it meant for the business.

**Key findings** (3–5 bullets, most impactful first)
Each bullet: what was found, in what system or flow, and what business risk or opportunity it represented.
- *Source: [engagement date and consulting objective]*

**Actions and outcomes** (table or bullets)
| Recommended action | Owner | Status | Measured outcome (if known) |
|---|---|---|---|

If no actions have known outcomes, state: "Outcome data not yet available — [action] was recommended on [date]."

**Capability development** (if relevant)
Instrumentation gaps identified and closed since [date]. New signals now available that were not before.

**Remaining opportunity** (bridge to current engagement)
1–2 sentences connecting the value summary to the current engagement's scope: "Building on these findings, this engagement focuses on [current consulting objective]."

---

### Step 5 — Present for approval

Present the brief to the consultant. Ask: "Does this accurately represent the value delivered? Any corrections, or findings the customer would recognize that I've missed?"

Revise based on feedback. Do not finalize until the consultant approves.

### Step 6 — Output

Write the approved brief to `memory/project-space/value-brief-YYYY-MM-DD.md` for inclusion in the Phase 3 one-pager or deck.

Inform the consultant: "Value brief saved. When we produce the Phase 3 one-pager or deck, include this as the 'Value delivered' section before the current-engagement findings."

## Common pitfalls

- **Inventing outcomes.** Only state outcomes that appear in `action-plan.md` targets AND are confirmed in `lessons-learned.md` or acknowledged by the consultant. Do not assume an action was completed just because it was recommended.
- **Mixing up clients.** If the archive contains engagements for similar-sounding clients, confirm the customer name precisely before including evidence.
- **Leaving out incomplete engagements.** An incomplete investigation may still contain confirmed findings worth highlighting. Include incomplete archives but label the source as "partial investigation."
- **Making it too long.** Two pages maximum. If the evidence doesn't fit, cut the lowest-impact items. The brief feeds a QBR deck — the audience has 2 minutes for the "value delivered" section, not 10.
- **Running this skill before any engagements are archived.** If there is nothing in `past-investigations/` for this client, there is no value to summarize. Stop and say so — do not fabricate a history.
