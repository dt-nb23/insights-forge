# Seed Prompt Generator IA Restructure — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Restructure the Seed Prompt Generator form from 10 steps to 9, per `docs/superpowers/specs/2026-07-10-seed-prompt-generator-ia-restructure-design.md`: merge Trigger into Outputs, split the dense C.S.I.R. page across Customer-context / Stakeholders / Goals / Pain steps, fold Audience into a per-stakeholder communication level, move the analyst Your-role field to Analyst context, and merge Specific info + Technical priorities into one Must-have Pain & constraints field.

**Architecture:** Same as round 1 — edit `html/seed-prompt-generator-src.html`, re-pack to `html/Insights Forge (Seed Prompt Generator) - Draft.html` via `python3 tools/seed-prompt-generator-bundle.py pack ...`. This is an ATOMIC refactor: the section markup, view-model, state, validation, and brief-generation all move together and the app does not render correctly until both the logic layer (Task 1) and the markup layer (Task 2) are complete. Behavioral verification happens at Task 2/3.

**Tech Stack:** Plain HTML/JS with the artifact's custom `DCLogic` template runtime (`{{ }}`, `<sc-if>`, `<sc-for>`). Python 3 stdlib for pack/unpack. Node + Playwright (from round 1) for headless verification.

## Global Constraints

- Never modify `html/Insights Forge (Seed Prompt Generator).html` (tracked) or `html/Insights Forge (Seed Prompt Generator) - Original.html` (untracked). All output to `html/Insights Forge (Seed Prompt Generator) - Draft.html`.
- Preserve every existing CSS custom property and style-helper method; moved field blocks keep their inner markup byte-for-byte except where a step explicitly changes it.
- New copy uses curly quotes (" ") and en/em-dashes to match the file's style.
- No new runtime dependencies.
- Final step count is 9 (indices 0–8), `REVIEW = 9`.

## Pack + verify command (used by every task)

```bash
python3 tools/seed-prompt-generator-bundle.py pack "html/Insights Forge (Seed Prompt Generator).html" "html/seed-prompt-generator-src.html" "html/Insights Forge (Seed Prompt Generator) - Draft.html"
```

---

## Task 1: Logic layer (state, constants, validation, brief, view-model)

**Files:** Modify `html/seed-prompt-generator-src.html`.

After this task the app does NOT render (markup still references removed keys). Its gate is static: pack produces valid JSON and structural greps pass. Task 2 completes the atomic change.

- [ ] **Step 1: State shape** — in `this.state.answers`, replace:
```js
        context:'', role:'', specific:'', intents:[], intentSuccess:'',
        audience:[], timeWindow:'', tone:'',
```
with:
```js
        context:'', role:'', intents:[], intentSuccess:'',
        painConstraints:'',
```
and replace:
```js
        stakeholders:[ {name:'', archetype:'Stakeholder — role to be confirmed', cares:''} ],
        techPriorities:'',
        triggers:[]
```
with:
```js
        stakeholders:[ {name:'', archetype:'Stakeholder — role to be confirmed', level:'Mixed', cares:''} ],
        triggers:[]
```

- [ ] **Step 2: `addStk()` default level** — replace:
```js
  addStk() { this.setState(s => ({ answers: Object.assign({}, s.answers, { stakeholders: s.answers.stakeholders.concat([{ name:'', archetype:'Stakeholder — role to be confirmed', cares:'' }]) }) })); }
```
with:
```js
  addStk() { this.setState(s => ({ answers: Object.assign({}, s.answers, { stakeholders: s.answers.stakeholders.concat([{ name:'', archetype:'Stakeholder — role to be confirmed', level:'Mixed', cares:'' }]) }) })); }
```

- [ ] **Step 3: `FREE` map** — remove the `specific:` and `techPriorities:` entries and add a merged `painConstraints:` entry. Replace the `specific: { … }` block (the entry beginning `specific: { guiding:'Known pain points?`) with nothing (delete it), and replace the `techPriorities: { … }` block (beginning `techPriorities: { guiding:'What frustrates`) with:
```js
      painConstraints: { guiding:'What's the team's day-to-day pain, and what constrains the plan? Alert noise, slow root cause, toil, on-call load — plus known commitments, prior QBR outcomes, or limits (regulated data, contract phase).', tip:'List facts, not hopes: the team's daily friction and anything off-limits. This is the boundary of what the plan can use.', chips:[
        {short:'Alert noise', text:'Alert noise / too many false positives'},
        {short:'Slow root cause', text:'Slow root-cause analysis'},
        {short:'Tool sprawl', text:'Tool sprawl & context switching'},
        {short:'Manual toil', text:'Manual, repetitive toil'},
        {short:'On-call load', text:'On-call burnout'},
        {short:'Prior QBR commitment', text:'Prior QBR flagged [issue]; we committed to [action] by [date].'},
        {short:'Regulated / limited data', text:'Regulated environment (PCI / HIPAA) limits access to [data].'},
        {short:'Renewal, budget scrutiny', text:'Renewal in [quarter]; budget scrutiny is high.'}
      ] }
```
Ensure the `intentSuccess` entry keeps its trailing comma and `painConstraints` is the last entry (no trailing comma before the closing `}`).

- [ ] **Step 4: `STEP_TITLES` + `REVIEW`** — replace:
```js
    this.STEP_TITLES = ['Requested outputs','Analyst context','Customer basics','Engagement framing','Active capabilities','Out of scope','Focus applications','Stakeholders','Technical priorities','Trigger'];
    this.REVIEW = 10;
```
with:
```js
    this.STEP_TITLES = ['Outputs & trigger','Analyst context','Customer context','Stakeholders & audience','Goals & success','Pain & constraints','Active capabilities','Out of scope','Focus applications'];
    this.REVIEW = 9;
```

- [ ] **Step 5: `_secData` grp map** — replace the whole `const grp = { … };` object (indices 0–9) with:
```js
    const grp = {
      0: { fields: [F(a.outputs), F(a.triggers)], req: [F(a.outputs)] },
      1: { fields: [!!anyScale, F(a.role)], req: anyScale ? [!!allScale] : [] },
      2: { fields: [F(a.customerName), vertOk, F(a.customerDesc), F(a.size), F(a.regions), F(a.context)], req: [F(a.customerName), vertOk, F(a.customerDesc), F(a.context)] },
      3: { fields: [a.stakeholders.some(s => F(s.name) || s.archetype || F(s.cares))], req: [stkOk] },
      4: { fields: [F(a.intents), F(a.intentSuccess)], req: [F(a.intents), F(a.intentSuccess)] },
      5: { fields: [F(a.painConstraints)], req: [F(a.painConstraints)] },
      6: { fields: [nonDavis], req: [nonDavis] },
      7: { fields: [F(a.outOfScope), F(a.outOfScopeNotes)], req: [] },
      8: { fields: [a.apps.some(ap => F(ap.name) || ap.rum || ap.sr)], req: this.s6Req() ? [appOk] : [] }
    };
```
The preamble lines that define `vertOk`, `anyScale`, `allScale`, `nonDavis`, `appOk`, `stkOk` above `const grp` are unchanged.

