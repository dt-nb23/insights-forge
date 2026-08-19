# Tools

This folder contains in-repo tools and their support files.

## What lives here

| File | Purpose |
|---|---|
| `pptx-generator.py` | Generates branded `.pptx` decks from a JSON spec against the Dynatrace template. Primary renderer for Phase 3 deck output. |
| `pptx-spec-example.json` | Annotated example spec showing all supported slide types and fields. Read this before writing a new deck spec. |
| `onepager-lint.py` | Lints HTML one-pagers against the design system in `skills/exec-onepager/reference/layout-system.md` (canonical `:root` tokens, design-system color palette, Arial fallback, structural markers). Run after Phase 3 HTML build: `python3 tools/onepager-lint.py <file.html>`. |
| `conformance-check.py` | Workspace conformance: repo-rooted paths in skills/agents resolve, no concrete client names in the shared tier, every critique lens carries a Hard-exclusions block. Run after editing skills or agents: `python3 tools/conformance-check.py`. |
| `client-isolation-hook.sh` | PreToolUse hook wired in `.claude/settings.json`. Blocks Read/Write/Edit/NotebookEdit calls into a different client's `memory/clients/` folder than the active one (marker: `.claude/active-client`). |
| `seed-prompt-generator-bundle.py` | Unpacks/repacks the application source embedded in the Seed Prompt Generator's Claude Artifact bundle export (`html/`), so the form can be edited and re-bundled. |
| `requirements.txt` | Python package dependencies. Install with `pip install -r tools/requirements.txt`. |

## Using the deck generator

```bash
# Install dependencies once
pip install -r tools/requirements.txt

# Generate a deck from a JSON spec
python3 tools/pptx-generator.py <ENGAGEMENT_PATH>/deck-spec-YYYY-MM-DD.json

# Or specify an explicit output path
python3 tools/pptx-generator.py <spec.json> <output.pptx>

# List all available layout names in the template
python3 tools/pptx-generator.py --list-layouts

# Install DT Flow fonts (first-time setup, or when fonts are missing)
python3 tools/pptx-generator.py --install-fonts
```

Output defaults to `<spec-dir>/deck-YYYY-MM-DD.pptx` (alongside the spec file, inside the engagement folder).

### Wave background spec fields

Any slide can carry a dark-themed wave background. Add these fields to the slide's spec object:

| Field | Required | Values / notes |
|---|---|---|
| `wave_background` | Yes | `"wave-bg"` (cover/closing slides), `"wave-ask"` (decision-required slides), or a repo-relative path string |
| `wave_overlay_opacity` | No | `0.0`–`1.0`; default `0.80`. Use `0.65`–`0.70` for title-only slides, `0.80`–`0.85` for body-text slides |

The wave PNG is inserted at the bottom of the z-stack; the dark overlay sits above it; existing slide content (placeholders, text) renders on top of the overlay.

### Chart spec fields

Use `"layout": "Chart"` to generate a branded chart slide. `"Chart"` is a dispatch key, not a template layout name — the chart is placed on `Blank_graphic` unless the slide spec sets `slide_layout` to another real layout name. The `chart` object contains:

| Field | Required | Values / notes |
|---|---|---|
| `type` | No | `XL_CHART_TYPE` name: `BAR_CLUSTERED`, `COLUMN_CLUSTERED`, `LINE`, `PIE`, etc. Default `BAR_CLUSTERED` |
| `categories` | Yes | List of category label strings (omitting logs a warning and the slide is created without a chart) |
| `series` | Yes | List of `{"name": "...", "values": [...]}` objects (omitting logs a warning and the slide is created without a chart) |
| `left`, `top`, `width`, `height` | No | Position/size in EMUs. Omit for the default: 0.5in left / 1.5in top insets, slide width − 1.0in, slide height − 2.0in |

Brand series colors (Teal → Light blue → Royal blue → Purple → Violet → Magenta) are applied automatically, cycling if there are more than six series.

## Boundary that all tools must respect

This agent does not run live queries or execute production changes. Any tool added to this folder must respect that boundary:

- A tool may **read** from internal documentation, design files, or local artifacts.
- A tool may **render** outputs into formats the team will use (PPTX, PDF, Markdown).
- A tool may **fetch** reference material from approved external sources.
- A tool **must not execute DQL, SQL, or any query language against production telemetry or data warehouses**.
- A tool **must not push configuration, deploy code, or modify production state**.

## External reference allowlist

External documentation lookup is governed by [`skills/external-research/SKILL.md`](../skills/external-research/SKILL.md). The approved domains are:

- `https://docs.dynatrace.com/` — Dynatrace product documentation.
- `https://community.dynatrace.com/` — Dynatrace community threads.

Any other domain requires explicit user approval.
