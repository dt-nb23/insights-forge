# ⚠️ Deprecated — Do Not Use

Past investigation archives have moved to the per-client workspace architecture to prevent cross-client context pollution.

**The correct location for engagement artifacts is:**
`memory/clients/<client-name>/engagements/<YYYY-MM-DD-slug>/` (nothing is moved on archive — the folder is marked `state: complete`)

**The correct location for a client's engagement history index is:**
`memory/clients/<client-name>/README.md`

Use `skills/investigation-reset/SKILL.md` to archive an investigation. Files placed in this directory will not be read by any skill.

See `memory/clients/README.md` for the full per-client workspace structure.

---

# Legacy index (pre-isolation architecture)

This content is preserved for reference only. Do not add new rows here.

## Archive format

Each completed investigation is archived as a dated subfolder:

```
memory/long-term/past-investigations/
└── YYYY-MM-DD-short-name/
    ├── current-context.md      (snapshot of the final framing)
    ├── issue-tree.md           (the final MECE tree)
    ├── hypotheses.md           (with final Status column — confirmed / ruled out)
    ├── signals-map.md
    ├── action-plan.md          (with what was actually executed)
    ├── decisions-log.md        (the full audit trail)
    ├── one-pager.md            (the final exec deliverable, if produced)
    └── lessons-learned.md      (new — see template below)
```

Each archive should capture:

- **The problem** — what the team set out to investigate.
- **The final issue tree** — the MECE decomposition the team converged on.
- **The validated hypotheses** — what was confirmed, what was ruled out, what was left inconclusive.
- **The action plan** — what was recommended and what was actually executed.
- **Lessons learned** — what would the team do differently next time. This is the most valuable section for future investigations and the most commonly skipped.

## Lessons learned template

Each archive's `lessons-learned.md` should answer four questions:

1. **What did we get right?** Decisions, framings, or instincts that held up. Worth repeating next time.
2. **What did we get wrong?** Hypotheses that wasted time, framings that misdirected the team, signals we trusted that turned out to be misleading.
3. **What did we discover that we did not know before?** New mappings between technical signals and business outcomes, new failure modes, new things to instrument.
4. **What should change in the playbook?** Updates to `frameworks.md`, `domain-knowledge.md`, or `stakeholder-profiles.md`. Surface candidates here; the user approves promotion to long-term memory.

## Index of completed investigations

| Date | Short name | Problem (one line) | Outcome | Key lesson |
|---|---|---|---|---|
| [YYYY-MM-DD] | [short-name] | [One-line problem statement.] | [Confirmed H-XX; rolled out fix; impact measured.] | [The single most reusable lesson from this engagement.] |

> Add a new row when an investigation is archived. Keep the "Key lesson" column to one sentence — it is the searchable hook future-you uses to find this archive.
