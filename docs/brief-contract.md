# The intake brief contract

**This file is canon.** It is the single source of truth for the Insights Forge intake brief — the markdown document that opens every seeded Phase 0 engagement. Three things must match it exactly, heading for heading and field line for field line:

1. **The Seed Prompt Generator's `buildBrief()`** in `html/seed-prompt-generator-src.html` — what the browser form emits.
2. **The `/drill` skill's embedded output template** in `skills/drill/SKILL.md` — what the chat-native intake emits.
3. **The step-2 mapping table** in `skills/context-framing/SKILL.md` — how Phase 0 reads the brief back.

`tools/conformance-check.py` verifies the sync. If you change the brief format, change it **here first**, then propagate to all three consumers in the same commit.

## Document shell

**H1 (exact, and the fast-path detection key in context-framing):**

```markdown
# Insights Forge intake brief
```

**Preamble** — a single blockquote, emitted verbatim, immediately after the H1:

```markdown
> **For the agent — read first.** This is a seeded Phase 0 engagement intake, captured with Insights Forge and aligned to skills/context-framing/SKILL.md. The **baseline deliverable is always a customer action plan**; "Requested outputs" below are the presentation formats to produce on top of it.
>
> **How the inputs are categorized:**
> - **Required context** — Requested outputs, Customer (name / what-they-do / vertical), Relationship & context, Pain & constraints, Dynatrace intent + customer success, Active capabilities, and at least one Stakeholder (role archetype required; a named person strongly preferred). Framing is not complete without these.
> - **Recommended context** — Analyst calibration (1–5) + role, Tenant, Customer region(s), per-stakeholder communication level & priorities, and Trigger. These sharpen tone, depth and KPI selection.
> - **Active capabilities are the boundary** of what insight you can surface — do not propose value that depends on a capability not listed. Davis AI is always on.
> - **Out of scope is a hard exclusion** — do not suggest or reference anything the customer has flagged as out of scope, even if the underlying capability is active.
> - Any value shown as "not provided" is a genuine gap.
>
> **Before you build the plan:** ask the consultant **1–3 rounds of clarifying questions**, one topic at a time, until you have enough substantial context to move forward confidently. Start with any Required item marked "not provided", then tighten Intent, capability scope, and what each stakeholder cares about. Do not advance past the Phase 0 gate until the consultant approves your framing.
```

**Empty-value convention:** any scalar field with no answer is emitted as the literal string `not provided`; any list section with no entries collapses to a single `not provided` line. Producers never omit a field line or a section — a gap is shown, not hidden.

## Sections, in order

The eight `##` headings, exactly as emitted, in exactly this order:

1. `## Requested outputs & trigger`
2. `## Customer context`
3. `## Stakeholders & audience`
4. `## Goals & success criteria`
5. `## Pain & constraints`
6. `## Active capabilities`
7. `## Out of scope / do not suggest`
8. `## Focus applications`

### 1. `## Requested outputs & trigger`

Five field lines, in order:

| Line (verbatim prefix) | Value format | Required? |
|---|---|---|
| `- Baseline (always): Customer action plan` | Fixed line, emitted verbatim every time | Always emitted |
| `- Additional formats: ` | Comma-separated list from: `Executive one-pager`, `PowerPoint deck`, `Execution guides` — or `none (action plan only)` | Required (the baseline satisfies it; `none (action plan only)` is a valid answer) |
| `- Trigger(s): ` | Comma-separated list from: `QBR`, `New Customer`, `Renewal`, `Expansion`, `Client Conversation`, `Incident follow-up`, or a free-text "Other" value — or `not provided` | Optional |
| `- Analyst: role ` | `<role>; experience <calibration>, account familiarity <calibration>, customer Dynatrace maturity <calibration>` — role from `Insights Analytics Consultant` / `CSM` / `SE` / `Consultant` / free-text Other | Role required; calibrations optional |
| `- Generated: ` | ISO date `YYYY-MM-DD` | Always emitted |

**Calibration value format** — each of the three calibrations is either `not provided` or:

```
N/5 — "<anchor text>"
```

where `N` is 1–5 and `<anchor text>` is the behavioral anchor for that level, copied exactly from the tables below. Example:

```markdown
- Analyst: role Insights Analytics Consultant; experience 3/5 — "Comfortable across the common patterns", account familiarity 5/5 — "Deep history — multi-year relationship", customer Dynatrace maturity 1/5 — "Just onboarding — basics only"
```

The three calibrations are independent — any subset may be answered; there is no rate-one-rate-all rule.

**Calibration anchors** (the five labels double as the selectable options in both the form and `/drill`):

*Experience with Dynatrace consulting* (`analystExp`):

| N | Anchor |
|---|---|
| 1 | New to Dynatrace consulting |
| 2 | A few engagements delivered |
| 3 | Comfortable across the common patterns |
| 4 | Deep experience across verticals |
| 5 | Expert — the person others ask |

*Account familiarity* (`accountFam`):

