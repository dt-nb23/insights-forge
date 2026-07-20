---
name: layout-system
description: |
  Design system catalog for Insights Forge HTML one-pagers. Defines the
  design tokens, component catalog (headers, beats, footer), recipe selection
  guide, and HTML/CSS conventions. Read this before selecting a recipe or
  writing any HTML. The canonical implementation is
  memory/clients/u-haul/engagements/2026-06-29-digital-experience-parity/uhaul-digital-experience-intelligence-v3.html.
---

# Insights Forge one-pager layout system

## Design tokens (CSS custom properties)

Copy the full `:root {}` block below verbatim into every one-pager. Do not invent new color values.

```css
:root {
  /* Beat accents — one fixed color per section */
  --setup:   #1966FF;   /* TL;DR / setup  */
  --problem: #8B1DC0;   /* 01 · Problem   */
  --guide:   #1A7A70;   /* 02 · Guide     */
  --plan:    #5E28E5;   /* 03 · Plan      */
  --stakes:  #C93FDB;   /* 04 · Stakes    */
  /* Dark frame */
  --frame1: #07101E; --frame2: #122040; --frame3: #1A2A4D; --footer: #0C1626;
  /* Neutrals & tints */
  --ink: #151A28; --navy: #1A2440; --gray: #6F747F; --stat-lbl: #41506E;
  --line: #E2E8F4; --line2: #CBD5E8; --panel: #F8F9FC; --pagebg: #E8ECF3;
  --tint-mag: #FDF0FF; --tint-teal: #F0FAF8; --tint-prob: #FBF3FD;
  /* Header / takeaway highlight hues */
  --sky: #8FB4FF; --mint: #5FE0CE; --lilac: #C9A8F5;
  --grad: linear-gradient(90deg,#3BACF0,#1966FF,#5E28E5,#C93FDB);
  --font: 'DTFlow', Arial, sans-serif;
}
```

## Font loading

Load all six weights. Adjust the path prefix to match the HTML file's depth relative to the project root (root-level: `DTFlow/`; five levels deep: `../../../../../DTFlow/`).

```css
@font-face { font-family:'DTFlow'; src:url('[path]/DTFlow/DTFlow-Light.otf')    format('opentype'); font-weight:300; }
@font-face { font-family:'DTFlow'; src:url('[path]/DTFlow/DTFlow-Regular.otf')  format('opentype'); font-weight:400; }
@font-face { font-family:'DTFlow'; src:url('[path]/DTFlow/DTFlow-Medium.otf')   format('opentype'); font-weight:500; }
@font-face { font-family:'DTFlow'; src:url('[path]/DTFlow/DTFlow-Semibold.otf') format('opentype'); font-weight:600; }
@font-face { font-family:'DTFlow'; src:url('[path]/DTFlow/DTFlow-Bold.otf')     format('opentype'); font-weight:700; }
@font-face { font-family:'DTFlow'; src:url('[path]/DTFlow/DTFlow-Extrabold.otf')format('opentype'); font-weight:800; }
```

## Page frame (always the same)

```css
*, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
body { background:var(--pagebg); font-family:var(--font); font-weight:300; color:var(--ink); -webkit-font-smoothing:antialiased; }
.page { width:960px; margin:22px auto; background:#fff; box-shadow:0 6px 30px rgba(12,22,38,0.14); }
.eyebrow { font-size:9px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; }
[aria-hidden="true"] { pointer-events:none; }
@page { size:Letter portrait; margin:0.3in; }
@media print { body{background:#fff;} .page{margin:0 auto;box-shadow:none;zoom:0.65;} }
```

---

## Component catalog

### Headers

**HdrA — inline header**

Compact single-row layout. Lockup, divider, and text block sit side by side. Use for exec-skim audiences where brevity signals confidence.

