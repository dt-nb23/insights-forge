---
name: investigation-reset
description: Archives or pauses the current investigation. Archive captures lessons-learned and updates the client's engagement history. Pause just clears the session pointer — no files move. Resume restores the pointer. Use when the user says "archive this investigation", "pause this", "resume [engagement]", or "start a new client engagement."
---

# Investigation Reset

## When to use

- The user explicitly says "archive this investigation," "reset the workspace," or "start a new client engagement."
- The user wants to begin work on a second client while the current investigation is in progress ("pause" mode).
- A completed engagement needs its lessons-learned captured before the context is lost.

**Do not use mid-investigation** unless the user explicitly calls for it.

## Two modes

| Mode | What happens | Where files go |
|---|---|---|
| **Archive (complete)** | Investigation is done; capture lessons and update the engagement history | Files stay in their engagement folder — nothing moves. The client README is updated with the outcome row. |
| **Pause** | Investigation is in progress but needs to yield to another client | Files stay in their engagement folder — nothing moves. The engagement's `current-context.md` is marked `state: paused`. |

Ask the user which mode they want before proceeding.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` for the engagement being archived or paused. If this session is actively working an engagement, that is the one — use the path held in working context. If the user named a different engagement ("archive the Acme checkout one") or no engagement is held, scan `memory/clients/*/engagements/*/current-context.md`, match on the front-matter `client`/`slug`, and confirm the target with the user.
2. If no engagement can be resolved, stop: "No engagement found — nothing to archive or pause."
3. ENGAGEMENT_PATH = the resolved path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`)
4. CLIENT_NAME = the path segment between `memory/clients/` and `/engagements/`
5. Phase file reads use `<ENGAGEMENT_PATH>/<file>`. Client-root files use `memory/clients/<CLIENT_NAME>/<file>`.

Then read:

- `<ENGAGEMENT_PATH>/current-context.md` — to confirm the engagement name and consulting objective.
- `<ENGAGEMENT_PATH>/decisions-log.md` — to confirm which phase the investigation reached.
- `memory/clients/<CLIENT_NAME>/README.md` — to append the new investigation row (archive mode only).

---

## Procedure — Archive mode

### Step 1 — Confirm closure

Read `<ENGAGEMENT_PATH>/decisions-log.md`. Look for a Phase 3 approval entry.

- If Phase 3 was approved → proceed normally.
- If the investigation did not reach Phase 3 → inform the user of the last phase completed and ask: "This investigation ended at Phase [N]. Archive as incomplete?" If yes, label it `status: incomplete` in Step 3. If no, stop and resume the investigation from the last gate.

### Step 2 — Capture lessons-learned

Ask the user four questions, one at a time. Do not batch them.

1. "What did we get right in this engagement that's worth repeating?"
2. "What wasted time or misdirected the team?"
3. "What did we learn that we didn't know going in — new signal patterns, new failure modes, or new business linkages?"
4. "Are there any updates worth promoting to `dynatrace-playbooks.md`, `domain-knowledge.md`, or `stakeholder-profiles.md`? If yes, summarize what to add."

Write the four answers to `<ENGAGEMENT_PATH>/lessons-learned.md` under these headings:
- What worked
- What to avoid
- New knowledge
- Proposed long-term memory updates (list or "none")

If the user declines to answer a question ("skip", "none", "n/a"), record that explicitly — do not leave the section blank.

### Step 3 — Update the client's engagement history

Append one row to the investigation history table in `memory/clients/<CLIENT_NAME>/README.md` with:
- **Date**: YYYY-MM-DD (today)
- **Engagement folder**: the ENGAGEMENT_PATH value (e.g., `engagements/2026-06-18-api-latency/`)
- **Problem one-liner**: the consulting objective (reframed), shortened to one sentence
- **Outcome**: the terminal hypothesis status from `<ENGAGEMENT_PATH>/hypotheses.md` (e.g., "3 confirmed, 2 ruled out, 1 open")
- **Status**: complete / incomplete
- **Key lesson**: one sentence from the "What worked" or "New knowledge" answers in `lessons-learned.md`

### Step 4 — Execute approved long-term memory promotions

Review the "Proposed long-term memory updates" from Step 2.

For each proposed update, present it to the user and ask for explicit approval before writing. Example: "Proposed addition to `dynatrace-playbooks.md`: [summary]. Approve?" Write only on approval. Tell the user which file was updated and what was added.

If no updates were proposed, skip this step.

### Step 5 — Mark the engagement complete

In `<ENGAGEMENT_PATH>/current-context.md`, set the status front-matter `state: complete` and update `last-touched:` to today. That is the only state change — there is no global pointer to clear. The session simply stops treating this engagement as active.

No files are moved or deleted — the engagement folder at ENGAGEMENT_PATH remains intact with all its files.

### Step 6 — Confirm completion

Present a summary to the user:

> "Investigation at `<ENGAGEMENT_PATH>` archived.
> Lessons-learned captured at `<ENGAGEMENT_PATH>/lessons-learned.md`.
> Engagement history updated in `memory/clients/<CLIENT_NAME>/README.md`.
> Long-term memory updates: [list, or "none"].
> Engagement marked `complete`.
> To start a new engagement, describe the problem you're trying to solve."

---

## Procedure — Pause mode

Use this when the user wants to set aside the current engagement to work on a different client, without closing the investigation.

### Step 1 — Confirm pause

Confirm the engagement to be paused (from `<ENGAGEMENT_PATH>/current-context.md`). In that file's status front-matter, set `state: paused` and update `last-touched:` to today.

No files are moved or deleted, and there is no global pointer to update. Because state lives in the engagement's own front-matter, any number of engagements can be paused at once — pausing one never disturbs another.

### Step 2 — Confirm

> "Engagement paused at `<ENGAGEMENT_PATH>` (marked `state: paused`).
> To resume it later, say 'resume [engagement name].' To start a new one, describe the problem you're trying to solve."

---

## Resuming a paused engagement

When the user says "resume [engagement name]" or a fresh session needs to pick up prior work:

1. Scan `memory/clients/*/engagements/*/current-context.md` for status front-matter with `state: active` or `state: paused`. Present the matches (client · slug · phase · last-touched). If the user named a specific engagement, match it directly.
2. User selects which engagement to resume.
3. In the selected engagement's `current-context.md`, set the status front-matter `state: active` and update `last-touched:` to today. Hold its ENGAGEMENT_PATH in working context for the rest of the session. There is no global pointer to update.
4. Read `<ENGAGEMENT_PATH>/decisions-log.md` to remind the user where the investigation was last paused.
5. Present: "Engagement `<dated-slug>` for [client] resumed at Phase [N]. [Last gate decision from decisions-log.md.] Ready to continue."

No files are copied — the engagement folder was always in the client workspace.

---

## Common pitfalls

- **Skipping lessons-learned.** This is the highest-value step. Never skip it — if the user declines to answer, record "declined" explicitly so the archive is honest about what was captured.
- **Archiving without confirming phase completion.** If Phase 3 was never approved, the investigation is incomplete. Label it so.
- **Promoting long-term memory without approval.** Every write to `dynatrace-playbooks.md`, `domain-knowledge.md`, or `stakeholder-profiles.md` requires explicit user confirmation per the Memory model rules in `CLAUDE.md`.
- **Looking for a global pointer or `memory/project-space/`.** There is none — it was removed. An engagement's state lives in its own `current-context.md` front-matter (`state:`), and its phase files live in the engagement folder. If you are looking for `current-context.md`, it is at `<ENGAGEMENT_PATH>/current-context.md`.
