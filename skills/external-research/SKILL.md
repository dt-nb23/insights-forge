---
name: external-research
description: Procedure for consulting domain knowledge and approved external references (Dynatrace docs, community posts) during an investigation. Use whenever a Dynatrace concept, feature, or terminology question arises that cannot be answered from the engagement folder alone.
---

# External Research

## When to use

Use this skill any time the investigation needs authoritative reference material that is **not already captured** in `memory/long-term/` or the engagement folder. Typical triggers:

- A stakeholder uses a Dynatrace concept the agent is not sure it has defined correctly (e.g., Grail retention, DPS billing units, Davis problem grouping, Smartscape topology semantics).
- A hypothesis or signal mapping depends on the precise behavior of a Dynatrace feature (RUM session capture, OneAgent vs OpenTelemetry ingest, DQL operators).
- A community thread is the only place a known issue, workaround, or migration nuance is documented.
- The team wants to confirm a default value, a quota, or a deprecation timeline before recommending an action.

If the answer is already in `memory/long-term/domain-knowledge.md` or `memory/long-term/terminology.md`, prefer that. Only reach for the web when local memory is silent, contradictory, or stale.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session (set by Phase 0 or on resume; held in working context). There is no shared pointer file to read.
2. If no engagement is established (research outside any engagement), use global long-term memory only — no engagement-scoped reads.
3. When an engagement is established, phase file reads use `<ENGAGEMENT_PATH>/<file>`.

Then read these files:

- `memory/long-term/dynatrace-playbooks.md` — hub index (already loaded at session init). For **procedural** questions ("how do I investigate X in Dynatrace?"), match to the problem shape in the index, then read the specific playbook file (e.g., `memory/long-term/playbooks/latency-backend.md`). Eight playbooks cover the common problem shapes; each carries its own doc citations. If the playbook answers the question, stop — no web fetch needed.
- `memory/long-term/domain-knowledge.md` — for the Dynatrace concept definitions and the "Authoritative external references" section that lists approved sources.
- `memory/long-term/terminology.md` — for terms the team has already defined.
- `<ENGAGEMENT_PATH>/current-context.md` — to scope the question to the active investigation (if an engagement is active).

## Approved external sources

External research is **allowlisted**. The agent may fetch from these domains and no others without explicit user approval:

| Source | URL root | What it is good for |
|---|---|---|
| Dynatrace product documentation | `https://docs.dynatrace.com/` | Authoritative reference for features, defaults, configuration, concepts, and supported behavior. Cite the page title and product version when relevant. |
| Dynatrace Community | `https://community.dynatrace.com/` | Practitioner discussions, known issues, workarounds, and migration experiences. Treat as practitioner reporting, not vendor commitment. |

Reserved for future integration (do **not** invoke without user approval and a configured tool):

- Internal Slack channels — practitioner discussion, incident retros, oncall handoffs.
- Salesforce — customer tickets, account-specific context, support history.

If the user names a different external source during an investigation, capture it in this section's table only after they confirm it should be added durably.

## Tools

- **WebFetch** — retrieve a specific page when the URL is known. Preferred when the user has linked a doc or community thread directly.
- **WebSearch** — locate the right page when only the topic is known. Constrain queries to the allowlisted domains with `site:docs.dynatrace.com` or `site:community.dynatrace.com`.

The agent does **not** use these tools to fetch from arbitrary domains. If a search result points outside the allowlist, surface the URL to the user and ask before fetching.

## Steps

