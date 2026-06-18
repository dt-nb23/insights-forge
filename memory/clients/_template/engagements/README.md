# Engagements

Each engagement gets its own subfolder, created by `context-framing` at Phase 0 start.

## Naming convention

```
YYYY-MM-DD-<slug>/
```

- **Date**: today's date when the engagement was started
- **Slug**: 2-3 word lowercase hyphen-separated description of the problem (e.g., `api-latency`, `auth-timeout`, `checkout-conversion`)
- **Collision**: if the same client+date+slug already exists, append `-2`, `-3`, etc.

## What lives inside each engagement folder

```
YYYY-MM-DD-<slug>/
├── current-context.md     (Phase 0 — context-framing)
├── issue-tree.md          (Phase 1 — mece-decomposition)
├── hypotheses.md          (Phase 1 — hypothesis-generation + ice-scoring)
├── signals-map.md         (Phase 1 — signal-mapping)
├── action-plan.md         (Phase 2 — action-plan-builder)
├── decisions-log.md       (all phases — append-only gate record)
├── lessons-learned.md     (investigation-reset — written at archive)
└── one-pager-YYYY-MM-DD.md (Phase 3 — exec-onepager, if produced)
```

## Status

Engagement status is tracked by the pointer in `memory/project-space/active-engagement.md` and by the engagement history table in this client's `README.md`. The folder itself is never deleted or moved — it remains here whether the engagement is active, paused, or complete.
