## Frontend / UX regression in RUM

### When this applies

A hypothesis names a user-visible problem — page slowness, abandoned flows, browser/device-specific errors, regional regressions, route-transition failures.

### Investigation sequence

1. Open **Users & Sessions** in the **New RUM Experience** for the affected application and the affected time window.
2. **Filter sessions** by duration, frontend, browser, browser window width, and location to find the segment that is regressed. The filter axes most often load-bearing are **browser/OS** (for client-side regressions), **location/region** (for CDN or network), and **route/view** (for page-scoped regressions).
3. **Sort by navigation count** to isolate the longest, most-deeply-engaged sessions and review the per-event timing — domain lookup, connection time, request duration, DOM processing — to identify which phase regressed.
4. Open **Error Inspector** to see the JS errors and HTTP failures grouped by frontend and route. Cross-check with the RUM-side failure list — RUM JS errors are independent of backend 5xx and often reveal client-side regressions that backend telemetry will miss.
5. If frontend timing isolates the regression to backend latency (e.g., long request duration), hand off to the latency-backend playbook using the named endpoint.

### What "confirmed" looks like

- A specific segment (browser/OS, region, route) shows the regression and an adjacent segment does not.
- The regressed timing phase is identified (lookup vs connect vs request vs DOM) — not a vague "page is slower".

### What "ruled out" looks like

- Session distributions, timing phases, and Error Inspector counts are flat across the affected window when sliced by the candidate segmentation axes.

### Common dead-ends

- Looking at aggregate RUM dashboards before filtering. The whole-app view almost always looks fine when the regression is segment-specific.
- Ignoring browser/OS and region. These are the highest-signal segmentation axes for frontend regressions and the first place to look.

### Source

- https://docs.dynatrace.com/docs/observe/digital-experience/new-rum-experience/users-and-sessions — page last-updated 2026-04-29; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/observe/digital-experience/new-rum-experience/error-inspector — page last-updated 2026-01-08; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/observe/digital-experience/rum-concepts/rum-overview — page last-updated 2023-10-20; retrieved 2026-05-20.
