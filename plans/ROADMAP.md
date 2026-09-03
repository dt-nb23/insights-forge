# Insights Forge — Improvement Roadmap

Candidate improvements surfaced during the 2026-05-26 architecture review session. Items are not committed — each requires a deliberate decision before implementation. Ordered within each tier by expected impact. Decisions recorded on 2026-09-03 are marked as such and are binding on the eventual build; they resolve the open design questions without starting the work.

---

## Tier 1 — High impact, pursue next

### Dynatrace API read-only context fetcher
**What**: A `tools/dt-context-fetcher.py` that calls the Dynatrace REST API to pull environment inventory — Management Zones, RUM application list, SLO definitions, OneAgent coverage, synthetic monitor list — and formats the output into the `environment.md` template for consultant review and approval.

**Why**: Phase 0 environment intake currently costs one batched environment message (Q4–Q6) plus the environment-intake skill when the tenant is unfamiliar. A context fetcher reduces this to a 2-minute review-and-confirm and — more importantly — replaces the consultant's recollection of what is active with the tenant's own inventory, which is what the never-recommend-missing-instrumentation guardrail actually depends on. The consultant still approves before anything is written to `memory/clients/<client-name>/environment.md`.

**Sequencing decision (2026-09-03)**: this fetcher ships **before** the CRM integration — an encoded dependency, not an impact-ordering coincidence. It strengthens an existing guardrail and removes a whole class of "we recommended a capability they don't have" errors, while CRM only improves framing and adds a new sensitive-data surface.

**Boundary clarification required**: The `tools/README.md` prohibits DQL/analytical queries. This tool would use configuration/inventory endpoints only ("what exists," not "what happened") — that distinction should be explicitly blessed before building.

**Implementation notes**:
- Read-only API token scoped to entity read + settings read
- No DQL, no metrics queries, no logs
- Output goes into the environment-intake skill flow for consultant approval
- Every fetched fact is provisional and dated (`source: tenant API, as of YYYY-MM-DD`), like a seed-prompt value: captured, not confirmed
- Credentials managed outside the workspace (env var or keychain)
- Register the tool's invocation as a `Bash(python3 tools/dt-context-fetcher.py:*)` allow rule in `.claude/settings.json`, matching the other tools

---

### Salesforce / CRM integration
**What**: MCP server or `tools/crm-fetcher.py` that pulls account context — renewal date, product usage tiers, open support tickets, prior QBR outcomes — into Phase 0 framing.

**Why**: Q3 (C.S.I.R. sub-sequence) currently relies partly on what the consultant remembers. CRM can supply **Context** and **Specific Information** (relationship history, contract phase, open tickets, prior QBR outcomes) — it **cannot** supply **Intent**, which exists only in the consultant's head, and it supplies nothing for **Response Format**.

**Design decisions (2026-09-03, binding on the build)**:
1. **Intent first.** Q3-Intent is asked *before* any CRM pull, and Intent is the retrieval filter — the pull is a query, not a context dump. Pull-then-filter is explicitly rejected: irrelevant renewal dates and ticket history would otherwise be woven into orientation hypotheses because they were present, not because they mattered.
2. **Scope by engagement trigger, not by account.** A small fixed field list per trigger (Q9): renewal → renewal date, ACV band, consumption vs. commit, open escalations; expansion → entitled-but-unlit capabilities, usage tiers; QBR → last QBR outcomes and the commitments made against them; incident follow-up → the incident record and open tickets only. A closed list is reviewable at the Phase 0 gate and testable; an open pull is neither.
3. **Provisional and dated.** Every CRM-derived fact lands in `current-context.md` tagged with source and as-of date and is treated like a seed-prompt value: captured, not confirmed. It appears under Assumptions at the Phase 0 gate until the consultant confirms it.

**Boundary**: Sensitive account data. Must write only into `memory/clients/<client-name>/` — never into `memory/long-term/`. The client-isolation PreToolUse hook (`tools/client-isolation-hook.sh`) now enforces this boundary mechanically for file-tool writes, which satisfies the build's isolation precondition; the fetcher itself must write through those file tools (not directly from Python) so the hook sees the write.

**Pre-requisite**: Salesforce API credentials and approval to use them in this workflow — and the Dynatrace context fetcher above ships first.

---

## Tier 2 — Medium impact, build as archive grows

### Semantic search over past investigations
**What**: `tools/investigation-search.py` that indexes `lessons-learned.md` and `hypotheses.md` files across all `memory/clients/<client-name>/engagements/` subfolders (filtered to `state: complete`) using the Anthropic embeddings endpoint (or a local model). Returns semantically relevant chunks during Phase 0 when generating orientation hypotheses.

