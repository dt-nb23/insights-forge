# Stakeholder Profiles

One profile per role archetype the agent regularly produces outputs for. The agent reads the matching profile before drafting any Phase 3 deliverable so the tone, depth, and emphasis match what that reader actually wants. Updated only on explicit user approval.

## How to use this file

When a Phase 3 one-pager or deck is intended for a specific reader, match them to the closest role archetype here. Titles vary widely across organizations — focus on what the person owns and decides, not what their badge says. If no profile is close enough, ask the consultant whether to create a new one.

## Profile template

Each profile carries the same fields. Keep entries short and concrete — "they ignore vendor logos in the appendix" is more useful than "they value clarity".

---

## Executive Sponsor

- **Typical titles**: CTO, CIO, VP of Engineering, VP of Technology, SVP of Digital, EVP of Digital Channels
- **What they care about**: Business outcomes, risk, and ROI. Wants to know what the problem costs the business, what the fix requires, and what happens if nothing is done. Does not read technical detail unless it is directly load-bearing for a decision.
- **What they ignore**: Query syntax, dashboard screenshots, vendor feature lists, anything that reads like a status update without a decision attached.
- **Preferred level of detail**: One page maximum. Lead with business impact. Three bullets of findings, three bullets of recommended actions, one clear decision ask. Appendix only if explicitly requested.
- **Typical questions they ask**:
  - "What is this costing us in revenue, customers, or reputation?"
  - "What do I need to approve to fix it?"
  - "What happens if we do nothing for another 30 days?"
  - "Who owns this and when will it be resolved?"
- **Decisions they own**: Budget allocation; go/no-go on significant remediation or tooling investment; cross-organizational priority calls; vendor strategy.
- **Tone notes**: Direct. No hedging. Tradeoffs surfaced in the same sentence as recommendations. Translate every technical finding into a business outcome before presenting it.

---

## Product Owner

- **Typical titles**: Product Manager, Senior Product Manager, Director of Product, VP of Product
- **What they care about**: User experience, feature velocity, release risk, and whether the application is behaving the way it was designed to. Wants to understand how technical signals connect to what users actually experience.
- **What they ignore**: Infrastructure-level detail that doesn't connect to a user journey or a product surface. Pure SRE framing without UX translation.
- **Preferred level of detail**: Moderate. Will engage with funnel data, session-level patterns, and user journey breakdowns. Needs findings framed around specific product surfaces or features, not generic service names.
- **Typical questions they ask**:
  - "Which users are affected and on which part of the product?"
  - "Is this correlated with a specific release or feature flag?"
  - "What does the user actually experience when this happens?"
  - "How does this affect our retention or activation metrics?"
- **Decisions they own**: Feature prioritization; release go/no-go; A/B test design; instrumentation requirements for new features.
- **Tone notes**: Frame findings around user journeys, not service topologies. Connect technical signals to product outcomes. Mention specific screens, flows, or user segments where possible.

---

## SRE / Reliability Engineer

- **Typical titles**: Site Reliability Engineer, Reliability Engineer, Director of SRE, Director of Reliability, Platform Reliability Lead
- **What they care about**: SLO health, error budget burn, incident patterns, instrumentation maturity, and blameless retrospective culture. Wants the data to be defensible and the exit criteria to be pre-agreed.
- **What they ignore**: Recommendations that don't tie back to a specific SLI, SLO, or error budget. Hype language. Findings stated without supporting telemetry.
- **Preferred level of detail**: High tolerance for technical depth. Will follow trace IDs, dashboard links, and DQL references if they support the argument. One-pager plus technical appendix is welcome.
- **Typical questions they ask**:
  - "Which SLO did this affect and how much error budget did it burn?"
  - "Is this a recurring pattern or a one-off?"
  - "What instrumentation gap let this hide for as long as it did?"
  - "What's the long-term fix versus the immediate mitigation?"
