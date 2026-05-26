# Client Workspaces — Per-Client Isolated Memory

Each subfolder in this directory is a fully isolated workspace for one client. All client-specific data lives here. The universal library at `memory/long-term/` contains **no client data** — only Dynatrace concepts, frameworks, brand, and generic role archetypes.

## Per-client folder structure

```
memory/clients/<client-name>/
├── README.md                    (engagement summary and status)
├── environment.md               (DT environment facts: MZs, SLOs, synthetic monitors, gaps)
├── stakeholder-overlays.md      (named leaders for this client only)
├── project-space/               (active investigation files — mirrored to memory/project-space/ when active)
│   ├── current-context.md
│   ├── issue-tree.md
│   ├── hypotheses.md
│   ├── signals-map.md
│   ├── action-plan.md
│   └── decisions-log.md
└── past-investigations/         (archived investigations for this client only)
    └── YYYY-MM-DD-<description>/
        ├── current-context.md
        ├── issue-tree.md
        ├── hypotheses.md
        ├── signals-map.md
        ├── action-plan.md
        ├── decisions-log.md
        ├── one-pager-YYYY-MM-DD.md  (if produced)
        └── lessons-learned.md
```

## Engagement states

| State | Where the active investigation files live |
|---|---|
| **Active** | `memory/project-space/` (mirrored from this client's folder) |
| **Paused** | `memory/clients/<client-name>/project-space/` |
| **Completed** | `memory/clients/<client-name>/past-investigations/<date-name>/` |

`memory/project-space/active-engagement.md` identifies which client is currently active.

## Context isolation rule

**The agent reads only one client folder per session.** When working on Client X, it reads `memory/long-term/` (universal library) and `memory/clients/X/` (Client X's workspace). It never reads `memory/clients/Y/` or any other client's folder. Client data does not cross client boundaries.

## How to create a new client workspace

Use `skills/investigation-reset/SKILL.md` (which handles pause/archive/resume) or manually create the folder structure above. A client folder is created the first time a Phase 0 engagement is started for that client.

## How to populate client-specific files

- **environment.md** — use `skills/environment-intake/SKILL.md` at the Phase 0 gate.
- **stakeholder-overlays.md** — use `skills/stakeholder-overlay/SKILL.md` when a named leader is identified in Q7.
- **past-investigations/** — populated automatically by `skills/investigation-reset/SKILL.md` at engagement close.
