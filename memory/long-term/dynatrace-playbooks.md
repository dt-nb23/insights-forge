# Dynatrace Investigation Playbooks

Client-agnostic procedural patterns for using Dynatrace to investigate common problem shapes. **These describe the workflow, not the configuration** — no specific Management Zone names, service names, or environment IDs appear here. Org-specific behavior (which Smartscape views the team trusts, which synthetic tests are load-bearing, which Davis problem types get auto-actioned) lives in `domain-knowledge.md`.

## How to use this file

- **Phase 1 (hypothesis generation)** — when a hypothesis names a problem shape (latency, errors, UX, etc.), the agent pulls the matching playbook's investigation sequence into the "validation approach" field and the playbook's "confirmed" / "ruled out" criteria into exit criteria.
- **Phase 2 (action plan)** — the playbook seeds the investigation-action rows. Each step becomes a candidate action with the playbook's source URL carried through as the citation.
- **Phase 3 (one-pager and deck)** — the playbook's "what good evidence looks like" anchors the "Top findings" framing so the deliverable matches what the team actually observed.

Playbook content was originally sourced from `docs.dynatrace.com` on 2026-05-12; baseline page-last-updated values for every citation were captured on 2026-05-20 by the `doc-freshness-checker` sub-agent (see `skills/external-research/SKILL.md`). Each citation in the individual playbook files carries both dates; the sub-agent re-validates them at the start of every Phase 0. Re-verify before relying on a procedural detail in a deliverable; product surfaces evolve.

## Playbook index

Individual playbooks live in `memory/long-term/playbooks/`. Read the matching file only when a hypothesis names its problem shape — do not load all playbooks at session start.

| Problem shape | File |
|---|---|
| Latency degradation on a backend service | `memory/long-term/playbooks/latency-backend.md` |
| Error rate / failure spike on a service | `memory/long-term/playbooks/service-failure.md` |
| User-visible slowness or errors in the browser/app | `memory/long-term/playbooks/frontend-rum.md` |
| Anomalous behavior in logs (volume, errors, content) | `memory/long-term/playbooks/log-grail.md` |
| SLO at risk or breached | `memory/long-term/playbooks/slo-burn.md` |
| Regression correlated with a deploy | `memory/long-term/playbooks/deploy-correlation.md` |
| Third-party dependency suspected | `memory/long-term/playbooks/third-party.md` |
| Triage starting from an open Davis problem | `memory/long-term/playbooks/davis-problem.md` |

**Traverse-on-need rule:** When Phase 1 matches a hypothesis to a problem shape, read only the file(s) for that shape. The investigation sequence, exit criteria, and source citations live in the individual file. The doc-freshness checker reads all files in `memory/long-term/playbooks/` to validate citations.

## What this file deliberately does NOT contain

- **Executable DQL.** The agent describes the pipeline shape (`fetch → filter → summarize`) in plain English. The team writes and runs the query.
- **Specific Management Zone names, service names, or environment IDs.** Those are client/team-specific and live in `domain-knowledge.md` brackets.
- **UI click paths past one level of detail.** Dynatrace UI evolves faster than the conceptual workflow. The playbooks name the *artifact* (Services app, Failure Analysis, Users & Sessions) and let the team click into it.
- **Recommendations on whether to use Classic vs new Apps.** Where both exist, the playbook names the concept and lets the team pick the surface their environment runs.
- **Configuration guidance.** This file is for *how to investigate*, not *how to set up*. SLO configuration, failure-detection rules, and synthetic test creation are out of scope here.