1. **Check local memory first.** For *procedural* questions ("how do I…") consult the playbook index (`dynatrace-playbooks.md`) and read the matched playbook file; for *conceptual* questions ("what is…") skim `domain-knowledge.md` and `terminology.md`. If the answer is already there and current, use it and stop.
2. **Frame the lookup as a specific question.** "Does Davis AI group multi-service problems by default?" is researchable. "Tell me about Davis" is not. Write the question down before fetching anything.
3. **Search within the allowlist when the URL is unknown.** Use `WebSearch` with a `site:docs.dynatrace.com` or `site:community.dynatrace.com` filter. Prefer documentation hits over community hits unless the question is specifically about practitioner experience.
4. **Fetch the most authoritative result.** Prefer `docs.dynatrace.com` for feature behavior and defaults. Use `community.dynatrace.com` for known-issue corroboration, not for ground truth on product behavior.
5. **Extract only what answers the question.** Pull the relevant fact, definition, or constraint. Do not dump full page contents into project memory. Quote sparingly and cite.
6. **Cite every fact from an external source.** Inline cite the URL, the page's own **"Last updated"** date (extracted from the top of the fetched page — write `last-updated unknown` if the page does not advertise one), and the **retrieval date** (today's date) wherever the fact lands — in `hypotheses.md`, `signals-map.md`, `action-plan.md`, the one-pager, or the deck. Citation format:

   > Davis AI groups related events into a single problem when they share dependencies in Smartscape. *(Source: https://docs.dynatrace.com/…/davis-problem-detection — page last-updated 2026-04-30; retrieved 2026-05-12.)*

   Capturing the page's own last-updated date lets the freshness routine (see below) detect drift — "the page was rewritten since we cited it" — without re-reading every sentence.

7. **Distinguish vendor doc from community report.** When citing community threads, label them as practitioner reports (e.g., "community thread; not vendor-confirmed"). Do not promote a community post to documentation-level confidence without corroboration.
8. **Gate any long-term memory update.** If a lookup surfaces a durable fact the team will want again — a Dynatrace concept definition, a quota, a known issue — present the binary approval gate: **"Proposed addition to `memory/long-term/domain-knowledge.md` [or `terminology.md`]: [one-line summary of the fact]. Approve?"** Write **only** on an explicit yes/approve/equivalent. Never write on "looks good" or on silence (per the rule in `memory/long-term/README.md`).

## Freshness and refresh

Dynatrace documentation updates almost daily/weekly and the site is periodically reformatted. Cited facts have a defined shelf life so the agent never quietly hands a stale claim to a leadership audience.

### Staleness threshold

A citation is **stale** when `today − retrieved > 7 days`. Stale citations must be re-validated before they are reused in:

- Any phase artifact (Phase 1 hypotheses/signals map, Phase 2 action plan, Phase 3 one-pager or deck).
- The Phase 2 → Phase 3 deliverable transition — re-validate **every** citation regardless of age, since this gate hardens work into a leadership deliverable.

The agent does not silently reuse a stale citation. If asked to, the agent first refreshes the citation or surfaces the staleness.

### Phase 0 background refresh

The refresh is operationalized as a **Haiku background sub-agent** (`doc-freshness-checker`, defined in `.claude/agents/doc-freshness-checker.md`). The main agent dispatches it at the start of Phase 0 — the context-framing skill — via the `Agent` tool with `subagent_type: doc-freshness-checker` and `run_in_background: true`. It runs in parallel with the consultant answering the nine clarifying questions, so its wall-clock cost is hidden inside an already-long phase. Haiku keeps the per-run model cost minor.

The sub-agent:

1. Reads every cited URL from `memory/long-term/domain-knowledge.md`, all files in `memory/long-term/playbooks/`, and `memory/long-term/terminology.md`.
2. Fetches each URL via `WebFetch` and extracts the page's current "Last updated" date.
3. Compares the current page-last-updated against the value stored in the existing citation.
4. Writes findings to `memory/long-term/freshness-report.md`, partitioned into four buckets:
   - **Unchanged** — page-last-updated has not moved since the stored value. The report records a refreshed `last-checked` date so the user can see the system is alive.
   - **Drifted** — current page-last-updated is newer than the stored value, OR the citation is in the legacy single-date format and needs a baseline capture, OR the page advertises no last-updated date. The report captures the new last-updated date, the URL, the affected memory file, and a one-line summary of what changed on the page.
   - **Unreachable** — URL returned 404, redirected, or timed out. The report captures the redirect target (if any) and the failure mode.
   - **Skipped — out of allowlist** — URL points outside the allowlisted Dynatrace domains. Recorded for visibility; not fetched.

The sub-agent **does not modify `domain-knowledge.md` or `dynatrace-playbooks.md` directly** — that would violate the "no silent writes to long-term memory" rule. It writes only to the freshness report.

### Surfacing drift to the user

At the **Phase 0 approval gate**, the main agent reads `memory/long-term/freshness-report.md`. If the report contains entries in the **Drifted** or **Unreachable** buckets, the agent surfaces them as part of the gate presentation:

> "While framing the engagement, the freshness sub-agent re-checked our Dynatrace doc citations. N pages have changed and M are unreachable. Want to approve memory updates as part of this Phase 0 gate, defer to the next phase gate, or skip?"

When the user approves an update at a phase gate, the main agent edits the relevant long-term memory file inline, bumps the citation (page-last-updated and retrieved), and clears the entry from the freshness report. This keeps long-term memory updates under explicit user control while the heavy lifting (detection) runs in the background on a cheap model.

If the sub-agent is still running when the main agent reaches the gate, the main agent briefly waits for the report (typically 30–60 seconds for ~30 URLs) before presenting the gate. The user is told the sub-agent is finalizing if the wait runs longer than ~60 seconds.

### Manual refresh

The user can trigger an immediate refresh at any time outside of Phase 0:

> "Refresh the docs" or "Run the freshness check now."

The main agent dispatches the same `doc-freshness-checker` sub-agent and presents the report when it completes.

## Output

This skill does not produce a dedicated artifact. Its outputs are:

- **Inline citations** in whatever phase artifact the lookup supported.
- **Proposed updates** to `memory/long-term/domain-knowledge.md` or `terminology.md`, surfaced to the user via the binary approval gate ("Proposed addition to [file]: [summary]. Approve?") at the next gate — written only on an explicit yes/approve, never on "looks good" or silence.
- **Source log entry** (optional) in `<ENGAGEMENT_PATH>/decisions-log.md` when a lookup materially shaped a decision — note the URL, what it confirmed or refuted, and where the fact was applied.

## Boundaries (do not cross)

- The allowlist is **read-only documentation lookup**. This skill does not log in, submit forms, post to community, open support tickets, or execute anything.
- The agent **does not generate DQL** from documentation it just fetched. Doc examples are reference material; the team writes and runs queries.
- The agent **does not invent facts** when a lookup is inconclusive. If the doc is silent or the community thread is contradictory, surface that as a finding, not as an answer.
- The agent **does not auto-expand the allowlist**. New sources require explicit user approval and a corresponding entry in the table above.
- The agent **does not fetch internal-system URLs** (Slack, Salesforce, internal wikis) until a dedicated tool integration exists and the user has approved its use.

## Common pitfalls

- **Web-first instead of memory-first.** Local memory exists precisely so the team is not paying for repeated lookups of the same fact. Always check `domain-knowledge.md` and `terminology.md` before reaching for the web.
- **Citing without dates.** Dynatrace documentation evolves continuously. Every citation needs both the page's own "Last updated" date and the agent's retrieval date — the first lets the refresh routine detect drift, the second drives the 7-day staleness threshold.
- **Reusing a stale citation.** A citation older than 7 days is presumed stale until re-validated. The agent does not paste a stale citation into a new phase artifact "because we cited it last week." Re-check first.
- **Ignoring the freshness report at session start.** The weekly routine writes to `memory/long-term/freshness-report.md`. If the agent starts a session without checking it, drifted citations make it into deliverables. Always check on session start.
- **Treating community threads as vendor commitment.** A community workaround can be load-bearing for an action plan, but it should be labeled as such and ideally corroborated with documentation or the team's own test.
- **Silent allowlist expansion.** Following a search-result link to a third-party blog and quoting it as if it were sanctioned. If it is not on the allowlist, ask first.
- **Auto-promoting findings into long-term memory.** Lookups land in the artifact and stay there. Long-term memory updates require the binary approval gate and an explicit yes/approve — never a write on "looks good" or silence.
