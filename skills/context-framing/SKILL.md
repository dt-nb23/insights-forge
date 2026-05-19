---
name: context-framing
description: Procedure for Phase 0 — understanding the customer engagement context, active Dynatrace capabilities, and stakeholder goals before surfacing insights or building any deliverable. Always use this skill at the start of a new engagement when a consultant describes a customer situation, mentions a customer name, references a Dynatrace environment, or says anything like "I have a QBR with X", "I need to show value to Y", "I'm working with a customer on Z", or "can you help me prepare for a customer engagement". This is the required first step — do not attempt MECE decomposition, hypothesis generation, or any Phase 1 work until this skill's gate has been passed.
---

# Context Framing

## When to use

**Phase 0 — the required first step of every engagement.** The agent reads this skill before asking the consultant a single clarifying question.

Use this skill when:

- A new engagement begins: a consultant describes a customer, a Dynatrace environment, an upcoming meeting, or a value-surfacing goal.
- The user has redirected scope after a Phase 0 gate and the framing needs to be reset.
- The existing `current-context.md` is stale and the user has asked to reframe.

**Do not advance to Phase 1 until the user explicitly approves the output of this skill.**

## Inputs

Read these files before starting:

- `memory/long-term/stakeholder-profiles.md` — to recognize named stakeholder types and calibrate what "exec-ready" means for this engagement.
- `memory/long-term/domain-knowledge.md` — for the tech → UX → business linkage table; helps identify which insights are likely surfaceable given the active capabilities.
- `memory/long-term/terminology.md` — to use consistent terminology when restating the engagement context.
- `memory/long-term/past-investigations.md` — scan the index for any prior engagement on the same customer, vertical, or problem shape. If a match exists, surface the key lesson from that archive before proceeding.

### Handling large upfront context blocks

If the consultant's opening message contains a detailed problem description, **extract answers before asking any questions**. Scan the description for answers to Q1, Q2, and each C.S.I.R. dimension. Mark each as captured or open. Begin the intake with only the questions that are not already answered. Before asking the first question, briefly state what you have already captured — this signals to the consultant that you read their input and prevents redundant questions.

If the consultant has not yet described the engagement, open with:

> "Tell me about the customer and what you're trying to accomplish with them."

Do not ask multiple questions at once. Let each answer drive the next question.

## Clarifying questions

Ask **one question at a time**, in adaptive order — if the consultant's opening description already answers a question, skip it and move to the next unknown. Stop asking when you have enough to write a confident context document.

The fifteen questions, in default order:

### Q1 — Customer and what they do
> "Who is the customer, and what does their business do?"

Capture: company name (or anonymized label), what product or service they sell, approximate size if known.

### Q2 — Customer vertical
> "Which industry vertical are they in?"

Common verticals: Retail / E-commerce, Financial Services (FSI), Healthcare / Life Sciences, Manufacturing, Telco / Media, Public Sector, Technology / SaaS, Logistics / Supply Chain. Accept the consultant's own label if it doesn't match this list.

The vertical shapes which KPIs matter to leadership and which signal → business linkages are most relevant in Phase 1.

### Q3 — Engagement Framing (C.S.I.R.)

Q3 is a structured sub-sequence, not a single question. Now that the customer and their vertical are established, use C.S.I.R. to lock in the full problem context before moving into environment and capability questions.

**Before asking any C.S.I.R. questions, scan the consultant's opening description for answers already provided.** Mark each dimension as captured or open. Only ask about open dimensions. Work through each open dimension in order, one prompt at a time.

#### C — Context
> "Walk me through the situation you're walking into — what's the history with this customer, and what's the mood heading into this engagement?"

Capture: relationship history (new logo, established customer, at-risk account), recent interactions or milestones, the consultant's role (CSM, SE, consultant, other), and the **engagement trigger** (QBR / renewal / expansion / scheduled touchpoint / other). The trigger shapes urgency, tone, and what a "good outcome" looks like.

