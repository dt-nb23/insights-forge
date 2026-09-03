# Client Workspaces — Per-Client Isolated Memory

Each subfolder in this directory is a fully isolated workspace for one client. All client-specific data lives here. The universal library at `memory/long-term/` contains **no client data** — only Dynatrace concepts, frameworks, brand, and generic role archetypes.

## Per-client folder structure

```
memory/clients/<client-name>/
├── README.md                    (engagement summary and history index)
├── environment.md               (DT environment facts: MZs, SLOs, synthetic monitors, gaps)
├── contract.md                  (commercial & consumption: DPS commit, renewal date, burn — confidential)
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
        ├── one-pager-YYYY-MM-DD.md   (Phase 3 — companion markdown, if produced)
        ├── <slug>-onepager.html      (Phase 3 — the one-pager HTML)
        ├── deck-spec-YYYY-MM-DD.json (Phase 3 — deck spec fed to tools/pptx-generator.py)
        └── deck-YYYY-MM-DD.pptx      (Phase 3 — the generated deck)
```

The engagement folder is created by `context-framing` at Phase 0. The slug is a 2-3 word description of the problem. All phase skills read and write directly to this folder — no files are ever moved.

## Engagement states

State lives in each engagement's own `current-context.md` status front-matter (`state:`), not in any shared file — so any number of engagements can be paused at once, and two concurrent sessions never contend over a global pointer.

| State | Where files live | How it's recorded |
|---|---|---|
| **Active** | `memory/clients/<name>/engagements/<dated-slug>/` | `state: active` in that engagement's `current-context.md`; the session holds its path |
| **Paused** | Same folder — nothing moves | `state: paused` in that engagement's `current-context.md` |
| **Completed** | Same folder — nothing moves | `state: complete` in `current-context.md` + README outcome row |

There is **no global pointer file**. A resuming session finds engagements by scanning `memory/clients/*/engagements/*/current-context.md` for `state: active` or `state: paused`.

## Context isolation rule

**The agent reads only one client folder per session.** When working on Client X, it reads `memory/long-term/` (universal library) and `memory/clients/X/` (Client X's workspace). It never reads `memory/clients/Y/` or any other client's folder. Client data does not cross client boundaries.

## How to create a new client workspace

A client folder is created automatically by `context-framing` at Phase 0 start (copied from `memory/clients/_template/`). The engagement subfolder is also created at that time.

## How to populate client-specific files

- **environment.md** — use `skills/environment-intake/SKILL.md` at the Phase 0 gate.
- **contract.md** — capture commercial/consumption context (DPS commit, renewal date, on-demand burn, commercial owner) when it surfaces, with explicit user approval. Treated as confidential client data; never promoted to long-term.
- **stakeholder-overlays.md** — use `skills/stakeholder-overlay/SKILL.md` when a named leader is identified in Q7.
- **engagements/** — populated automatically by `context-framing` (Phase 0) and phase skills throughout the investigation.
