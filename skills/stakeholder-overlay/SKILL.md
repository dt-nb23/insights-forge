---
name: stakeholder-overlay
description: Captures a named client leader as a stakeholder overlay in the active client's workspace at memory/clients/<client-name>/stakeholder-overlays.md. Run when the consultant names a specific individual (e.g., "Sarah Chen, VP of Engineering") and no overlay exists for that person. Builds on the parent role archetype from the shared library, captures what is unique to this leader, and makes Phase 3 deliverables specific rather than generic. Requires explicit user approval before writing. Never writes named individuals to memory/long-term/stakeholder-profiles.md.
---

# Stakeholder Overlay

## When to use

- The consultant names a specific client leader during Phase 0 (Q7) and no overlay for that person exists in the active client's workspace.
- A Phase 3 deliverable needs to be tailored to a specific named leader not yet profiled.
- The user says "add this stakeholder" or "create a profile for [name]."

**This skill writes to `memory/clients/<active-client-name>/stakeholder-overlays.md` — the client's isolated workspace. It never writes named individuals to `memory/long-term/stakeholder-profiles.md`, which contains only generic title-type overlays. Always gate the write with the binary approval pattern — write only on an explicit yes/approve, never on "looks good" or silence.**

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session. The agent fixes it once — when Phase 0 (`context-framing`) creates the engagement folder, or when a paused/active engagement is resumed — and holds it in working context for the rest of the session. There is **no shared pointer file** to read; nothing depends on a global "active" file a second concurrent session could overwrite.
2. If no engagement is established yet (a fresh session picking up earlier work), resolve it with the resume procedure in `skills/investigation-reset/SKILL.md`: scan `memory/clients/*/engagements/*/current-context.md` for a `state:` of `active` or `paused`, present the matches, and have the user pick one. If none, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = the established/selected path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`)
4. CLIENT_NAME = the path segment between `memory/clients/` and `/engagements/`
5. Phase file reads use `<ENGAGEMENT_PATH>/<file>`. Client-root files use `memory/clients/<CLIENT_NAME>/<file>`.

Then read these files:

- `memory/long-term/stakeholder-profiles.md` — to identify the parent role archetype (generic archetypes only — no named people here).
- `memory/clients/<CLIENT_NAME>/stakeholder-overlays.md` — to check whether an overlay already exists for this person.
- `<ENGAGEMENT_PATH>/current-context.md` — for the client name, vertical, and what the consultant has already shared about this person.

## Procedure

### Step 1 — Identify the parent archetype

From what the consultant has already shared (title, role, what they care about), match the leader to one of the eight role archetypes in `stakeholder-profiles.md`:

1. Executive Sponsor
2. Product Owner
3. SRE / Reliability Engineer
4. IT Operations Manager
5. Application Developer
6. Platform / DevOps Engineer
7. Security / Compliance Officer
8. Data / Analytics Lead

If the title suggests a different archetype (e.g., a "Director of Observability" probably sits closest to SRE / Reliability Engineer), name the closest match and note the gap.

### Step 2 — Check for an existing overlay

Search `memory/clients/<CLIENT_NAME>/stakeholder-overlays.md` for any overlay that matches this person's name or title. If the file does not exist yet, it will be created in Step 5. If a matching overlay exists:
- Read it to the consultant and ask whether it needs updating.
- If updating, proceed to Step 3 with the delta fields only.
- If current, confirm and stop.

### Step 3 — Ask the overlay questions

Ask the consultant these questions, one at a time. Skip any already answered in Q7 or earlier in the conversation.

1. **Full name and title:** "What is their full name and exact title?"
2. **Organization / company:** (usually already known from current-context.md — confirm rather than re-ask)
3. **What they care about most:** "In their own words or yours — what does this person care about most? What keeps them up at night?"
4. **What they consistently ignore or deprioritize:** "What do they tend to tune out or push back on?"
5. **How they prefer information:** "Do they prefer details and evidence, or summary and decision? Do they want the 'so what' first, or do they want to follow the reasoning?"
6. **Their KPI vocabulary:** "What metrics do they actually talk about — not the ones that should matter, but the ones that come up in their conversations? Examples: MTTR, conversion rate, cost per transaction, uptime SLA, deployment frequency."
7. **Known background or technical depth:** "Do they have a technical background? Are they hands-on or removed from the day-to-day?"
8. **Any known constraints or sensitivities:** "Is there anything sensitive in this relationship — vendor fatigue, a past incident that shapes their perception, a budget pressure, or a previous commitment that limits the conversation?"
9. **Prior Dynatrace experience:** "How long have they been working with Dynatrace, and what's their general impression?"

Stop when you have enough to distinguish this person from the generic archetype. Not all nine questions need answers.

### Step 4 — Draft the overlay

Write a draft overlay section in the format used by existing named-leader overlays in `stakeholder-profiles.md`:

```markdown
### [Full Name] — [Title] at [Company]
Parent archetype: [archetype name]
Vertical: [from current-context.md]

**What they care about:** [2–3 sentences from Q3 answer]
**What they ignore:** [1–2 sentences from Q4 answer]
**Information preference:** [summary / detail / decision-first — from Q5]
**KPI vocabulary:** [list from Q6]
**Technical depth:** [shallow / moderate / deep — from Q7]
**Sensitivities:** [from Q8, or "none noted"]
**Dynatrace familiarity:** [from Q9, or "unknown"]

**Phase 3 notes:** [1–2 sentences on how to frame a deliverable for this person — derived, not asked]
```

Present the draft and gate the write with the binary pattern: **"Proposed addition to `memory/clients/<CLIENT_NAME>/stakeholder-overlays.md`: overlay for [name], [title]. Approve?"** Write **only** on an explicit yes/approve/equivalent — never on "looks good" or silence.

### Step 5 — Write to client workspace (on approval only)

Only after the consultant approves the draft:

- If `memory/clients/<CLIENT_NAME>/stakeholder-overlays.md` does not exist, copy it from `memory/clients/_template/stakeholder-overlays.md` first.
- Append the overlay to `memory/clients/<CLIENT_NAME>/stakeholder-overlays.md`.
- Confirm: "Overlay for [name] saved to this client's workspace. Phase 3 deliverables for this engagement will read against it. This profile is not visible in other clients' sessions."

If the consultant declines or wants to revise, update the draft and re-present before writing.

## Output

A named-leader overlay appended to `memory/clients/<CLIENT_NAME>/stakeholder-overlays.md`, covering the fields above. This file is isolated to this client's workspace — it is never written to `memory/long-term/stakeholder-profiles.md`.

## Common pitfalls

- **Writing without approval.** This skill modifies durable, cross-engagement client memory. Never write until the consultant answers the binary gate with an explicit "yes," "approve," or equivalent. "Looks good" and silence are **not** approval — re-ask the gate.
- **Over-asking.** If the consultant has already described this person in detail during Q7, use what was said and ask only for the gaps. Re-asking questions already answered wastes time.
- **Generic Phase 3 notes.** The "Phase 3 notes" field is the most valuable field in the overlay — it should say something specific about how to frame a deliverable for this person, not just repeat what they care about. Derive it from the combination of Information preference, KPI vocabulary, and Sensitivities.
- **Skipping the archetype match.** The overlay layers on top of an archetype. If the archetype is wrong, the overlay inherits the wrong defaults. Always name the parent archetype explicitly.