*Why this matters:* The relationship context shapes tone, urgency, and how findings should be framed. An at-risk renewal and a healthy expansion require completely different narratives even if the Dynatrace data is identical.

#### S — Specific Information
> "What specific information do you already have — for example, known pain points, prior QBR outcomes, commitments made, or anything that limits or shapes what's possible?"

Capture: known environment facts, prior QBR outcomes, existing commitments, contract phase (new, renewal, expansion), known pain points, and any constraints (e.g., limited data access, regulated industry restrictions).

**Competitive context follow-up (ask only if the account is at-risk and a competitor is mentioned):**
> "Do you know which competitor they're evaluating, and what their pitch is — is it a feature gap, a cost argument, or something else?"

Capture: competitor name if known, their claimed differentiator (feature breadth, pricing, simplicity, open source / in-house), and any specific objections the customer has raised about Dynatrace. This shapes how the renewal narrative is framed — a cost-reduction play requires a different response than a feature-gap argument.

*Why this matters:* Specific information is the boundary of what's usable. Without it, orientation hypotheses in Step 5 will be generic rather than targeted.

#### I — Intent
> "What are you ultimately trying to accomplish — and what does a successful outcome look like for you as the consultant?"

Capture: the consultant's goal (e.g., prove value, secure renewal, justify expansion, prepare a QBR narrative) and the customer's expected outcome (e.g., confidence in their Dynatrace investment, a clear roadmap, reduced noise in their environment).

*Why this matters:* Intent shapes the consulting objective written in Step 4. If the consultant's goal is renewal and the customer's goal is cost justification, the deliverable must speak to ROI — not feature breadth.

#### R — Response Format
> "What does the deliverable need to look like — for example, a slide deck, a written findings report, a live walkthrough, a dashboard, or something else? And who is the primary audience?"

Capture: format (deck / report / walkthrough / dashboard / other), audience (exec / technical / mixed), and any known constraints on length, tone, or branding.

*Why this matters:* Format and audience determine how findings are packaged in Phase 3. An exec deck and a technical findings report require completely different structures, depths, and vocabularies.

---

**Q3 gate:** Before moving to Q4, confirm all four C.S.I.R. dimensions are captured, including the engagement trigger under C. If any are still unknown, ask one follow-up question to close the gap. Record Q3 outputs in `current-context.md` under "Engagement Framing (C.S.I.R.)".

### Q4 — Tenant type
> "Is this customer on a SaaS tenant or a Managed (on-premises) deployment?"

This affects which features and data are available and constrains what insights and recommendations are possible in later phases.

### Q5 — Dynatrace adoption maturity
> "How long has this customer been using Dynatrace, and how would you describe where they are in their adoption — early-stage, established, or mature?"

Capture: approximate time as a Dynatrace customer, and the consultant's read on adoption depth — are they actively using what they have, or is the deployment underutilized relative to their contract?

Common patterns:
- **Early-stage (0–12 months)** — instrumentation is likely incomplete, dashboards are sparse, and the team is still learning the platform. Unrealized value is expected and forgivable. The consulting narrative should focus on quick wins and a roadmap.
- **Established (1–3 years)** — core instrumentation is in place but advanced capabilities (Davis AI, Business Events, Session Replay review workflows) may be underutilized. The narrative should surface what they're leaving on the table.
- **Mature (3+ years)** — deep instrumentation, active use of advanced features. Perceived value problems here are more serious — either the team has outgrown their current use or there is a relationship or positioning issue to address.

*Why this matters:* Adoption maturity shapes the consulting objective and the tone of orientation hypotheses. A six-month customer with gaps is in a different situation than a three-year customer with the same gaps.

### Q6 — Timeline and deadline
> "What's the timeline for this engagement — is there a specific date this needs to land by, like a renewal deadline or a scheduled presentation?"

Capture: the hard deadline (if any), the target delivery date for the deliverable, and any intermediate milestones (internal review, pre-call with AE, executive presentation date).

