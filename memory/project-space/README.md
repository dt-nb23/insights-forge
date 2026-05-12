# Project Space — Live Investigation Memory

This folder holds the **live state of the current investigation**. Files here are read and written every session. The agent treats this folder as its working memory for the active engagement.

## What lives here

- `current-context.md` — problem statement, scope, stakeholders, current phase, and open questions.
- `issue-tree.md` — the MECE issue tree under active development.
- `hypotheses.md` — the ranked hypothesis table with ICE scores and status.
- `signals-map.md` — SLI/SLO → UX outcome → business KPI mapping for the active investigation.
- `action-plan.md` — investigation actions, recommended actions, decision asks, risks.
- `decisions-log.md` — append-only record of every gate decision (approve / redirect / iterate).

## Rules

- The agent **reads and writes freely** in this folder. Every phase deliverable lands here.
- Files in this folder represent the **current investigation only**. They are not historical.
- **When a new investigation starts**, the user instructs the agent to:
  1. Move the current contents to `memory/long-term/past-investigations/YYYY-MM-DD-<short-name>/` with a date stamp.
  2. Reset the files in this folder back to their template state.
  3. Begin Phase 0 with a fresh problem statement.

## Why this separation matters

Mixing live investigation state with durable knowledge leads to two failure modes: (1) stale assumptions from a previous engagement bleeding into a new one, and (2) hard-won lessons being lost when the workspace is reset. The two-folder split solves both — `project-space/` is the scratch pad; `long-term/` is the archive and the playbook.
