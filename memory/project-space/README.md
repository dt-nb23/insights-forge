# Project Space — Session Pointer Only

This folder holds **one file**: `active-engagement.md`. All investigation phase files now live directly inside the client's dated engagement folder.

## What lives here

- `active-engagement.md` — the session pointer. Format:

```
active: memory/clients/<client-name>/engagements/YYYY-MM-DD-<slug>/
```

Set to `active: none` when no engagement is open. On pause, a `paused:` line is added alongside.

## Why this design

Previously this folder held all live phase files (current-context.md, issue-tree.md, etc.), which meant two concurrent sessions would overwrite each other's work. Moving phase files directly into client-scoped, dated engagement folders eliminates that risk — each session creates its own uniquely-named folder at Phase 0 and writes only there.

## Architecture overview

```
memory/
├── long-term/          ← Universal knowledge (Dynatrace, frameworks, brand). Never client data.
│
├── clients/            ← Per-client workspaces. Strictly isolated.
│   └── <client-name>/
│       ├── environment.md
│       ├── stakeholder-overlays.md
│       └── engagements/
│           └── YYYY-MM-DD-<slug>/   ← All phase files live here
│
└── project-space/
    └── active-engagement.md         ← "You are here." Points to the active engagement folder.
```

## State transitions

- **Active**: `active: memory/clients/<name>/engagements/<dated-slug>/`
- **Paused**: `active: none` + `paused: memory/clients/<name>/engagements/<dated-slug>/`
- **No engagement**: `active: none`

Use `skills/investigation-reset/SKILL.md` for all pause, archive, and resume operations.