*Why this matters:* A renewal conversation in three weeks requires a completely different pacing than an expansion discussion with no fixed deadline. If the timeline is tight, the Phase 2 action plan must prioritize what is deliverable within the window — not what is theoretically optimal. Flag immediately if the timeline is shorter than what the full phased workflow can support, and surface a scoped-down alternative.

### Q7 — Application scope
> "Which application or applications will this engagement focus on? For example — is this a single web app, a mobile app, a suite of branded sites, or a specific service within a larger platform?"

Capture: the name(s) of the application(s) in scope, the type (web / mobile / API / backend service / other), and any applications explicitly out of scope. If the consultant names more than one application, ask which is the primary focus before moving on.

*Why this matters:* Application scope determines which RUM data, APM services, synthetic tests, and Business Events are relevant. Hypotheses and investigation actions generated in Phase 1 must be grounded in the specific application being examined — not the customer's entire estate. Scope creep at Phase 0 inflates Phase 1 and produces unfocused deliverables.

### Q8 — Environment scope
> "Should this engagement take into account lower environments — development, test, staging — in addition to production? Or is the focus production only?"

Capture: which environments are in scope (production / staging / test / development / all), and whether proposed solutions should include a lower-environment validation step before production promotion.

*Why this matters:* If lower environments are in scope, the Phase 2 action plan must account for a staging-first workflow — changes are validated in a lower environment before being promoted to production. This is especially relevant for instrumentation changes, OneAgent deployments, RUM tag updates, or any configuration change that could affect live traffic. If production only, the action plan sequences differently.

Common patterns to capture:
- **Production only** — investigation and recommendations apply directly to the live environment.
- **Staging + production** — proposed changes are first validated in staging, then promoted. Action plan includes explicit staging validation steps and go/no-go criteria before production.
- **Full pipeline** — dev → test → staging → production. Instrumentation governance and coverage standards apply at every tier.

Record the environment scope in `current-context.md` under "Environment scope". Flag any known differences in Dynatrace instrumentation between environments (e.g., OneAgent not deployed in dev, RUM only active in production).

### Q9 — Active Dynatrace capabilities
> "Which of these Dynatrace capabilities are active in their environment? Select all that apply."

Present as a multi-select checklist — do not pre-check anything:

**Core observability**
- [ ] Full-Stack Monitoring (OneAgent)
- [ ] Infrastructure Monitoring only
- [ ] Application Performance Monitoring (APM / Distributed Tracing)

**User experience**
- [ ] Real User Monitoring — Web
- [ ] Real User Monitoring — Mobile
- [ ] Session Replay
- [ ] Synthetic Monitoring

**Data & logs**
- [ ] Log Management (Grail)
- [ ] Business Analytics / Business Events
- [ ] Metrics ingestion (custom or third-party)

**AI & automation**
- [ ] Davis AI (problem detection)
- [ ] Davis CoPilot
- [ ] Workflows / Automation

**Security**
- [ ] Application Security
- [ ] Cloud Security

**Platform**
- [ ] Grail (data lakehouse)
- [ ] Site Reliability Guardian
- [ ] Dashboards & Notebooks

Record the checked items in `current-context.md` under "Active capabilities". This list is the boundary of what insights can be surfaced in Phase 1.

**RUM follow-up (ask immediately after Q9 if RUM Web or RUM Mobile is checked):**
> "Is RUM enabled on the specific application we'll be focusing on? And if so, is Session Replay active for it?"

This determines whether a user experience story is available. If RUM is not enabled on the specific application, flag it immediately as a capability gap — the insight narrative will need to anchor on APM and infrastructure signals instead. If RUM is not checked in Q9 at all, skip this follow-up entirely.

**OneAgent coverage follow-up (ask immediately after Q9 if Full-Stack Monitoring is checked):**
> "Is OneAgent deployed across their full estate, or are there known coverage gaps — for example, specific services, cloud workloads, or environments that aren't instrumented?"

Capture: known unmonitored services, hosts, or cloud workloads; any environments (dev, test, staging) where OneAgent is absent; and whether the team is aware of the gaps or if discovery is needed. Flag coverage gaps as a Phase 1 investigation item — a hypothesis about a specific service is only valid if that service is actually instrumented.

