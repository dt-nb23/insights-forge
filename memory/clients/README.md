# Client Workspaces — Per-Client Isolated Memory

Each subfolder in this directory is a fully isolated workspace for one client. All client-specific data lives here. The universal library at `memory/long-term/` contains **no client data** — only Dynatrace concepts, frameworks, brand, and generic role archetypes.

## Per-client folder structure

```
memory/clients/<client-name>/
├── README.md                    (engagement summary and history index)
├── environment.md               (DT environment facts: MZs, SLOs, synthetic monitors, gaps)
├── stakeholder-overlays.md      (named leaders for this client only)
└── engagements/                 (one subfolder per engagement, created at Phase 0)
    └── YYYY-MM-DD-<slug>/
        ├── current-context.md
        ├── issue-tree.md
        ├── hypotheses.md
        ├── signals-map.md
        ├── action-plan.md
        ├── decisions-log.md
        ├── lessons-learned.md   (written by investigation-reset at archive)
        └── one-pager-YYYY-MM-DD.md  (if produced in Phase 3)
```

The engagement folder is created by `context-framing` at Phase 0. The slug is a 2-3 word description of the problem. All phase skills read and write directly to this folder — no files are ever moved.

## Engagement states

| State | Where files live | Pointer in active-engagement.md |
|---|---|---|
| **Active** | `memory/clients/<name>/engagements/<dated-slug>/` | `active: memory/clients/<name>/engagements/<dated-slug>/` |
| **Paused** | Same folder — nothing moves | `active: none` + `paused: memory/clients/<name>/engagements/<dated-slug>/` |
| **Completed** | Same folder — nothing moves | `active: none` (README updated with outcome row) |

`memory/project-space/active-engagement.md` is the session pointer. It stores the full path to the active engagement folder, not just the client name.

## Context isolation rule

**The agent reads only one client folder per session.** When working on Client X, it reads `memory/long-term/` (universal library) and `memory/clients/X/` (Client X's workspace). It never reads `memory/clients/Y/` or any other client's folder. Client data does not cross client boundaries.

## How to create a new client workspace

A client folder is created automatically by `context-framing` at Phase 0 start (copied from `memory/clients/_template/`). The engagement subfolder is also created at that time.

## How to populate client-specific files

- **environment.md** — use `skills/environment-intake/SKILL.md` at the Phase 0 gate.
- **stakeholder-overlays.md** — use `skills/stakeholder-overlay/SKILL.md` when a named leader is identified in Q7.
- **engagements/** — populated automatically by `context-framing` (Phase 0) and phase skills throughout the investigation.
