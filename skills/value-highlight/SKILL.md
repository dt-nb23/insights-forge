---
name: value-highlight
description: Produces a backward-looking "Dynatrace value delivered" brief for renewal and QBR engagements. Reads past investigation archives for the same client and synthesizes confirmed findings, resolved hypotheses, and actions taken into a written summary that a CSM can use as the value-surfacing section of a QBR deck. Requires at least one archived investigation for the target client. Medium priority — build value after investigation-reset has run 2+ times for a client.
---

# Engagement Value Highlight

## When to use

- The engagement trigger (Q9) is a QBR, renewal, or expansion conversation.
- The consultant asks for "what Dynatrace found for this client" or "a value summary" for the period.
- Phase 3 deliverable needs a backward-looking "here's what we surfaced" section before the current-engagement findings.

**Pre-requisite:** At least one prior completed engagement must exist in `memory/clients/<client-name>/engagements/` for this client **AND** that engagement must contain at least one confirmed finding or verifiable outcome (an action with a measured result, a confirmed hypothesis, or a documented resolved risk). A thin engagement — open hypotheses only, no confirmed findings, no actions with verifiable outcomes — does **not** qualify; a value brief built from it would be fabricated confidence. If the prerequisite is not met, inform the consultant and offer to run Phase 0 → Phase 3 for the current engagement, then use this skill on the next renewal cycle once verifiable outcomes exist.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session. The agent fixes it once — when Phase 0 (`context-framing`) creates the engagement folder, or when a paused/active engagement is resumed — and holds it in working context for the rest of the session. There is **no shared pointer file** to read; nothing depends on a global "active" file a second concurrent session could overwrite.
2. If no engagement is established yet (a fresh session picking up earlier work), resolve it with the resume procedure in `skills/investigation-reset/SKILL.md`: scan `memory/clients/*/engagements/*/current-context.md` for a `state:` of `active` or `paused`, present the matches, and have the user pick one. If none, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = the established/selected path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`)
4. CLIENT_NAME = the path segment between `memory/clients/` and `/engagements/`
5. Phase file reads use `<ENGAGEMENT_PATH>/<file>`. Client-root files use `memory/clients/<CLIENT_NAME>/<file>`.

Then read these files:

- `memory/clients/<CLIENT_NAME>/README.md` — the engagement history index for this client (contains the list of engagement folders and their status).
- `memory/clients/<CLIENT_NAME>/engagements/<dated-slug>/hypotheses.md` — confirmed, ruled-out, and open hypotheses with ICE scores (for each selected prior engagement).
- `memory/clients/<CLIENT_NAME>/engagements/<dated-slug>/action-plan.md` — recommended actions and any stated outcomes.
- `memory/clients/<CLIENT_NAME>/engagements/<dated-slug>/current-context.md` — consulting objective and engagement trigger.
- `memory/clients/<CLIENT_NAME>/engagements/<dated-slug>/lessons-learned.md` — "What worked / new knowledge."
- `memory/clients/<CLIENT_NAME>/environment.md` — for environment context (if the file exists).
- `memory/clients/<CLIENT_NAME>/contract.md` — for commercial/consumption context (DPS commit, renewal date, on-demand burn, commercial owner), if the file exists. Anchors the renewal/QBR framing in the client's actual commercial posture; if absent or fields are "unknown", say so rather than inventing numbers.
- `<ENGAGEMENT_PATH>/current-context.md` — for the current engagement's scope, named stakeholder, and **Out-of-scope exclusions**. The brief never credits, proposes, or builds its "Remaining opportunity" bridge on an excluded capability, even if a prior engagement used it — a value story that leans on something the customer has ruled out undermines the renewal conversation it is meant to support.

## Procedure

### Step 1 — Find prior engagements for this client

The engagement path and CLIENT_NAME were resolved in the Inputs step. Read `memory/clients/<CLIENT_NAME>/README.md` and find the engagement history table.

List the prior engagements to the consultant:

> "I found [N] prior engagement(s) for [client]:
> - [Folder path] — [Problem one-liner] — [status: complete / incomplete]
> - [Folder path] — [Problem one-liner] — [status]"

Ask the consultant: "Which engagements should be included in the value summary? (Default: all completed ones.)"

If `memory/clients/<CLIENT_NAME>/engagements/` is empty or contains only the current active engagement, inform the consultant and stop:

> "No prior completed engagements found for [client] in their workspace. This skill requires at least one archived investigation. Once this engagement completes and is archived, the value summary will be available for the next renewal cycle."

If prior engagements exist but none clears the verifiable-outcome bar (after Step 2's verification), stop and say so rather than padding a brief:

> "I found [N] prior engagement(s) for [client], but none has a confirmed finding or verifiable outcome I can cite against a dashboard, ticket, or log. A value brief built from open hypotheses alone would overstate what we delivered. Recommend we run the current engagement to a confirmed outcome first, then build the brief next cycle."

### Step 2 — Extract value evidence

For each selected prior engagement, read the archive folder and extract:

**From `hypotheses.md`:**
- Confirmed hypotheses: what was found, and what was the business impact (from signals-map or action-plan).
- High-ICE open hypotheses that were surfaced as important even if not yet validated.

**From `action-plan.md`:**
- Recommended actions: what the team was advised to do. If any are claimed completed, mark them **unverified** — do not treat the claim as fact yet (see the evidence-verification gate below).
- Decision asks: what leadership was asked to decide.

**Evidence-verification gate (applies to every "completed" or claimed outcome):**

A recommended action being *in the plan* is not evidence it was *done*, and a confirmed hypothesis is not evidence the impact *moved*. Before any outcome is cited in the brief, it must be confirmed against a concrete source:

- A dashboard or metric showing the before/after movement,
- A ticket (incident, change, or work item) recording the action as completed, or
- A log / configuration record demonstrating the change is live.

For each claimed outcome, record the verifying source alongside it. If the consultant asserts an outcome verbally, ask which dashboard, ticket, or log confirms it before citing it. Any outcome that cannot be tied to one of these sources is carried as **"recommended; outcome unverified"** — never as a delivered result. Do not cite an unverifiable outcome as value delivered.

**From `lessons-learned.md`:**
- New knowledge entries that are client-relevant (new signal patterns found in this environment, failure modes unique to this vertical).

**From `current-context.md`:**
- The consulting objective for that engagement — what was the consultant trying to accomplish.

Build a raw evidence list organized by engagement date. Do not write prose yet — just collect the facts.

### Step 3 — Identify the value narrative thread

Look across the evidence for 2–4 themes that make a compelling value story:

- **Discovery themes:** "We surfaced that your [system] had a problem you didn't know about."
- **Improvement themes:** "These actions we recommended have reduced [metric] by [X]." (Only if the action-plan included measurable targets AND the outcome cleared the evidence-verification gate — confirmed against a dashboard, ticket, or log. An unverified outcome cannot anchor an improvement theme.)
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
| Recommended action | Owner | Status | Measured outcome (if known) | Verifying source |
|---|---|---|---|---|

Populate **Verifying source** with the dashboard, ticket, or log that confirms the outcome. A row with a "Measured outcome" but no verifying source is not allowed — downgrade its status to "recommended; outcome unverified" and clear the outcome cell. If no actions have verified outcomes, state: "Outcome data not yet available — [action] was recommended on [date]."

**Capability development** (if relevant)
Instrumentation gaps identified and closed since [date]. New signals now available that were not before.

**Remaining opportunity** (bridge to current engagement)
1–2 sentences connecting the value summary to the current engagement's scope: "Building on these findings, this engagement focuses on [current consulting objective]."

---

### Step 5 — Present for approval

Present the brief and gate finalization with the binary pattern: **"Proposed value brief for [client], covering [N] engagement(s); every cited outcome is tied to a verifying source. Approve?"** Finalize and write **only** on an explicit yes/approve/equivalent — never on "looks good" or silence. If the consultant flags a correction or an unverifiable claim, revise (re-running the evidence-verification gate on any disputed outcome) and re-present.

### Step 6 — Output

Write the approved brief to `<ENGAGEMENT_PATH>/value-brief-YYYY-MM-DD.md` for inclusion in the Phase 3 one-pager or deck.

Inform the consultant: "Value brief saved. When we produce the Phase 3 one-pager or deck, include this as the 'Value delivered' section before the current-engagement findings."

## Common pitfalls

- **Inventing outcomes.** Only state outcomes that clear the evidence-verification gate — confirmed against a dashboard, ticket, or log. A target in `action-plan.md`, a verbal "we shipped that," or a note in `lessons-learned.md` is a claim, not verification: tie it to a source or carry it as "recommended; outcome unverified." Do not assume an action was completed just because it was recommended.
- **Mixing up clients.** If the archive contains engagements for similar-sounding clients, confirm the customer name precisely before including evidence.
- **Leaving out incomplete engagements.** An incomplete investigation may still contain confirmed findings worth highlighting. Include incomplete archives but label the source as "partial investigation."
- **Making it too long.** Two pages maximum. If the evidence doesn't fit, cut the lowest-impact items. The brief feeds a QBR deck — the audience has 2 minutes for the "value delivered" section, not 10.
- **Running this skill before any prior engagement is complete.** If the client has no completed prior engagement in `engagements/` (only the current one, or only thin/open ones), there is no value to summarize. Stop and say so — do not fabricate a history.
