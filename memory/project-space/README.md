# Project Space — Active Client's Working Directory

This folder holds the **live investigation files for the currently active client**. Think of it as "you are here" — while an engagement is open, the agent works directly in this folder. The `active-engagement.md` file names which client this is.

## What lives here

- `active-engagement.md` — identifies the active client (maps to `memory/clients/<name>/`).
- `current-context.md` — problem statement, scope, stakeholders, current phase, and open questions.
- `issue-tree.md` — the MECE issue tree under active development.
- `hypotheses.md` — the ranked hypothesis table with ICE scores and status.
- `signals-map.md` — SLI/SLO → UX outcome → business KPI mapping for the active investigation.
- `action-plan.md` — investigation actions, recommended actions, decision asks, risks.
- `decisions-log.md` — append-only record of every gate decision (approve / redirect / iterate).

## Two-tier memory architecture

```
memory/
├── long-term/          ← Root library: Dynatrace knowledge, frameworks, brand, generic archetypes.
│                          Universal. Never contains client data. Read on every session.
│
├── clients/            ← Per-client workspaces. Strictly isolated.
│   └── <client-name>/
│       ├── environment.md          (DT environment facts for this client)
│       ├── stakeholder-overlays.md (named leaders at this client)
│       ├── project-space/          (investigation files when paused)
│       └── past-investigations/    (archived investigations for this client only)
│
└── project-space/      ← "You are here." The active client's working files.
    └── active-engagement.md names which client is active.
```

## Context isolation rule

The agent reads `memory/long-term/` (universal) + `memory/clients/<active-client-name>/` (this client only). It never reads another client's folder. Client data does not cross client boundaries.

## State transitions

Use `skills/investigation-reset/SKILL.md` to:
- **Pause** — move files to `memory/clients/<client-name>/project-space/`, clear this folder, start a new engagement.
- **Archive** — capture lessons-learned, move files to `memory/clients/<client-name>/past-investigations/<date-name>/`, reset.
- **Resume** — copy files from `memory/clients/<client-name>/project-space/` back here, set `active-engagement.md`.