- [ ] **Step 6: `missing()`** — replace:
```js
    if (!a.context.trim()) m.push('Engagement context (C)');
    if (!a.specific.trim()) m.push('Specific information (S)');
    if (!a.intents.length) m.push('Intent — pick at least one goal');
    if (!a.intentSuccess.trim()) m.push('What success looks like');
    if (!a.audience.length) m.push('Audience (response format)');
```
with:
```js
    if (!a.context.trim()) m.push('Customer context (relationship & history)');
    if (!a.intents.length) m.push('Intent — pick at least one goal');
    if (!a.intentSuccess.trim()) m.push('What success looks like');
    if (!a.painConstraints.trim()) m.push('Pain & constraints');
```

- [ ] **Step 7: `buildBrief()` restructure** — replace the two preamble Must/Should lines:
```js
      + '> - **Must-have context** — Requested outputs, Customer (name / what-they-do / vertical), Engagement framing (Context, Specific info, Intent, Response format), Active capabilities, and at least one Stakeholder (role archetype required; a named person strongly preferred). Framing is not complete without these.\n'
      + '> - **Should-have context** — Analyst calibration (1–5), Tenant, Customer region(s), per-stakeholder priorities, Technical team priorities, and Trigger. These sharpen tone, depth and KPI selection.\n'
```
with:
```js
      + '> - **Must-have context** — Requested outputs, Customer (name / what-they-do / vertical), Customer context (relationship), Goals + success criteria, Pain & constraints, Active capabilities, and at least one Stakeholder (role archetype required; a named person strongly preferred). Framing is not complete without these.\n'
      + '> - **Should-have context** — Analyst calibration (1–5) + role, Tenant, Customer region(s), per-stakeholder communication level & priorities, and Trigger. These sharpen tone, depth and KPI selection.\n'
```
Then update the stakeholder line builder — replace:
```js
    const stkLines = a.stakeholders.filter(s => s.name.trim() || s.archetype || s.cares.trim()).map(s => '- ' + (s.name.trim() || '(unnamed)') + ' · ' + (s.archetype || 'archetype not provided') + ' — cares about: ' + (s.cares.trim() || 'not provided'));
```
with:
```js
    const stkLines = a.stakeholders.filter(s => s.name.trim() || s.archetype || s.cares.trim()).map(s => '- ' + (s.name.trim() || '(unnamed)') + ' · ' + (s.archetype || 'archetype not provided') + ' · communication level: ' + (s.level || 'Mixed') + ' — cares about: ' + (s.cares.trim() || 'not provided'));
```
Then replace the entire brief body from `\n## Requested outputs\n` through the final `## Trigger(s)` line, i.e. replace:
```js
      + '\n## Requested outputs\n'
      + '- Baseline (always): Customer action plan\n'
      + '- Additional formats: ' + outputs + '\n'
      + '- Analyst calibration — experience: ' + sc(a.analystExp) + ', account familiarity: ' + sc(a.accountFam) + ', Dynatrace maturity: ' + sc(a.domainFluency) + '\n'
      + '- Generated: ' + today + '\n'
      + '\n## Customer\n'
      + '- Name: ' + np(a.customerName) + '\n'
      + '- What they do: ' + np(a.customerDesc) + '\n'
      + '- Vertical(s): ' + vert + '\n'
      + '- Customer size (ACV): ' + np(a.size) + '\n'
      + '- Tenant type: ' + np(a.tenant) + '\n'
      + '- Region(s): ' + np(a.regions) + '\n'
      + '\n## Engagement framing (C.S.I.R.)\n'
      + '### Context\n' + np(a.context) + '\n'
      + 'Consultant role: ' + np(a.role) + '\n'
      + '### Specific information\n' + np(a.specific) + '\n'
      + '### Intent\n'
      + 'Goals: ' + np(a.intents) + '\n'
      + 'Success looks like: ' + np(a.intentSuccess) + '\n'
      + '### Response format\n'
      + 'Requested outputs: ' + outputs + '\n'
      + 'Audience: ' + np(a.audience) + '\n'
      + 'Time window: ' + np(a.timeWindow) + '\n'
      + 'Tone / branding: ' + np(a.tone) + '\n'
      + '\n## Active capabilities\n' + caps + '\n'
      + '\n## Out of scope / do not suggest\n' + oos + '\n'
      + '\n## Focus applications\n' + apps + '\n'
      + '\n## Stakeholders\n' + stks + '\n'
      + '\n## Technical team priorities\n' + np(a.techPriorities) + '\n'
      + '\n## Trigger(s)\n' + np(a.triggers) + '\n';
```
with:
```js
      + '\n## Requested outputs & trigger\n'
      + '- Baseline (always): Customer action plan\n'
      + '- Additional formats: ' + outputs + '\n'
      + '- Trigger(s): ' + np(a.triggers) + '\n'
      + '- Analyst: role ' + np(a.role) + '; experience ' + sc(a.analystExp) + ', account familiarity ' + sc(a.accountFam) + ', customer Dynatrace maturity ' + sc(a.domainFluency) + '\n'
      + '- Generated: ' + today + '\n'
      + '\n## Customer context\n'
      + '- Name: ' + np(a.customerName) + '\n'
      + '- What they do: ' + np(a.customerDesc) + '\n'
      + '- Vertical(s): ' + vert + '\n'
      + '- Customer size (ACV): ' + np(a.size) + '\n'
      + '- Tenant type: ' + np(a.tenant) + '\n'
      + '- Region(s): ' + np(a.regions) + '\n'
      + '- Relationship & context: ' + np(a.context) + '\n'
      + '\n## Stakeholders & audience\n' + stks + '\n'
      + '\n## Goals & success criteria\n'
      + 'Goals: ' + np(a.intents) + '\n'
      + 'Success looks like: ' + np(a.intentSuccess) + '\n'
      + '\n## Pain & constraints\n' + np(a.painConstraints) + '\n'
      + '\n## Active capabilities\n' + caps + '\n'
      + '\n## Out of scope / do not suggest\n' + oos + '\n'
      + '\n## Focus applications\n' + apps + '\n';
```

- [ ] **Step 8: View-model — `show` loop bound** — replace `const show = {}; for (let i = 0; i < 10; i++) show['showSec' + i] = step === i;` with `const show = {}; for (let i = 0; i < 9; i++) show['showSec' + i] = step === i;`

- [ ] **Step 9: View-model — progress text** — replace `progressText: step < this.REVIEW ? ('Step ' + (step + 1) + ' of 10') : 'Complete',` with `progressText: step < this.REVIEW ? ('Step ' + (step + 1) + ' of 9') : 'Complete',`

- [ ] **Step 10: View-model — remove `audienceOptions`** — delete the line:
```js
      audienceOptions: ['Executive','Technical','Mixed'].map(v => ({ label:v, onClick:()=>this.toggleArr('audience', v), style:this.pill(a.audience.indexOf(v) >= 0) })),
```

- [ ] **Step 11: View-model — per-stakeholder level** — in the `stakeholders: a.stakeholders.map((sk, i) => ({ … }))` view-model, add `level`/`onLevel` by replacing:
```js
        archetype: sk.archetype, onArch:(e)=>this.setStk(i, 'archetype', e.target.value),
        cares: sk.cares, onCares:(e)=>this.setStk(i, 'cares', e.target.value),
```
with:
```js
        archetype: sk.archetype, onArch:(e)=>this.setStk(i, 'archetype', e.target.value),
        level: sk.level, onLevel:(e)=>this.setStk(i, 'level', e.target.value),
        cares: sk.cares, onCares:(e)=>this.setStk(i, 'cares', e.target.value),
```

