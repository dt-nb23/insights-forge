# Dynatrace Doc Citation Freshness Report

Written by the `doc-freshness-checker` sub-agent (defined in `.claude/agents/doc-freshness-checker.md`).
The main agent dispatches it as a Haiku background task at the start of every Phase 0 (context-framing) and reads this report at the Phase 0 gate. The user can also trigger a manual refresh at any time.

The sub-agent **never edits `domain-knowledge.md` or `dynatrace-playbooks.md` directly**. It only writes here. Updates to long-term memory require explicit user approval at a phase gate.

---

## Last refresh

- **Run date:** 2026-05-20
- **Source:** `doc-freshness-checker` sub-agent (manual test dispatch via general-purpose+haiku) + post-run baseline migration approved by user
- **Cadence:** per engagement (every Phase 0) + on-demand
- **URLs in scope:** 23 unique Dynatrace doc citations across `domain-knowledge.md` (8 citations), `dynatrace-playbooks.md` (16 citations after the 2026-05-20 cleanup of the broken `service-level-objective-basics` URL), and `terminology.md` (8 citations — 7 URLs overlap with `domain-knowledge.md`, so no new unique URLs added)

## Drifted (page rewritten since our citation, or baseline missing)

_None. All citations were migrated from legacy single-date format to dual-date format on 2026-05-20 and now carry their captured page-last-updated values._

## Unreachable (404, redirect, or timeout)

_None. The broken `https://docs.dynatrace.com/docs/deliver/service-level-objectives/service-level-objective-basics` citation was removed from `dynatrace-playbooks.md` on 2026-05-20 — its parent page `https://docs.dynatrace.com/docs/deliver/service-level-objectives` (reachable; last-updated 2026-03-17) covers the same SLO material and is the remaining citation in the SLO breach playbook._

## Unchanged (verified current)

Baselines captured 2026-05-20. The next sub-agent run will compare each stored page-last-updated against the current value.

### domain-knowledge.md

| URL | Stored page-last-updated | Last checked |
|---|---|---|
| https://docs.dynatrace.com/docs/manage/dynatrace-platform-subscription | 2025-09-03 | 2026-05-20 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-grail | 2026-01-28 | 2026-05-20 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language | 2026-01-28 | 2026-05-20 |
| https://docs.dynatrace.com/docs/platform/smartscape | unknown | 2026-05-20 |
| https://docs.dynatrace.com/docs/platform/davis-ai | 2026-01-28 | 2026-05-20 |
| https://docs.dynatrace.com/docs/manage/identity-access-management/permission-management/management-zones | unknown | 2026-05-20 |
| https://docs.dynatrace.com/docs/ingest-from/dynatrace-oneagent | unknown | 2026-05-20 |
| https://docs.dynatrace.com/docs/observe/digital-experience/rum-concepts/rum-overview | 2023-10-20 | 2026-05-20 |

### terminology.md

The 8 citations in `terminology.md` (Grail, DQL, Smartscape, Davis AI, OneAgent, Management Zones, DPS, RUM session) all reference URLs that also appear in `domain-knowledge.md` (entries above) plus one in `dynatrace-playbooks.md`. Stored page-last-updated values and last-checked dates match the corresponding rows in those sections; no separate baselines required.

### dynatrace-playbooks.md

| URL | Stored page-last-updated | Last checked |
|---|---|---|
| https://docs.dynatrace.com/docs/observe/application-observability/distributed-traces/analysis/get-started | 2024-08-13 | 2026-05-20 |
| https://docs.dynatrace.com/docs/observe/application-observability/distributed-tracing/use-traces-and-dql-to-spot-patterns | 2025-11-20 | 2026-05-20 |
| https://docs.dynatrace.com/docs/observe/application-observability/services/services-app | 2026-05-19 | 2026-05-20 |
| https://docs.dynatrace.com/docs/observe/application-observability/services/failure-analysis | 2025-10-23 | 2026-05-20 |
| https://docs.dynatrace.com/docs/observe/application-observability/distributed-tracing/exception-analysis | 2026-01-12 | 2026-05-20 |
| https://docs.dynatrace.com/docs/analyze-explore-automate/distributed-traces/use-cases/error-analysis | 2024-05-17 | 2026-05-20 |
| https://docs.dynatrace.com/docs/observe/digital-experience/new-rum-experience/users-and-sessions | 2026-04-29 | 2026-05-20 |
| https://docs.dynatrace.com/docs/observe/digital-experience/new-rum-experience/error-inspector | 2026-01-08 | 2026-05-20 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/dql-guide | 2026-05-04 | 2026-05-20 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/filtering-commands | 2026-05-07 | 2026-05-20 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/aggregation-commands | 2026-03-23 | 2026-05-20 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/extraction-and-parsing-commands | 2024-08-12 | 2026-05-20 |
| https://docs.dynatrace.com/docs/deliver/service-level-objectives | 2026-03-17 | 2026-05-20 |
| https://docs.dynatrace.com/docs/deliver/release-monitoring/monitor-releases-with-dynatrace | 2025-08-11 | 2026-05-20 |
| https://docs.dynatrace.com/docs/deliver/release-monitoring/version-detection-strategies | 2025-08-11 | 2026-05-20 |
| https://docs.dynatrace.com/docs/deliver/pipeline-observability-sdlc-events | 2025-05-04 | 2026-05-20 |
| https://docs.dynatrace.com/docs/observe/digital-experience/synthetic-monitoring | unknown | 2026-05-20 |
| https://docs.dynatrace.com/docs/observe/digital-experience/synthetic-monitoring/network-availability-monitors/network-availability-monitoring | 2024-08-08 | 2026-05-20 |
| https://docs.dynatrace.com/docs/observe/applications-and-microservices/services/service-detection-v1/monitor-3rd-party-services | 2023-02-21 | 2026-05-20 |
| https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/root-cause-analysis/davis-problems-app | 2026-04-08 | 2026-05-20 |
| https://docs.dynatrace.com/docs/platform/davis-ai/problem-and-root-cause | 2026-01-28 | 2026-05-20 |
| https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/root-cause-analysis/concepts/events | 2026-05-04 | 2026-05-20 |

## Skipped — out of allowlist

_None. All cited URLs are within the `docs.dynatrace.com` allowlist._

---

## Operating notes

- When the user approves an update at a phase gate, the main agent edits the relevant long-term memory file inline (bumping page-last-updated and retrieved), then **clears the entry from the Drifted / Unreachable tables above** and moves it back into Unchanged with today's last-checked date.
- The `Stored page-last-updated: unknown` entries above are pages where Dynatrace does not advertise a "Last updated" timestamp at the top. The sub-agent re-checks these each run; classify as Drifted only if the page begins advertising a date that we can capture.
- If the sub-agent fails entirely (network error, rate limit), the next-run report will note that — silence is not a signal that everything is fine.
