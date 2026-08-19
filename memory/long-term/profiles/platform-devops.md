## Platform / DevOps Engineer

- **Typical titles**: Platform Engineer, DevOps Engineer, Infrastructure Engineer, Site Reliability Engineer (infrastructure-focused), Cloud Engineer
- **What they care about**: Deploy safety, pipeline reliability, observability coverage across the stack, and infrastructure-as-code consistency. Wants to know if a change they shipped caused something downstream and how to prevent it next time.
- **What they ignore**: Application-layer findings that don't connect to infrastructure or deployment events. Business framing without a technical hook.
- **Preferred level of detail**: High. Will engage with infrastructure metrics, deployment event correlation, OneAgent coverage gaps, and configuration-level findings. Appendix with technical detail is welcome.
- **Typical questions they ask**:
  - "Is this correlated with a deployment or infrastructure change?"
  - "Where are our OneAgent coverage gaps?"
  - "What configuration change would prevent this class of problem?"
  - "How do we instrument this in the pipeline?"
- **Decisions they own**: Infrastructure configuration; deployment pipeline design; OneAgent and instrumentation rollout; observability tooling standards.
- **Tone notes**: Technical and systems-level. Frame findings around infrastructure events, coverage gaps, and configuration. Connect to deployment events where possible. They think in systems — show the chain of causation.
