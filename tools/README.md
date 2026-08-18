# Tools

This folder contains in-repo tools and their support files.

## What lives here

| File | Purpose |
|---|---|
| `pptx-generator.py` | Generates branded `.pptx` decks from a JSON spec against the Dynatrace template. Primary renderer for Phase 3 deck output. |
| `pptx-spec-example.json` | Annotated example spec showing all supported slide types and fields. Read this before writing a new deck spec. |
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