```html
<header>
  <div class="masthead"><!-- wave-bg gradient overlay applied via CSS -->
    <img class="mast-lockup" src="[path]/assets/insights-lockup-rev.png" alt="Dynatrace Insights" />
    <div class="mast-divider" aria-hidden="true"></div>
    <div>
      <p class="eyebrow mast-eyebrow">[Engagement type] · [Client name]</p>
      <h1 class="mast-title">[Document title]</h1>
      <p class="mast-meta">[Stakeholder name, role] · [Date]</p>
    </div>
  </div>
  <div class="grad-bar" aria-hidden="true"></div>
</header>
```

Key CSS: `.mast-lockup { height:24px; }` `.mast-divider { width:1px; height:42px; background:rgba(255,255,255,0.22); }` `.mast-title { font-size:20px; font-weight:600; color:#fff; }`

---

**HdrB — stacked header** *(default; used in v3)*

Two-row layout. Lockup stacks above the title on the left; meta (stakeholder names, date) right-aligned. Use for working-session or standard delivery audiences.

```html
<header class="masthead"><!-- wave-bg gradient overlay applied via CSS -->
  <div class="mast-top">
    <div class="mast-left">
      <img class="mast-lockup" src="[path]/assets/insights-lockup-rev.png" alt="Dynatrace Insights" />
      <p class="eyebrow mast-eyebrow">[Engagement type] · [Client name]</p>
      <h1 class="mast-title">[Document title]</h1>
      <p class="mast-promise">[One-line value statement]</p>
    </div>
    <p class="mast-meta"><b>[Name]</b><br>[Title]<br><b>[Name]</b><br>[Title]<br>[Date]</p>
  </div>
  <div class="grad-bar" aria-hidden="true"></div>
</header>
```

Key CSS: `.mast-top { display:flex; justify-content:space-between; align-items:flex-start; }` `.mast-meta { text-align:right; font-size:9.5px; font-weight:300; }`

Wave background (both headers):
```css
.masthead {
  background:
    linear-gradient(to right, rgba(7,16,30,0.93) 0%, rgba(7,16,30,0.82) 46%, rgba(7,16,30,0.55) 100%),
    url('[path]/assets/wave-bg.png') center / cover no-repeat var(--frame1);
  padding:20px 34px 0;
}
.grad-bar { height:3px; border-radius:2px; background:var(--grad); margin-top:16px; }
```

---

### TL;DR (fixed — always include)

Two-column summary block immediately below the header. Left: one-sentence summary with key numbers bolded. Right: 4-stat grid.

```html
<section class="tldr" aria-label="Executive summary">
  <div>
    <p class="eyebrow tldr-eyebrow">TL;DR</p>
    <p class="tldr-sent">[Summary sentence. Key dates or outcomes in <b>bold</b>.]</p>
  </div>
  <div class="stats" role="list">
    <div role="listitem"><div class="stat-num" style="color:var(--[token]);">[N]</div><div class="stat-lbl">[Label]</div></div>
    <!-- repeat for 4 stats total -->
  </div>
</section>
```

Key CSS: `.tldr { display:grid; grid-template-columns:1.1fr 1.35fr; gap:28px; background:#EEF3FF; border-left:4px solid var(--setup); margin:14px 34px 0; padding:13px 20px; }` `.stats { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; text-align:center; }` `.stat-num { font-size:24px; font-weight:800; }`

---

### Beat scaffold (shared by 01–04)

Every numbered section opens with the same scaffold: a colored circle node and a section name.

```html
<section class="beat" aria-labelledby="b[N]">
  <div class="beat-head">
    <span class="node" style="background:var(--[section-token]);" aria-hidden="true">[NN]</span>
    <span class="beat-name" id="b[N]"><span class="num">[NN] · </span>[Section title]</span>
  </div>
  <!-- component content here -->
</section>
```

Optional subheading before the component block: `<p class="beat-line">[One-line setup sentence]</p>`

Key CSS: `.beat { padding:15px 34px 16px; border-top:1px solid var(--line); }` `.node { width:22px; height:22px; border-radius:50%; color:#fff; font-size:10px; font-weight:800; display:flex; align-items:center; justify-content:center; }`

---

### 01 · Problem (node color: `--problem` `#8B1DC0`)

**01A — bold statement**

