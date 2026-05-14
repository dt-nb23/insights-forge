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

If the consultant has not yet described the engagement, open with:

> "Tell me about the customer and what you're trying to accomplish with them."

Do not ask multiple questions at once. Let each answer drive the next question.

## Clarifying questions

Ask **one question at a time**, in adaptive order — if the consultant's opening description already answers a question, skip it and move to the next unknown. Stop asking when you have enough to write a confident context document.

The eight questions, in default order:

### Q1 — Customer and what they do
> "Who is the customer, and what does their business do?"

Capture: company name (or anonymized label), what product or service they sell, approximate size if known.

### Q2 — Customer vertical
> "Which industry vertical are they in?"

Common verticals: Retail / E-commerce, Financial Services (FSI), Healthcare / Life Sciences, Manufacturing, Telco / Media, Public Sector, Technology / SaaS, Logistics / Supply Chain. Accept the consultant's own label if it doesn't match this list.

The vertical shapes which KPIs matter to leadership and which signal → business linkages are most relevant in Phase 1.

### Q3 — Tenant type
> "Is this customer on a SaaS tenant or a Managed (on-premises) deployment?"

This affects which features and data are available and constrains what insights and recommendations are possible in later phases.

### Q4 — Active Dynatrace capabilities
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

### Q5 — RUM on the application in question
> "Is Real User Monitoring enabled on the specific application we'll be focusing on? And if so, is Session Replay active for it?"

This determines whether a user experience story is available. If RUM is not enabled, flag it immediately as a capability gap — the insight narrative will need to anchor on APM and infrastructure signals instead.

### Q6 — Who will consume the deliverable and what they care about
> "Who on the customer side will we be presenting findings to, and what do they care about most — what KPIs, business outcomes, or strategic priorities are top of mind for them right now?"

Capture the person's role and priorities. Match them to the closest role archetype in `stakeholder-profiles.md` — focus on what they own and decide, not their exact title. The eight archetypes are: Executive Sponsor, Product Owner, SRE / Reliability Engineer, IT Operations Manager, Application Developer, Platform / DevOps Engineer, Security / Compliance Officer, Data / Analytics Lead. If no archetype is close enough, note the gap and ask the consultant whether to create a new profile. Capture named KPIs where possible (conversion rate, MTTR, uptime SLA, cost per transaction).

### Q7 — What the technical team cares about
> "What does their primary technical team care about day-to-day — what are their pain points, priorities, or frustrations with the current setup?"

The technical team and leadership often have different definitions of success. Capturing both ensures the deliverable speaks to both audiences.

### Q8 — Trigger for this engagement
> "What is driving this engagement right now — is it a QBR, a renewal conversation, an expansion discussion, a scheduled touchpoint, or something else?"

The trigger shapes urgency, tone, and what a "good outcome" looks like for the consultant.

## Steps

1. **Open the conversation** with the prompt above if the consultant has not described the engagement yet.
2. **Ask clarifying questions** one at a time in adaptive order, skipping any already answered.
3. **Check past investigations** for any prior engagement on the same customer or vertical. Surface the key lesson if found.
4. **Reframe the engagement** as a clear consulting objective: what insight will be surfaced, for whom, and to what end. Write this under "Consulting objective" in `current-context.md`. Example: *"Surface underutilized RUM and Davis AI insights for [Customer]'s Executive Sponsor ahead of their Q3 renewal, demonstrating measurable value from their Full-Stack and RUM investment."*
5. **Surface 3–5 orientation hypotheses** about where value is likely hiding in the environment, given the active capabilities and vertical. Label them clearly as pre-scoring candidates — not findings. Pull from the tech → UX → business linkages in `domain-knowledge.md` and the vertical context. Example: *"Davis AI may be grouping related problems in ways the team hasn't reviewed, understating incident volume and MTTR improvement."*
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
| Customer | Name / label, industry, size |
| Vertical | Named vertical |
| Tenant type | SaaS or Managed |
| Active capabilities | Checked list from Q4 |
| RUM status | Enabled / not enabled on the app in question; session replay on/off |
| Consulting objective | The reframed engagement goal |
| Leadership priorities | Named KPIs and strategic priorities |
| Technical team priorities | Day-to-day pain points and priorities |
| Engagement trigger | QBR / renewal / expansion / touchpoint / other |
| Orientation hypotheses | 3–5 pre-scoring candidates labeled as such |
| Capability gaps | Anything not active that limits insight surface |
| Stakeholder role archetype | Matched archetype from `stakeholder-profiles.md`; flag if no close match exists |
| Prior engagement reference | Link to archived investigation if a match was found |
| Gate decision | Approved / Redirected / Iterating — with date |

## Common pitfalls

- **Jumping to Phase 1 before the gate.** The insight narrative is only as strong as the context underneath it. A wrong scope in Phase 0 propagates through every subsequent artifact.
- **Asking all clarifying questions at once.** One question at a time. A wall of questions produces short, low-quality answers.
- **Skipping the capabilities checklist.** Open-ended capability questions produce vague answers. Always use the checklist for Q4.
- **Assuming RUM is active.** Never assume. If RUM is not enabled, the user experience story is not available and the insight narrative must be reanchored.
- **Ignoring the vertical.** Retail and FSI leadership have completely different KPI vocabularies. The vertical determines which tech → business linkages are load-bearing in Phase 1.
- **Presenting orientation hypotheses as findings.** Label them clearly as pre-scoring candidates. They are navigation aids, not conclusions.
- **Leaving stakeholder profile gaps unflagged.** If the Phase 3 reader doesn't match any of the eight role archetypes closely enough, Phase 3 will be generic. Flag the gap now and ask the consultant whether to create a new profile.
- **Skipping the past engagement check.** If the team has worked with this customer or vertical before, the lessons from that archive save Phase 1 time and prevent repeated mistakes.