### Q10 — Access and permissions
> "What level of access do you or the team have to their Dynatrace environment — full access, read-only, or are you working from exports and shared screenshots?"

Capture: access level (full / read-only / no direct access), whether the Dynatrace consultant can query Grail directly, and whether live investigation is possible or the team is working from exported data.

*Why this matters:* Phase 2 investigation actions depend on the team's ability to look at the data. An action plan that requires running DQL queries against Grail is not executable if the consultant has no direct access. Flag access limitations immediately and adjust investigation actions to match what is actually possible.

Common patterns:
- **Full access** — consultant can navigate the environment, build dashboards, and run queries directly. Full action plan is executable.
- **Read-only** — consultant can view but not configure. Investigation is possible; remediation actions require customer-side execution.
- **No direct access** — consultant works from exports, screenshots, or a shared screen session. All investigation depends on the customer team pulling data and sharing it. Phase 2 actions must be framed as instructions to the customer, not tasks the consultant performs.

### Q11 — Dynatrace version (Managed deployments only)
> "If this is a Managed deployment, do you know which version they're running?"

Ask only if Q4 confirmed a Managed deployment. Skip entirely for SaaS tenants (SaaS updates automatically).

Capture: the Managed version if known, or flag as unknown. Cross-reference against known feature availability — certain capabilities (Grail, Davis CoPilot, newer RUM features) require recent versions and may not be available on older Managed deployments.

*Why this matters:* A Phase 1 hypothesis that depends on a feature introduced in a recent version is invalid for a customer running an older Managed deployment. Flag version-dependent assumptions explicitly rather than discovering them in Phase 2.

### Q12 — Data retention and availability window
> "Do you know what their Dynatrace data retention looks like — for example, how far back RUM, logs, and metrics data is available?"

Capture: retention window per data type if known (RUM sessions, logs, metrics, traces), or flag as unknown if the consultant doesn't have this information.

*Why this matters:* A hypothesis that requires 90 days of RUM trend data is only valid if retention is configured that long. If retention windows are unknown, flag this as a Phase 1 discovery item rather than assuming data is available. Short retention windows (e.g., 7-day log retention) narrow the investigation window significantly and should be surfaced in the action plan.

### Q13 — Who will consume the deliverable and what they care about
> "Who on the customer side will we be presenting findings to, and what do they care about most — what KPIs, business outcomes, or strategic priorities are top of mind for them right now?"

Capture the person's role and priorities. Match them to the closest role archetype in `stakeholder-profiles.md` — focus on what they own and decide, not their exact title. The eight archetypes are: Executive Sponsor, Product Owner, SRE / Reliability Engineer, IT Operations Manager, Application Developer, Platform / DevOps Engineer, Security / Compliance Officer, Data / Analytics Lead. If no archetype is close enough, note the gap and ask the consultant whether to create a new profile. Capture named KPIs where possible (conversion rate, MTTR, uptime SLA, cost per transaction).

### Q14 — What the technical team cares about
> "What does their primary technical team care about day-to-day — what are their pain points, priorities, or frustrations with the current setup?"

The technical team and leadership often have different definitions of success. Capturing both ensures the deliverable speaks to both audiences.

### Q15 — Engagement team composition
> "Who is leading this engagement on the Dynatrace side, and who is supporting? For example — is this AE-led with SE and CSM support, or something else?"

Capture: who leads (AE / CSM / SE / Insights Consultant / other), who supports, and what each role owns in the deliverable. This shapes tone, decision authority, and how findings are positioned internally before they reach the customer.

*Why this matters:* An AE-led expansion discussion and a CSM-led value review require different internal positioning even when the customer deliverable is the same.

## Steps

