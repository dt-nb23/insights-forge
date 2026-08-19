## Deploy / release correlation

### When this applies

A hypothesis names a deploy, release, or configuration change as the suspected cause — typically a step-function regression timestamped close to a known change event.

### Investigation sequence

1. Pull **deployment events** and **SDLC events** for the suspected service(s) in the affected window. Dynatrace shows process restart events and deployment events; SDLC events represent release, deploy, and quality-gate transitions emitted by CI/CD pipelines.
2. Confirm the **version detection** is reliable for the service — process version, package version, or container image tag — so the "before/after" comparison is clean.
3. Overlay the deploy timestamp on the affected metric (latency, error rate, RUM signal). A **step-function change at the deploy timestamp** is a strong signal; a slow drift starting before the deploy is not.
4. Read Dynatrace's **event correlation** for the same window — Davis correlates deployment events with downstream symptoms when the topology supports it. The correlation may already name the originating change.
5. Confirm against the team's change log / release notes for the deployed version. Without that confirmation, the correlation is suggestive, not proven.

### What "confirmed" looks like

- A clean step-function change in the affected SLI at the deployment timestamp, persisting through the post-deploy window, with a named version delta and a plausible mechanism in the change set.

### What "ruled out" looks like

- The metric was already trending before the deploy timestamp, **or** other instances on the same version are unaffected, **or** rolling back the version does not restore the SLI.

### Common dead-ends

- Treating temporal correlation as causation. A deploy and a CDN config change in the same hour are equally suspect until the change set is read.
- Trusting version detection silently. If the service's version label is stale or missing, the before/after comparison is unreliable — verify the version detection strategy first.

### Source

- https://docs.dynatrace.com/docs/deliver/release-monitoring/monitor-releases-with-dynatrace — page last-updated 2025-08-11; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/deliver/release-monitoring/version-detection-strategies — page last-updated 2025-08-11; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/deliver/pipeline-observability-sdlc-events — page last-updated 2025-05-04; retrieved 2026-05-20.
