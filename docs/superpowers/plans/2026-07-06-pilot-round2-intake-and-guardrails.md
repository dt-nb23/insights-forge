# Pilot Round 2 — Intake Form + Guardrails Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved spec at `docs/superpowers/specs/2026-07-06-pilot-round2-intake-and-guardrails-design.md` — an analyst intake form that generates a Phase 0 seed prompt, plus session-wide guardrails and deliverable-consistency changes across CLAUDE.md, the phase skills, and long-term memory.

**Architecture:** Input rigor lives in a self-contained HTML form (deterministic, analyst-independent). Output rigor lives in CLAUDE.md operating rules (session-wide). Phase-local behavior stays in the phase SKILL.md files. No new session-startup reads.

**Tech Stack:** Vanilla HTML/CSS/JS (single file, zero external requests); Markdown skill/doc edits; git on branch `pilot-round2-intake-and-guardrails`.

## Global Constraints

- Branch: all commits go to `pilot-round2-intake-and-guardrails` (already created; spec is committed there). Never commit to `main`.
- The seed-prompt header is the exact string `# Insights Forge intake brief (v1)`; detection matches on the prefix `# Insights Forge intake brief`. Both Task 2 (form) and Task 3 (skill) must use these strings verbatim.
- Thin-answer word threshold is **15 words**; the "prior-outcomes depth" proxy for tier upgrade is **30 words**. Both live in one JS config object in the form.
- Output tier names are exactly `Simple` and `Advanced`.
- Unanswered form fields render as the literal string `not provided` — never omitted.
- No lens opt-out anywhere: checkpoints add steering/visibility, never skipping. The ≥3-round council minimum and full four-lens set always run.
- Query policy: agent never executes queries; structural pseudo-queries in conversation/working artifacts; illustrative examples allowed only in markdown deliverables, labeled "unvalidated — verify before use"; DQL only where Grail (Gen3) is confirmed for that data type; USQL for Classic RUM.
- One-pager: 450–550 words of prose; fixed section order TL;DR → Situation → Business impact → Key findings → Recommended actions (30/60/90) → Risks and decision asks → Sources.
- `memory/long-term/` writes require explicit user approval before applying (Task 7 ends at an approval gate).
- This repo has no test framework; every task's verification is exact `grep` checks with expected output plus (for the form) a browser walkthrough checklist.
- The repo pattern for inserted procedure steps between existing numbered steps is a suffixed number (`2a.`, `5a.`) — do not renumber existing steps.

---

### Task 1: CLAUDE.md guardrails, query policy, pacing flags

**Files:**
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: nothing (foundation task).
- Produces: a `## Communication protocol` section that Tasks 4, 5 reference by name ("per the CLAUDE.md communication protocol"); the seeded-intake detection sentence Task 3 relies on; the query-policy wording Tasks 6–7 must stay consistent with.

- [ ] **Step 1: Rewrite the query-prohibition operating principle**

In `CLAUDE.md`, under `## Operating principles`, replace this bullet:

```markdown
- The agent **never runs live queries or executes production changes**. It references metrics, SLIs, SLOs, and observability concepts but does not generate raw DQL (Dynatrace Query Language) or any other executable query syntax. Validation and execution remain with the human team.
```

with:

```markdown
- The agent **never runs live queries or executes production changes**. In conversation and working artifacts it describes query logic structurally (fetch X → filter Y → summarize Z) rather than emitting executable syntax. In **markdown deliverables** it may include illustrative query examples clearly labeled **"unvalidated — verify before use"** — and only version-correctly: DQL (Dynatrace Query Language) only where Grail (Gen3) is confirmed active for that data type; USQL for Classic RUM. If the generation is unconfirmed, include no example — name the gap instead. Validation and execution remain with the human team.
```

- [ ] **Step 2: Update the matching bullet in "What this agent does NOT do"**

Replace:

```markdown
- It does **not** generate raw DQL, SQL, or other executable query syntax.
```

with:

```markdown
- It does **not** execute queries, and does not emit executable query syntax outside markdown deliverables. Deliverable examples are labeled "unvalidated — verify before use" and version-gated: DQL only where Grail (Gen3) is confirmed; USQL for Classic RUM; no example when the generation is unconfirmed.
```

- [ ] **Step 3: Add the Communication protocol section**

Insert a new section immediately after the `## Human-in-the-loop gates` section (after its final paragraph about decisions-log.md and before `## Sub-agent lenses`):

```markdown
## Communication protocol

Every phase gate — and every mid-conversation question — follows one shape:

1. A 2–3 sentence summary of what was just produced.
2. The spelled-out choice: **approve**, **redirect**, or **name a lens** (at checkpoints: **continue**, **steer**, or **adjust**).
3. A pointer to the full artifact file.

Any question the agent asks is the last, visually separated element of its message — never buried mid-explanation, never a bare "does this look right?".

Three further session-wide guardrails:

- **No off-context capability recommendations.** Any recommended action or hypothesis that introduces a Dynatrace capability not already established as active or in-scope (per the engagement's `current-context.md` Active capabilities) is posed as a question to the analyst — never asserted as a recommendation.
- **Stalled-session recovery.** If three consecutive turns produce no artifact progress (no phase file created or updated), proactively offer to pause and resume via `skills/investigation-reset/SKILL.md` rather than continuing.
- **Version awareness.** Classic and Grail (Gen3) capability generations can be active on the same client simultaneously — RUM, Session Replay, dashboards, and metrics all split. Confirm which generation is active before assuming a capability or query path (see "Capability generations" in `memory/long-term/domain-knowledge.md`).
```

- [ ] **Step 4: Add pacing defaults to the Phased workflow section**

Immediately after the phase table in `## Phased workflow` (before the "On-demand skills" sentence), insert:

```markdown
Two pacing defaults are ON until the team explicitly turns them off (procedure lives in the phase skills):

- **Phase 1 checkpoint mode** — after each Phase 1 artifact (issue tree, hypotheses, signals map) the agent pauses for a quick confirmation per the Communication protocol, and asks rather than silently chooses when a structuring call is genuinely ambiguous.
- **Phase 2 direction check and council round checkpoints** — the action plan opens with a one-screen skeleton for confirmation before the full draft is built, and the persona council pauses after every round for a progress summary the user can steer.
```

- [ ] **Step 5: Update the Interaction starter for seeded intake**

Replace:

```markdown
## Interaction starter

Open every new investigation with: "Describe the problem you're trying to solve."
```

with:

```markdown
## Interaction starter

If the first message contains the header `# Insights Forge intake brief`, skip the opening question — the analyst has pre-filled context with the intake form (`html/intake-form.html`); enter the seeded-intake procedure in `skills/context-framing/SKILL.md`.

Otherwise open every new investigation with: "Describe the problem you're trying to solve."
```

- [ ] **Step 6: Verify the edits**

Run: `grep -c "Communication protocol\|unvalidated — verify before use\|Insights Forge intake brief\|checkpoint mode" CLAUDE.md`
Expected: `5` or more (section heading + version-awareness cross-ref, two query bullets, starter, pacing).

Run: `grep -n "does not generate raw DQL" CLAUDE.md`
Expected: no output (old wording fully removed).

- [ ] **Step 7: Commit**

```bash
git add CLAUDE.md
git commit -m "Add communication protocol, query policy, and pacing guardrails to operating manual"
```

---

### Task 2: The intake form — `html/intake-form.html`

**Files:**
- Create: `html/intake-form.html`

**Interfaces:**
- Consumes: nothing.
- Produces: the seed-prompt markdown format (contract quoted below) that Task 3's seeded-intake mode parses. Header string: `# Insights Forge intake brief (v1)`. Config values: `CONFIG.thinWords = 15`, `CONFIG.specificDepthWords = 30`. Tier labels `Simple` / `Advanced`.

- [ ] **Step 1: Write the complete file**