1. **Open the conversation** with the prompt above if the consultant has not described the engagement yet. If a detailed problem description has already been provided, extract what is already answered before asking anything.
2. **Ask clarifying questions** one at a time in adaptive order, skipping any already answered.
3. **Check past investigations** for any prior engagement on the same customer or vertical. Surface the key lesson if found.
4. **Reframe the engagement** as a clear consulting objective: what insight will be surfaced, for whom, and to what end. Write this under "Consulting objective" in `current-context.md`. Example: *"Surface underutilized RUM and Davis AI insights for [Customer]'s Executive Sponsor ahead of their Q3 renewal, demonstrating measurable value from their Full-Stack and RUM investment."*
5. **Surface 3–5 orientation hypotheses** about where value is likely hiding in the environment, given the active capabilities and vertical. **Only generate hypotheses after Q9 (active capabilities) and the RUM follow-up are confirmed.** Hypotheses that depend on RUM, Session Replay, or Business Events are only valid if those capabilities are confirmed active. Label all hypotheses clearly as pre-scoring candidates — not findings. Pull from the tech → UX → business linkages in `domain-knowledge.md` and the vertical context. Example: *"Davis AI may be grouping related problems in ways the team hasn't reviewed, understating incident volume and MTTR improvement."*
6. **Confirm scope** — what this engagement will cover and what it will not. Name any capability gaps (e.g., RUM not enabled) that limit the insight surface.
7. **Write `memory/project-space/current-context.md`** fully populated — no placeholders.
8. **Present and pause at the gate.** State clearly:

   > "This is the Phase 0 framing. Please **approve**, **redirect**, or **iterate** before I begin the diagnosis."

   Record the gate decision in `memory/project-space/decisions-log.md`.

**Do not begin Phase 1 until the user approves.**

## Output

`memory/project-space/current-context.md`, fully populated:

| Section | Contents |
|---|---|
| Engagement Framing (C.S.I.R.) | **C** — Customer name/label, business description, consultant role, engagement trigger; **S** — Known constraints, environment facts, contract phase, prior outcomes, competitive context if at-risk; **I** — Consultant's goal and customer's expected outcome; **R** — Deliverable format, primary audience, tone/length constraints |
| Customer | Name / label, industry, size |
| Vertical | Named vertical |
| Tenant type | SaaS or Managed |
| Adoption maturity | Early-stage / established / mature; time as Dynatrace customer; consultant's read on utilization depth |
| Timeline and deadline | Hard deadline (if any); target delivery date; intermediate milestones; flag if timeline is tighter than the full phased workflow supports |
| Application scope | Named application(s) in scope; primary focus application; out-of-scope applications |
| Environment scope | Production only / staging + production / full pipeline; whether lower-environment validation steps are required before production promotion; known instrumentation differences between environments |
| Engagement team | AE / CSM / SE / Insights Consultant — who leads, who supports, what each role owns |
| Active capabilities | Checked list from Q9 |
| OneAgent coverage | Full estate / known gaps — list unmonitored services, hosts, or environments |
| Access and permissions | Full / read-only / no direct access; whether live investigation is possible or consultant works from exports |
| Dynatrace version | Managed only — version number or flagged as unknown; version-dependent feature assumptions flagged |
| Data retention | Retention windows per data type (RUM, logs, metrics, traces) if known; flagged as discovery item if unknown |
| RUM status | Enabled / not enabled on the specific app in question; session replay on/off |
| Consulting objective | The reframed engagement goal |
| Leadership priorities | Named KPIs and strategic priorities |
| Technical team priorities | Day-to-day pain points and priorities |
| Orientation hypotheses | 3–5 pre-scoring candidates labeled as such; generated only after capabilities confirmed |
| Capability gaps | Anything not active that limits insight surface |
| Stakeholder role archetype | Matched archetype from `stakeholder-profiles.md`; flag if no close match exists |
| Prior engagement reference | Link to archived investigation if a match was found |
| Gate decision | Approved / Redirected / Iterating — with date |

## PII and named individuals

**Do not include named individuals (first name, last name, or full name) in the consulting objective, orientation hypotheses, capability gaps, or any customer-facing deliverable** unless the consultant explicitly confirms the person's name should appear. Default to role titles (e.g., "Manager of Technologies & Web Services", "Director of Reliability") instead of personal names throughout all outputs.