Large two-line claim (first line navy, second line problem-colored) with a support sentence and a single standout stat. Use when the finding is stark enough to state as a claim.

```html
<div class="claim-wrap">
  <p class="claim"><span class="c1">[First half of claim.]</span><br><span class="c2">[Second half — the contrast.]</span></p>
  <p class="claim-support">[One sentence of context or evidence.]</p>
  <div class="claim-stat">
    <span class="big">[N%]</span>
    <span class="lbl">[What that number means]</span>
  </div>
</div>
```

Key CSS: `.claim { font-size:22px; font-weight:800; }` `.c1 { color:var(--navy); }` `.c2 { color:var(--problem); }` `.claim-stat { display:flex; align-items:center; gap:11px; border-top:1px solid var(--line); padding-top:11px; }` `.big { font-size:30px; font-weight:800; color:var(--problem); }`

---

**01B — symptom → consequence table** *(used in v3)*

Two-column table: Symptom | Why it hurts. A thin magenta stripe on the left edge signals the problem accent. Use when multiple distinct symptoms each carry their own consequence — the parallel structure helps a reader scan.

```html
<div class="ptable" role="table" aria-label="Symptoms and why they hurt">
  <div class="ptable-head" role="row">
    <div aria-hidden="true"></div>
    <div role="columnheader">Symptom</div>
    <div class="c2" role="columnheader">Why it hurts</div>
  </div>
  <div class="ptable-row" role="row">
    <div class="stripe" aria-hidden="true"></div>
    <div class="sym" role="cell">[Symptom]</div>
    <div class="con" role="cell">[Business consequence]</div>
  </div>
  <!-- repeat ptable-row for each symptom -->
</div>
```

Key CSS: `.ptable { border:1px solid var(--line); border-radius:8px; overflow:hidden; }` `.ptable-head { display:grid; grid-template-columns:5px 1fr 1.25fr; font-size:9px; font-weight:700; color:var(--problem); background:var(--tint-prob); }` `.ptable-row { display:grid; grid-template-columns:5px 1fr 1.25fr; border-top:1px solid var(--line); }` `.stripe { background:var(--stakes); }` `.sym,.con { padding:9px 13px; font-size:11px; color:#333; line-height:1.4; }`

---

**01C — pull-quote**

A named stakeholder's words carry the problem. Use when a real quote is available and more persuasive than a symptom table — the attribution makes it concrete.

```html
<figure class="pquote">
  <blockquote class="pq-quote">&ldquo;[Quote text.]&rdquo;</blockquote>
  <figcaption class="pq-attr">— [Attribution: name, role, or context]</figcaption>
</figure>
<div class="pq-context" role="list" aria-label="Context">
  <span class="pq-pill" role="listitem">[Context fact 1]</span>
  <span class="pq-pill" role="listitem">[Context fact 2]</span>
</div>
```

Key CSS: `.pquote { border-left:4px solid var(--problem); padding-left:14px; margin-left:31px; }` `.pq-quote { font-size:18px; font-weight:600; font-style:italic; color:var(--navy); }` `.pq-pill { background:var(--tint-mag); color:var(--problem); font-size:9.5px; font-weight:600; padding:4px 9px; border-radius:5px; }`

---

**01D — three-tile snapshot**

Three equal-width tiles, each with a big number and a label. Use when multiple distinct metrics each capture a different dimension of the problem — pure-numeric framing reads fast to senior audiences.

```html
<div class="tiles" role="list" aria-label="[Description of what these numbers represent]">
  <div class="tile" role="listitem"><div class="tile-num">[N]</div><div class="tile-lbl">[Label]</div></div>
  <div class="tile" role="listitem"><div class="tile-num">[N]</div><div class="tile-lbl">[Label]</div></div>
  <div class="tile" role="listitem"><div class="tile-num">[N]</div><div class="tile-lbl">[Label]</div></div>
</div>
<p class="tie-line">[Single sentence tying the three numbers together.]</p>
```

Key CSS: `.tiles { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }` `.tile { background:var(--tint-mag); border-radius:8px; padding:13px 10px; text-align:center; }` `.tile-num { font-size:26px; font-weight:800; color:var(--problem); }`

