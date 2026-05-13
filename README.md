# insights-forge

An agentic workspace that helps consultants and analytics teams structure ambiguous problems, generate testable hypotheses, connect technical signals to user experience and business impact, and produce exec-ready outputs for senior technical leadership.

The agent works in **explicit phases with a human approval gate between each phase**. It accelerates engineering and analytics judgment — it does not replace it. It never runs live queries or executes production changes.

## What it does

- Reframes vague problem statements into MECE-decomposed issue trees.
- Generates ranked, testable hypotheses with explicit exit criteria.
- Scores hypotheses and actions with ICE (Impact × Confidence / Effort).
- Maps technical signals (SLI/SLO, RUM, APM) through user-visible UX outcomes to business KPIs.
- Builds investigation plans with named owners, timeframes, and exit criteria.
- Produces VP/Director-ready one-pagers and decks tailored to specific stakeholder profiles.
- Stress-tests recommendations through six critique lenses before leadership review.

## What it does NOT do

- Run live queries against Dynatrace, data warehouses, or any production system.
- Generate raw DQL, SQL, or other executable query syntax.
- Execute production changes, deploys, or configuration updates.
- Replace engineering or analytics judgment.
- Bypass review gates.

## Phased workflow

Each phase produces a specific artifact and ends at a human approval gate.

| Phase | Purpose | Artifact |
|---|---|---|
| 0 — Context | Frame the problem; confirm scope and stakeholders | [`memory/project-space/current-context.md`](memory/project-space/current-context.md) |
| 1 — Diagnose | MECE issue tree, ranked hypotheses, signals map | [`issue-tree.md`](memory/project-space/issue-tree.md), [`hypotheses.md`](memory/project-space/hypotheses.md), [`signals-map.md`](memory/project-space/signals-map.md) |
| 2 — Solution | Investigation plan, recommended actions, decision asks | [`action-plan.md`](memory/project-space/action-plan.md) |
| 3 — Deliver | Exec one-pager and PowerPoint deck | one-pager + deck (generated) |

At each gate, the user can **approve**, **redirect**, or **iterate** through one or more critique lenses.

## Critique lenses

Six sub-agents critique work product on demand. Each has a narrow job and a defined output format.

| Lens | Job |
|---|---|
| [MECE](.claude/agents/mece-lens.md) | Critiques issue trees for overlap, gaps, and mixed abstraction |
| [Optimist](.claude/agents/optimist-lens.md) | Steelmans the plan; surfaces upside and parallelization opportunities |
| [ICE](.claude/agents/ice-lens.md) | Scores and re-ranks hypotheses or actions |
| [Consultative](.claude/agents/consultative-lens.md) | Translates findings into senior technical leadership voice |
| [Customer](.claude/agents/customer-lens.md) | Asks whether the work matches what users actually experience |
| [Skeptic](.claude/agents/skeptic-lens.md) | Stress-tests for failure modes and hostile leadership questions |

## Structure

```
.
├── CLAUDE.md                     # Agent operating manual
├── .claude/agents/               # Six critique lens sub-agents
├── memory/
│   ├── project-space/            # Live investigation (read/write)
│   └── long-term/                # Durable knowledge (read freely; write on user approval)
├── skills/                       # Procedural skills, one per phase deliverable
└── tools/                        # Reserved for future integrations (read-only boundary)
```

### Memory model

- **`memory/project-space/`** — the live state of the *current* investigation. The agent reads and writes freely. Archived to `memory/long-term/past-investigations/` when an investigation completes.
- **`memory/long-term/`** — durable knowledge (frameworks, domain knowledge, stakeholder profiles, terminology, past investigations). The agent reads freely but only writes on explicit user approval.

### Skills

Each phase deliverable has a corresponding procedural skill the agent reads before producing the artifact:

- [`mece-decomposition`](skills/mece-decomposition/SKILL.md) — build a MECE issue tree.
- [`hypothesis-generation`](skills/hypothesis-generation/SKILL.md) — draft testable hypotheses per branch.
- [`ice-scoring`](skills/ice-scoring/SKILL.md) — score and rank with Impact × Confidence / Effort.
- [`signal-mapping`](skills/signal-mapping/SKILL.md) — connect technical signals to UX outcomes and business KPIs.
- [`action-plan-builder`](skills/action-plan-builder/SKILL.md) — Phase 2 investigation and recommendation plan.
- [`exec-onepager`](skills/exec-onepager/SKILL.md) — Phase 3 one-page written deliverable.
- [`pptx-builder`](skills/pptx-builder/SKILL.md) — Phase 3 PowerPoint deck (adapter; calls the standard pptx skill when available).
- [`external-research`](skills/external-research/SKILL.md) — consult domain knowledge and allowlisted external references (Dynatrace docs and community) with citation.

### External references

The agent grounds Dynatrace-specific claims in local domain knowledge first, then in approved external sources. Local domain knowledge:

- [`memory/long-term/domain-knowledge.md`](memory/long-term/domain-knowledge.md) — concepts, signal patterns, Dynatrace concept definitions, tech → UX → business linkages.
- [`memory/long-term/terminology.md`](memory/long-term/terminology.md) — glossary of recurring terms.
- [`memory/long-term/dynatrace-playbooks.md`](memory/long-term/dynatrace-playbooks.md) — client-agnostic procedural patterns for how to investigate common problem shapes (latency, errors, RUM regressions, Grail logs, SLO burn, deploy correlation, third-party dependencies, Davis problems).

External allowlist (used when local memory is silent or stale):

- [`docs.dynatrace.com`](https://docs.dynatrace.com/) — vendor-authoritative product documentation.
- [`community.dynatrace.com`](https://community.dynatrace.com/) — practitioner threads, known issues, workarounds.

Future internal sources (Slack, Salesforce, internal wikis) require user approval and a dedicated tool integration before the agent will use them. See [`skills/external-research/SKILL.md`](skills/external-research/SKILL.md).

## Getting started

1. Open this workspace in Claude Code.
2. The agent reads [`CLAUDE.md`](CLAUDE.md) on every session — review and adjust the operating principles to your organization's specifics.
3. Populate [`memory/long-term/stakeholder-profiles.md`](memory/long-term/stakeholder-profiles.md) with the real leaders you produce outputs for.
4. Populate [`memory/long-term/domain-knowledge.md`](memory/long-term/domain-knowledge.md) with your specific Dynatrace and observability context (the Dynatrace section is stubbed).
5. Decide which critique lenses to invoke on demand vs by default.
6. Begin an investigation: *"Describe the problem you're trying to solve."*

## Operating boundary

This workspace is designed to **structure and accelerate** engineering and analytics judgment, not replace it. The agent advises; humans validate and execute. Any future tool added to [`tools/`](tools/) must respect that boundary — see [`tools/README.md`](tools/README.md) for the rule.
