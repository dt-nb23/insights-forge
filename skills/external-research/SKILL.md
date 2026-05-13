---
name: external-research
description: Procedure for consulting domain knowledge and approved external references (Dynatrace docs, community posts) during an investigation. Use whenever a Dynatrace concept, feature, or terminology question arises that cannot be answered from project-space alone.
---

# External Research

## When to use

Use this skill any time the investigation needs authoritative reference material that is **not already captured** in `memory/long-term/` or `memory/project-space/`. Typical triggers:

- A stakeholder uses a Dynatrace concept the agent is not sure it has defined correctly (e.g., Grail retention, DPS billing units, Davis problem grouping, Smartscape topology semantics).
- A hypothesis or signal mapping depends on the precise behavior of a Dynatrace feature (RUM session capture, OneAgent vs OpenTelemetry ingest, DQL operators).
- A community thread is the only place a known issue, workaround, or migration nuance is documented.
- The team wants to confirm a default value, a quota, or a deprecation timeline before recommending an action.

If the answer is already in `memory/long-term/domain-knowledge.md` or `memory/long-term/terminology.md`, prefer that. Only reach for the web when local memory is silent, contradictory, or stale.

## Inputs

Read these files first:

- `memory/long-term/dynatrace-playbooks.md` — for **procedural** questions ("how do I investigate X in Dynatrace?"). Eight playbooks cover the common problem shapes; each carries its own doc citations. If the playbook answers the question, stop — no web fetch needed.
- `memory/long-term/domain-knowledge.md` — for the Dynatrace concept definitions and the "Authoritative external references" section that lists approved sources.
- `memory/long-term/terminology.md` — for terms the team has already defined.
- `memory/project-space/current-context.md` — to scope the question to the active investigation.

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

1. **Check local memory first.** For *procedural* questions ("how do I…") skim `dynatrace-playbooks.md`; for *conceptual* questions ("what is…") skim `domain-knowledge.md` and `terminology.md`. If the answer is already there and current, use it and stop.
2. **Frame the lookup as a specific question.** "Does Davis AI group multi-service problems by default?" is researchable. "Tell me about Davis" is not. Write the question down before fetching anything.
3. **Search within the allowlist when the URL is unknown.** Use `WebSearch` with a `site:docs.dynatrace.com` or `site:community.dynatrace.com` filter. Prefer documentation hits over community hits unless the question is specifically about practitioner experience.
4. **Fetch the most authoritative result.** Prefer `docs.dynatrace.com` for feature behavior and defaults. Use `community.dynatrace.com` for known-issue corroboration, not for ground truth on product behavior.
5. **Extract only what answers the question.** Pull the relevant fact, definition, or constraint. Do not dump full page contents into project memory. Quote sparingly and cite.
6. **Cite every fact from an external source.** Inline cite the URL and the **retrieval date** (today's date) wherever the fact lands — in `hypotheses.md`, `signals-map.md`, `action-plan.md`, the one-pager, or the deck. Citation format:

   > Davis AI groups related events into a single problem when they share dependencies in Smartscape. *(Source: https://docs.dynatrace.com/…/davis-problem-detection — retrieved 2026-05-12.)*

7. **Distinguish vendor doc from community report.** When citing community threads, label them as practitioner reports (e.g., "community thread; not vendor-confirmed"). Do not promote a community post to documentation-level confidence without corroboration.
8. **Offer to update long-term memory.** If a lookup surfaces a durable fact the team will want again — a Dynatrace concept definition, a quota, a known issue — propose adding it to `memory/long-term/domain-knowledge.md` or `terminology.md`. **Do not write to long-term memory without the user's explicit approval** (per the rule in `memory/long-term/README.md`).

## Output

This skill does not produce a dedicated artifact. Its outputs are:

- **Inline citations** in whatever phase artifact the lookup supported.
- **Proposed updates** to `memory/long-term/domain-knowledge.md` or `terminology.md`, surfaced to the user for approval at the next gate.
- **Source log entry** (optional) in `memory/project-space/decisions-log.md` when a lookup materially shaped a decision — note the URL, what it confirmed or refuted, and where the fact was applied.

## Boundaries (do not cross)

- The allowlist is **read-only documentation lookup**. This skill does not log in, submit forms, post to community, open support tickets, or execute anything.
- The agent **does not generate DQL** from documentation it just fetched. Doc examples are reference material; the team writes and runs queries.
- The agent **does not invent facts** when a lookup is inconclusive. If the doc is silent or the community thread is contradictory, surface that as a finding, not as an answer.
- The agent **does not auto-expand the allowlist**. New sources require explicit user approval and a corresponding entry in the table above.
- The agent **does not fetch internal-system URLs** (Slack, Salesforce, internal wikis) until a dedicated tool integration exists and the user has approved its use.

## Common pitfalls

- **Web-first instead of memory-first.** Local memory exists precisely so the team is not paying for repeated lookups of the same fact. Always check `domain-knowledge.md` and `terminology.md` before reaching for the web.
- **Citing without a retrieval date.** Dynatrace documentation evolves. A 2024 citation may no longer hold in 2026 — the date matters.
- **Treating community threads as vendor commitment.** A community workaround can be load-bearing for an action plan, but it should be labeled as such and ideally corroborated with documentation or the team's own test.
- **Silent allowlist expansion.** Following a search-result link to a third-party blog and quoting it as if it were sanctioned. If it is not on the allowlist, ask first.
- **Auto-promoting findings into long-term memory.** Lookups land in the artifact and stay there. Long-term memory updates require the user's explicit go-ahead.