---

### 02 · Guide (node color: `--guide` `#1A7A70`)

**02A — thesis + capability map** *(used in v3)*

A thesis paragraph followed by a pain → capability mapping table. Use when the audience needs to see the direct link between their stated problems and specific platform capabilities.

```html
<p class="guide-thesis">[Positioning sentence. Key differentiator in <b>bold</b>.]</p>
<div class="cmap" role="list" aria-label="[Description]">
  <div class="cmap-head" aria-hidden="true">
    <span>The question</span><span></span><span>Answered by</span>
  </div>
  <div class="cmap-row" role="listitem">
    <div class="pain-pill">[Customer pain question]</div>
    <span class="arrow" aria-hidden="true">→</span>
    <div class="cap-pill">[Capability that answers it]</div>
  </div>
  <!-- repeat cmap-row -->
</div>
```

Key CSS: `.guide-thesis { font-size:11.5px; color:#333; line-height:1.45; margin:0 0 12px 31px; }` `.cmap-row { display:flex; align-items:center; gap:10px; margin-bottom:8px; }` `.pain-pill { flex:1; background:var(--tint-mag); border-radius:7px; padding:9px 12px; font-size:11px; }` `.arrow { color:var(--guide); font-size:15px; font-weight:700; width:26px; text-align:center; }` `.cap-pill { flex:1.15; background:var(--tint-teal); border-radius:7px; padding:9px 12px; font-size:11px; font-weight:600; color:var(--guide); }`

---

**02B — positioning + capability chips**

A short positioning statement followed by chip-pill tags showing which capabilities are already active, plus a trust stat. Use when the audience needs reassurance that the required capabilities exist — chips read as checkmarks.

```html
<p class="pos-line">[Positioning sentence — what's already in place.]</p>
<div class="chips" role="list" aria-label="Active capabilities">
  <span class="chip" role="listitem"><span class="chip-dot" aria-hidden="true"></span>[Capability name]</span>
  <!-- repeat -->
</div>
<div class="trust">
  <span class="trust-num">[N]</span>
  <span class="trust-lbl">[What zero or the number means for the customer]</span>
</div>
```

Key CSS: `.pos-line { font-size:14px; font-weight:600; color:var(--navy); }` `.chip { display:inline-flex; align-items:center; gap:6px; background:#fff; border:1px solid #CFE9E4; border-radius:6px; padding:5px 10px; font-size:10.5px; }` `.chip-dot { width:8px; height:8px; border-radius:50%; background:var(--guide); }` `.trust { display:flex; align-items:center; gap:10px; margin-top:13px; background:var(--tint-teal); border-radius:8px; padding:10px 12px; }` `.trust-num { font-size:26px; font-weight:800; color:var(--guide); }`

---

**02D — statement + proof band**

One confident assertion followed by three proof numbers separated by dividers. Use when the value is already demonstrable and you just need to state it plainly.

```html
<div class="g-wrap">
  <p class="g-statement">[Positioning assertion. <span class="accent">Key phrase accented.</span>]</p>
  <div class="proof-band" role="list" aria-label="[Description]">
    <div class="proof" role="listitem"><div class="proof-num">[N]<span>[unit]</span></div><div class="proof-lbl">[Label]</div></div>
    <div class="proof-div" aria-hidden="true"></div>
    <div class="proof" role="listitem"><div class="proof-num">[N]<span>[unit]</span></div><div class="proof-lbl">[Label]</div></div>
    <div class="proof-div" aria-hidden="true"></div>
    <div class="proof" role="listitem"><div class="proof-num">[N]</div><div class="proof-lbl">[Label]</div></div>
  </div>
</div>
```

Key CSS: `.g-statement { font-size:20px; font-weight:700; color:var(--navy); }` `.accent { color:var(--guide); }` `.proof-band { display:flex; margin-top:13px; border-top:1px solid var(--line); padding-top:11px; }` `.proof { flex:1; text-align:center; }` `.proof-num { font-size:24px; font-weight:800; color:var(--guide); }` `.proof-div { width:1px; background:var(--line); }`

