# Dynatrace Doc Citation Freshness Report

Written by the `doc-freshness-checker` sub-agent (defined in `.claude/agents/doc-freshness-checker.md`).
The main agent dispatches it as a Haiku background task at the start of every Phase 0 (context-framing) and reads this report at the Phase 0 gate. The user can also trigger a manual refresh at any time.

The sub-agent **never edits `domain-knowledge.md` or `dynatrace-playbooks.md` directly**. It only writes here. Updates to long-term memory require explicit user approval at a phase gate.

---

## Last refresh

- **Run date:** 2026-06-29
- **Source:** Phase 0 sub-agent (doc-freshness-checker) — U-Haul digital-experience-parity engagement
- **URLs in scope:** 28 unique Dynatrace documentation URLs
- **Gate action:** All 8 drifted entries approved and applied to long-term memory at Phase 0 gate (2026-06-29). Freshness report cleared.

---

## Drifted — re-check before reuse

_None. All 8 drifted entries from the 2026-06-29 run were approved and applied at the Phase 0 gate._

---

## Unreachable — verify redirect or 404

_None._

---

## Unchanged — verified current

Baselines last captured or updated 2026-06-29.

### domain-knowledge.md

| URL | Stored page-last-updated | Last checked |
|---|---|---|
| https://docs.dynatrace.com/docs/manage/dynatrace-platform-subscription | 2026-05-04 | 2026-06-29 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-grail | 2026-01-28 | 2026-06-29 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language | 2026-01-28 | 2026-06-29 |
| https://docs.dynatrace.com/docs/platform/smartscape | 2017-07-19 | 2026-06-29 |
| https://docs.dynatrace.com/docs/platform/davis-ai | 2026-01-28 | 2026-06-29 |
| https://docs.dynatrace.com/docs/manage/identity-access-management/permission-management/management-zones | 2018-09-25 | 2026-06-29 |
| https://docs.dynatrace.com/docs/ingest-from/dynatrace-oneagent | 2018-10-09 | 2026-06-29 |
| https://docs.dynatrace.com/docs/observe/digital-experience/rum-concepts/rum-overview | 2023-10-20 | 2026-06-29 |

### dynatrace-playbooks.md

| URL | Stored page-last-updated | Last checked |
|---|---|---|
| https://docs.dynatrace.com/docs/observe/application-observability/distributed-traces/analysis/get-started | 2024-08-13 | 2026-06-29 |
| https://docs.dynatrace.com/docs/observe/application-observability/distributed-tracing/use-traces-and-dql-to-spot-patterns | 2025-11-20 | 2026-06-29 |
| https://docs.dynatrace.com/docs/observe/application-observability/services/services-app | 2026-05-29 | 2026-06-29 |
| https://docs.dynatrace.com/docs/observe/application-observability/services/failure-analysis | 2025-10-23 | 2026-06-29 |
| https://docs.dynatrace.com/docs/observe/application-observability/distributed-tracing/exception-analysis | 2026-01-12 | 2026-06-29 |
| https://docs.dynatrace.com/docs/analyze-explore-automate/distributed-traces/use-cases/error-analysis | 2024-05-17 | 2026-06-29 |
| https://docs.dynatrace.com/docs/observe/digital-experience/new-rum-experience/users-and-sessions | 2026-04-29 | 2026-06-29 |
| https://docs.dynatrace.com/docs/observe/digital-experience/new-rum-experience/error-inspector | 2026-01-08 | 2026-06-29 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/dql-guide | 2026-05-04 | 2026-06-29 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/filtering-commands | 2026-05-07 | 2026-06-29 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/aggregation-commands | 2026-03-23 | 2026-06-29 |
| https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/extraction-and-parsing-commands | 2024-08-12 | 2026-06-29 |
| https://docs.dynatrace.com/docs/deliver/service-level-objectives | 2026-03-17 | 2026-06-29 |
| https://docs.dynatrace.com/docs/deliver/release-monitoring/monitor-releases-with-dynatrace | 2025-08-11 | 2026-06-29 |
| https://docs.dynatrace.com/docs/deliver/release-monitoring/version-detection-strategies | 2025-08-11 | 2026-06-29 |
| https://docs.dynatrace.com/docs/deliver/pipeline-observability-sdlc-events | 2026-06-09 | 2026-06-29 |
| https://docs.dynatrace.com/docs/observe/digital-experience/synthetic-monitoring | 2018-09-25 | 2026-06-29 |
| https://docs.dynatrace.com/docs/observe/digital-experience/synthetic-monitoring/network-availability-monitors/network-availability-monitoring | 2024-08-08 | 2026-06-29 |
| https://docs.dynatrace.com/docs/observe/applications-and-microservices/services/service-detection-v1/monitor-3rd-party-services | 2023-02-21 | 2026-06-29 |
| https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/root-cause-analysis/davis-problems-app | 2026-06-19 | 2026-06-29 |
| https://docs.dynatrace.com/docs/platform/davis-ai/problem-and-root-cause | 2026-01-28 | 2026-06-29 |
| https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/root-cause-analysis/concepts/events | 2026-05-04 | 2026-06-29 |

---

## Skipped — out of allowlist

_None. All cited URLs are within the `docs.dynatrace.com` allowlist._

---

## Operating notes

- When the user approves an update at a phase gate, the main agent edits the relevant long-term memory file inline (bumping page-last-updated and retrieved), then **clears the entry from the Drifted / Unreachable tables above** and moves it back into Unchanged with today's last-checked date.
- The `Stored page-last-updated` entries showing dates in 2017–2018 are pages where Dynatrace's current "Last updated" timestamp reflects the original publish date (not a content revision). Monitor these for actual content changes, not date drift.
- If the sub-agent fails entirely (network error, rate limit), the next-run report will note that — silence is not a signal that everything is fine.