| N | Anchor |
|---|---|
| 1 | First touch — no history with this account |
| 2 | Read the notes, never worked it |
| 3 | A few working sessions in |
| 4 | Know the environment and the players |
| 5 | Deep history — multi-year relationship |

*Customer's Dynatrace maturity* (`domainFluency`):

| N | Anchor |
|---|---|
| 1 | Just onboarding — basics only |
| 2 | Core APM in place, little else |
| 3 | Several capabilities in active use |
| 4 | Broad adoption with SLOs and some automation |
| 5 | Advanced — full-stack, Grail, automation at scale |

### 2. `## Customer context`

Seven field lines, in order:

| Line (verbatim prefix) | Value format | Required? |
|---|---|---|
| `- Name: ` | Free text | Required |
| `- What they do: ` | One-line free text | Required |
| `- Vertical(s): ` | Comma-separated list from: `Retail / E-commerce`, `Financial Services (FSI)`, `Healthcare / Life Sciences`, `Manufacturing`, `Telco / Media`, `Public Sector`, `Technology / SaaS`, `Logistics / Supply Chain`, or a free-text Other value | Required (at least one) |
| `- Customer size (ACV): ` | ACV band, free text | Optional |
| `- Tenant type: ` | `SaaS` or `Managed` | Optional (form defaults to `SaaS`) |
| `- Region(s): ` | Comma-separated list from: `NORAM`, `LATAM`, `EMEA`, `APAC` | Optional |
| `- Relationship & context: ` | Free text — relationship history, mood, recent milestones/incidents | Required |

### 3. `## Stakeholders & audience`

One bullet per stakeholder, no other lines. Format:

```markdown
- <name or "(unnamed)"> · <archetype or "archetype not provided"> · communication level: <Technical | Executive | Mixed> — cares about: <free text or "not provided">
```

Required: at least one stakeholder with a role archetype. Name strongly preferred; communication level defaults to `Mixed`; "cares about" optional.

### 4. `## Goals & success criteria`

Two field lines (no bullet markers), in order:

| Line (verbatim prefix) | Value format | Required? |
|---|---|---|
| `Dynatrace intent: ` | Free text — what Dynatrace wants from the engagement (prove value, secure renewal, justify expansion) | Required |
| `Customer success: ` | Free text — what the customer would call success | Required |

### 5. `## Pain & constraints`

A single free-text block (no field label): the team's day-to-day pain plus anything that constrains the plan — alert noise, slow root cause, toil, on-call load, prior commitments, regulated-data limits. Required.

When the brief comes from `/drill`, the block may end with one optional trailing line, `Technical team priorities: [sheet Q1] …; [sheet Q2] …`, carrying the answers to the vertical drill sheet (`memory/long-term/drill-sheets/`) tagged by question number. The browser form does not emit this line; context-framing reads it when present and runs the drill sheet itself when absent.

### 6. `## Active capabilities`

One bullet per active capability:

```markdown
- <capability label>[ — <generation>][ (always on)]
```

- `<capability label>` comes from the form's capability checklist (e.g. `Full-Stack Monitoring (OneAgent)`, `Real User Monitoring — Web`, `Log Management (Grail)`).
- `— <generation>` appears only for capabilities that carry a generation qualifier (`Classic` / `Grail` / `Mixed`; for Dashboards: `Classic (Gen2)` / `Grail (Gen3)` / `Mixed`).
- `(always on)` is appended to the Davis line only: `- Davis AI (problem detection) (always on)` — always present.
- If capabilities are unconfirmed, this extra bullet is added verbatim: `- Capabilities unconfirmed — analyst requests help confirming during framing`.

Required: at least one capability beyond Davis, or the unconfirmed line.

### 7. `## Out of scope / do not suggest`

One bullet per excluded capability, same `- <label>[ — <generation>]` format as Active capabilities (no `(always on)` variant), plus an optional free-text line:

```markdown
- Notes: <free text>
```

Optional section — collapses to `not provided` when nothing is excluded. When populated it is a **hard, engagement-wide exclusion**.

### 8. `## Focus applications`

One bullet per application:

```markdown
- <app name or "(unnamed app)"> — RUM: <Yes | No | Unsure | "not provided">; Session Replay: <Yes | No | Unsure | "not provided">
```

Optional — **becomes required** (at least one app with name, RUM, and Session Replay status) when the Goals & success text signals a digital-experience intent. Both producers use the same phrase set for that test, case-insensitively: `digital experience`, `user experience`, `RUM` (word-bounded), `real user`, `customer journey`, `frontend`.

## Change control

- The form's `buildBrief()` (see `docs/seed-prompt-generator.md` for the edit/repack loop), `/drill`'s embedded template, and context-framing's mapping table are deliberate duplications of this contract; `tools/conformance-check.py` keeps them honest.
- Heading text, heading order, field-line prefixes, and the calibration/stakeholder/capability/app line formats are all load-bearing — context-framing's seed-prompt intake path parses against them, and the fast path keys on the H1.