---

### 03 · Plan (node color: `--plan` `#5E28E5`)

**03A — phase cards, clean** *(used in v3)*

Colored header (eyebrow + phase name), panel body (days + description). No owner/gate detail. Use for exec-skim or when pacing is more important than accountability.

```html
<p class="beat-line">[Optional one-line setup sentence.]</p>
<div class="phases" role="list" aria-label="[Phase description and concurrency note]">
  <div class="phase" role="listitem">
    <div class="phase-head" style="background:var(--guide);">
      <div class="p-eyebrow">Phase 1</div>
      <div class="p-name">[Phase name]</div>
    </div>
    <div class="phase-body">
      <div class="p-days">Days [N–N]</div>
      <div class="p-desc">[What gets done]</div>
    </div>
  </div>
  <!-- repeat for each phase; use --setup, --plan for phases 2, 3 -->
</div>
<p class="concurrency">[Concurrency or sequencing note. Key window in <b>bold</b>.]</p>
```

Key CSS: `.phases { display:flex; gap:9px; }` `.phase { flex:1; border:1px solid #E4E8F0; border-radius:7px; overflow:hidden; }` `.phase-head { padding:7px 11px; }` `.p-eyebrow { color:rgba(255,255,255,0.82); font-size:8.5px; font-weight:700; }` `.p-name { font-size:12.5px; font-weight:600; color:#fff; }` `.phase-body { padding:9px 11px; background:var(--panel); }` `.p-days { font-size:10.5px; font-weight:700; color:var(--navy); }` `.p-desc { font-size:10px; color:#444; }`

---

**03B — phase cards, labeled detail**

Same card frame as 03A, but the body shows Owner, Gate, and Output rows instead of days + description. Use for director or engineering-lead audiences who need to see who owns each phase and what the gate is.

Body region replaces 03A's body with:
```html
<div class="phase-body">
  <div><b>Owner</b> · [Who]</div>
  <div><b>Gate</b> · [Decision or approval required]</div>
  <div><b>Output</b> · [What ships at the end of this phase]</div>
</div>
```

Key CSS same as 03A. Phase head uses `p-eyebrow` (phase name) + `p-days` (day range) instead of p-eyebrow + p-name.

---

**03D — numbered steps**

Sequential step circles in color-coded order with a name, timing qualifier, and description. Use when chronological sequence matters more than phase ownership.

```html
<div class="steps" role="list" aria-label="[Steps description and concurrency note]">
  <div class="step" role="listitem">
    <div class="step-node" style="background:var(--guide);" aria-hidden="true">1</div>
    <div>
      <div class="step-name">[Step name] <span class="days">· Days [N–N]</span></div>
      <div class="step-desc">[What this step does]</div>
    </div>
  </div>
  <!-- repeat -->
</div>
<p class="concurrency">[Concurrency note. Total window in <b>bold</b>.]</p>
```

Key CSS: `.steps { display:flex; flex-direction:column; gap:9px; margin-left:31px; }` `.step { display:flex; gap:11px; align-items:center; }` `.step-node { width:30px; height:30px; border-radius:50%; color:#fff; font-size:14px; font-weight:800; display:flex; align-items:center; justify-content:center; }` `.step-name { font-size:12px; font-weight:700; color:var(--navy); }` `.days { font-weight:400; color:var(--gray); font-size:10px; }` `.step-desc { font-size:10px; color:var(--stat-lbl); }`

---

### 04 · Stakes (node color: `--stakes` `#C93FDB`)

**04A — risk vs. success split** *(used in v3)*

Two panels side by side: risk (tint-mag, problem border) and success (tint-teal, guide border). Use as the default — it names both what we lose by waiting and what we gain by acting.

```html
<div class="split">
  <div class="stake stake-risk" role="note" aria-label="If we wait">
    <h3>If we wait</h3>
    <p>[Risk 1]</p>
    <p>[Risk 2]</p>
  </div>
  <div class="stake stake-win" role="note" aria-label="By day [N]">
    <h3>By day [N]</h3>
    <p>[Win 1]</p>
    <p>[Win 2]</p>
  </div>
</div>
```

