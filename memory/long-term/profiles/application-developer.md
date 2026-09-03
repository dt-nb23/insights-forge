## Application Developer

- **Typical titles**: Software Engineer, Senior Software Engineer, Staff Engineer, Lead Developer, Engineering Manager (technical)
- **What they care about**: Finding root cause fast, understanding how their service is behaving in production, and not being paged for things outside their control. Wants specific, actionable signal — not aggregated summaries.
- **What they ignore**: Business KPI framing without a technical translation. Broad platform-level findings that don't point to a specific service, endpoint, or code path.
- **Preferred level of detail**: High. Will engage with trace-level data, error details, specific endpoint behavior, and deployment correlation. Wants enough detail to act immediately.
- **Typical questions they ask**:
  - "Which endpoint or service is the source?"
  - "Is this correlated with our last deploy?"
  - "What does the trace show for the failing requests?"
  - "Is this happening for all users or a specific segment?"
- **Decisions they own**: Code-level fixes; hotfix prioritization; service-level instrumentation; local escalation to platform or infrastructure teams.
- **Tone notes**: Technical and specific. Name the service, the endpoint, the error type. Skip the business framing unless they ask. They want to fix it — give them what they need to do that.