- [ ] **Step 12: Pack + static verify**
```bash
python3 tools/seed-prompt-generator-bundle.py pack "html/Insights Forge (Seed Prompt Generator).html" "html/seed-prompt-generator-src.html" "html/Insights Forge (Seed Prompt Generator) - Draft.html"
python3 -c "
import json
s = open('html/seed-prompt-generator-src.html', encoding='utf-8').read()
json.loads(open('html/Insights Forge (Seed Prompt Generator) - Draft.html', encoding='utf-8').readlines()[193])  # pack is valid JSON
for gone in [\"a.specific\", \"a.audience\", \"a.timeWindow\", \"a.tone\", \"a.techPriorities\", \"'Trigger'\", 'of 10', 'audienceOptions']:
    assert gone not in s, 'still present: '+gone
for present in ['painConstraints', \"level:'Mixed'\", \"'Outputs & trigger'\", 'communication level', 'this.REVIEW = 9']:
    assert present in s, 'missing: '+present
print('OK: logic layer updated (static)')
"
```
Expected: `OK: logic layer updated (static)`. (App will not render yet — markup completes in Task 2.)

- [ ] **Step 13: Commit**
```bash
git add "html/seed-prompt-generator-src.html" "html/Insights Forge (Seed Prompt Generator) - Draft.html"
git commit -m "$(cat <<'EOF'
Restructure Seed Prompt Generator: logic layer for 9-step reflow

State, constants, validation, brief and view-model for the round-2
IA restructure (10 steps -> 9): merged pain/constraints field,
per-stakeholder communication level, trigger folded into outputs,
audience/time/tone removed. Markup completes in the next commit.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Markup layer (rewrite the form-column sections region)

**Files:** Modify `html/seed-prompt-generator-src.html`.

Replace the entire sections region — from the line `<!-- SECTION 1 — Requested outputs -->` through the closing `</sc-if>` of the old Trigger section (the `</sc-if>` immediately before `<!-- PREVIEW COLUMN -->`) — with the complete new 9-section markup below. Everything outside this region (nav rail, progress bar, preview aside, footer) is unchanged.

- [ ] **Step 1: Replace the sections region** with this exact markup:

```html
      <!-- SECTION 1 — Outputs & trigger -->
      <sc-if value="{{ showSec0 }}" hint-placeholder-val="{{ true }}">
      <section data-screen-label="Section 1 — Outputs & trigger" style="background:var(--card,#212135); border:1px solid var(--border,#3b3b52); border-radius:14px; padding:22px 24px; margin-bottom:16px; animation:ifFade .25s ease both;">
        <div style="display:flex; align-items:center; gap:11px; flex-wrap:wrap;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:25px; height:25px; border-radius:8px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); font-weight:700; font-size:13px; flex-shrink:0;">1</span>
          <h2 style="margin:0; font-size:16px; font-weight:700; color:var(--text,#ebecff);">Outputs &amp; trigger</h2>
          <span style="font-size:10px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:2px 8px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); border:1px solid var(--primary-border,#adb0ff);">Must-have</span>
        </div>
        <p style="margin:8px 0 0; font-size:12px; color:var(--text-faint,#8a8bad);"><span style="color:var(--text-sub,#b1b2d2);">Why —</span> What you're producing and what prompted it. The customer action plan is always produced; pick the presentation formats to build on top of it.</p>
        <label style="display:flex; align-items:center; gap:8px; margin:16px 0 8px; font-size:13px; font-weight:600; color:var(--text,#ebecff);">Engagement trigger <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; color:var(--text-sub,#b1b2d2); border:1px solid var(--border,#3b3b52);">Should</span> <span style="font-size:11px; font-weight:400; color:var(--text-faint,#8a8bad);">what prompted this — select any that apply</span></label>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <sc-for list="{{ triggers }}" as="o" hint-placeholder-count="6">
            <button onclick="{{ o.onClick }}" style="{{ o.style }}" style-hover="border-color:var(--border-hover,#4d4e66);">{{ o.label }}</button>
          </sc-for>
        </div>
        <div style="margin-top:20px; padding-top:18px; border-top:1px solid var(--border,#3b3b52);">
          <label style="display:flex; align-items:center; gap:8px; margin-bottom:2px; font-size:13px; font-weight:600; color:var(--text,#ebecff);">Requested outputs <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff);">Must</span></label>
          <div style="display:flex; align-items:center; gap:10px; margin-top:12px; padding:12px 14px; border:1px solid var(--success,#6fc3ba); border-radius:10px; background:var(--field,#1b1b30);">
            <span style="display:inline-flex; align-items:center; justify-content:center; width:20px; height:20px; border-radius:6px; background:var(--success,#6fc3ba); color:var(--on-primary,#1f2037); font-weight:700; font-size:12px;">✓</span>
            <div><strong style="font-size:13.5px; color:var(--text,#ebecff);">Customer action plan</strong> <span style="font-size:12px; color:var(--success,#6fc3ba);">· baseline, always produced</span><div style="font-size:12px; color:var(--text-sub,#b1b2d2); margin-top:2px;">The phased plan the customer acts on — generated every time.</div></div>
          </div>
          <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:10px; margin-top:10px;">
            <sc-for list="{{ outputs }}" as="u" hint-placeholder-count="3">
              <label onclick="{{ u.onClick }}" style="{{ u.style }}" style-hover="border-color:var(--border-hover,#4d4e66);">
                <div style="display:flex; align-items:center; gap:9px;">
                  <span style="{{ u.boxStyle }}"><sc-if value="{{ u.selected }}" hint-placeholder-val="{{ false }}"><span style="width:10px; height:10px; border-radius:3px; background:var(--primary-border,#adb0ff); display:block;"></span></sc-if></span>
                  <strong style="font-size:13.5px; font-weight:600; color:var(--text,#ebecff);">{{ u.label }}</strong>
                </div>
                <small style="display:block; margin-top:6px; margin-left:27px; font-size:12px; color:var(--text-sub,#b1b2d2); line-height:1.4;">{{ u.desc }}</small>
              </label>
            </sc-for>
          </div>
        </div>
      </section>
      </sc-if>

      <!-- SECTION 2 — Analyst context -->
      <sc-if value="{{ showSec1 }}" hint-placeholder-val="{{ true }}">
      <section data-screen-label="Section 2 — Analyst context" style="background:var(--card,#212135); border:1px solid var(--border,#3b3b52); border-radius:14px; padding:22px 24px; margin-bottom:16px; animation:ifFade .25s ease both;">
        <div style="display:flex; align-items:center; gap:11px; flex-wrap:wrap;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:25px; height:25px; border-radius:8px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); font-weight:700; font-size:13px;">2</span>
          <h2 style="margin:0; font-size:16px; font-weight:700; color:var(--text,#ebecff);">Analyst context</h2>
          <span style="font-size:10px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:2px 8px; border-radius:100px; color:var(--text-sub,#b1b2d2); border:1px solid var(--border,#3b3b52);">Rate 1–5</span>
        </div>
        <p style="margin:8px 0 0; font-size:12px; color:var(--text-faint,#8a8bad);"><span style="color:var(--text-sub,#b1b2d2);">Why —</span> Calibrates the plan's depth and tone. Optional — but once you rate one, rate all three (that's what unlocks copy/download).</p>
        <label style="display:block; margin:16px 0 6px; font-size:13px; font-weight:500; color:var(--text-sub,#b1b2d2);">Your role</label>
        <select data-fid="role" value="{{ answers.role }}" onchange="{{ onInput }}" style="width:100%; max-width:300px; background:var(--field,#1b1b30); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:10px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);">
          <option value="">— select —</option><option>CSM</option><option>SE</option><option>Consultant</option><option>Insights Analytics Consultant</option><option>Other</option>
        </select>
        <div style="margin-top:6px;">
          <sc-for list="{{ scales }}" as="sc" hint-placeholder-count="3">
            <div style="margin-top:14px;">
              <label style="display:block; margin-bottom:7px; font-size:13px; font-weight:500; color:var(--text-sub,#b1b2d2);">{{ sc.label }}</label>
              <div style="display:flex; align-items:center; gap:11px; flex-wrap:wrap;">
                <span style="font-size:11px; color:var(--text-faint,#8a8bad); width:64px; text-align:right;">{{ sc.lo }}</span>
                <div style="display:flex; gap:6px;">
                  <sc-for list="{{ sc.buttons }}" as="b" hint-placeholder-count="5">
                    <button onclick="{{ b.onClick }}" style="{{ b.style }}">{{ b.n }}</button>
                  </sc-for>
                </div>
                <span style="font-size:11px; color:var(--text-faint,#8a8bad);">{{ sc.hi }}</span>
              </div>
            </div>
          </sc-for>
        </div>
      </section>
      </sc-if>

      <!-- SECTION 3 — Customer context -->
      <sc-if value="{{ showSec2 }}" hint-placeholder-val="{{ true }}">
      <section data-screen-label="Section 3 — Customer context" style="background:var(--card,#212135); border:1px solid var(--border,#3b3b52); border-radius:14px; padding:22px 24px; margin-bottom:16px; animation:ifFade .25s ease both;">
        <div style="display:flex; align-items:center; gap:11px; flex-wrap:wrap;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:25px; height:25px; border-radius:8px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); font-weight:700; font-size:13px;">3</span>
          <h2 style="margin:0; font-size:16px; font-weight:700; color:var(--text,#ebecff);">Customer context</h2>
          <span style="font-size:10px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:2px 8px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); border:1px solid var(--primary-border,#adb0ff);">Must-have</span>
        </div>
        <p style="margin:8px 0 0; font-size:12px; color:var(--text-faint,#8a8bad);"><span style="color:var(--text-sub,#b1b2d2);">Why —</span> Who the customer is and where the relationship stands. The basics plus the relationship history frame everything downstream.</p>
        <div style="margin-top:14px;">
          <label style="display:flex; align-items:center; gap:8px; margin-bottom:6px; font-size:13px; font-weight:500; color:var(--text-sub,#b1b2d2);">Customer name <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff);">Must</span></label>
          <input type="text" data-fid="customerName" value="{{ answers.customerName }}" oninput="{{ onInput }}" placeholder="e.g. Northwind Retail" style="width:100%; max-width:420px; background:var(--field,#1b1b30); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:10px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);">
        </div>
        <label style="display:flex; align-items:center; gap:8px; margin:14px 0 6px; font-size:13px; font-weight:500; color:var(--text-sub,#b1b2d2);">What does the customer's business do? <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff);">Must</span></label>
        <input type="text" data-fid="customerDesc" value="{{ answers.customerDesc }}" oninput="{{ onInput }}" placeholder="One line — e.g. mid-size online retailer selling home goods" style="width:100%; background:var(--field,#1b1b30); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:10px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);">
        <label style="display:flex; align-items:center; gap:8px; margin:14px 0 6px; font-size:13px; font-weight:500; color:var(--text-sub,#b1b2d2);">Vertical <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff);">Must</span> <span style="font-size:11px; font-weight:400; color:var(--text-faint,#8a8bad);">select any that apply</span></label>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <sc-for list="{{ verticals }}" as="o" hint-placeholder-count="9">
            <button onclick="{{ o.onClick }}" style="{{ o.style }}" style-hover="border-color:var(--border-hover,#4d4e66);">{{ o.label }}</button>
          </sc-for>
        </div>
        <sc-if value="{{ showVerticalOther }}" hint-placeholder-val="{{ false }}">
          <input type="text" data-fid="verticalOther" value="{{ answers.verticalOther }}" oninput="{{ onInput }}" placeholder="Name the vertical" style="width:100%; max-width:320px; margin-top:9px; background:var(--field,#1b1b30); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:9px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);">
        </sc-if>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:14px; align-items:start;">
          <div>
            <label style="display:flex; align-items:center; gap:8px; margin-bottom:6px; font-size:13px; font-weight:500; color:var(--text-sub,#b1b2d2);">Customer size (ACV) <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; color:var(--text-faint,#8a8bad); border:1px dashed var(--border,#3b3b52);">Nice</span></label>
            <select data-fid="size" value="{{ answers.size }}" onchange="{{ onInput }}" style="width:100%; background:var(--field,#1b1b30); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:10px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);">
              <option value="">— select —</option><option>Acceleration (&lt; $250K ACV)</option><option>Mid-Enterprise ($250K–$1M ACV)</option><option>Large Enterprise (&gt; $1M ACV)</option>
            </select>
          </div>
          <div>
            <label style="display:flex; align-items:center; gap:8px; margin-bottom:6px; font-size:13px; font-weight:500; color:var(--text-sub,#b1b2d2);">Tenant type <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; color:var(--text-sub,#b1b2d2); border:1px solid var(--border,#3b3b52);">Should</span></label>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <sc-for list="{{ tenantOptions }}" as="o" hint-placeholder-count="2">
                <button onclick="{{ o.onClick }}" style="{{ o.style }}" style-hover="border-color:var(--border-hover,#4d4e66);">{{ o.label }}</button>
              </sc-for>
            </div>
          </div>
        </div>
        <div style="margin-top:16px;">
          <label style="display:flex; align-items:center; gap:8px; margin-bottom:8px; font-size:13px; font-weight:500; color:var(--text-sub,#b1b2d2);">Customer region(s) <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; color:var(--text-sub,#b1b2d2); border:1px solid var(--border,#3b3b52);">Should</span> <span style="font-size:11px; font-weight:400; color:var(--text-faint,#8a8bad);">select any that apply — local laws (e.g. GDPR) may shape what the plan can suggest</span></label>
          <div style="border:1px solid var(--border,#3b3b52); border-radius:10px; padding:12px 14px; background:var(--field,#1b1b30); display:flex; gap:8px; flex-wrap:wrap;">
            <sc-for list="{{ regionOptions }}" as="r" hint-placeholder-count="4">
              <label onclick="{{ r.onClick }}" style="{{ r.rowStyle }}" style-hover="border-color:var(--border-hover,#4d4e66);">
                <span style="{{ r.boxStyle }}"><sc-if value="{{ r.selected }}" hint-placeholder-val="{{ false }}"><span style="width:9px; height:9px; border-radius:2px; background:var(--primary-border,#adb0ff); display:block;"></span></sc-if></span>
                <span>{{ r.label }}</span>
              </label>
            </sc-for>
          </div>
        </div>
        <div style="margin-top:18px; padding-top:16px; border-top:1px solid var(--border,#3b3b52);">
          <label style="display:flex; align-items:center; gap:8px; margin:0 0 6px; font-size:13px; font-weight:600; color:var(--text,#ebecff);">Relationship &amp; context <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff);">Must</span></label>
          <textarea data-fid="context" value="{{ free.context.value }}" oninput="{{ onInput }}" placeholder="Relationship history, mood, recent milestones…" style="width:100%; min-height:74px; resize:vertical; background:var(--field,#1b1b30); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:10px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);"></textarea>
          <p style="margin:7px 0 0; font-size:12px; color:var(--text-sub,#b1b2d2); line-height:1.45;">{{ free.context.guiding }}</p>
          <div style="display:flex; flex-wrap:wrap; gap:7px; margin-top:9px; align-items:center;">
            <span style="font-size:11px; color:var(--text-faint,#8a8bad);">Starters:</span>
            <sc-for list="{{ free.context.chips }}" as="c" hint-placeholder-count="4">
              <button onclick="{{ c.onClick }}" style="{{ c.style }}">{{ c.label }}</button>
            </sc-for>
          </div>
          <button onclick="{{ free.context.onToggle }}" style="margin-top:9px; background:none; border:none; color:var(--primary,#999bed); font-size:12px; cursor:pointer; padding:0;">{{ free.context.toggleLabel }}</button>
          <sc-if value="{{ free.context.expanded }}" hint-placeholder-val="{{ false }}"><div style="margin-top:8px; border-left:2px solid var(--primary-border,#adb0ff); padding:8px 12px; background:var(--field,#1b1b30); border-radius:0 8px 8px 0; font-size:12.5px; color:var(--text-sub,#b1b2d2); line-height:1.5;">{{ free.context.tip }}</div></sc-if>
        </div>
      </section>
      </sc-if>

      <!-- SECTION 4 — Stakeholders & audience -->
      <sc-if value="{{ showSec3 }}" hint-placeholder-val="{{ true }}">
      <section data-screen-label="Section 4 — Stakeholders & audience" style="background:var(--card,#212135); border:1px solid var(--border,#3b3b52); border-radius:14px; padding:22px 24px; margin-bottom:16px; animation:ifFade .25s ease both;">
        <div style="display:flex; align-items:center; gap:11px; flex-wrap:wrap;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:25px; height:25px; border-radius:8px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); font-weight:700; font-size:13px;">4</span>
          <h2 style="margin:0; font-size:16px; font-weight:700; color:var(--text,#ebecff);">Stakeholders &amp; audience</h2>
          <span style="font-size:10px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:2px 8px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); border:1px solid var(--primary-border,#adb0ff);">Must-have</span>
        </div>
        <p style="margin:8px 0 0; font-size:12px; color:var(--text-faint,#8a8bad);"><span style="color:var(--text-sub,#b1b2d2);">Why —</span> Who consumes or influences the deliverable, and how technical each one is. Each stakeholder carries their own communication level (Executive / Technical / Mixed) so the plan can speak to the whole room — this replaces a single form-level audience.</p>
        <div style="margin-top:10px; border-left:2px solid var(--primary-border,#adb0ff); padding:8px 12px; background:var(--field,#1b1b30); border-radius:0 8px 8px 0; font-size:12.5px; color:var(--text-sub,#b1b2d2); line-height:1.5;">Check Salesforce for the account team and named contacts — a real, named stakeholder sharpens the output far more than a role-only fallback.</div>
        <sc-for list="{{ stakeholders }}" as="sk" hint-placeholder-count="1">
          <div style="margin-top:14px; border:1px solid var(--border,#3b3b52); border-radius:10px; padding:14px; background:var(--field,#1b1b30);">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
              <span style="font-size:11px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; color:var(--text-faint,#8a8bad);">{{ sk.label }}</span>
              <sc-if value="{{ sk.showRemove }}" hint-placeholder-val="{{ false }}"><button onclick="{{ sk.onRemove }}" style="background:none; border:none; color:var(--text-faint,#8a8bad); font-size:16px; cursor:pointer; line-height:1; padding:0 4px;" style-hover="color:var(--critical,#ff999c);">×</button></sc-if>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:8px;">
              <div>
                <label style="display:flex; align-items:center; gap:6px; margin-bottom:6px; font-size:12.5px; font-weight:500; color:var(--text-sub,#b1b2d2);">Name &amp; title <span style="font-size:9px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; padding:1px 5px; border-radius:100px; color:var(--text-sub,#b1b2d2); border:1px solid var(--border,#3b3b52);">Should</span></label>
                <input type="text" value="{{ sk.name }}" oninput="{{ sk.onName }}" placeholder="e.g. Sarah Chen, VP Engineering" style="width:100%; background:var(--card,#212135); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:9px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);">
              </div>
              <div>
                <label style="display:flex; align-items:center; gap:6px; margin-bottom:6px; font-size:12.5px; font-weight:500; color:var(--text-sub,#b1b2d2);">Role archetype <span style="font-size:9px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; padding:1px 5px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff);">Must</span></label>
                <select value="{{ sk.archetype }}" onchange="{{ sk.onArch }}" style="width:100%; background:var(--card,#212135); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:9px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);">
                  <option>Stakeholder — role to be confirmed</option><option>Executive Sponsor</option><option>Product Owner</option><option>SRE / Reliability Engineer</option><option>IT Operations Manager</option><option>Application Developer</option><option>Platform / DevOps Engineer</option><option>Security / Compliance Officer</option><option>Data / Analytics Lead</option><option>Marketing / Business</option><option>unsure</option>
                </select>
              </div>
            </div>
            <label style="display:flex; align-items:center; gap:6px; margin:12px 0 6px; font-size:12.5px; font-weight:500; color:var(--text-sub,#b1b2d2);">Communication level <span style="font-size:9px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; padding:1px 5px; border-radius:100px; color:var(--text-sub,#b1b2d2); border:1px solid var(--border,#3b3b52);">Should</span> <span style="font-size:11px; font-weight:400; color:var(--text-faint,#8a8bad);">how technical this person's read should be</span></label>
            <select value="{{ sk.level }}" onchange="{{ sk.onLevel }}" style="width:100%; max-width:260px; background:var(--card,#212135); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:9px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);">
              <option>Executive</option><option>Technical</option><option>Mixed</option>
            </select>
            <label style="display:flex; align-items:center; gap:6px; margin:12px 0 6px; font-size:12.5px; font-weight:500; color:var(--text-sub,#b1b2d2);">What does this stakeholder care about? <span style="font-size:9px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; padding:1px 5px; border-radius:100px; color:var(--text-sub,#b1b2d2); border:1px solid var(--border,#3b3b52);">Should</span></label>
            <textarea value="{{ sk.cares }}" oninput="{{ sk.onCares }}" placeholder="KPIs, outcomes or priorities this person judges success by…" style="width:100%; min-height:52px; resize:vertical; background:var(--card,#212135); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:9px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);"></textarea>
            <div style="display:flex; flex-wrap:wrap; gap:7px; margin-top:8px;">
              <sc-for list="{{ sk.caresChips }}" as="c" hint-placeholder-count="6"><button onclick="{{ c.onClick }}" style="border:1px solid var(--border,#3b3b52); background:var(--card,#212135); color:var(--text-sub,#b1b2d2); border-radius:100px; padding:5px 11px; font-size:12px; cursor:pointer; white-space:nowrap;" style-hover="border-color:var(--primary-border,#adb0ff); color:var(--text,#ebecff);">{{ c.label }}</button></sc-for>
            </div>
          </div>
        </sc-for>
        <button onclick="{{ onAddStk }}" style="margin-top:12px; background:transparent; border:1px dashed var(--border-hover,#4d4e66); color:var(--primary,#999bed); border-radius:8px; padding:9px 16px; font-size:13px; font-weight:500; cursor:pointer;" style-hover="border-color:var(--primary-border,#adb0ff);">+ Add stakeholder</button>
      </section>
      </sc-if>

      <!-- SECTION 5 — Goals & success criteria -->
      <sc-if value="{{ showSec4 }}" hint-placeholder-val="{{ true }}">
      <section data-screen-label="Section 5 — Goals & success criteria" style="background:var(--card,#212135); border:1px solid var(--border,#3b3b52); border-radius:14px; padding:22px 24px; margin-bottom:16px; animation:ifFade .25s ease both;">
        <div style="display:flex; align-items:center; gap:11px; flex-wrap:wrap;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:25px; height:25px; border-radius:8px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); font-weight:700; font-size:13px;">5</span>
          <h2 style="margin:0; font-size:16px; font-weight:700; color:var(--text,#ebecff);">Goals &amp; success criteria</h2>
          <span style="font-size:10px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:2px 8px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); border:1px solid var(--primary-border,#adb0ff);">Must-have</span>
        </div>
        <p style="margin:8px 0 0; font-size:12px; color:var(--text-faint,#8a8bad);"><span style="color:var(--text-sub,#b1b2d2);">Why —</span> What Dynatrace wants from this engagement and what the customer would call success — the load-bearing core the objective can't be written without.</p>
        <label style="display:flex; align-items:center; gap:8px; margin:16px 0 8px; font-size:13px; font-weight:600; color:var(--text,#ebecff);">Intent — goals <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff);">Must</span> <span style="font-size:11px; font-weight:400; color:var(--text-faint,#8a8bad);">select any that apply</span></label>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <sc-for list="{{ intents }}" as="o" hint-placeholder-count="7">
            <button onclick="{{ o.onClick }}" style="{{ o.style }}" style-hover="border-color:var(--border-hover,#4d4e66);">{{ o.label }}</button>
          </sc-for>
        </div>
        <label style="display:flex; align-items:center; gap:8px; margin:16px 0 6px; font-size:13px; font-weight:600; color:var(--text,#ebecff);">What does a successful outcome look like? <span style="font-size:9.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:1px 6px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff);">Must</span></label>
        <textarea data-fid="intentSuccess" value="{{ free.intentSuccess.value }}" oninput="{{ onInput }}" placeholder="What the customer would say changed if this works…" style="width:100%; min-height:64px; resize:vertical; background:var(--field,#1b1b30); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:10px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);"></textarea>
        <p style="margin:7px 0 0; font-size:12px; color:var(--text-sub,#b1b2d2); line-height:1.45;">{{ free.intentSuccess.guiding }}</p>
        <div style="display:flex; flex-wrap:wrap; gap:7px; margin-top:9px; align-items:center;">
          <span style="font-size:11px; color:var(--text-faint,#8a8bad);">Starters:</span>
          <sc-for list="{{ free.intentSuccess.chips }}" as="c" hint-placeholder-count="4">
            <button onclick="{{ c.onClick }}" style="{{ c.style }}">{{ c.label }}</button>
          </sc-for>
        </div>
        <button onclick="{{ free.intentSuccess.onToggle }}" style="margin-top:9px; background:none; border:none; color:var(--primary,#999bed); font-size:12px; cursor:pointer; padding:0;">{{ free.intentSuccess.toggleLabel }}</button>
        <sc-if value="{{ free.intentSuccess.expanded }}" hint-placeholder-val="{{ false }}"><div style="margin-top:8px; border-left:2px solid var(--primary-border,#adb0ff); padding:8px 12px; background:var(--field,#1b1b30); border-radius:0 8px 8px 0; font-size:12.5px; color:var(--text-sub,#b1b2d2); line-height:1.5;">{{ free.intentSuccess.tip }}</div></sc-if>
      </section>
      </sc-if>

      <!-- SECTION 6 — Pain & constraints -->
      <sc-if value="{{ showSec5 }}" hint-placeholder-val="{{ true }}">
      <section data-screen-label="Section 6 — Pain & constraints" style="background:var(--card,#212135); border:1px solid var(--border,#3b3b52); border-radius:14px; padding:22px 24px; margin-bottom:16px; animation:ifFade .25s ease both;">
        <div style="display:flex; align-items:center; gap:11px; flex-wrap:wrap;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:25px; height:25px; border-radius:8px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); font-weight:700; font-size:13px;">6</span>
          <h2 style="margin:0; font-size:16px; font-weight:700; color:var(--text,#ebecff);">Pain &amp; constraints</h2>
          <span style="font-size:10px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:2px 8px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); border:1px solid var(--primary-border,#adb0ff);">Must-have</span>
        </div>
        <p style="margin:8px 0 0; font-size:12px; color:var(--text-faint,#8a8bad);"><span style="color:var(--text-sub,#b1b2d2);">Why —</span> The team's day-to-day pain and anything that limits the plan — commitments, prior QBR outcomes, regulatory or contract limits. This is the boundary of what the plan can use.</p>
        <textarea data-fid="painConstraints" value="{{ free.painConstraints.value }}" oninput="{{ onInput }}" placeholder="Alert noise, slow root cause, toil, on-call load — plus commitments, prior outcomes, and limits…" style="width:100%; min-height:74px; margin-top:12px; resize:vertical; background:var(--field,#1b1b30); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:10px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);"></textarea>
        <p style="margin:7px 0 0; font-size:12px; color:var(--text-sub,#b1b2d2); line-height:1.45;">{{ free.painConstraints.guiding }}</p>
        <div style="display:flex; flex-wrap:wrap; gap:7px; margin-top:9px; align-items:center;">
          <span style="font-size:11px; color:var(--text-faint,#8a8bad);">Starters:</span>
          <sc-for list="{{ free.painConstraints.chips }}" as="c" hint-placeholder-count="8">
            <button onclick="{{ c.onClick }}" style="{{ c.style }}">{{ c.label }}</button>
          </sc-for>
        </div>
        <button onclick="{{ free.painConstraints.onToggle }}" style="margin-top:9px; background:none; border:none; color:var(--primary,#999bed); font-size:12px; cursor:pointer; padding:0;">{{ free.painConstraints.toggleLabel }}</button>
        <sc-if value="{{ free.painConstraints.expanded }}" hint-placeholder-val="{{ false }}"><div style="margin-top:8px; border-left:2px solid var(--primary-border,#adb0ff); padding:8px 12px; background:var(--field,#1b1b30); border-radius:0 8px 8px 0; font-size:12.5px; color:var(--text-sub,#b1b2d2); line-height:1.5;">{{ free.painConstraints.tip }}</div></sc-if>
      </section>
      </sc-if>

      <!-- SECTION 7 — Active capabilities -->
      <sc-if value="{{ showSec6 }}" hint-placeholder-val="{{ true }}">
      <section data-screen-label="Section 7 — Active capabilities" style="background:var(--card,#212135); border:1px solid var(--border,#3b3b52); border-radius:14px; padding:22px 24px; margin-bottom:16px; animation:ifFade .25s ease both;">
        <div style="display:flex; align-items:center; gap:11px; flex-wrap:wrap;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:25px; height:25px; border-radius:8px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); font-weight:700; font-size:13px;">7</span>
          <h2 style="margin:0; font-size:16px; font-weight:700; color:var(--text,#ebecff);">Active Dynatrace capabilities</h2>
          <span style="font-size:10px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:2px 8px; border-radius:100px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); border:1px solid var(--primary-border,#adb0ff);">Must-have</span>
        </div>
        <p style="margin:8px 0 0; font-size:12px; color:var(--text-faint,#8a8bad);"><span style="color:var(--text-sub,#b1b2d2);">Why —</span> The boundary of what insights can surface. For RUM, Session Replay and Dashboards, pick the generation. Davis AI is always on.</p>
        <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(258px,1fr)); gap:14px; margin-top:16px;">
          <sc-for list="{{ capGroups }}" as="g" hint-placeholder-count="6">
            <div style="border:1px solid var(--border,#3b3b52); border-radius:10px; padding:12px 14px; background:var(--field,#1b1b30);">
              <h3 style="margin:0 0 8px; font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:var(--text-faint,#8a8bad); font-weight:700;">{{ g.title }}</h3>
              <sc-for list="{{ g.items }}" as="it" hint-placeholder-count="3">
                <div style="margin:4px 0;">
                  <label onclick="{{ it.onClick }}" style="{{ it.rowStyle }}" style-hover="border-color:var(--border-hover,#4d4e66);">
                    <span style="{{ it.boxStyle }}"><sc-if value="{{ it.selected }}" hint-placeholder-val="{{ false }}"><span style="width:9px; height:9px; border-radius:2px; background:var(--primary-border,#adb0ff); display:block;"></span></sc-if></span>
                    <span style="flex:1;">{{ it.label }}</span>
                    <sc-if value="{{ it.always }}" hint-placeholder-val="{{ false }}"><span style="font-size:9.5px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; color:var(--success,#6fc3ba); border:1px solid var(--success,#6fc3ba); border-radius:100px; padding:1px 7px;">Always on</span></sc-if>
                  </label>
                  <sc-if value="{{ it.showGen }}" hint-placeholder-val="{{ false }}">
                    <div style="display:flex; gap:6px; margin:6px 0 2px 30px; flex-wrap:wrap;">
                      <sc-for list="{{ it.genButtons }}" as="gb" hint-placeholder-count="3">
                        <button onclick="{{ gb.onClick }}" style="{{ gb.style }}" style-hover="border-color:var(--border-hover,#4d4e66);">{{ gb.label }}</button>
                      </sc-for>
                    </div>
                  </sc-if>
                </div>
              </sc-for>
            </div>
          </sc-for>
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid var(--border,#3b3b52);">
          <label onclick="{{ capsUnsure.onClick }}" style="{{ capsUnsure.rowStyle }}">
            <span style="{{ capsUnsure.boxStyle }}"><sc-if value="{{ capsUnsure.selected }}" hint-placeholder-val="{{ false }}"><span style="width:9px; height:9px; border-radius:2px; background:var(--primary-border,#adb0ff); display:block;"></span></sc-if></span>
            <em style="flex:1; font-style:italic; color:var(--text-sub,#b1b2d2);">Unsure — help me confirm capabilities during framing</em>
          </label>
        </div>
      </section>
      </sc-if>

      <!-- SECTION 8 — Out of scope -->
      <sc-if value="{{ showSec7 }}" hint-placeholder-val="{{ true }}">
      <section data-screen-label="Section 8 — Out of scope" style="background:var(--card,#212135); border:1px solid var(--border,#3b3b52); border-radius:14px; padding:22px 24px; margin-bottom:16px; animation:ifFade .25s ease both;">
        <div style="display:flex; align-items:center; gap:11px; flex-wrap:wrap;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:25px; height:25px; border-radius:8px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); font-weight:700; font-size:13px;">8</span>
          <h2 style="margin:0; font-size:16px; font-weight:700; color:var(--text,#ebecff);">Out of scope</h2>
          <span style="font-size:10px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; padding:2px 8px; border-radius:100px; color:var(--text-sub,#b1b2d2); border:1px solid var(--border,#3b3b52);">Should</span>
        </div>
        <p style="margin:8px 0 0; font-size:12px; color:var(--text-faint,#8a8bad);"><span style="color:var(--text-sub,#b1b2d2);">Why —</span> A hard boundary, not a preference — the agent will not suggest these even if the capability is active. Use for compliance constraints (e.g. GDPR limits on Session Replay) or anything the customer has explicitly ruled out.</p>
        <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(258px,1fr)); gap:14px; margin-top:16px;">
          <sc-for list="{{ outOfScopeGroups }}" as="g" hint-placeholder-count="3">
            <div style="border:1px solid var(--border,#3b3b52); border-radius:10px; padding:12px 14px; background:var(--field,#1b1b30);">
              <h3 style="margin:0 0 8px; font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:var(--text-faint,#8a8bad); font-weight:700;">{{ g.title }}</h3>
              <sc-for list="{{ g.items }}" as="it" hint-placeholder-count="3">
                <div style="margin:4px 0;">
                  <label onclick="{{ it.onClick }}" style="{{ it.rowStyle }}" style-hover="border-color:var(--border-hover,#4d4e66);">
                    <span style="{{ it.boxStyle }}"><sc-if value="{{ it.selected }}" hint-placeholder-val="{{ false }}"><span style="width:9px; height:9px; border-radius:2px; background:var(--primary-border,#adb0ff); display:block;"></span></sc-if></span>
                    <span style="flex:1;">{{ it.label }}</span>
                  </label>
                  <sc-if value="{{ it.showGen }}" hint-placeholder-val="{{ false }}">
                    <div style="display:flex; gap:6px; margin:6px 0 2px 30px; flex-wrap:wrap;">
                      <sc-for list="{{ it.genButtons }}" as="gb" hint-placeholder-count="3">
                        <button onclick="{{ gb.onClick }}" style="{{ gb.style }}" style-hover="border-color:var(--border-hover,#4d4e66);">{{ gb.label }}</button>
                      </sc-for>
                    </div>
                  </sc-if>
                </div>
              </sc-for>
            </div>
          </sc-for>
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid var(--border,#3b3b52);">
          <label style="display:flex; align-items:center; gap:8px; margin-bottom:6px; font-size:13px; font-weight:500; color:var(--text-sub,#b1b2d2);">Notes <span style="font-size:11px; font-weight:400; color:var(--text-faint,#8a8bad);">why it's out of scope — regulation, prior commitment, contract terms…</span></label>
          <textarea data-fid="outOfScopeNotes" value="{{ answers.outOfScopeNotes }}" oninput="{{ onInput }}" placeholder="e.g. GDPR — no Session Replay in the EU tenant" style="width:100%; min-height:64px; resize:vertical; background:var(--field,#1b1b30); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:9px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);"></textarea>
        </div>
      </section>
      </sc-if>

      <!-- SECTION 9 — Focus applications -->
      <sc-if value="{{ showSec8 }}" hint-placeholder-val="{{ true }}">
      <section data-screen-label="Section 9 — Focus applications" style="background:var(--card,#212135); border:1px solid var(--border,#3b3b52); border-radius:14px; padding:22px 24px; margin-bottom:16px; animation:ifFade .25s ease both;">
        <div style="display:flex; align-items:center; gap:11px; flex-wrap:wrap;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:25px; height:25px; border-radius:8px; background:var(--primary-bg,#292944); color:var(--primary-border,#adb0ff); font-weight:700; font-size:13px;">9</span>
          <h2 style="margin:0; font-size:16px; font-weight:700; color:var(--text,#ebecff);">Focus applications &amp; RUM</h2>
          <span style="{{ s6TagStyle }}">{{ s6TagLabel }}</span>
        </div>
        <p style="margin:8px 0 0; font-size:12px; color:var(--text-faint,#8a8bad);"><span style="color:var(--text-sub,#b1b2d2);">Why —</span> {{ s6Why }}</p>
        <sc-for list="{{ apps }}" as="ap" hint-placeholder-count="1">
          <div style="margin-top:14px; border:1px solid var(--border,#3b3b52); border-radius:10px; padding:14px; background:var(--field,#1b1b30);">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
              <span style="font-size:11px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; color:var(--text-faint,#8a8bad);">{{ ap.label }}</span>
              <sc-if value="{{ ap.showRemove }}" hint-placeholder-val="{{ false }}"><button onclick="{{ ap.onRemove }}" style="background:none; border:none; color:var(--text-faint,#8a8bad); font-size:16px; cursor:pointer; line-height:1; padding:0 4px;" style-hover="color:var(--critical,#ff999c);">×</button></sc-if>
            </div>
            <input type="text" value="{{ ap.name }}" oninput="{{ ap.onName }}" placeholder="Application name — e.g. Checkout web app" style="width:100%; margin-top:8px; background:var(--card,#212135); color:var(--text,#ebecff); border:1px solid var(--border,#3b3b52); border-radius:6px; padding:9px 12px; font-size:14px; outline:none;" style-focus="border-color:var(--primary-border,#adb0ff); box-shadow:0 0 0 3px rgba(25,102,255,.25);">
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:12px;">
              <div>
                <label style="display:block; margin-bottom:6px; font-size:12.5px; font-weight:500; color:var(--text-sub,#b1b2d2);">RUM enabled?</label>
                <div style="display:flex; gap:7px; flex-wrap:wrap;"><sc-for list="{{ ap.rumOptions }}" as="o" hint-placeholder-count="3"><button onclick="{{ o.onClick }}" style="{{ o.style }}" style-hover="border-color:var(--border-hover,#4d4e66);">{{ o.label }}</button></sc-for></div>
              </div>
              <div>
                <label style="display:block; margin-bottom:6px; font-size:12.5px; font-weight:500; color:var(--text-sub,#b1b2d2);">Session Replay active?</label>
                <div style="display:flex; gap:7px; flex-wrap:wrap;"><sc-for list="{{ ap.srOptions }}" as="o" hint-placeholder-count="3"><button onclick="{{ o.onClick }}" style="{{ o.style }}" style-hover="border-color:var(--border-hover,#4d4e66);">{{ o.label }}</button></sc-for></div>
              </div>
            </div>
          </div>
        </sc-for>
        <button onclick="{{ onAddApp }}" style="margin-top:12px; background:transparent; border:1px dashed var(--border-hover,#4d4e66); color:var(--primary,#999bed); border-radius:8px; padding:9px 16px; font-size:13px; font-weight:500; cursor:pointer;" style-hover="border-color:var(--primary-border,#adb0ff);">+ Add application</button>
      </section>
      </sc-if>
```

- [ ] **Step 2: Pack + headless verify** — run the pack command, then:
```bash
node /private/tmp/claude-501/-Users-nburwick-insights-forge/82719aa8-8a08-4dc8-a421-f0c85668c765/scratchpad/load-test.cjs "$(pwd)/html/Insights Forge (Seed Prompt Generator) - Draft.html"
```
Expected: `bundler error box: (none)`, `console/page errors: (none)`, `h1: "Insights Forge"`. If the app errors, a template key is mismatched between markup and Task 1's view-model — fix before committing.

- [ ] **Step 3: Commit**
```bash
git add "html/seed-prompt-generator-src.html" "html/Insights Forge (Seed Prompt Generator) - Draft.html"
git commit -m "$(cat <<'EOF'
Restructure Seed Prompt Generator: 9-step markup reflow

Rewrites the form-column sections to the round-2 structure: Outputs &
trigger, Analyst context (+ Your role), Customer context (+ relationship),
Stakeholders & audience (+ per-stakeholder communication level), Goals &
success, Pain & constraints, then capabilities / out-of-scope / focus apps.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: End-to-end verification

**Files:** none modified — drives the Draft produced by Tasks 1–2.

- [ ] **Step 1: Headless walkthrough** — extend the round-1 verify approach (a Playwright `.cjs` that navigates all steps and asserts). Confirm:
  - 9 nav items + "Review & generate"; progress reads "Step N of 9"; no bundler/console errors.
  - Step 1 shows Trigger pills + output cards; Step 2 shows Your role + the 3 scales; Step 3 shows customer basics + a "Relationship & context" textarea; Step 4 shows a per-stakeholder "Communication level" dropdown defaulting to Mixed; Step 5 shows Intent + success; Step 6 shows the single "Pain & constraints" textarea with 8 starter chips.
  - The strings "Meeting / read-time window", "Tone or branding", and a form-level "Response format — audience" block are absent.
  - Export gate: fill outputs, customer name/desc/vertical, relationship context, intent + success, pain & constraints, one capability — leave stakeholders at default — and confirm Copy/Download enable.
  - Generated brief (readonly textarea) contains "## Requested outputs & trigger", a "Trigger(s):" line, "communication level:" on the stakeholder line, "## Pain & constraints", and does NOT contain "Time window" or "Tone / branding".
  - Toggle theme: a required-but-incomplete section's nav dot is amber in dark, crimson in light (unchanged round-1 behavior).

- [ ] **Step 2: Report** — screenshots of the new Step 1, Step 4 (stakeholder level), and Step 6 (pain & constraints); confirm the file is ready for manual review at `html/Insights Forge (Seed Prompt Generator) - Draft.html`.

## Self-review notes (controller)

- The `_secData` preamble vars (`vertOk`, `anyScale`, `allScale`, `nonDavis`, `appOk`, `stkOk`) are defined above `const grp` and are unchanged — the new grp references the same names.
- `s6Req()` still keys on `intents` (now rendered in Step 5) — unchanged; the Focus-apps conditional-Must still works.
- `freeVM` in `renderVals()` iterates `Object.keys(this.FREE)`, so dropping `specific`/`techPriorities` and adding `painConstraints` automatically flows to `free.painConstraints` in the template — no separate view-model edit needed for the free fields.
- Round-1's Salesforce note and archetype-default/`level` defaults are preserved in the new Stakeholders markup.