Key CSS: `.split { display:grid; grid-template-columns:1fr 1.15fr; gap:13px; }` `.stake { border-radius:8px; padding:12px 15px; }` `.stake-risk { background:var(--tint-mag); border-top:3px solid var(--problem); }` `.stake-win { background:var(--tint-teal); border-top:3px solid var(--guide); }` `.stake h3 { font-size:12px; font-weight:700; }` `.stake-risk h3 { color:var(--problem); }` `.stake-win h3 { color:var(--guide); }` `.stake p { font-size:11px; color:#333; line-height:1.4; }`

---

**04B — head-to-head + verdict**

Two panels in a row separated by a "VS" divider, with a verdict badge below. Use when the choice is binary and you want a visual conclusion.

```html
<div class="h2h">
  <div class="h2h-side h2h-wait" role="note" aria-label="If we wait">
    <h3>If we wait</h3>
    <p>[Consequence 1]</p>
  </div>
  <div class="h2h-vs" aria-hidden="true"><span>VS</span></div>
  <div class="h2h-side h2h-act" role="note" aria-label="If we act">
    <h3>If we act</h3>
    <p>[Outcome 1]</p>
  </div>
</div>
<div class="verdict"><span>[Verdict sentence.]</span></div>
```

Key CSS: `.h2h { display:flex; align-items:stretch; border:1px solid var(--line); border-radius:8px; overflow:hidden; }` `.h2h-side { flex:1; padding:12px 14px; }` `.h2h-wait { background:var(--tint-mag); }` `.h2h-act { background:var(--tint-teal); }` `.h2h-vs { display:flex; align-items:center; justify-content:center; background:#fff; padding:0 5px; font-size:11px; font-weight:800; color:var(--gray); }` `.verdict { margin-top:11px; text-align:center; }` `.verdict span { display:inline-block; background:var(--navy); color:#fff; font-size:11.5px; font-weight:700; padding:7px 16px; border-radius:16px; }`

---

**04D — risk ✕ / win ✓ checklist**

Sequential lines with ✕ and ✓ markers, separated by a divider. Use when stakes are clear and you need the most compact format.

```html
<div role="note" aria-label="Risks and wins">
  <p class="check-h risk">Risk if we wait</p>
  <p class="check-item"><span class="x" aria-hidden="true">✕</span> [Risk statement]</p>
  <div class="check-div" aria-hidden="true"></div>
  <p class="check-h win">If we act</p>
  <p class="check-item"><span class="v" aria-hidden="true">✓</span> [Win statement]</p>
</div>
```

Key CSS: `.check-h { font-size:11px; font-weight:700; margin-bottom:7px; }` `.check-h.risk { color:var(--problem); }` `.check-h.win { color:var(--guide); }` `.check-item { font-size:10.5px; color:#333; line-height:1.5; margin-bottom:4px; }` `.x { color:var(--problem); font-weight:700; }` `.v { color:var(--guide); font-weight:700; }` `.check-div { height:1px; background:var(--line); margin:11px 0; }`

---

### 05 · Takeaway (always dark with wave background)

All 05 variants share the same dark wave container:

```css
.takeaway {
  background:
    linear-gradient(to right, rgba(7,16,30,0.95) 0%, rgba(7,16,30,0.88) 40%, rgba(7,16,30,0.72) 100%),
    url('[path]/assets/wave-bg.png') center / cover no-repeat var(--frame1);
  padding:18px 34px 20px;
}
.tk-eyebrow { color:rgba(255,255,255,0.5); margin-bottom:8px; }
.tk-line { font-size:16px; font-weight:600; color:#fff; line-height:1.4; }
.tk-line .ask { color:var(--sky); }
.tk-line .pay { color:var(--mint); }
```

---

**05A — dark + 2 decision chips** *(used in v3)*

Named decisions visible as cards. Use whenever the one-pager must surface the exact decisions being requested — the chip format makes them scannable.

