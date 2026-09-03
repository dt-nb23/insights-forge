## Log investigation in Grail

### When this applies

A hypothesis depends on log evidence — error volume in a window, specific error messages, log-derived metrics, parsed fields not exposed elsewhere.

### Investigation sequence

1. Frame the question as a **DQL pipeline shape** before opening any UI: `fetch <data> → filter <predicate> → summarize <aggregation>`. The agent describes this pipeline to the team in plain English; **the team writes the DQL** (per CLAUDE.md).
2. Specify the **data source** for `fetch` — logs, events, business events, security data, spans, or metrics — and the time window (`from:` parameter).
3. Specify the **filter** predicates needed: field operators (`==`, `!=`), substring matching (`contains`, `endsWith`), and any field extraction patterns required (DPL — Dynatrace Pattern Language — with elements like `LD:` for line data and typed fields like `INT:httpstatus`).
4. Specify the **aggregation** needed in `summarize` — count, distinct, percentile, time-bucketed series — and the group-by dimensions.
5. Hand the pipeline shape to the team alongside the hypothesis. The team validates the query and shares the result back as evidence on the hypothesis row.

### What "confirmed" looks like

- The team's executed query returns the expected pattern (volume, rate, distribution) and the shape matches the hypothesis's expected signal.

### What "ruled out" looks like

- The query executes against the right window and returns flat or absent signal where the hypothesis predicted a change.

### Common dead-ends

- Asking the team to "look at the logs". Logs without a query are archaeological. Always specify the pipeline shape.
- Forgetting the **time window**. DQL queries default to a UI-selected window; the hypothesis specifies what window is meaningful — pass it through.
- Querying without a parsing strategy when the field is unstructured. If the relevant data is inside a free-text message, the team will need a `parse` step with a DPL pattern; flag this up front.

### Source

- https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/dql-guide — page last-updated 2026-05-04; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/filtering-commands — page last-updated 2026-05-07; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/aggregation-commands — page last-updated 2026-03-23; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/extraction-and-parsing-commands — page last-updated 2024-08-12; retrieved 2026-05-20.