- **Decisions they own**: SLO definition and revision; on-call practice changes; observability platform investment; reliability roadmap; instrumentation standards.
- **Tone notes**: Technical precision matters. SLI/SLO terminology must be used correctly. Treat error-budget framing as load-bearing language. Cite the telemetry source for every finding.

---

## IT Operations Manager

- **Typical titles**: IT Operations Manager, Head of IT Operations, Infrastructure Manager, NOC Manager, Director of Infrastructure
- **What they care about**: Day-to-day stability, alert noise reduction, MTTR, team capacity, and keeping the lights on without burning out the on-call team. Pragmatic — wants tools and processes that work reliably, not theoretical frameworks.
- **What they ignore**: Academic framing, long-term strategic recommendations without a near-term action, anything that adds to their team's workload without a clear payoff.
- **Preferred level of detail**: Moderate. Wants actionable findings with clear owners and timeframes. Tolerates technical depth only when it directly informs an operational decision.
- **Typical questions they ask**:
  - "How do we reduce the alert noise from this?"
  - "Which of my team's existing processes does this change?"
  - "What does this require from my team to implement?"
  - "How long until we see the benefit?"
- **Decisions they own**: On-call roster and escalation paths; monitoring tool configuration; incident response process; day-to-day infrastructure prioritization.
- **Tone notes**: Practical and concrete. Frame recommendations as operational changes, not strategic initiatives. Owner and timeframe on every action. Avoid acronym-heavy framing unless they use it themselves.

---

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

---

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

---

## Security / Compliance Officer

- **Typical titles**: CISO, Chief Security Officer, Director of Security, Compliance Manager, Risk Officer, VP of Information Security
- **What they care about**: Audit trails, vulnerability exposure, regulatory risk, data handling compliance, and whether the tooling introduces new attack surface. In FSI and Healthcare, regulatory framing (SOC 2, PCI-DSS, HIPAA) is often load-bearing.
- **What they ignore**: Performance findings that don't connect to a security or compliance risk. Technical detail without a risk or regulatory translation.
- **Preferred level of detail**: Moderate. Wants findings framed as risks with likelihood and impact. Will engage with technical detail only when it directly supports a compliance or risk argument.
- **Typical questions they ask**:
  - "Does this introduce new data exposure or attack surface?"
  - "Is this finding relevant to our SOC 2 / PCI-DSS / HIPAA posture?"
  - "What is the audit trail for this change?"
  - "What is our liability if this goes unaddressed?"
- **Decisions they own**: Security tooling approval; data handling policy; regulatory reporting; vendor risk assessment; access control policy.
- **Tone notes**: Risk and compliance framing first. Translate technical findings into risk statements with likelihood and potential regulatory consequence. Cite regulatory frameworks by name when relevant. Avoid performance-centric language unless it connects to a security risk.

---

## Data / Analytics Lead

- **Typical titles**: Head of Data Analytics, VP of Analytics, Director of Business Intelligence, Chief Data Officer, Analytics Engineering Manager
- **What they care about**: Data quality, instrumentation coverage, the integrity of the metrics being cited, whether the conclusion is statistically defensible, and whether funnel attribution holds up under scrutiny.
- **What they ignore**: Backend-only framing without a business KPI translation. Conclusions stated without confidence intervals or methodology. Single-point estimates presented as ground truth.
- **Preferred level of detail**: High. Wants the numbers, the time windows, the segments, and the methodology. Will push back on anything stated without context. Appendix with methodology is welcome and expected.
- **Typical questions they ask**:
  - "What's the confidence interval on that number?"
  - "How did we segment the population?"
  - "Are we comparing like to like in the before/after window?"
  - "Which KPI does this actually move, and by how much?"
- **Decisions they own**: Metrics definition; experiment readouts; analytics roadmap; data team prioritization; instrumentation requirements for business events.
- **Tone notes**: Cite the source telemetry; name the time window; acknowledge confounders. Translate technical signals into KPI deltas with explicit math. Never present a single number without its denominator and time window.

---

## [Add new profiles below as needed. Maintain the same field structure.]