```html
<section class="takeaway" aria-labelledby="b5">
  <p class="eyebrow tk-eyebrow" id="b5">05 · The ask</p>
  <p class="tk-line">[Setup phrase.] <span class="ask">[The ask]</span> [payoff phrase with <span class="pay">accent.</span>]</p>
  <div class="decisions" role="list">
    <div class="decision d1" role="listitem">
      <div class="d-num">Decision 1</div>
      <div class="d-name">[Decision name]</div>
      <div class="d-desc">[Who approves and what they're agreeing to]</div>
    </div>
    <div class="decision d2" role="listitem">
      <div class="d-num">Decision 2</div>
      <div class="d-name">[Decision name]</div>
      <div class="d-desc">[Who approves and what they're agreeing to]</div>
    </div>
  </div>
</section>
```

Key CSS: `.decisions { display:flex; gap:11px; margin-top:15px; }` `.decision { flex:1; background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.13); border-radius:8px; padding:10px 13px; }` `.d-num { font-size:8.5px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; margin-bottom:3px; }` `.decision.d1 .d-num { color:var(--sky); }` `.decision.d2 .d-num { color:var(--lilac); }` `.d-name { font-size:11.5px; font-weight:600; color:#fff; }` `.d-desc { font-size:10px; font-weight:300; color:rgba(255,255,255,0.72); }`

---

**05C — dark + decision chips + reassurance**

Same as 05A, add a `.reassure` line below the decisions:

```html
<p class="reassure">[Italic confidence line that reduces perceived risk of saying yes.]</p>
```

Key CSS: `.reassure { font-size:10px; color:rgba(255,255,255,0.6); margin-top:12px; line-height:1.4; font-style:italic; }`

---

**05D — minimal one-liner**

Just the takeaway sentence with an accented payoff phrase. Use for exec-skim audiences where the decision detail lives in the deck.

```html
<section class="takeaway" aria-labelledby="b5">
  <p class="eyebrow tk-eyebrow" id="b5">05 · The ask</p>
  <p class="tk-line">[Setup phrase.] <span class="pay">[Payoff phrase.]</span></p>
  <p class="tk-qualifier">[Optional qualifier — e.g., "Decision detail lives in the leadership deck."]</p>
</section>
```

Key CSS: `.tk-qualifier { font-size:10.5px; color:rgba(255,255,255,0.6); margin-top:11px; }`

---

### Footer — FtrB (always the same)

```html
<footer class="foot">
  <div class="foot-bar" aria-hidden="true"></div>
  <div class="foot-copy">© 2026 Dynatrace, LLC. &nbsp;·&nbsp; Confidential</div>
  <div class="foot-src">Sources: [citation 1] · [citation 2]</div>
</footer>
```

Key CSS: `.foot { background:var(--footer); padding:15px 34px; text-align:center; }` `.foot-bar { width:64px; height:3px; border-radius:2px; background:var(--grad); margin:0 auto 11px; }` `.foot-copy { font-size:10px; color:rgba(255,255,255,0.72); }` `.foot-src { font-size:8.5px; color:rgba(255,255,255,0.42); margin-top:6px; line-height:1.45; max-width:760px; margin:0 auto; }`

---

## Recipe selection

A recipe is the ordered sequence of components for a deliverable. Record it as a comment on line 2 of every HTML file (after `<!DOCTYPE html>`):

```html
<!-- Recipe: HdrX · TL;DR · 01X · 02X · 03X · 04X · 05X · FtrB | Why: [one sentence explaining the layout logic for this audience and content] -->
```

The `Why:` clause is required — it records the design rationale so future edits know which choices were deliberate.

### How to select components

The recipe is a storytelling decision, not a template. Start from the plan and the reader, not from a default. For each section, ask what the content is and what it needs to do, then pick the component that serves that.

**01 · Problem — how should the problem land?**