If a named individual appears in the consultant's problem description, capture their role title in the output — not their name. If the consultant explicitly asks to include a name, confirm once before doing so and apply consistently.

## Common pitfalls

- **Treating Q3 as a single question.** Q3 is a four-part C.S.I.R. sub-sequence. Skipping Specific Information means orientation hypotheses will be generic. Skipping Intent means the consulting objective won't reflect what the consultant actually needs. Skipping Response Format means Phase 3 packaging decisions are made too late. Skipping the engagement trigger (now under C — Context) means urgency and tone will be miscalibrated.
- **Not scanning upfront context before asking questions.** If the consultant provides a detailed problem description, extract what is already answered before starting the question sequence. Asking questions the consultant just answered signals inattention and wastes their time.
- **Jumping to Phase 1 before the gate.** The insight narrative is only as strong as the context underneath it. A wrong scope in Phase 0 propagates through every subsequent artifact.
- **Asking all clarifying questions at once.** One question at a time. A wall of questions produces short, low-quality answers.
- **Skipping the capabilities checklist.** Open-ended capability questions produce vague answers. Always use the checklist for Q9.
- **Generating orientation hypotheses before capabilities are confirmed.** Hypotheses that depend on RUM, Session Replay, Business Events, or Davis AI are only valid if those capabilities are confirmed active. Generate hypotheses after Q9 and the RUM follow-up are answered, not before.
- **Assuming RUM is active.** Never assume. If RUM is not enabled on the specific application, the user experience story is not available and the insight narrative must be reanchored on APM and infrastructure signals.
- **Assuming production-only scope.** Many engagements involve changes that must be validated in staging before production promotion. Always ask about environment scope explicitly — never assume the answer. If lower environments are in scope, the action plan must include explicit staging validation steps and go/no-go criteria.
- **Ignoring application scope.** An engagement focused on a single checkout service and one focused on a full suite of branded websites require completely different hypotheses and investigation actions. Confirm which application is the primary focus before Phase 1 begins.
- **Ignoring adoption maturity.** A six-month customer with instrumentation gaps is in a fundamentally different position than a three-year customer with the same gaps. The consulting objective and orientation hypotheses must reflect where the customer is in their adoption journey.
- **Not asking about timeline.** A tight renewal deadline changes what is deliverable. If the timeline is shorter than the full phased workflow supports, flag it immediately and surface a scoped-down alternative — don't discover the constraint in Phase 2.
- **Assuming full access.** If the consultant has read-only or no direct access to the Dynatrace environment, Phase 2 investigation actions must be reframed as instructions to the customer rather than tasks the consultant performs. Discover this at Phase 0, not mid-investigation.
- **Skipping the competitive context question on at-risk accounts.** Knowing whether the competitor's pitch is a feature gap, a cost argument, or an open-source play materially changes how the renewal narrative is framed. Ask it whenever an at-risk account is identified.
- **Assuming full OneAgent coverage.** Full-Stack Monitoring being active does not mean every service is instrumented. Flag known coverage gaps at Phase 0 and treat them as Phase 1 discovery items.
- **Ignoring the vertical.** Retail and FSI leadership have completely different KPI vocabularies. The vertical determines which tech → business linkages are load-bearing in Phase 1.
- **Presenting orientation hypotheses as findings.** Label them clearly as pre-scoring candidates. They are navigation aids, not conclusions.
- **Leaving stakeholder profile gaps unflagged.** If the Phase 3 reader doesn't match any of the eight role archetypes closely enough, Phase 3 will be generic. Flag the gap now and ask the consultant whether to create a new profile.
- **Skipping the past engagement check.** If the team has worked with this customer or vertical before, the lessons from that archive save Phase 1 time and prevent repeated mistakes.
- **Including named individuals in outputs without confirmation.** Role titles are always safe; personal names require explicit consultant approval before appearing in any deliverable. When in doubt, use the title.