**Why**: The current cross-engagement lookup (context-framing Step 4) matches on the tagged `lessons-learned.md` front-matter — vertical, problem shape, capabilities — and reads only the front-matter plus the Cross-engagement hook line across clients. Tag matching is exact and cheap, and it is the right tool while the archive is small; it misses prior work whose relevance is semantic rather than categorical ("any engagement where Davis problem correlation was a *confirmed* hypothesis"). Semantic matching becomes worth its complexity once tag matching visibly misses.

**Implementation notes**:
- Index runs as a background sub-agent on the `haiku` alias
- The index must **not** live under `memory/clients/` — the client-isolation hook treats every folder there as a client and would lock a session to `search-index`. Store it under `.claude/search-index/` (gitignored), keyed by engagement path.
- The index stores only what the cross-client read exception already permits (front-matter and hook line), so the lookup never widens the isolation boundary; full lessons text stays inside its client folder.
- Re-index triggered on investigation archive (via investigation-reset skill)
- Fallback to the tag-matching read if the index doesn't exist yet

---

### Wider external research allowlist
**What**: Add three domains to the fetch allowlist — `tools/fetch-allowlist.txt` (which `tools/fetch-allowlist-hook.sh` enforces at fetch time) plus matching `WebFetch(domain:…)` allow rules in `.claude/settings.json` — and to the allowlist table in `skills/external-research/SKILL.md`, which must stay in sync with the file:

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
- Hook runs only when an engagement is active — the session's marker in `.claude/session-clients/` says which client, so scope the `git add` to that client's folder rather than all of `memory/clients/` (two concurrent sessions must not commit each other's work)
- Commit message should include the active client name for traceability
- Can be configured in `.claude/settings.json` under `hooks.Stop`, alongside the existing `SessionEnd` hook (`tools/session-end-hook.sh`) — decide whether Stop-level granularity is worth the commit noise before adding it

---

### PDF renderer for Phase 3 one-pagers
**What**: `tools/pdf-generator.py` using Playwright (headless Chromium) or WeasyPrint to convert the HTML one-pager output from `skills/exec-onepager/SKILL.md` into a print-ready PDF.

**Why**: The exec-onepager skill produces HTML (for brand fidelity) and Markdown. Clients receive PDF. Currently the consultant converts manually via browser print dialog, which loses the wave background rendering on some browsers. A programmatic converter closes the Phase 3 delivery chain.

**Implementation notes**:
- `tools/onepager-lint.py` already renders the one-pager through headless Chrome to count pages for Gate 1 — the PDF renderer should reuse that path rather than add Playwright as a second browser dependency
- Input: the `<slug>-onepager.html` inside the engagement folder — never the repo root (all Phase 3 artifacts live in `<ENGAGEMENT_PATH>/`)
- Output: `*.pdf` alongside the source HTML, and only after the linter passes
- Add to the exec-onepager skill's Step 3 gate as the delivery step, not to pptx-builder (a PDF is the one-pager's delivery format; the deck has its own)

---

### Extended thinking on Skeptic lens for high-stakes deliverables
**What**: An opt-in mode for the Skeptic sub-agent that enables extended thinking. User triggers explicitly: "run a deep skeptic pass on this."

**Why**: The Skeptic lens on the workspace's default `sonnet` alias is good for standard engagements. For board-level renewals, large expansion proposals, or politically sensitive deliverables, extended thinking produces qualitatively deeper risk identification — the kind that catches non-obvious second-order risks and anticipates hostile questions that aren't visible from a surface read of the plan.

**Implementation notes**:
- Add a `skeptic-lens-deep.md` agent variant with thinking enabled (or use a flag in the existing agent); keep the model as an alias, never a dated model ID, so it moves with the workspace default
- Triggered by user phrasing: "deep skeptic pass," "thorough risk review," or similar — and consider making it automatic when the action-plan council's escape hatch fires for a high-stakes deliverable
- Document the cost premium so the consultant can make an informed call

---

## Notes

- Items in Tier 1 require explicit go-ahead before implementation (scope/boundary decisions involved).
- Items in Tier 3 can be implemented in a single session each.
- The Salesforce integration requires IT/platform approval for API credentials before it can move forward.
- The semantic search tool becomes worthwhile once there are 5+ archived investigations in `memory/clients/` and the tag-based lookup has visibly missed a relevant one.
- The Tier 1 sequencing (fetcher, then CRM) and the three CRM design decisions are recorded above and are not to be re-litigated at build time without a new review.