| If the problem is… | Use |
|---|---|
| A stark binary — something exists that the audience can't access, or something changed that shouldn't have | 01A · bold statement — states the contrast directly |
| Multiple distinct symptoms that each have their own consequence | 01B · symptom → consequence table — parallel structure helps scanning |
| Best carried by a named person's words — a stakeholder's quote captures the pain better than data | 01C · pull-quote — attribution makes it concrete |
| Multiple distinct metrics that each measure a different dimension of the gap | 01D · three-tile snapshot — numeric framing reads fast to senior audiences |

**02 · Guide — how should Dynatrace's value be shown?**

| If the value proof is… | Use |
|---|---|
| The audience doesn't yet see the connection between their stated pain and the platform's capabilities | 02A · thesis + capability map — makes the pain→solution link visible |
| The capabilities are already active and the audience needs reassurance, not persuasion | 02B · capability chips — reads as a checklist of things already in place |
| The value is already demonstrable and you just need to state it with backing numbers | 02D · statement + proof band — confident assertion, no mapping needed |

**03 · Plan — what does the reader need to know about the plan?**

| If the audience needs… | Use |
|---|---|
| A sense of pacing and momentum — what happens in each phase | 03A · phase cards, clean — names and day ranges carry the story |
| To know who owns what and what the gates are — accountability matters | 03B · phase cards, labeled detail — owner, gate, output per phase |
| To see a chronological sequence where the order of steps matters | 03D · numbered steps — sequence and timing are the point |

**04 · Stakes — how should the risk/reward be framed?**

| If the stakes are… | Use |
|---|---|
| A named set of risks with a named set of wins — both sides need equal weight | 04A · risk vs. success split — default for most engagements |
| Binary: the only question is "do we act or not" and a verdict seals it | 04B · head-to-head + verdict — the visual close clinches the argument |
| Clear and numerous — you need to list them compactly without taking space | 04D · risk / win checklist — most compact format |

**05 · Takeaway — how explicit should the ask be?**

| If the close needs… | Use |
|---|---|
| Named decisions that each map to a specific owner — the reader needs to know exactly what they're saying yes to | 05A · decision chips — each chip names the decision and who approves it |
| The same, but the ask feels large and a confidence line reduces friction | 05C · decision chips + reassurance — adds a grounding qualifier |
| Minimal — the decision detail lives in the deck, this just sets the payoff | 05D · one-liner — reads in one breath and lands the key phrase |

**Header — how much space does context need?**

| If the document needs… | Use |
|---|---|
| Maximum density — the audience is time-constrained and every pixel counts | HdrA · inline — compact single row |
| Room to name the audience, the promise, and the context | HdrB · stacked — lockup above, title and meta below |

### Reference implementation

The canonical approved one-pager is `memory/clients/u-haul/engagements/2026-06-29-digital-experience-parity/uhaul-digital-experience-intelligence-v3.html`. Its recipe (`HdrB · TL;DR · 01B · 02A · 03A · 04A · 05A`) is a reference, not a default — it was right for that engagement's story. A different engagement needs a different recipe.

### Semantic color assignments (do not reassign)

| Content type | Token | Hex |
|---|---|---|
| Confirmed findings | `--guide` | `#1A7A70` |
| Open hypotheses | `--plan` | `#5E28E5` |
| Risks / instrumentation gaps | `--stakes` | `#C93FDB` |
| Problem statement | `--problem` | `#8B1DC0` |

---

## Accessibility requirements

Apply during build, not as a post-hoc pass.

- `aria-hidden="true"` on all decorative elements (wave backgrounds, stripe divs, dividers, `→` arrows)
- `role="list"` + `role="listitem"` on visual card groups that function as lists (stats, tiles, chips, phases, steps, decisions, cmap rows)
- `role="table"`, `role="row"`, `role="columnheader"`, `role="cell"` on ptable (01B)
- `role="note"` with `aria-label` on side-by-side comparison panels (h2h, split stakes)
- `aria-label` on `<section>` or use `aria-labelledby` pointing to the beat-name `id`
- Body text minimum 10px; eyebrow labels minimum 9px; stat labels minimum 9.5px
- Never white text on `#49C2B3` (brand teal, fails WCAG AA); use `rgba(255,255,255,0.8)` on dark backgrounds instead
