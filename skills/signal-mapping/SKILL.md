---
name: signal-mapping
description: Procedure for mapping technical signals to UX outcomes and business KPIs. Use whenever a deliverable needs to connect technical findings to business impact.
---

# Signal Mapping

## When to use

Any time the investigation needs to connect a technical signal (latency, error rate, throughput) to a user-visible UX outcome (slowness, failure, friction) and then to a business KPI (conversion, churn, revenue). This skill produces the chain that turns "p95 latency rose 200ms" into "conversion dropped by 1.2pp, which is roughly $X/week at current volume".

Use this skill:

- In Phase 1, **after `hypothesis-generation` has drafted `hypotheses.md`**, to ground the hypotheses in business impact. This skill runs before ICE scoring and **hands off to `ice-scoring`** once the map is written — Impact scores anchor on the business KPIs produced here.
- In Phase 2, when the action plan needs to justify priorities by business value.
- In Phase 3, when one-pagers and decks need to lead with business impact rather than technical detail.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session. The agent fixes it once — when Phase 0 (`context-framing`) creates the engagement folder, or when a paused/active engagement is resumed — and holds it in working context for the rest of the session. There is **no shared pointer file** to read; nothing depends on a global "active" file a second concurrent session could overwrite.
2. If no engagement is established yet (a fresh session picking up earlier work), resolve it with the resume procedure in `skills/investigation-reset/SKILL.md`: scan `memory/clients/*/engagements/*/current-context.md` for a `state:` of `active` or `paused`, present the matches, and have the user pick one. If none, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = the established/selected path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`). CLIENT_NAME = the segment between `memory/clients/` and `/engagements/`.
4. All phase file reads/writes use ENGAGEMENT_PATH as the base — e.g., `<ENGAGEMENT_PATH>/signals-map.md`.

Then read these files:

- `<ENGAGEMENT_PATH>/hypotheses.md` — the hypotheses being mapped.
- `memory/long-term/domain-knowledge.md` — for the standard tech → UX → business mapping table, the common signal patterns, and the "Authoritative external references" allowlist.
- `memory/long-term/dynatrace-playbooks.md` — hub index (already loaded at session init). Read the specific playbook file for each hypothesis's problem shape (e.g., `memory/long-term/playbooks/latency-backend.md`) to pull its named SLIs and signal artifacts (Services app response time, Failure Analysis error rates, RUM session-event timing, SLO burn rate) into the SLI/SLO column rather than inventing them. Read only the matched file(s) — do not load all playbooks.
- `<ENGAGEMENT_PATH>/current-context.md` — for stakeholders, since the KPI ladder depends on who owns the KPI, and for the **Out-of-scope exclusions** that bound which signals may be proposed.

If the mapping depends on the exact semantics of a Dynatrace metric or feature (e.g., what counts as a "user action" in RUM, how an SLO is computed in Grail, what Davis treats as a root cause), consult `skills/external-research/SKILL.md` before writing the row. Cite the source URL and retrieval date in the relevant cell of `signals-map.md`.

## Steps

1. **List the SLIs/SLOs relevant to each hypothesis.** For each hypothesis, name the specific service-level indicators that would move if the hypothesis is true. Include the current value and the SLO target where known. A signal that only an excluded capability could provide (per the Out-of-scope exclusions in `current-context.md`) is marked "unavailable (out of scope)" in the map rather than proposed — the map never recommends turning on an excluded capability to close a gap.
2. **Map each SLI to user-visible UX outcomes.** Use the standard mappings in `domain-knowledge.md` as a starting point and adapt to the specific product surface. State how the user *experiences* the technical signal — "longer wait before page paints", not "p95 latency degraded".
3. **Map UX outcomes to business KPIs.** Use the standard mappings as a starting point and validate against the team's actual KPI ladder. Where possible, quantify the link: "every 100ms of page load on the payment screen historically corresponds to ~0.4pp conversion drop." If the linkage is qualitative, say so explicitly.
4. **Scan `hypotheses.md` for upstream-flagged gaps and consolidate them.** `hypothesis-generation` records each hypothesis that depends on telemetry the team lacks as a row with Status `blocked: instrumentation` inside `hypotheses.md`. Read those rows and pull every such gap into the "Instrumentation gaps" section of `signals-map.md`, one entry per gap, tagged with the hypothesis ID(s) it blocks. This is the single consolidation point — `signals-map.md` becomes the authoritative gap register that `ice-scoring` consumes.
5. **Flag any further instrumentation gaps you find while mapping.** Every step in the chain depends on telemetry. Where the chain breaks because the team cannot measure something — even if no hypothesis row flagged it — document the gap in the same "Instrumentation gaps" section. Each gap becomes a candidate work item in the action plan.
6. **Verify each layer connects to the next.** A signal that does not connect to a UX outcome is noise. A UX outcome that does not connect to a business KPI cannot drive a leadership decision. If you cannot complete the chain for a hypothesis, that is a finding — surface it.
7. **Hand off to ICE scoring.** Once the four sections are populated — and the Instrumentation gaps section consolidates every `blocked: instrumentation` row from `hypotheses.md` — invoke `skills/ice-scoring/SKILL.md`. The signals map must exist before ICE runs, because Impact anchors on its business KPIs and ICE's gap adjustment reads its Instrumentation gaps section.

## Output

The agent writes to `<ENGAGEMENT_PATH>/signals-map.md`, populating the four sections: SLIs/SLOs, UX outcomes, Business KPIs, Instrumentation gaps. Each section is a table with concrete entries — no placeholders left in the live file.

## Common pitfalls

- **Stopping at the technical signal.** A signals map that lists SLIs without translating them to UX and business outcomes is half-built. Complete the chain.
- **Fabricating quantitative linkages.** If the team does not have a measured relationship between page load time and conversion, do not invent one. State the linkage qualitatively and flag it as a candidate for measurement.
- **Treating the standard mappings as truth.** The table in `domain-knowledge.md` is a starting point. Every product surface has its own quirks; validate the mapping against the team's actual experience.
- **Burying instrumentation gaps.** Gaps are not embarrassments — they are findings. Surface them in their own section so the action plan can address them.
- **Leaving `blocked: instrumentation` rows stranded in `hypotheses.md`.** Those rows are created upstream but must be consolidated here. If you skip step 4, `ice-scoring` cannot adjust the affected scores and the gap silently disappears from the ranked table.
