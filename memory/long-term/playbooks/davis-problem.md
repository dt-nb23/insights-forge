## Reading a Davis problem

### When this applies

The investigation starts from an open Davis problem (the team was paged, the Problems app surfaced an issue) rather than from a hypothesis. The agent's job is to extract the problem's structure before generating hypotheses.

### Investigation sequence

1. Open the **Problems app** and select the problem. Read the problem title, severity, and time window first.
2. Read the **root cause entity** — Davis marks one entity with a red mark as the suggested starting point. Treat this as Davis's hypothesis, not as truth; it is a starting point for investigation.
3. Scan the **Affected entities** section to see the blast radius — entity types and event counts. A problem with a single affected service is a different shape from one with 40 affected services and a shared dependency.
4. Read the **events timeline** within the problem. Davis correlates events that share a root cause into a single problem; the timeline shows the sequence in which symptoms appeared.
5. Use the root cause entity and event sequence to seed Phase 1 hypotheses — typically the matching playbook (latency-backend, service-failure, deploy-correlation, etc.) — rather than restarting from scratch.

### What "confirmed" looks like

- The Davis-suggested root cause entity, when investigated with the matching playbook, produces a coherent story for the entire affected-entity list.

### What "ruled out" looks like

- The Davis-suggested root cause does not explain the observed symptoms when investigated, **or** affected entities exist that have no causal path from the suggested root.

### Common dead-ends

- Treating Davis's root cause as the answer. Davis's job is to propose; the team's job is to verify. The red-mark entity is where to *start*, not where to *stop*.
- Ignoring the affected-entity list. The blast radius shape (one service vs many services on a shared dependency) usually picks the playbook for you.

### Source

- https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/root-cause-analysis/davis-problems-app — page last-updated 2026-04-08; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/platform/davis-ai/problem-and-root-cause — page last-updated 2026-01-28; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/root-cause-analysis/concepts/events — page last-updated 2026-05-04; retrieved 2026-05-20.
