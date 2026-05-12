# Decisions Log

An **append-only** record of every gate decision the user has made during this investigation. The agent writes a new entry whenever the user approves, redirects, or asks for iteration through a lens. Never edit or delete prior entries — they are the audit trail.

## Entry format

Each entry must include:

- **Timestamp** — ISO 8601 (YYYY-MM-DD HH:MM)
- **Phase** — 0 / 1 / 2 / 3
- **Presented** — what the agent presented at this gate (one sentence)
- **Decision** — approve / redirect / iterate
- **Rationale** — the user's reasoning, captured in their words where possible
- **Next action** — what the agent does next as a result of this decision

## Entries

### YYYY-MM-DD HH:MM — Phase 0 framing presented

- **Phase**: 0
- **Presented**: Reframed problem statement, scope, stakeholder list, initial candidate hypotheses.
- **Decision**: [approve / redirect / iterate]
- **Rationale**: [user's reasoning]
- **Next action**: [e.g., "Proceed to Phase 1 — build MECE issue tree." or "Redirect: narrow scope to iOS only; rebuild Phase 0 framing."]

### YYYY-MM-DD HH:MM — Phase 1 diagnosis presented

- **Phase**: 1
- **Presented**: MECE issue tree, ranked hypotheses with ICE scores, signals map.
- **Decision**: [...]
- **Rationale**: [...]
- **Next action**: [...]

### [Append new entries below this line — newest at the bottom]
