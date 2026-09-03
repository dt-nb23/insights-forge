---
name: html-renderer
description: |
  Step 2 of the exec-onepager build. Takes the brand-humanizer-approved copy
  and the selected recipe, and produces the finished HTML file. References
  reference/layout-system.md for component CSS and HTML patterns.
---

# Step 2 — HTML build

Read this file at step 4 of the exec-onepager skill. The humanized copy is ready. The recipe is selected. Now build the HTML.

**Do not improvise CSS or invent new color values.** Every component has a defined pattern in `skills/exec-onepager/reference/layout-system.md`. Use those patterns exactly.

**Do not add text outside a component's defined slots.** No legends, footnotes, "Note:" callouts, "Source:" inline annotations, or free-standing paragraphs added outside the component's defined slots within section bodies. The only permitted prose extensions per section are the slots the layout system names: `beat-line` (optional one-line setup sentence before the component), `concurrency` (after 03A/03B/03D phase cards or steps), `tie-line` (after 01D stats), `claim-support` (inside 01A bold statement), `guide-thesis`/`pos-line`/`g-statement` (per 02 variant), `verdict` (04B single verdict sentence), `reassure` (05C reassurance line), `tk-qualifier` (05D optional qualifier sentence). If content does not fit in a defined slot, choose a different component variant — do not add supplemental text. All citations and source references go exclusively in `.foot-src` in the FtrB footer.

## File setup

**Output path:** Write the HTML to `<ENGAGEMENT_PATH>/<slug>-onepager.html` — inside the engagement folder, never the repo root or `html/`. Use a kebab-case name that reflects the client and engagement (e.g., `acme-api-latency-onepager.html`).

**Companion markdown:** Also write `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md` — a plain-text version of the content for the pptx-builder. The markdown companion carries only content (sections, bullets, numbers) — not CSS or HTML structure.

## HTML file structure

```html
<!DOCTYPE html>
<!-- Recipe: [recipe string] | Why: [rationale] -->
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>[Document title] | [Client name]</title>
<style>
  [font-face declarations]
  [reset + page frame]
  [:root token block]
  [component CSS for each component in the recipe]
  [[aria-hidden] rule]
  [print media query]
</style>
</head>
<body>
<main class="page">
  [components in recipe order]
</main>
</body>
</html>
```

## Step-by-step build procedure

### 1. Write the recipe comment

Line 2, immediately after `<!DOCTYPE html>`:
```html
<!-- Recipe: HdrX · TL;DR · 01X · 02X · 03X · 04X · 05X · FtrB | Why: [one sentence] -->
```

### 2. Copy the font-face block

From `reference/layout-system.md` — all six DTFlow weights. The HTML lives in the engagement folder, which is five directories below the repo root (`memory/clients/<client>/engagements/<dated-slug>/`), so every local asset path uses the five-up prefix:
- `../../../../../DTFlow/DTFlow-Light.otf`

(The sanitized reference file sits three levels deep under `skills/`, which is why it uses `../../../`. Count the directories for any other location; the linter's `DESIGN-ASSET` check fails the build if a font, wave, or lockup path does not resolve from the file's own directory.)

### 3. Copy the token block

Copy the full `:root {}` block from `reference/layout-system.md` verbatim. Do not modify any values.

### 4. Write page frame CSS

Copy the page frame block from `reference/layout-system.md`:
```css
*, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
body { background:var(--pagebg); font-family:var(--font); font-weight:300; color:var(--ink); -webkit-font-smoothing:antialiased; }
.page { width:960px; margin:22px auto; background:#fff; box-shadow:0 6px 30px rgba(12,22,38,0.14); }
.eyebrow { font-size:9px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; }
```

### 5. Write component CSS (recipe components only)

For each component code in the recipe, copy its CSS block from `reference/layout-system.md`. Only include CSS for components that are actually in this recipe. Do not include CSS for unused components.

Always include after the component CSS:
```css
[aria-hidden="true"] { pointer-events:none; }
@page { size:Letter portrait; margin:0.3in; }
@media print { body{background:#fff;} .page{margin:0 auto;box-shadow:none;zoom:0.65;} }
```

### 6. Build the HTML body in recipe order

Open with `<main class="page">`, close with `</main>`. Place components in the exact order specified by the recipe. For each component:

1. Use the HTML pattern from `reference/layout-system.md`
2. Insert the humanizer-approved copy into the template placeholders
3. Apply accessibility attributes as defined in `reference/layout-system.md`'s accessibility section

**Beat numbers follow the recipe order:**
- 01 → `id="b1"`, node text `01`
- 02 → `id="b2"`, node text `02`
- 03 → `id="b3"`, node text `03`
- 04 → `id="b4"`, node text `04`
- 05 → referenced as `id="b5"` in the takeaway

**Section accent colors are fixed to the section, not the content:**
- 01 node: `background:var(--problem)` — always
- 02 node: `background:var(--guide)` — always
- 03 node: `background:var(--plan)` — always
- 04 node: `background:var(--stakes)` — always
- Stats and stat numbers: use the token that matches the semantic meaning (guide for active/positive, setup for setup-phase numbers, plan for plan-phase numbers, navy for neutral)

### 7. Write the footer

Use the FtrB pattern from `reference/layout-system.md`. Include all externally sourced facts in `.foot-src` — each citation needs a URL and retrieval date. Format: `[Source name] — [domain] (retrieved [YYYY-MM-DD])`. Separate citations with ` · `.

## Asset paths

Both the wave background and the lockup resolve from `assets/` relative to the project root:

| Asset | Path from project root |
|---|---|
| Wave background | `assets/wave-bg.png` |
| Insights lockup (dark headers) | `assets/insights-lockup-rev.png` |

From the engagement folder (five levels deep) that is `../../../../../assets/wave-bg.png` and `../../../../../assets/insights-lockup-rev.png`.

**Do not generate or substitute these assets.** If `assets/wave-bg.png` is missing, flag it and stop rather than substituting another image.

## Semantic color assignments

Apply these consistently throughout all copy and component choices:

| Content type | CSS token | Hex |
|---|---|---|
| Confirmed findings | `--guide` | `#1A7A70` |
| Open hypotheses | `--plan` | `#5E28E5` |
| Risks / instrumentation gaps | `--stakes` | `#C93FDB` |
| Problem statement | `--problem` | `#8B1DC0` |

In the 04 · Stakes section: risk panel always uses `--problem` border / `--tint-mag` background; success panel always uses `--guide` border / `--tint-teal` background.

## Companion markdown

Write `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md` alongside the HTML. This file feeds the pptx-builder.

Structure it as:
```markdown
# [Document title] | [Client name]
*[Stakeholder name, role] · [Date]*

## TL;DR
[Summary sentence]
- Stat 1: [N] — [label]
- Stat 2: [N] — [label]
- Stat 3: [N] — [label]
- Stat 4: [N] — [label]

## 01 · [Problem section title]
[Content]

## 02 · [Guide section title]
[Content]

## 03 · [Plan section title]
[Content]

## 04 · [Stakes section title]
[Content]

## 05 · The ask
[Content]

---
*© 2026 Dynatrace, LLC. Confidential*
Sources: [...]
```

Record the recipe and color assignments in a front-matter comment at the top:
```markdown
<!--
Recipe: [recipe string]
Color: confirmed=guide, open=plan, risks=stakes, problem=problem
Wave: assets/wave-bg.png
-->
```

The pptx-builder reads this comment to stay visually consistent with the HTML.
