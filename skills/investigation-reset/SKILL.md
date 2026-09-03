---
name: investigation-reset
description: Archives or pauses the current investigation. Archive captures lessons-learned and updates the client's engagement history. Pause just sets `state: paused` in the engagement's own `current-context.md` front-matter — there is no session pointer, and no files move. Resume sets it back to `active`. Use when the user says "archive this investigation", "pause this", "resume [engagement]", or "start a new client engagement."
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

The write target is `<ENGAGEMENT_PATH>/lessons-learned.md`, and its contract is the template at `memory/clients/_template/engagements/lessons-learned.md`. Phase 0's cross-client readback filters on the template's front-matter tags and surfaces its "Cross-engagement hook" line, so the headings and front-matter field names below must match the template exactly — a lessons file written with other headings or missing tags is invisible to retrieval. If the engagement folder has no `lessons-learned.md` yet, copy the template in first.

Ask the user four questions, one at a time. Do not batch them. Write each answer under the template heading shown:

| # | Question | Template heading |
|---|---|---|
| 1 | "What did we get right in this engagement that's worth repeating?" | `## What we got right` |
| 2 | "What wasted time or misdirected the team?" | `## What we got wrong` |
| 3 | "What did we learn that we didn't know going in — new signal patterns, new failure modes, or new business linkages?" | `## What we discovered that we did not know before` |
| 4 | "Are there any updates worth promoting to the long-term library — a playbook file in `memory/long-term/playbooks/`, `domain-knowledge.md`, or a profile file in `memory/long-term/profiles/`? If yes, summarize what to add." | `## What should change in the playbook` |

If the user declines to answer a question ("skip", "none", "n/a"), record that explicitly under its heading — do not leave the section blank.

**After Q3, before Q4 — draft the Cross-engagement hook.** Draft one sentence combining the core problem, the key lesson, and the vertical/capability context that makes the lesson useful elsewhere (e.g., *"Retail RUM-adoption engagement: Davis AI grouping drift understated incident volume — check grouping config before trusting MTTR baselines."*). Confirm the sentence with the user, then write it under the template's `## Cross-engagement hook` heading. Never leave the hook blank — this one line is what Phase 0 retrieval surfaces to future engagements.

**Front-matter.** Write the file with the template's full front-matter block, filled as follows:

- `vertical:` — the value of the Vertical row in `<ENGAGEMENT_PATH>/current-context.md`.
- `problem-shape:` — a slug derived from the engagement slug (e.g., `2026-06-18-api-latency` → `api-latency`).
- `capabilities:` — the subset of the Active capabilities list in `current-context.md` that the four answers actually touch.
- `state: complete` — set only once all four answers are recorded (the template ships `state: draft`; a partially captured file stays `draft`).
- `archived:` — today's date, `YYYY-MM-DD`.
- `engagement:` — the engagement folder name (e.g., `2026-06-18-api-latency`).

Propose `problem-shape` and `capabilities` and confirm both with the user in one line before writing — e.g., "Tagging this `problem-shape: api-latency`, `capabilities: [apm, davis]` — correct?" — since these two tags drive Phase 0 cross-client matching.

### Step 3 — Update the client's engagement history

Append one row to the investigation history table in `memory/clients/<CLIENT_NAME>/README.md` with:
- **Date**: YYYY-MM-DD (today)
- **Engagement folder**: the ENGAGEMENT_PATH value (e.g., `engagements/2026-06-18-api-latency/`)
- **Problem one-liner**: the consulting objective (reframed), shortened to one sentence
- **Outcome**: the terminal hypothesis status from `<ENGAGEMENT_PATH>/hypotheses.md` (e.g., "3 confirmed, 2 ruled out, 1 open")
- **Status**: complete / incomplete
- **Key lesson**: one sentence from the "What we got right" or "What we discovered that we did not know before" answers in `lessons-learned.md` — the Cross-engagement hook line is usually the right candidate

### Step 4 — Execute approved long-term memory promotions

Review the "What should change in the playbook" answers from Step 2.

For each proposed update, present it to the user and ask for explicit approval before writing. Example: "Proposed addition to the `slo-burn` playbook in `memory/long-term/playbooks/`: [summary]. Approve?" Write only on approval. Tell the user which file was updated and what was added. (A new playbook or profile also gets an index row in its hub file.)

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
3. In the selected engagement's `current-context.md`, set the status front-matter `state: active` and update `last-touched:` to today. Hold its ENGAGEMENT_PATH in working context for the rest of the session. There is no global pointer to update. Make this the **first write** into the resumed client's folder: the client-isolation hook re-locks the session to that client automatically on the first write into its folder, so this `state: active` / `last-touched:` update should precede any other write there.
4. Read `<ENGAGEMENT_PATH>/decisions-log.md` to remind the user where the investigation was last paused.
5. Present: "Engagement `<dated-slug>` for [client] resumed at Phase [N]. [Last gate decision from decisions-log.md.] Ready to continue."

No files are copied — the engagement folder was always in the client workspace.

**Backfill check.** When resuming or archiving work for a client whose archived engagements hold `lessons-learned.md` files with missing front-matter or the old headings ("What worked" / "What to avoid" / "New knowledge"), offer to retag and re-head them in place to the template contract (`memory/clients/_template/engagements/lessons-learned.md`) so Phase 0 retrieval can find them. The content stays as written — only the front-matter and headings change.

---

## Switching clients in the same session

After a pause or archive, the client-isolation hook (`tools/client-isolation-hook.sh`) may still hold the session locked to the previous client. To switch:

1. Present the unlock command for the user's approval: `rm .claude/session-clients/<session-id>`. The session id is injected into context at session start; the permission prompt on the `rm` is the human gate for the switch.
2. Once the lock file is removed, the next touch of a client folder re-locks the session to that client automatically — no manual re-lock step is needed.

---

## Common pitfalls

- **Skipping lessons-learned.** This is the highest-value step. Never skip it — if the user declines to answer, record "declined" explicitly so the archive is honest about what was captured.
- **Writing the old lessons headings.** Phase 0 cross-client retrieval matches the template's headings and front-matter tags exactly — writing "What worked" / "What to avoid" / "New knowledge" (the pre-template headings) breaks that retrieval and strands the lesson. Use the Step 2 question → heading table verbatim.
- **Skipping the Cross-engagement hook draft.** The hook line is the only content Phase 0 surfaces cross-client; a lessons file without it is effectively unretrievable. Draft and confirm it after Q3 — never leave the heading blank.
- **Archiving without confirming phase completion.** If Phase 3 was never approved, the investigation is incomplete. Label it so.
- **Promoting long-term memory without approval.** Every write to the long-term library — the hub files, any file in `memory/long-term/playbooks/` or `memory/long-term/profiles/`, or `domain-knowledge.md` — requires explicit user confirmation per the Memory model rules in `CLAUDE.md`.
- **Looking for a global pointer or `memory/project-space/`.** There is none — it was removed. An engagement's state lives in its own `current-context.md` front-matter (`state:`), and its phase files live in the engagement folder. If you are looking for `current-context.md`, it is at `<ENGAGEMENT_PATH>/current-context.md`.
