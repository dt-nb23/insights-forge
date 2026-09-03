# Root Library — Universal Knowledge

This folder is the **root library** — knowledge that applies to every client and every engagement. The agent reads it on every session. It is intentionally kept free of client data.

## The rule: no client data here

**This folder must never contain:**
- Client names, company names, or organization-identifying information
- Named individuals from a client (stakeholder overlays go in `memory/clients/<client-name>/stakeholder-overlays.md`)
- Client-specific Dynatrace environment details (environment profiles go in `memory/clients/<client-name>/environment.md`)
- Investigation artifacts from a specific engagement (these live in `memory/clients/<client-name>/engagements/<dated-slug>/`)

If client data ends up here, it bleeds into every future engagement. That is the failure mode this design prevents.

The `[team to note: …]` slots in `domain-knowledge.md` are for **org-level operational context only** (e.g., which DPS capabilities the org's standard contract includes). They are not for client-specific facts.

## What lives here

| File | What it contains | Read frequency |
|---|---|---|
| `domain-knowledge.md` | Observability concepts, signal patterns, tech → UX → business linkages, Dynatrace concept definitions with citations. | Every session (session initialization) |
| `dynatrace-playbooks.md` | Hub index for the eight client-agnostic investigation patterns. Playbook content lives in `playbooks/`. | Every session (hub only, at session initialization) |
| `playbooks/` | The eight individual playbook files (investigation sequence, exit criteria, citations per problem shape). | On demand (when Phase 1 matches a hypothesis to a problem shape) |
| `frameworks.md` | MECE, ICE, issue-tree-to-hypothesis mapping, exit-criteria definitions. | Every session (session initialization) |
| `stakeholder-profiles.md` | Hub index for the eight generic role archetypes and title-type overlays (e.g., "VP of Engineering" as a role type). Profile content lives in `profiles/`. **No named individuals.** | Every session (hub only, at session initialization) |
| `profiles/` | The eight individual archetype files, with title-type overlays co-located in the parent archetype's file. | On demand (when a phase calibrates for a named stakeholder) |
| `terminology.md` | Glossary of recurring terms and Dynatrace platform glossary with citations. | On demand |
| `client-question-bank.md` | Client-facing phrasings of Phase 0 questions, by rubric tier. | Phase 0 (when doing live discovery with the customer) |
| `drill-sheets/` | Eight per-vertical drill sheets (five fixed-order questions each, with capability dependencies and Phase 1 hooks) that replace the generic Q8 probe. Index in `drill-sheets/README.md`; shipped as drafts pending practitioner validation. | Phase 0, Phase C (the matched vertical's sheet only) |
| `brand/brand-spec.md` | Dynatrace brand specification (colors, typography, layouts, voice, footer) for Phase 3 deliverables. | Phase 3 |
| `phased-plan-timeline-framing.md` | The 30/60/90-day phased-plan framing rules for Phase 3 content assembly (day framing over week-range estimates, 90 days max). | Phase 3 |
| `freshness-report.md` | Operational — the doc-freshness-checker sub-agent's citation drift findings. Overwritten each run. | Phase 0 gate |

## Rules

- The agent **reads** from this folder freely. Every file here is fair game as context.
- The agent **writes** here only on explicit user instruction.
- `freshness-report.md` is the only file the agent writes to automatically (the doc-freshness-checker sub-agent updates it; it contains no client data).

## Valid write triggers (root library only)

- *"Add [term] to `terminology.md` as [definition]."*
- *"Update `domain-knowledge.md` — DPS-based reporting recently changed."*
- *"Promote this investigation sequence into a new playbook."* (A new playbook is a new file in `playbooks/` plus an index row in `dynatrace-playbooks.md`.)

For client-specific data, use the appropriate skill instead: `skills/environment-intake/SKILL.md` or `skills/stakeholder-overlay/SKILL.md`.

## Removed legacy files

Two tombstones from an earlier architecture (`past-investigations.md` and `client-environments/`) have been deleted. Client environment profiles live in `memory/clients/<client-name>/environment.md`; engagement artifacts live in `memory/clients/<client-name>/engagements/<dated-slug>/` (nothing is moved on archive — the folder is marked `state: complete`). Cross-client lessons travel through each engagement's `lessons-learned.md` front-matter tags and Cross-engagement hook line, read back at Phase 0 — not through any shared index.
