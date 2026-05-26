---
name: investigation-reset
description: Archives the current investigation into long-term memory and resets the project-space to template state. Use when the user says "archive this investigation", "reset the workspace", or "start a new client engagement." Always captures lessons-learned before clearing project-space. Also supports "pause" — moving a live investigation to memory/clients/ without archiving it, to make room for a different active engagement.
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
| **Archive (complete)** | Investigation is done; capture lessons and close it | `memory/long-term/past-investigations/<date-name>/` |
| **Pause** | Investigation is in progress but needs to yield to another client | `memory/clients/<engagement-name>/` |

Ask the user which mode they want before proceeding.

## Inputs

Read before starting:

- `memory/project-space/active-engagement.md` — to get the active client name (sets all target paths).
- `memory/project-space/current-context.md` — to extract the client short-name and confirm the engagement name.
- `memory/project-space/decisions-log.md` — to confirm which phase the investigation reached and whether it was completed.
- `memory/clients/<active-client-name>/README.md` — to append the new investigation row to the client's engagement history (archive mode only).

## Procedure — Archive mode

### Step 1 — Confirm closure

Read `memory/project-space/decisions-log.md`. Look for a Phase 3 approval entry.

- If Phase 3 was approved → proceed normally.
- If the investigation did not reach Phase 3 → inform the user of the last phase completed and ask: "This investigation ended at Phase [N]. Archive as incomplete?" If yes, label it `status: incomplete` in the archive index. If no, stop and resume the investigation from the last gate.

### Step 2 — Capture lessons-learned

Ask the user four questions, one at a time. Do not batch them.

1. "What did we get right in this engagement that's worth repeating?"
2. "What wasted time or misdirected the team?"
3. "What did we learn that we didn't know going in — new signal patterns, new failure modes, or new business linkages?"
4. "Are there any updates worth promoting to `dynatrace-playbooks.md`, `domain-knowledge.md`, or `stakeholder-profiles.md`? If yes, summarize what to add."

Write the four answers to `memory/project-space/lessons-learned.md` under these headings:
- What worked
- What to avoid
- New knowledge
- Proposed long-term memory updates (list or "none")

If the user declines to answer a question ("skip", "none", "n/a"), record that explicitly — do not leave the section blank.

### Step 3 — Determine archive name

Propose: `YYYY-MM-DD-<client-short-name>` derived from `current-context.md` and today's date. Confirm with the user. If they provide a different name, use it.

### Step 4 — Create the archive folder and copy files

Ensure the client folder exists at `memory/clients/<active-client-name>/`. If it does not, create it by copying from `memory/clients/_template/` first.

Create the directory `memory/clients/<active-client-name>/past-investigations/<archive-name>/`.

Copy all of the following from `memory/project-space/` into the archive folder:
- `current-context.md`
- `issue-tree.md`
- `hypotheses.md`
- `signals-map.md`
- `action-plan.md`
- `decisions-log.md`
- `lessons-learned.md` (created in Step 2)
- Any `one-pager-YYYY-MM-DD.md` files

Do not copy `active-engagement.md` — that is workspace state, not investigation state.

### Step 5 — Update the client's engagement index

Append one row to the investigation history table in `memory/clients/<active-client-name>/README.md` with:
- **Date**: YYYY-MM-DD (today)
- **Archive name**: the folder name
- **Customer**: from `current-context.md`
- **Problem one-liner**: the consulting objective (reframed), shortened to one sentence
- **Outcome**: the terminal hypothesis status from `hypotheses.md` (e.g., "3 confirmed, 2 ruled out, 1 open")
- **Status**: complete / incomplete
- **Key lesson**: one sentence from the "What worked" or "New knowledge" answers in `lessons-learned.md`

### Step 6 — Execute approved long-term memory promotions

Review the "Proposed long-term memory updates" from Step 2.

For each proposed update, present it to the user and ask for explicit approval before writing. Example: "Proposed addition to `dynatrace-playbooks.md`: [summary]. Approve?" Write only on approval. Tell the user which file was updated and what was added.

If no updates were proposed, skip this step.

### Step 7 — Reset project-space

Overwrite each file in `memory/project-space/` with its template content (the blank template state). Files to reset:
- `current-context.md`
- `issue-tree.md`
- `hypotheses.md`
- `signals-map.md`
- `action-plan.md`
- `decisions-log.md`

Delete `lessons-learned.md` (it now lives in the archive).

Update `memory/project-space/active-engagement.md` to:
```
active: none
```

### Step 8 — Confirm completion

Present a summary to the user:

> "Investigation `<archive-name>` archived at `memory/long-term/past-investigations/<archive-name>/`.
> Long-term memory updates: [list, or "none"].
> Workspace reset and ready for the next engagement.
> To start a new engagement, describe the problem you're trying to solve."

---

## Procedure — Pause mode

Use this when the user wants to set aside the current engagement to work on a different client, without closing the investigation.

### Step 1 — Confirm pause

Ask the user for a short engagement name for the paused investigation (suggest: `<client-short-name>-<YYYY-MM>` or use what's in `current-context.md`). Confirm.

### Step 2 — Move project-space to client's project-space subfolder

Ensure the client folder exists at `memory/clients/<active-client-name>/`. Read `active-engagement.md` to get the client name.

Create the directory `memory/clients/<active-client-name>/project-space/`.

Move (copy then delete from source) all current files from `memory/project-space/` into `memory/clients/<active-client-name>/project-space/`:
- `current-context.md`
- `issue-tree.md`
- `hypotheses.md`
- `signals-map.md`
- `action-plan.md`
- `decisions-log.md`
- Any `one-pager-YYYY-MM-DD.md` files

### Step 3 — Reset project-space to template

Overwrite project-space files with template content (same as Archive Step 7).

Update `memory/project-space/active-engagement.md` to:
```
active: none
paused: memory/clients/<active-client-name>/project-space/
```

### Step 4 — Confirm

> "Engagement `<engagement-name>` paused at `memory/clients/<active-client-name>/project-space/`.
> Workspace is clear. To resume this engagement later, say 'resume <engagement-name>.' To start a new one, describe the problem you're trying to solve."

---

## Resuming a paused engagement

When the user says "resume [engagement name]" or session start finds folders in `memory/clients/`:

1. Present the list of paused engagements from `memory/clients/` (check each client folder for a `project-space/` subfolder).
2. User selects which to resume.
3. Copy all files from `memory/clients/<client-name>/project-space/` back into `memory/project-space/`.
4. Update `memory/project-space/active-engagement.md`:
   ```
   active: memory/clients/<engagement-name>/
   ```
5. Read `memory/project-space/decisions-log.md` to remind the user where the investigation was last paused.
6. Present: "Engagement `<engagement-name>` resumed at Phase [N]. [Last gate decision from decisions-log.md.] Ready to continue."

---

## Common pitfalls

- **Skipping lessons-learned.** This is the highest-value step. Never skip it — if the user declines to answer, record "declined" explicitly so the archive is honest about what was captured.
- **Archiving without confirming phase completion.** If Phase 3 was never approved, the investigation is incomplete. Label it so.
- **Promoting long-term memory without approval.** Every write to `dynatrace-playbooks.md`, `domain-knowledge.md`, or `stakeholder-profiles.md` requires explicit user confirmation per the Memory model rules in `CLAUDE.md`.
- **Forgetting to reset `active-engagement.md`.** If this file still names an archived engagement, the next session will try to resume something that no longer exists in project-space.
