# Insights Forge — Improvement Roadmap

Candidate improvements surfaced during the 2026-05-26 architecture review session. Items are not committed — each requires a deliberate decision before implementation. Ordered within each tier by expected impact.

---

## Tier 1 — High impact, pursue next

### Dynatrace API read-only context fetcher
**What**: A `tools/dt-context-fetcher.py` that calls the Dynatrace REST API to pull environment inventory — Management Zones, RUM application list, SLO definitions, OneAgent coverage, synthetic monitor list — and formats the output into the `environment.md` template for consultant review and approval.

**Why**: Phase 0 environment intake currently requires a 10–20 minute manual interview (Q4–Q6 plus the environment-intake skill). A context fetcher reduces this to a 2-minute review-and-confirm. The consultant still approves before anything is written to `memory/clients/<client-name>/environment.md`.

**Boundary clarification required**: The `tools/README.md` prohibits DQL/analytical queries. This tool would use configuration/inventory endpoints only ("what exists," not "what happened") — that distinction should be explicitly blessed before building.

**Implementation notes**:
- Read-only API token scoped to entity read + settings read
- No DQL, no metrics queries, no logs
- Output goes into the environment-intake skill flow for consultant approval
- Credentials managed outside the workspace (env var or keychain)

---

### Salesforce / CRM integration
**What**: MCP server or `tools/crm-fetcher.py` that pulls account context — renewal date, product usage tiers, open support tickets, prior QBR outcomes — into Phase 0 framing.

**Why**: Q3 (C.S.I.R. sub-sequence) currently relies entirely on what the consultant remembers. CRM data makes the engagement framing more complete and faster.

**Boundary**: Sensitive account data. Must write only into `memory/clients/<client-name>/` — never into `memory/long-term/`.

**Pre-requisite**: Salesforce API credentials and approval to use them in this workflow.

---

## Tier 2 — Medium impact, build as archive grows

### Semantic search over past investigations
**What**: `tools/investigation-search.py` that indexes `lessons-learned.md` and `hypotheses.md` files across all `memory/clients/<client-name>/engagements/` subfolders (filtered to `state: complete`) using the Anthropic embeddings endpoint (or a local model). Returns semantically relevant chunks during Phase 0 when generating orientation hypotheses.

**Why**: The current past-investigation lookup reads a flat `README.md` index per client. As the archive grows across verticals and problem types, keyword matching misses relevant prior work. Semantic matching — "surface any investigation where Davis AI problem correlation was a confirmed hypothesis" — would meaningfully improve Phase 1 seeding.

**Implementation notes**:
- Index runs as a background Haiku sub-agent
- Embeddings stored in `memory/clients/search-index/` (or similar)
- Re-index triggered on investigation archive (via investigation-reset skill)
- Fallback to flat index read if index doesn't exist yet

---

### Wider external research allowlist
**What**: Add three domains to the `WebFetch`/`WebSearch` allowlist in `settings.json` and `skills/external-research/SKILL.md`:

1. `dora.dev` — DORA metrics (deployment frequency, lead time, MTTR, change failure rate)
2. `opentelemetry.io/docs/` — OTel signal semantics for hybrid instrumentation environments
3. Cloud provider observability docs (AWS CloudWatch, GCP Cloud Operations) — for hybrid-cloud investigations

**Why**: These domains come up in nearly every Phase 1 hypothesis discussion involving engineering leadership. Having cited definitions improves signal-map quality and reduces "the team should look this up" gaps in action plans.

**Implementation notes**:
- Update `skills/external-research/SKILL.md` allowlist table
- Update `memory/long-term/domain-knowledge.md` authoritative references table
- Add new URLs to doc-freshness-checker scope

---

## Tier 3 — Low effort, high consistency value

### Auto-save hook on agent Stop
**What**: A `Stop` hook in `.claude/settings.json` that runs `git add memory/clients/ && git commit -m "Auto-save investigation state $(date +%Y-%m-%dT%H:%M)"` after every agent response.

**Why**: Investigation state is written to the engagement folder under `memory/clients/` across multiple sessions. If a session crashes or the workspace is closed mid-investigation, the last committed state is the recovery point. Without the hook, that recovery point is whenever the consultant last ran `git commit` manually — which in practice is rarely.

**Implementation notes**:
- Hook runs only when an engagement is active (avoid committing an empty workspace)
- Commit message should include the active client name for traceability
- Can be configured in `.claude/settings.json` under `hooks.Stop`

---

### PDF renderer for Phase 3 one-pagers
**What**: `tools/pdf-generator.py` using Playwright (headless Chromium) or WeasyPrint to convert the HTML one-pager output from `skills/exec-onepager/SKILL.md` into a print-ready PDF.

**Why**: The exec-onepager skill produces HTML (for brand fidelity) and Markdown. Clients receive PDF. Currently the consultant converts manually via browser print dialog, which loses the wave background rendering on some browsers. A programmatic converter closes the Phase 3 delivery chain.

**Implementation notes**:
- Playwright preferred (handles CSS backgrounds correctly)
- Input: `*.html` file in project root or the engagement folder
- Output: `*.pdf` alongside the source HTML
- Add to pptx-builder skill as a parallel option ("generate PDF" vs "generate PPTX")

---

### Extended thinking on Skeptic lens for high-stakes deliverables
**What**: An opt-in mode for the Skeptic sub-agent that enables extended thinking (available on Sonnet). User triggers explicitly: "run a deep skeptic pass on this."

**Why**: The Skeptic lens on `claude-sonnet-4-6` is good for standard engagements. For board-level renewals, large expansion proposals, or politically sensitive deliverables, extended thinking produces qualitatively deeper risk identification — the kind that catches non-obvious second-order risks and anticipates hostile questions that aren't visible from a surface read of the plan.

**Implementation notes**:
- Add a `skeptic-lens-deep.md` agent variant with thinking enabled (or use a flag in the existing agent)
- Triggered by user phrasing: "deep skeptic pass," "thorough risk review," or similar
- Document the cost premium so the consultant can make an informed call

---

## Notes

- Items in Tier 1 require explicit go-ahead before implementation (scope/boundary decisions involved).
- Items in Tier 3 can be implemented in a single session each.
- The Salesforce integration requires IT/platform approval for API credentials before it can move forward.
- The semantic search tool becomes worthwhile once there are 5+ archived investigations in `memory/clients/`.
