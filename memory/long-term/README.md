# Long-Term Memory

This folder holds **durable knowledge that persists across investigations**. The agent reads from this folder freely on every session but **writes here only when the user explicitly approves an update** — for example: "add this stakeholder to the profile", "log this lesson learned from the investigation", "extend the glossary with this new term", "update the domain-knowledge notes on RUM with what we just learned".

## What lives here

- `frameworks.md` — MECE, ICE, issue-tree-to-hypothesis mapping, exit criteria. The agent's procedural reference for structured analysis.
- `domain-knowledge.md` — observability concepts, common signal patterns, tech → UX → business linkages, Dynatrace concept definitions (vendor-sourced with citations + `[team to note: …]` slots for org-specific behavior).
- `dynatrace-playbooks.md` — **client-agnostic procedural patterns** for how to investigate common problem shapes in Dynatrace (latency, error spike, RUM regression, Grail logs, SLO burn, deploy correlation, third-party dependency, Davis problem). The agent matches each Phase 1 hypothesis to a playbook and pulls its investigation sequence and exit criteria into the live artifacts. Sourced from `docs.dynatrace.com`; re-verify retrieval dates before relying on procedural detail in a deliverable.
- `stakeholder-profiles.md` — one profile per leader the agent regularly produces outputs for; what they care about, what they ignore, decisions they own.
- `terminology.md` — glossary of recurring terms (MECE, ICE, SLI, SLO, RUM, hypothesis, signal, exit criteria) plus a Dynatrace platform glossary with cited definitions.
- `client-question-bank.md` — client-facing phrasings of the Phase 0 clarifying questions, grouped by the MUST-HAVE / SHOULD-HAVE / NICE-TO-HAVE rubric. Loaded by the context-framing skill; used when the consultant is gathering context live with the customer or wants reference phrasings for their own discovery calls.
- `past-investigations.md` — index of archived investigations and the lessons each one surfaced.
- `brand/brand-spec.md` — Dynatrace brand specification (colors, typography, layout patterns, voice, terminology, footer text) authoritative for Phase 3 one-pager and PPTX deliverables. Mirrored from the Dynatrace PowerPoint brand template PDF, styleguide.dynatrace.com, and the Insights product lockup SVGs. Re-verify when the brand assets are refreshed.
- `brand/reference/` — supporting notes; currently `source-pdf-notes.md` maps each pattern in the brand spec to its page in the source PDF.

## Rules

- The agent **reads** from this folder freely. Anything here is fair game as context for the current investigation.
- The agent **writes** here only on explicit user instruction. Examples of valid write triggers:
  - "Add [name] to the stakeholder profiles as Director of Reliability."
  - "Log a lesson learned: when SDK version segmentation is missing in RUM, always flag it as an instrumentation gap in Phase 1."
  - "Update the Dynatrace section of domain knowledge with the note that DPS-based reporting recently changed."
- The agent does **not** auto-promote project-space findings into long-term memory. That decision belongs to the user.

## Why this rule exists

Auto-promotion of session-specific findings into durable memory creates two failure modes: (1) one-off context bleeding into future investigations as if it were universal truth, and (2) the agent slowly accumulating wrong or stale "knowledge" that nobody asked it to remember. Requiring explicit user approval keeps long-term memory curated and trustworthy.
