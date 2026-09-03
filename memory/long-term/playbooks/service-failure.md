## Service failure spike

### When this applies

A hypothesis names elevated error rate (5xx, gRPC errors, span-status errors, or unhandled exceptions) on a specific service or call path.

### Investigation sequence

1. Open **Failure Analysis** for the suspected service. Dynatrace detects failed states based on **HTTP/gRPC response codes, span status, and the presence of exceptions within traces** — read all three.
2. In the failed-trace list, drill down to **service failure causes**. Group by exception type or HTTP status code to see whether one root error dominates or whether the failure is broad.
3. Open **Exception Analysis** for the dominant exception. Errors are captured as span attributes with type, message, stack trace, and timestamp — read the stack trace, not just the message.
4. Use the **Spans** view filtered to failed spans and grouped by **Service** and **Endpoint** to confirm whether the failure is endpoint-scoped or service-wide.
5. Confirm against any open **Davis problem** for the same window — Davis correlates events with the same root cause into a single problem, so the problem record may already name the originating entity.

### What "confirmed" looks like

- A specific exception type or HTTP status code accounts for the failure spike, with a recognizable stack trace, and the same signature appears across the failing traces.
- The endpoint or call path producing the failures is identifiable, not spread uniformly across the service.

### What "ruled out" looks like

- The service's failure rate is steady across the affected window and Failure Analysis shows no new exception types, no new failing endpoints, and no Davis problem.

### Common dead-ends

- Reading the exception **message** without the stack trace. Messages are often generic ("connection refused"); the stack trace says where in the code path the failure originated.
- Treating 4xx and 5xx the same. 4xx usually points upstream (bad input, client/protocol issue); 5xx usually points to the service itself. Investigate them separately.

### Source

- https://docs.dynatrace.com/docs/observe/application-observability/services/failure-analysis — page last-updated 2025-10-23; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/observe/application-observability/distributed-tracing/exception-analysis — page last-updated 2026-01-12; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/analyze-explore-automate/distributed-traces/use-cases/error-analysis — page last-updated 2024-05-17; retrieved 2026-05-20.