Create `html/intake-form.html` with exactly this content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Insights Forge — Engagement Intake</title>
<style>
  :root {
    --navy:#07101e; --navy2:#0d1f38; --teal:#49C2B3; --blue:#1966FF;
    --magenta:#C93FDB; --gray:#6F747F; --gray-lt:#b0b5be; --white:#f0f4f8;
    --card:rgba(255,255,255,.04); --border:rgba(255,255,255,.14);
  }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--navy); color:var(--white); font-family:Arial,Helvetica,sans-serif; font-size:15px; line-height:1.55; padding:32px 16px 80px; }
  main { max-width:880px; margin:0 auto; }
  h1 { font-size:26px; margin-bottom:6px; }
  .lead { color:var(--gray-lt); margin-bottom:20px; max-width:640px; }
  fieldset { border:1px solid var(--border); border-radius:10px; padding:20px; margin-bottom:22px; background:var(--card); }
  legend { padding:0 10px; font-weight:bold; color:var(--teal); font-size:15px; }
  legend.req::after, label.req::after { content:" *"; color:var(--magenta); }
  label { display:block; margin:12px 0 4px; font-size:13px; color:var(--gray-lt); }
  input[type=text], select, textarea { width:100%; background:var(--navy2); color:var(--white); border:1px solid var(--border); border-radius:6px; padding:8px 10px; font-size:14px; font-family:inherit; }
  textarea { min-height:84px; resize:vertical; }
  .radio-cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:10px; }
  .radio-cards label { border:1px solid var(--border); border-radius:8px; padding:12px; cursor:pointer; margin:0; color:var(--white); font-size:13px; }
  .radio-cards label:has(input:checked) { border-color:var(--teal); background:rgba(73,194,179,.08); }
  .radio-cards input { margin-right:6px; }
  .radio-cards small { color:var(--gray-lt); display:block; margin-top:4px; }
  .inline-radios label { display:inline-block; margin-right:18px; color:var(--white); font-size:14px; cursor:pointer; }
  .row2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  .row3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; }
  .cap-group { margin-top:14px; }
  .cap-group h3 { font-size:12px; text-transform:uppercase; letter-spacing:.06em; color:var(--gray); margin-bottom:4px; }
  .cap-row { display:flex; align-items:center; gap:10px; margin:6px 0; font-size:14px; }
  .cap-row input { flex-shrink:0; }
  .cap-row select { width:auto; min-width:150px; }
  .hint { display:none; color:var(--magenta); font-size:12px; margin-top:4px; }
  .hint.show { display:block; }
  #tier-badge { position:sticky; top:0; z-index:5; background:var(--navy2); border:1px solid var(--border); border-radius:8px; padding:10px 14px; margin-bottom:20px; font-size:14px; }
  #tier-label.advanced { color:var(--teal); }
  #tier-hint { color:var(--gray-lt); font-size:12px; margin-left:8px; }
  button { background:var(--blue); color:#fff; border:none; border-radius:6px; padding:12px 22px; font-size:15px; cursor:pointer; margin-right:10px; }
  button.secondary { background:transparent; border:1px solid var(--border); color:var(--white); }
  button:disabled { opacity:.4; cursor:not-allowed; }
  #missing { color:var(--magenta); font-size:13px; margin:12px 0; white-space:pre-line; }
  #output { width:100%; min-height:300px; font-family:Menlo,Consolas,monospace; font-size:12px; margin-top:14px; display:none; }
  #output.show { display:block; }
  footer { color:var(--gray); font-size:12px; margin-top:40px; }
  @media (max-width:700px){ .row2,.row3 { grid-template-columns:1fr; } }
</style>
</head>
<body>
<main>
<header>
  <h1>Insights Forge — engagement intake</h1>
  <p class="lead">Fill in what you know. Required fields (<span style="color:var(--magenta)">*</span>) unlock prompt generation; optional depth upgrades the output tier. Paste the generated brief as your <strong>first message</strong> in a Claude Code session.</p>
</header>

<div id="tier-badge" aria-live="polite">Output tier: <strong id="tier-label">Simple</strong><span id="tier-hint"></span></div>

<form id="intake" onsubmit="return false">

<fieldset>
  <legend class="req">1 · Use case — what deliverable do you need?</legend>
  <div class="radio-cards" role="radiogroup" aria-label="Use case">
    <label><input type="radio" name="usecase" value="Executive one-pager"><strong>Executive one-pager</strong><small>A 2–3 minute leadership read with a 30/60/90 plan.</small></label>
    <label><input type="radio" name="usecase" value="Analyst execution guide"><strong>Analyst execution guide</strong><small>Step-by-step technical walkthrough for the analyst or account team.</small></label>
    <label><input type="radio" name="usecase" value="Customer action plan"><strong>Customer action plan</strong><small>Full phased plan the customer acts on (deepest path).</small></label>
    <label><input type="radio" name="usecase" value="QBR / renewal brief"><strong>QBR / renewal brief</strong><small>Value-realization narrative for a renewal or QBR conversation.</small></label>
  </div>
</fieldset>

<fieldset>
  <legend class="req">2 · Analyst context</legend>
  <div class="row3">
    <div>
      <label class="req" for="analyst-exp">Your experience with this tool + Dynatrace consulting</label>
      <select id="analyst-exp"><option value="">— select —</option><option>new</option><option>intermediate</option><option>expert</option></select>
    </div>
    <div>
      <label class="req" for="account-fam">Account familiarity</label>
      <select id="account-fam"><option value="">— select —</option><option>new-to-me</option><option>familiar</option><option>deep history</option></select>
    </div>
    <div>
      <label class="req" for="domain-fluency">Customer's own observability fluency</label>
      <select id="domain-fluency"><option value="">— select —</option><option>low</option><option>mixed</option><option>high</option></select>
    </div>
  </div>
</fieldset>

<fieldset>
  <legend class="req">3 · Customer basics</legend>
  <div class="row2">
    <div>
      <label class="req" for="customer-name">Customer name</label>
      <input type="text" id="customer-name" autocomplete="off">
    </div>
    <div>
      <label class="req" for="vertical">Vertical</label>
      <select id="vertical">
        <option value="">— select —</option>
        <option>Retail / E-commerce</option><option>Financial Services (FSI)</option>
        <option>Healthcare / Life Sciences</option><option>Manufacturing</option>
        <option>Telco / Media</option><option>Public Sector</option>
        <option>Technology / SaaS</option><option>Logistics / Supply Chain</option>
        <option>Other</option>
      </select>
      <input type="text" id="vertical-other" placeholder="Name the vertical" style="display:none;margin-top:6px">
    </div>
  </div>
  <div class="row2">
    <div>
      <label class="req" for="size">Company size</label>
      <select id="size"><option value="">— select —</option><option>SMB</option><option>mid-market</option><option>large enterprise</option><option>unsure</option></select>
    </div>
    <div>
      <label class="req">Tenant type</label>
      <div class="inline-radios">
        <label><input type="radio" name="tenant" value="SaaS"> SaaS</label>
        <label><input type="radio" name="tenant" value="Managed"> Managed</label>
        <label><input type="radio" name="tenant" value="unsure"> Unsure</label>
      </div>
    </div>
  </div>
</fieldset>

<fieldset>
  <legend class="req">4 · Engagement framing (C.S.I.R.)</legend>
  <label class="req" for="csir-context">Context — relationship history, mood, recent milestones</label>
  <textarea id="csir-context" class="thin" data-hint="A sentence or two more materially improves the plan — what changed, when, and who noticed?"></textarea>
  <div class="hint" id="csir-context-hint"></div>
  <label class="req" for="consultant-role">Your role</label>
  <select id="consultant-role"><option value="">— select —</option><option>CSM</option><option>SE</option><option>consultant</option><option>other</option></select>

  <label class="req" for="csir-specific">Specific information — known pain points, prior QBR outcomes, commitments, constraints</label>
  <textarea id="csir-specific" class="thin" data-hint="Name concrete facts: pain points, commitments made, environment constraints. This is the boundary of what the plan can use."></textarea>
  <div class="hint" id="csir-specific-hint"></div>

  <label class="req" for="intent-goal">Intent — primary goal</label>
  <select id="intent-goal">
    <option value="">— select —</option>
    <option>prove value</option><option>secure renewal</option><option>justify expansion</option>
    <option>prepare QBR narrative</option><option>improve digital experience</option>
    <option>diagnose a problem</option><option>other</option>
  </select>
  <label class="req" for="intent-success">What does a successful outcome look like?</label>
  <textarea id="intent-success" class="thin" data-hint="What would the customer say changed if this works? One concrete sentence beats a paragraph of goals."></textarea>
  <div class="hint" id="intent-success-hint"></div>

  <label>Response format — audience (check all that apply)</label>
  <div class="inline-radios">
    <label><input type="checkbox" id="aud-exec"> Executive</label>
    <label><input type="checkbox" id="aud-tech"> Technical</label>
    <label><input type="checkbox" id="aud-mixed"> Mixed</label>
  </div>
  <div class="row2">
    <div>
      <label for="time-window">Meeting / read time window</label>
      <select id="time-window"><option value="">— select —</option><option>15 min</option><option>30 min</option><option>60 min</option><option>async document</option></select>
    </div>
    <div>
      <label for="tone">Tone or branding constraints</label>
      <input type="text" id="tone" autocomplete="off">
    </div>
  </div>
</fieldset>

<fieldset>
  <legend class="req">5 · Active Dynatrace capabilities</legend>
  <p style="font-size:13px;color:var(--gray-lt)">Check what you know is active. Classic and Grail generations can both be live at once — say which where asked.</p>
  <div class="cap-group"><h3>Core observability</h3>
    <div class="cap-row"><input type="checkbox" id="cap-fullstack"><label for="cap-fullstack" style="margin:0;color:var(--white)">Full-Stack Monitoring (OneAgent)</label></div>
    <div class="cap-row"><input type="checkbox" id="cap-infra"><label for="cap-infra" style="margin:0;color:var(--white)">Infrastructure Monitoring only</label></div>
    <div class="cap-row"><input type="checkbox" id="cap-apm"><label for="cap-apm" style="margin:0;color:var(--white)">APM / Distributed Tracing</label></div>
  </div>
  <div class="cap-group"><h3>User experience</h3>
    <div class="cap-row"><input type="checkbox" id="cap-rum-web" data-gen="gen-rum-web"><label for="cap-rum-web" style="margin:0;color:var(--white)">Real User Monitoring — Web</label>
      <select id="gen-rum-web" style="display:none"><option>Classic only</option><option>Grail only</option><option>both</option><option selected>unsure</option></select></div>
    <div class="cap-row"><input type="checkbox" id="cap-rum-mobile" data-gen="gen-rum-mobile"><label for="cap-rum-mobile" style="margin:0;color:var(--white)">Real User Monitoring — Mobile</label>
      <select id="gen-rum-mobile" style="display:none"><option>Classic only</option><option>Grail only</option><option>both</option><option selected>unsure</option></select></div>
    <div class="cap-row"><input type="checkbox" id="cap-sr" data-gen="gen-sr"><label for="cap-sr" style="margin:0;color:var(--white)">Session Replay</label>
      <select id="gen-sr" style="display:none"><option>Classic only</option><option>Grail only</option><option>both</option><option selected>unsure</option></select></div>
    <div class="cap-row"><input type="checkbox" id="cap-synthetic"><label for="cap-synthetic" style="margin:0;color:var(--white)">Synthetic Monitoring</label></div>
  </div>
  <div class="cap-group"><h3>Data &amp; logs</h3>
    <div class="cap-row"><input type="checkbox" id="cap-logs"><label for="cap-logs" style="margin:0;color:var(--white)">Log Management (Grail)</label></div>
    <div class="cap-row"><input type="checkbox" id="cap-bizevents"><label for="cap-bizevents" style="margin:0;color:var(--white)">Business Analytics / Business Events</label></div>
    <div class="cap-row"><input type="checkbox" id="cap-metrics"><label for="cap-metrics" style="margin:0;color:var(--white)">Metrics ingestion (custom or third-party)</label></div>
  </div>
  <div class="cap-group"><h3>AI &amp; automation</h3>
    <div class="cap-row"><input type="checkbox" id="cap-davis"><label for="cap-davis" style="margin:0;color:var(--white)">Davis AI (problem detection)</label></div>
    <div class="cap-row"><input type="checkbox" id="cap-copilot"><label for="cap-copilot" style="margin:0;color:var(--white)">Davis CoPilot</label></div>
    <div class="cap-row"><input type="checkbox" id="cap-workflows"><label for="cap-workflows" style="margin:0;color:var(--white)">Workflows / Automation</label></div>
  </div>
  <div class="cap-group"><h3>Security</h3>
    <div class="cap-row"><input type="checkbox" id="cap-appsec"><label for="cap-appsec" style="margin:0;color:var(--white)">Application Security</label></div>
    <div class="cap-row"><input type="checkbox" id="cap-cloudsec"><label for="cap-cloudsec" style="margin:0;color:var(--white)">Cloud Security</label></div>
  </div>
  <div class="cap-group"><h3>Platform</h3>
    <div class="cap-row"><input type="checkbox" id="cap-grail"><label for="cap-grail" style="margin:0;color:var(--white)">Grail (data lakehouse)</label></div>
    <div class="cap-row"><input type="checkbox" id="cap-srg"><label for="cap-srg" style="margin:0;color:var(--white)">Site Reliability Guardian</label></div>
    <div class="cap-row"><input type="checkbox" id="cap-dashboards" data-gen="gen-dashboards"><label for="cap-dashboards" style="margin:0;color:var(--white)">Dashboards</label>
      <select id="gen-dashboards" style="display:none"><option>Gen2 (Classic)</option><option>Gen3 (Grail)</option><option>both</option><option selected>unsure</option></select></div>
    <div class="cap-row"><input type="checkbox" id="cap-notebooks"><label for="cap-notebooks" style="margin:0;color:var(--white)">Notebooks</label></div>
  </div>
  <div class="cap-row" style="margin-top:14px;border-top:1px solid var(--border);padding-top:12px">
    <input type="checkbox" id="caps-unsure"><label for="caps-unsure" style="margin:0;color:var(--white)"><em>Unsure — help me confirm capabilities during framing</em></label>
  </div>
</fieldset>

<fieldset id="s6">
  <legend id="s6-legend">6 · Focus application &amp; RUM status</legend>
  <p id="s6-note" style="font-size:13px;color:var(--gray-lt)">Optional — becomes required when your Intent is "improve digital experience".</p>
  <label for="app-name" id="app-name-label">Application name</label>
  <input type="text" id="app-name" autocomplete="off">
  <div class="row2">
    <div>
      <label id="rum-app-label">RUM enabled on this app?</label>
      <div class="inline-radios">
        <label><input type="radio" name="rum-app" value="yes"> Yes</label>
        <label><input type="radio" name="rum-app" value="no"> No</label>
        <label><input type="radio" name="rum-app" value="unsure"> Unsure</label>
      </div>
    </div>
    <div>
      <label id="sr-app-label">Session Replay active on this app?</label>
      <div class="inline-radios">
        <label><input type="radio" name="sr-app" value="yes"> Yes</label>
        <label><input type="radio" name="sr-app" value="no"> No</label>
        <label><input type="radio" name="sr-app" value="unsure"> Unsure</label>
      </div>
    </div>
  </div>
</fieldset>

<fieldset>
  <legend>7 · Stakeholders</legend>
  <div class="row2">
    <div>
      <label for="stakeholder-name">Primary audience — name and title</label>
      <input type="text" id="stakeholder-name" autocomplete="off">
    </div>
    <div>
      <label for="archetype">Role archetype</label>
      <select id="archetype">
        <option value="">— select —</option>
        <option>Executive Sponsor</option><option>Product Owner</option>
        <option>SRE / Reliability Engineer</option><option>IT Operations Manager</option>
        <option>Application Developer</option><option>Platform / DevOps Engineer</option>
        <option>Security / Compliance Officer</option><option>Data / Analytics Lead</option>
        <option>unsure</option>
      </select>
    </div>
  </div>
  <label for="kpis">What leadership cares about — named KPIs, strategic priorities <em>(upgrades output tier)</em></label>
  <textarea id="kpis"></textarea>
  <label for="tech-priorities">Technical team priorities — day-to-day pain points <em>(upgrades output tier)</em></label>
  <textarea id="tech-priorities"></textarea>
</fieldset>

<fieldset>
  <legend>8 · Engagement trigger</legend>
  <select id="trigger"><option value="">— select —</option><option>QBR</option><option>renewal</option><option>expansion</option><option>scheduled touchpoint</option><option>incident follow-up</option><option>other</option></select>
</fieldset>

<div id="missing" role="alert"></div>
<button id="generate">Generate seed prompt</button>
<button id="copy" class="secondary" disabled>Copy to clipboard</button>
<button id="download" class="secondary" disabled>Download .md</button>
<textarea id="output" readonly aria-label="Generated seed prompt"></textarea>

</form>
<footer>© 2026 Dynatrace, LLC. &nbsp; Internal tool — Insights Forge intake v1.</footer>
</main>

<script>
const CONFIG = { thinWords: 15, specificDepthWords: 30 };
const BRIEF_HEADER = '# Insights Forge intake brief (v1)';

const $ = id => document.getElementById(id);
const val = id => ($(id) && $(id).value.trim()) || '';
const orNP = s => s || 'not provided';
const wordCount = s => s ? s.trim().split(/\s+/).filter(Boolean).length : 0;
const radioVal = name => { const r = document.querySelector(`input[name="${name}"]:checked`); return r ? r.value : ''; };

const CAPS = [
  ['cap-fullstack','Full-Stack Monitoring (OneAgent)'],['cap-infra','Infrastructure Monitoring only'],
  ['cap-apm','APM / Distributed Tracing'],['cap-rum-web','RUM — Web'],['cap-rum-mobile','RUM — Mobile'],
  ['cap-sr','Session Replay'],['cap-synthetic','Synthetic Monitoring'],['cap-logs','Log Management (Grail)'],
  ['cap-bizevents','Business Analytics / Business Events'],['cap-metrics','Metrics ingestion'],
  ['cap-davis','Davis AI'],['cap-copilot','Davis CoPilot'],['cap-workflows','Workflows / Automation'],
  ['cap-appsec','Application Security'],['cap-cloudsec','Cloud Security'],['cap-grail','Grail (data lakehouse)'],
  ['cap-srg','Site Reliability Guardian'],['cap-dashboards','Dashboards'],['cap-notebooks','Notebooks']
];

function capLines() {
  const lines = [];
  for (const [id, label] of CAPS) {
    const box = $(id);
    if (!box.checked) continue;
    const genSel = box.dataset.gen ? $(box.dataset.gen) : null;
    lines.push(`- ${label}${genSel ? `: ${genSel.value}` : ''}`);
  }
  if ($('caps-unsure').checked) lines.push('- Capabilities unconfirmed — analyst requests help confirming during framing');
  return lines.length ? lines.join('\n') : 'not provided';
}

function s6Complete() {
  return !!(val('app-name') && radioVal('rum-app') && radioVal('sr-app'));
}

function computeTier() {
  const a = wordCount(val('kpis')) >= CONFIG.thinWords;
  const b = wordCount(val('tech-priorities')) >= CONFIG.thinWords;
  const c = wordCount(val('csir-specific')) >= CONFIG.specificDepthWords || s6Complete();
  return (a && b && c) ? 'Advanced' : 'Simple';
}

function tierHint() {
  if (computeTier() === 'Advanced') return ' — full-depth plan unlocked';
  const needs = [];
  if (wordCount(val('kpis')) < CONFIG.thinWords) needs.push('leadership KPIs');
  if (wordCount(val('tech-priorities')) < CONFIG.thinWords) needs.push('technical team priorities');
  if (wordCount(val('csir-specific')) < CONFIG.specificDepthWords && !s6Complete()) needs.push('more specific information or the focus-app section');
  return needs.length ? ` — add ${needs.join(', ')} to unlock Advanced` : '';
}

function updateTier() {
  const t = computeTier();
  $('tier-label').textContent = t;
  $('tier-label').className = t === 'Advanced' ? 'advanced' : '';
  $('tier-hint').textContent = tierHint();
}

function updateThinHints() {
  document.querySelectorAll('textarea.thin').forEach(ta => {
    const hint = $(ta.id + '-hint');
    const wc = wordCount(ta.value);
    if (wc > 0 && wc < CONFIG.thinWords) { hint.textContent = ta.dataset.hint; hint.classList.add('show'); }
    else hint.classList.remove('show');
  });
}

function s6Required() { return val('intent-goal') === 'improve digital experience'; }

function updateS6() {
  const req = s6Required();
  $('s6-legend').classList.toggle('req', req);
  $('app-name-label').classList.toggle('req', req);
  $('rum-app-label').classList.toggle('req', req);
  $('sr-app-label').classList.toggle('req', req);
  $('s6-note').textContent = req
    ? 'Required — your Intent is "improve digital experience", so RUM status decides whether the UX story is available.'
    : 'Optional — becomes required when your Intent is "improve digital experience".';
}

function validate() {
  const missing = [];
  if (!radioVal('usecase')) missing.push('Use case (section 1)');
  if (!val('analyst-exp')) missing.push('Analyst experience (section 2)');
  if (!val('account-fam')) missing.push('Account familiarity (section 2)');
  if (!val('domain-fluency')) missing.push('Customer domain fluency (section 2)');
  if (!val('customer-name')) missing.push('Customer name (section 3)');
  if (!val('vertical') || (val('vertical') === 'Other' && !val('vertical-other'))) missing.push('Vertical (section 3)');
  if (!val('size')) missing.push('Company size (section 3)');
  if (!radioVal('tenant')) missing.push('Tenant type (section 3)');
  if (!val('csir-context')) missing.push('C.S.I.R. Context (section 4)');
  if (!val('consultant-role')) missing.push('Your role (section 4)');
  if (!val('csir-specific')) missing.push('C.S.I.R. Specific information (section 4)');
  if (!val('intent-goal')) missing.push('Intent goal (section 4)');
  if (!val('intent-success')) missing.push('Successful outcome (section 4)');
  const anyCap = CAPS.some(([id]) => $(id).checked) || $('caps-unsure').checked;
  if (!anyCap) missing.push('At least one capability, or "unsure" (section 5)');
  if (s6Required() && !s6Complete()) missing.push('Focus application & RUM status (section 6 — required for digital-experience intent)');
  return missing;
}

function audienceText() {
  const a = [];
  if ($('aud-exec').checked) a.push('executive');
  if ($('aud-tech').checked) a.push('technical');
  if ($('aud-mixed').checked) a.push('mixed');
  return a.join(', ');
}

function verticalText() {
  return val('vertical') === 'Other' ? val('vertical-other') : val('vertical');
}

function buildBrief() {
  const today = new Date().toISOString().slice(0, 10);
  return `${BRIEF_HEADER}

> Agent: treat this as a seeded Phase 0 intake per skills/context-framing/SKILL.md.

## Meta
- Use case: ${orNP(radioVal('usecase'))}
- Output tier: ${computeTier()}
- Analyst experience: ${orNP(val('analyst-exp'))} · Account familiarity: ${orNP(val('account-fam'))} · Customer domain fluency: ${orNP(val('domain-fluency'))}
- Generated: ${today}

## Customer
- Name: ${orNP(val('customer-name'))}
- Vertical: ${orNP(verticalText())}
- Size: ${orNP(val('size'))}
- Tenant type: ${orNP(radioVal('tenant'))}

## Engagement framing (C.S.I.R.)
### Context
${orNP(val('csir-context'))}
Consultant role: ${orNP(val('consultant-role'))}
### Specific information
${orNP(val('csir-specific'))}
### Intent
Goal: ${orNP(val('intent-goal'))}
Success looks like: ${orNP(val('intent-success'))}
### Response format
Deliverable: ${orNP(radioVal('usecase'))}
Audience: ${orNP(audienceText())}
Time window: ${orNP(val('time-window'))}
Tone/branding constraints: ${orNP(val('tone'))}

## Active capabilities
${capLines()}

## Focus application
- Application: ${orNP(val('app-name'))}
- RUM enabled: ${orNP(radioVal('rum-app'))}
- Session Replay active: ${orNP(radioVal('sr-app'))}

## Stakeholders
- Primary audience: ${orNP(val('stakeholder-name'))}
- Role archetype: ${orNP(val('archetype'))}
- Leadership priorities: ${orNP(val('kpis'))}
- Technical team priorities: ${orNP(val('tech-priorities'))}

## Trigger
${orNP(val('trigger'))}
`;
}

document.addEventListener('input', () => { updateTier(); updateThinHints(); });
document.addEventListener('change', e => {
  if (e.target.id === 'vertical') $('vertical-other').style.display = val('vertical') === 'Other' ? 'block' : 'none';
  if (e.target.id === 'intent-goal') updateS6();
  if (e.target.dataset && e.target.dataset.gen) $(e.target.dataset.gen).style.display = e.target.checked ? 'inline-block' : 'none';
  updateTier();
});

$('generate').addEventListener('click', () => {
  const missing = validate();
  if (missing.length) {
    $('missing').textContent = 'Required before generating:\n· ' + missing.join('\n· ');
    $('output').classList.remove('show');
    $('copy').disabled = $('download').disabled = true;
    return;
  }
  $('missing').textContent = '';
  $('output').value = buildBrief();
  $('output').classList.add('show');
  $('copy').disabled = $('download').disabled = false;
});

$('copy').addEventListener('click', async () => {
  try { await navigator.clipboard.writeText($('output').value); $('copy').textContent = 'Copied ✓'; }
  catch { $('output').select(); document.execCommand('copy'); $('copy').textContent = 'Copied ✓'; }
  setTimeout(() => { $('copy').textContent = 'Copy to clipboard'; }, 1600);
});

$('download').addEventListener('click', () => {
  const name = (val('customer-name') || 'intake').toLowerCase().replace(/[^a-z0-9]+/g, '-');
  const blob = new Blob([$('output').value], { type: 'text/markdown' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `insights-forge-intake-${name}-${new Date().toISOString().slice(0,10)}.md`;
  a.click();
  URL.revokeObjectURL(a.href);
});

updateTier(); updateS6();
</script>
</body>
</html>
```

- [ ] **Step 2: Verify no external requests**

Run: `grep -nE 'https?://|@import|url\(' html/intake-form.html`
Expected: no output.

- [ ] **Step 3: Browser walkthrough (manual)**

Run: `open html/intake-form.html` and verify each acceptance criterion:

1. Click **Generate** immediately → magenta list names every missing required field; no output shown.
2. Fill only required core (use case, section 2 selects, customer basics, three C.S.I.R. textareas + role + goal, one capability) → tier badge reads **Simple** with an upgrade hint; Generate produces the brief; every unfilled field reads `not provided`.
3. Type 5 words into Context → magenta hint appears; extend past 15 words → hint disappears.
4. Fill KPIs (15+ words), technical priorities (15+ words), and complete section 6 → badge flips to **Advanced**.
5. Set Intent goal to "improve digital experience" → section 6 legend gains the required asterisk and Generate blocks until it is complete.
6. Check RUM — Web → generation dropdown appears (defaults to "unsure"); pick "both" → brief line reads `- RUM — Web: both`.
7. Copy and Download both work; downloaded file opens with `# Insights Forge intake brief (v1)`.
8. Narrow the window below 700px → two-column rows stack to one column; nothing overflows horizontally.

- [ ] **Step 4: Commit**

```bash
git add html/intake-form.html
git commit -m "Add analyst intake form generating Phase 0 seed prompt"
```

---

### Task 3: Seeded-intake mode — `skills/context-framing/SKILL.md`

**Files:**
- Modify: `skills/context-framing/SKILL.md`

**Interfaces:**
- Consumes: the brief format from Task 2 (header `# Insights Forge intake brief (v1)`; sections Meta / Customer / Engagement framing (C.S.I.R.) / Active capabilities / Focus application / Stakeholders / Trigger; sentinel `not provided`).
- Produces: `current-context.md` gains an "Intake meta" row and a "Known context gaps" row that downstream skills may read (Task 5/6 do not depend on them; they are engagement-file additions).

- [ ] **Step 1: Add the seeded-intake procedure**

In `skills/context-framing/SKILL.md`, immediately after the paragraph ending "Do not ask multiple questions at once. Let each answer drive the next question." (end of the Inputs section), insert:

```markdown
## Seeded intake (form brief detected)

If the first user message contains the header `# Insights Forge intake brief`, the analyst pre-filled the intake form (`html/intake-form.html`). Do not open with the standard prompt or walk Q1–Q9 serially. Instead:

1. **Parse every brief field onto the Q1–Q9 / C.S.I.R. structure.** A field with a real value is answered — do not re-ask it. A field reading `not provided` is unanswered.
2. **Run the thin-answer check on pre-filled MUST-HAVE fields.** An answer of only a few words does not count as satisfied. Ask **at most one follow-up per thin field** — e.g., "You gave me three words about session replay — tell me more: what are users doing when it matters?" Whatever comes back, including "that's all I know," is accepted; record the residual gap under "Known context gaps" in `current-context.md`. Never loop on the same field. This is the anti-wall rule.
3. **Batch SHOULD-HAVE confirmations into the gate message** (the existing "not required to proceed, but…" phrasing) instead of asking them one at a time.
4. **Record the intake meta** in `current-context.md`: use case, analyst experience, account familiarity, customer domain fluency, and output tier (Simple or Advanced).
5. **Bind the Phase 3 deliverable now** from the use case: Executive one-pager / Customer action plan → `exec-onepager` (plan-first path); Analyst execution guide → action-plan detail emphasis; QBR / renewal brief → `value-highlight`. Downstream skills read the output tier to scale sophistication, and analyst experience to calibrate how much the agent explains and how often it checkpoints (new → more of both).
6. **The exit-criteria rubric is unchanged.** A seeded brief pre-populates the rubric; every MUST-HAVE must still hold a real value before the gate closes.

Unseeded sessions run the standard flow below — and the same thin-answer rule applies to conversational answers: a MUST-HAVE answered in a few words gets exactly one follow-up, then the residual gap is recorded.
```

- [ ] **Step 2: Add the generation split to the Q5 checklist**

In the Q5 checklist, replace these four lines:

```markdown
- [ ] Real User Monitoring — Web
- [ ] Real User Monitoring — Mobile
- [ ] Session Replay
```

and

```markdown
- [ ] Dashboards & Notebooks
```

with:

```markdown
- [ ] Real User Monitoring — Web (Classic / Grail / both / unsure)
- [ ] Real User Monitoring — Mobile (Classic / Grail / both / unsure)
- [ ] Session Replay (Classic / Grail / both / unsure)
```

and

```markdown
- [ ] Dashboards (Gen2 / Gen3 / both / unsure)
- [ ] Notebooks
```

Then append to the paragraph after the checklist ("Record the checked items…"):

```markdown
For every generation-split capability (RUM, Session Replay, Dashboards), record which generation is active — Classic and Grail can both be live on the same client at once, and they differ in what is queryable (see "Capability generations" in `memory/long-term/domain-knowledge.md`).
```

- [ ] **Step 3: Add the new rows to the Output section table**

In the Output section's body-sections table, after the row `| Engagement Framing (C.S.I.R.) | ... |`, add:

```markdown
| Intake meta | Use case; analyst experience; account familiarity; customer domain fluency; output tier (Simple/Advanced). Populated from a seeded intake brief; recorded as `not provided` otherwise |
| Known context gaps | Fields where the analyst could not go deeper after one follow-up — carried forward so downstream phases treat them as open, not answered |
```

- [ ] **Step 4: Add common pitfalls**

Append to the Common pitfalls list:

```markdown
- **Re-asking a field the intake brief already answered.** The brief is the analyst's context, gathered once. Re-asking it burns goodwill and makes the form pointless. Parse first; ask only about `not provided` and thin fields.
- **Looping on a thin answer.** One follow-up per thin field, then accept and record the gap. An analyst who cannot go deeper is telling you the context boundary — respect it and name the gap in the artifact instead.
```

- [ ] **Step 5: Verify**

Run: `grep -c "Seeded intake\|Known context gaps\|Classic / Grail / both / unsure\|Gen2 / Gen3" skills/context-framing/SKILL.md`
Expected: `7` or more.

Run: `grep -n "Dashboards & Notebooks" skills/context-framing/SKILL.md`
Expected: no output.

- [ ] **Step 6: Commit**

```bash
git add skills/context-framing/SKILL.md
git commit -m "Add seeded-intake mode, thin-answer rule, and capability generation split to Phase 0"
```

---

### Task 4: Phase 1 checkpoint mode

**Files:**
- Modify: `skills/mece-decomposition/SKILL.md`
- Modify: `skills/hypothesis-generation/SKILL.md`
- Modify: `skills/signal-mapping/SKILL.md`
- Modify: `docs/workflow.md`

**Interfaces:**
- Consumes: the `## Communication protocol` section name from Task 1 (referenced verbatim as "the CLAUDE.md communication protocol").
- Produces: the setting name **"Phase 1 checkpoint mode"** used identically in all four files.

- [ ] **Step 1: Add the ambiguity rule and checkpoint step to mece-decomposition**

In `skills/mece-decomposition/SKILL.md`, at the end of step 2 (after "Do not mix axes inside a single level of the tree."), append:

```markdown
If two axes fit comparably well, present both with one line on what each surfaces best and ask (per the CLAUDE.md communication protocol) rather than picking silently — this is a Phase 1 checkpoint mode behavior.
```

After step 10 ("Write to `<ENGAGEMENT_PATH>/issue-tree.md`…"), add:

```markdown
11. **Checkpoint (Phase 1 checkpoint mode — default ON).** Before hypothesis generation begins, pause and present per the CLAUDE.md communication protocol: a 2–3 sentence summary of the tree and its axis, the choice (confirm / adjust / name a lens), and a pointer to `issue-tree.md`. Skip this step only if the user has explicitly turned Phase 1 checkpoint mode off for the session.
```

- [ ] **Step 2: Add the checkpoint step to hypothesis-generation**

In `skills/hypothesis-generation/SKILL.md`, between step 5 (the Consultative framing pass) and step 6 (hand off to signal mapping), insert (using the repo's suffix convention, as with `2a.` in action-plan-builder):

```markdown
5a. **Checkpoint (Phase 1 checkpoint mode — default ON).** Before handing off to signal mapping, pause and present per the CLAUDE.md communication protocol: a 2–3 sentence summary of the hypothesis set (count per branch, any `blocked: instrumentation` rows), the choice (confirm / adjust / name a lens), and a pointer to `hypotheses.md`. If a playbook match for a hypothesis was a genuinely ambiguous call, say which playbook was chosen and why, and ask. Skip only if the user has turned Phase 1 checkpoint mode off.
```

- [ ] **Step 3: Add the checkpoint step to signal-mapping**

In `skills/signal-mapping/SKILL.md`, between step 6 and step 7 ("Hand off to ICE scoring"), insert:

```markdown
6a. **Checkpoint (Phase 1 checkpoint mode — default ON).** Before invoking ICE scoring, pause and present per the CLAUDE.md communication protocol: a 2–3 sentence summary of the signal chains and the consolidated instrumentation gaps, the choice (confirm / adjust / name a lens), and a pointer to `signals-map.md`. Skip only if the user has turned Phase 1 checkpoint mode off.
```

- [ ] **Step 4: Note checkpoint mode in docs/workflow.md Phase 1**

In `docs/workflow.md`, after the Phase 1 numbered list (after the paragraph beginning "In Phase 1, ICE Confidence means…"), insert:

```markdown
**Phase 1 checkpoint mode (default ON).** The agent pauses for a quick confirmation after each of the three artifacts rather than running the whole phase to a single gate — and when a structuring call is genuinely ambiguous (which decomposition axis, which playbook match), it asks instead of silently choosing. Once the team trusts the agent's judgment on these calls, tell it to turn Phase 1 checkpoint mode off and it reverts to the single end-of-phase gate.
```

- [ ] **Step 5: Verify**

Run: `grep -c "Phase 1 checkpoint mode" skills/mece-decomposition/SKILL.md skills/hypothesis-generation/SKILL.md skills/signal-mapping/SKILL.md docs/workflow.md`
Expected: each file reports at least `1` (mece-decomposition reports `2`).

- [ ] **Step 6: Commit**

```bash
git add skills/mece-decomposition/SKILL.md skills/hypothesis-generation/SKILL.md skills/signal-mapping/SKILL.md docs/workflow.md
git commit -m "Add Phase 1 checkpoint mode: per-artifact confirmation and ask-on-ambiguity"
```

---

### Task 5: Phase 2 direction check + council round checkpoints

**Files:**
- Modify: `skills/action-plan-builder/SKILL.md`
- Modify: `docs/lenses.md`
- Modify: `docs/workflow.md`

**Interfaces:**
- Consumes: "the CLAUDE.md communication protocol" (Task 1). Checkpoint verbs: **continue / steer / proceed**.
- Produces: nothing downstream depends on these edits.

- [ ] **Step 1: Add the direction check to action-plan-builder**

In `skills/action-plan-builder/SKILL.md`, between step 1 (MECE on the opportunity space) and step 2, insert:

```markdown
1a. **Direction check (default ON).** Before building the full plan, draft a one-screen skeleton: the headline framing, the wave/phase structure, and the candidate action list as titles only — no owners, no exit criteria, no detail. Present it per the CLAUDE.md communication protocol (confirm direction / redirect) and wait. Only after confirmation do steps 2–9 run. A redirect here costs minutes; a redirect after the council costs a rebuilt plan.
```

- [ ] **Step 2: Add round checkpoints to the council procedure**

In step 6 of `skills/action-plan-builder/SKILL.md`, after the "**Continue if needed.**" bullet and before the "**Reconciliation — the agent decides (after the rounds).**" paragraph, insert:

```markdown
   - **Round checkpoints (always).** After each round completes, pause and present per the CLAUDE.md communication protocol: 2–3 bullets per lens on its material position or what shifted this round, where the live tensions stand, and what the next round will do. The user chooses: **continue** (run the next round as planned), **steer** (their guidance is injected verbatim into every lens's briefing for the next round), or — after the final round — **proceed** to reconciliation and ICE re-ranking. Checkpoints add visibility and steering, never skipping: the ≥3-round minimum and the full four-lens set always run.
```

- [ ] **Step 3: Add the black-box pitfall**

Append to Common pitfalls in `skills/action-plan-builder/SKILL.md`:

```markdown
- **Running the council as a black box.** The user sees a round summary after every round and can steer the next one. Skipping the checkpoints hides exactly the deliberation the user most needs visibility into — and steering arrives too late to matter.
```

- [ ] **Step 4: Update docs/lenses.md council section**

In `docs/lenses.md`, in "## The Phase 2 council runs in rounds", after the numbered round list and before "Only then does the **agent reconcile**…", insert:

```markdown
After every round the agent pauses with a round summary — each lens's position or shift, the live tensions, what the next round will do — and you can **continue**, **steer** (your guidance goes verbatim into every lens's next-round briefing), or, after the final round, **proceed** to reconciliation. The checkpoints never skip anything: three rounds is still the floor and all four lenses always run.
```

- [ ] **Step 5: Update docs/workflow.md Phase 2**

In `docs/workflow.md` Phase 2, in numbered item 2 ("**Draft the plan** against that set…"), prepend the sentence:

```markdown
A one-screen direction check — headline, wave structure, candidate action titles — is confirmed with you before the full draft is built.
```

In numbered item 3 ("**Convene the persona council…**"), after "(more rounds if they're still moving)", insert:

```markdown
After every round you get a progress summary and can steer the next round or let it continue.
```

- [ ] **Step 6: Verify**

Run: `grep -c "Direction check\|Round checkpoints\|steer" skills/action-plan-builder/SKILL.md docs/lenses.md docs/workflow.md`
Expected: each file reports at least `1` (action-plan-builder at least `3`).

- [ ] **Step 7: Commit**

```bash
git add skills/action-plan-builder/SKILL.md docs/lenses.md docs/workflow.md
git commit -m "Add Phase 2 direction check and council round checkpoints"
```

---

### Task 6: One-pager restructure — `skills/exec-onepager/SKILL.md`

**Files:**
- Modify: `skills/exec-onepager/SKILL.md`
- Modify: `skills/pptx-builder/SKILL.md`
- Modify: `docs/deliverables.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the fixed section order and 30/60/90 block names that `pptx-builder` inherits.

- [ ] **Step 1: Replace the Content structure section**

In `skills/exec-onepager/SKILL.md`, replace the entire `## Content structure` section (from the heading through the end of item 5) with:

```markdown
## Content structure

Every one-pager uses this fixed section order — identical for every analyst and engagement. Consistency is a pilot requirement: deliverables must be recognizable at a glance and attachable in Salesforce without re-explanation.

**Density target: 450–550 words of prose — a 2–3 minute read.** The one-page constraint alone does not control density; count the words. Over target → cut, don't compress.

1. **TL;DR (one bold sentence).** What is happening and what the reader is being asked to decide. Written last, placed first.
2. **Situation (2–3 sentences).** What is the problem, what is the urgency, what changed in the business — not what was observed in telemetry.
3. **Business impact.** Quantify where possible. "Conversion on iOS checkout has declined 8% week-over-week — approximately $X/week in revenue at risk." Name confidence intervals or assumptions in one short clause. Avoid false precision.
4. **Key findings (3–5 bullets).** Confirmed hypotheses, high-ICE open ones, and the instrumentation gaps that matter. One sentence each — what was found and what evidence supports it.
5. **Recommended actions — 30/60/90-day plan.** Three labeled blocks: **Days 0–30**, **Days 31–60**, **Days 61–90**. Every action carries an **owner**, a **timeframe**, and its **cost or risk on the same line**. Rank order within each block mirrors `action-plan.md` — no silent re-ordering, and block assignment is part of plan fidelity.
6. **Risks and decision asks.** One short paragraph or three bullets: the questions the leader needs to answer, ending with the specific decision being requested.
7. **Sources.** The footnote block — externally sourced facts keep URL + retrieval date here, not inline.
```

- [ ] **Step 2: Extend the finalizing gates**

In the `## Finalizing` section of `skills/exec-onepager/SKILL.md`:

In the **Plan-fidelity gate** item 1, replace "The recommended-actions section lists actions in the same order the action plan ranks them. No silent re-ordering, promotion, or demotion." with:

```markdown
The recommended-actions section lists actions in the same order the action plan ranks them, and each action sits in the correct 30/60/90 block for its timeframe. No silent re-ordering, promotion, demotion, or block reassignment.
```

After the **One-page constraint** bullet, add:

```markdown
- **Word-count gate.** Count the prose words (body text; exclude header metadata and the sources block). Target 450–550. Over 550 → cut, don't compress; under 450 is fine if the story is complete. Report the count when presenting the deliverable.
```

- [ ] **Step 3: Add the structural exemplar**

At the end of `skills/exec-onepager/SKILL.md` (after Common pitfalls), append:

````markdown
## Structural exemplar (anonymized)

The shape below is extracted from the strongest pilot deliverable. Client content removed — follow the shape, not the words. Color assignments per brand spec: teal = confirmed/available, royal blue = open/requires action, magenta = gap/risk.

```text
TL;DR: [Customer] can answer three of its four digital-experience questions today —
the fourth needs a one-time configuration sprint leadership must approve.

SITUATION (2–3 sentences)
Since [transition/event], [what the business can't do]. [Who is affected and how].

BUSINESS IMPACT
[Quantified where possible; assumption named in one clause.]

KEY FINDINGS (3–5, one sentence each, color-coded)
• Available today — [capability] answers [question] with no new instrumentation. (teal)
• Configuration required — [outcome] needs [one-time work]; cost of delay: [what stays broken]. (blue)
• Platform advantage — [what this platform does that the old one could not]. (teal, with caveat if conditional)
• Known gap — [capability] is not available; [honest workaround]. (magenta)

RECOMMENDED ACTIONS — 30/60/90
Days 0–30:  [action] — [owner] · [timeframe] · Cost/risk: [same line]
Days 31–60: [action] — [owner] · [timeframe] · Cost/risk: [same line]
Days 61–90: [action] — [owner] · [timeframe] · Cost/risk: [same line]

RISKS AND DECISION ASKS
DA-1: [specific approval needed and from whom]
DA-2: [specific approval needed and from whom]

SOURCES
[URL + retrieval date footnotes]
```
````

- [ ] **Step 4: pptx-builder inherits the 30/60/90 structure**

In `skills/pptx-builder/SKILL.md`, at the end of the `## Deck structure` section, append:

```markdown
The recommended-actions slide(s) inherit the one-pager's 30/60/90-day blocks — Days 0–30, Days 31–60, Days 61–90 — in the same order and block assignment. Do not flatten them back into a single list.
```

- [ ] **Step 5: Update docs/deliverables.md**

In `docs/deliverables.md`, in the "## What the one-pager looks like" section, append:

```markdown
Structure is fixed across every engagement: a one-sentence TL;DR up top, then situation, business impact, key findings, a 30/60/90-day action plan, decision asks, and sources. Density target is 450–550 words of prose — a 2–3 minute read — enforced at the finalizing gate alongside the one-page constraint.
```

- [ ] **Step 6: Verify**

Run: `grep -c "TL;DR\|30/60/90\|450–550" skills/exec-onepager/SKILL.md skills/pptx-builder/SKILL.md docs/deliverables.md`
Expected: exec-onepager at least `5`; pptx-builder at least `1`; deliverables at least `2`.

- [ ] **Step 7: Commit**

```bash
git add skills/exec-onepager/SKILL.md skills/pptx-builder/SKILL.md docs/deliverables.md
git commit -m "Restructure one-pager: TL;DR, 30/60/90 plan, 450-550 word target, fixed section order"
```

---

### Task 7: Capability generations + version audit (ends at a user-approval gate)

**Files:**
- Modify: `memory/long-term/domain-knowledge.md` (only after user approval)
- Modify: `memory/long-term/dynatrace-playbooks.md` (only after user approval)

**Interfaces:**
- Consumes: the version-awareness rule wording from Task 1 (must stay consistent).
- Produces: the "Capability generations" section title that CLAUDE.md (Task 1) and context-framing (Task 3) already cross-reference.

- [ ] **Step 1: Fetch current doc dates**

For each URL below, use WebFetch to confirm the page exists and capture its last-updated date (ask: "What is this page's last-updated date and what does it say about Classic vs Grail generations?"):

- `https://docs.dynatrace.com/docs/platform/grail/dynatrace-grail`
- `https://docs.dynatrace.com/docs/observe/digital-experience/rum-grail` (RUM on Grail; if 404, search docs.dynatrace.com for "Real User Monitoring on Grail" and use the canonical URL found)
- `https://docs.dynatrace.com/docs/observe/digital-experience/session-replay` (Session Replay; note any Classic-vs-Grail split described)
- `https://docs.dynatrace.com/docs/analyze-explore-automate/dashboards-classic` (Gen2 dashboards; if 404, find the canonical "Dashboards Classic" page)

Record the resolved URL, page-last-updated, and retrieval date (today) for each — these fill the citation clauses in Step 2.

- [ ] **Step 2: Draft the Capability generations section**

Draft (do not yet write) this section for `memory/long-term/domain-knowledge.md`, to be inserted after the "## Dynatrace-specific concepts" section. Fill each `(Source: …)` clause with the resolved URL + dates from Step 1:

```markdown
## Capability generations (Classic vs Grail / Gen3)

Several Dynatrace capabilities exist in two generations with different query paths and different data models. **Both generations can be active on the same client at the same time.** Never assume a capability or query path is available from the capability name alone — confirm which generation is active first (Q5 in context-framing captures this per client).

| Capability | Classic (Gen2) | Grail (Gen3) | Query path |
|---|---|---|---|
| RUM | RUM Classic — user actions, USQL-queryable, session action limits apply | RUM on Grail — gesture-level `user.events`, no session action limit, OpenPipeline | Classic → USQL; Grail → DQL |
| Session Replay | Session Replay Classic | Session Replay on Grail | Replay is visual; behavioral queries follow the RUM generation |
| Dashboards | Dashboards Classic (Gen2) — classic metrics and USQL tiles | Dashboards (Gen3) — Grail-backed, DQL tiles | Gen2 tiles cannot query Grail tables; Gen3 tiles cannot use classic USQL |
| Custom metrics | Classic custom metrics (metric keys, calculated service metrics) | Grail metrics (ingested via OpenPipeline, DQL `timeseries`) | Classic → metric selectors; Grail → DQL |

*(Source citations: one per row, from Step 1 fetches — URL, page-last-updated, retrieved date.)*

**Standing rule:** DQL applies to Gen3/Grail data only; USQL applies to Classic RUM. A query example in a deliverable must match the generation confirmed active for that client and data type — if the generation is unconfirmed, name the gap instead of guessing the query path.
```

- [ ] **Step 3: Audit the long-term files for version-ambiguous statements**

Run: `grep -n -i "RUM\|USQL\|DQL\|session replay\|dashboard\|custom metric" memory/long-term/dynatrace-playbooks.md memory/long-term/domain-knowledge.md`

For every hit, read the surrounding statement and classify: **(a) generation-explicit** (already says Classic or Grail) — no change; **(b) generation-ambiguous** (assumes one generation silently — e.g., a playbook step that says "query user actions with USQL" without noting it is Classic-only, or "fetch user.events" without noting it requires RUM on Grail) — draft a one-line edit adding the generation qualifier; **(c) generation-irrelevant** — no change. Collect all (b) edits into a numbered list: file, line, current text, proposed text.

- [ ] **Step 4: Present the proposed edits for approval — STOP**

Present to the user in one message: the drafted Capability generations section (Step 2) and the numbered audit edit list (Step 3). Long-term memory writes require explicit approval. **Do not write either file until the user approves.** Apply exactly what is approved, then bump any affected page-last-updated/retrieved citation dates.

- [ ] **Step 5: Verify (after approval + write)**

Run: `grep -c "Capability generations\|Standing rule" memory/long-term/domain-knowledge.md`
Expected: at least `2`.

- [ ] **Step 6: Commit**

```bash
git add memory/long-term/domain-knowledge.md memory/long-term/dynatrace-playbooks.md
git commit -m "Add capability generations reference and version-qualify ambiguous statements"
```

---

### Task 8: ROADMAP rulings + getting-started intake path

**Files:**
- Modify: `ROADMAP.md`
- Modify: `docs/getting-started.md`

**Interfaces:**
- Consumes: the ruling wording from the spec (quoted below verbatim).
- Produces: nothing downstream.

- [ ] **Step 1: Add the rulings section to ROADMAP.md**

At the top of `ROADMAP.md`, immediately after the intro paragraph ("Candidate improvements surfaced during…"), insert:

```markdown
---

## Pilot round 2 — rulings and committed changes (2026-07-06)

Implemented per `docs/superpowers/specs/2026-07-06-pilot-round2-intake-and-guardrails-design.md`. Four rulings are settled — do not re-litigate without new evidence:

| Decision | Ruling |
|---|---|
| v1 intake form scope | All four use cases in one form; the pilot may still be run narrowly by instruction. |
| Input depth enforcement | Tiered form + agent probes: required core blocks generation; thin answers get one follow-up max, then the gap is recorded. |
| Raw query examples | Structural pseudo-queries in conversation; illustrative editable examples allowed in markdown deliverables, labeled "unvalidated — verify before use"; DQL = Grail/Gen3 only, USQL = Classic RUM. |
| Early exit from mandatory lenses | No opt-out. Checkpoints add steering and visibility, never skipping. |

Process notes (organizational, not codebase): leadership reviews outputs before any customer-facing use; license expansion (8 seats requested) and Salesforce/Slack integration remain open — the latter stays Tier 1 below. Phase success criterion: "would we sign off on this plan for any analyst," not customer execution.

---
```

- [ ] **Step 2: Add the intake-form path to getting-started**

In `docs/getting-started.md`, in "### Step 1 — Open with the problem", after the line "…or just describe the problem and client directly.", insert:

```markdown
**Or start from the intake form.** Open `html/intake-form.html` in a browser, fill in what you know (required fields unlock generation; optional depth upgrades the output tier), and paste the generated brief as your first message. The agent skips every question the brief already answers and probes only the gaps — one follow-up per thin answer, never a wall.
```

- [ ] **Step 3: Verify**

Run: `grep -c "Pilot round 2\|intake form" ROADMAP.md docs/getting-started.md`
Expected: at least `1` per file.

- [ ] **Step 4: Commit**

```bash
git add ROADMAP.md docs/getting-started.md
git commit -m "Record pilot round 2 rulings and document intake-form entry path"
```

---

### Task 9: Publish the intake form as an Artifact (MAIN SESSION ONLY)

**Files:**
- Read: `html/intake-form.html`
- Create: `<scratchpad>/intake-form-artifact.html` (stripped copy)

**Interfaces:**
- Consumes: the completed form from Task 2.
- Produces: a hosted Artifact URL for analysts without repo access.

The Artifact tool is not available to subagents — this task runs in the main session after Task 2 is merged into the working branch.

- [ ] **Step 1: Create the Artifact variant**

The Artifact host wraps content in its own `<!doctype html>…<head>…<body>` skeleton. Copy `html/intake-form.html` to the scratchpad directory and strip the outer skeleton: remove `<!DOCTYPE html>`, `<html>`, `<head>`, `</head>`, `<body>`, `</body>`, `</html>`, and the `<meta>`/`<title>` lines, keeping `<title>Insights Forge — Engagement Intake</title>` as the first line, followed by the `<style>` block, the page content (`<main>…</main>`), and the `<script>` block, in that order.

- [ ] **Step 2: Publish**

Call the Artifact tool with the scratchpad file, `favicon: "📝"`, and description "Analyst intake form that generates an Insights Forge Phase 0 seed prompt."

- [ ] **Step 3: Verify**

Open the returned URL; repeat browser-walkthrough checks 1, 2, and 7 from Task 2 Step 3 (required-field blocking, Simple-tier generation, copy button). Confirm zero console errors from blocked external requests (there should be no external requests at all).

- [ ] **Step 4: Record the URL**

Add the Artifact URL to `docs/getting-started.md` in the paragraph added by Task 8 Step 2, as: "A hosted copy lives at <URL> for analysts without the repo." Commit:

```bash
git add docs/getting-started.md
git commit -m "Link hosted intake-form artifact"
```

---

## Execution order and dependencies

```
Task 1 (CLAUDE.md) ──► Task 4, Task 5 (reference the communication protocol)
Task 2 (form) ──► Task 3 (parses the brief format) ──► Task 9 (publishes the form)
Task 6 (one-pager) — independent
Task 7 (memory audit) — independent; ENDS AT USER-APPROVAL GATE before writing
Task 8 (roadmap/docs) — last of the doc edits, references everything
```

Recommended sequence: 1 → 2 → 3 → 4 → 5 → 6 → 7 (to the approval gate) → 8 → 9, with Task 7's approval and write completing whenever the user rules on the edit list.
