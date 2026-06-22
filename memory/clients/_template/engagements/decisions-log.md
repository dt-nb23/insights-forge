# [Client Name] — [YYYY-MM-DD-slug] — Decisions Log

**Engagement:** memory/clients/[client-name]/engagements/[YYYY-MM-DD-slug]/
**Started:** YYYY-MM-DD

Append-only record of every human-in-the-loop gate decision. One row per gate
event. Never edit or delete a prior row — corrections are added as a new row.

<!--
Per row:
- Date          — YYYY-MM-DD of the gate decision
- Phase / Gate  — Phase 0 Context | Phase 1 Diagnose | Phase 2 Plan | Phase 3 Deliver
- Decision      — Approve | Redirect | Iterate-through-a-lens
- Lens invoked  — MECE | Optimist | ICE | Consultative | Customer | Skeptic
                  (or "—" when no lens was used)
- Rationale     — 1-2 sentences: why the user chose this, and what changed as a result
-->

| Date | Phase / Gate | Decision | Lens invoked | Rationale |
|---|---|---|---|---|
| YYYY-MM-DD | Phase 0 Context | Approve | — | [Why the user approved / what was confirmed] |
| YYYY-MM-DD | Phase 1 Diagnose | Iterate-through-a-lens | Skeptic | [What the lens surfaced and what was revised before re-presenting] |
| YYYY-MM-DD | Phase 1 Diagnose | Redirect | — | [What scope/framing/priority changed and why] |

<!--
Decision vocabulary (from CLAUDE.md "Human-in-the-loop gates"):
- Approve                 — proceed to the next phase.
- Redirect                — change scope, framing, or priority; artifacts updated and re-presented.
- Iterate-through-a-lens  — re-review through a named lens, then revise before re-presenting.

Mandatory-per-phase lenses still record a row here when run at a gate:
- Phase 1: MECE + Consultative (framing) + ICE (after signal-mapping)
- Phase 2: MECE + persona panel (Skeptic, Optimist, Customer, Consultative) + ICE (re-rank)
On-demand lens invocations (any of the six, at any gate) are logged the same way.
-->
