#!/usr/bin/env python3
"""
tools/pptx-generator.py — Insights Forge deck generator

Accepts a JSON spec and produces a branded .pptx using
Dynatrace_Brand_Insights-Forge.pptx as the template base.
All brand mechanics (layouts, fonts, master, footer) are handled
by the template. This tool fills in engagement-specific content.

DT Flow fonts are automatically installed from DTFlow/ on first run
so the output renders correctly in PowerPoint without any manual setup.

Usage:
    python3 tools/pptx-generator.py <spec.json> [output.pptx]
        Generate a deck. Output defaults to <spec-dir>/deck-YYYY-MM-DD.pptx

    python3 tools/pptx-generator.py --list-layouts
        Print all 64 named layouts in the template.

    python3 tools/pptx-generator.py --install-fonts
        Install DT Flow fonts from DTFlow/ to the system font directory
        (macOS: ~/Library/Fonts, Linux: ~/.fonts). Safe to run multiple
        times — skips fonts already installed.

Spec format:  tools/pptx-spec-example.json
"""

import sys
import json
import platform
import shutil
from datetime import date
from pathlib import Path
from pptx import Presentation

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE     = PROJECT_ROOT / "Dynatrace_Brand_Insights-Forge.pptx"
FONTS_DIR    = PROJECT_ROOT / "DTFlow"


# ── Font installation ──────────────────────────────────────────────────────

def _user_font_dir() -> Path | None:
    """Return the user font directory for the current OS, or None if unsupported."""
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Fonts"
    if system == "Linux":
        return Path.home() / ".fonts"
    return None


def ensure_dtflow_fonts(verbose: bool = True) -> int:
    """Install DT Flow fonts from DTFlow/ into the user font directory.

    Copies only fonts that are not already present.  Safe to call on
    every generator run — the check is fast and the copy only happens
    once.  Returns the number of fonts newly installed.
    """
    if not FONTS_DIR.exists():
        if verbose:
            print(f"  ⚠ DTFlow/ not found — skipping font install", file=sys.stderr)
        return 0

    font_dir = _user_font_dir()
    if font_dir is None:
        if verbose:
            print(f"  ⚠ Font auto-install not supported on {platform.system()}."
                  f"  Install DTFlow/*.otf manually.", file=sys.stderr)
        return 0

    font_dir.mkdir(parents=True, exist_ok=True)

    otf_files = sorted(FONTS_DIR.glob("*.otf"))
    if not otf_files:
        if verbose:
            print("  ⚠ No .otf files found in DTFlow/", file=sys.stderr)
        return 0

    installed = []
    for otf in otf_files:
        dest = font_dir / otf.name
        if not dest.exists():
            shutil.copy2(otf, dest)
            installed.append(otf.name)

    if installed:
        print(f"  ✓ Installed {len(installed)} DT Flow font(s) → {font_dir}")
        # Refresh font cache on Linux so apps can see the new fonts
        if platform.system() == "Linux":
            import subprocess
            subprocess.run(["fc-cache", "-fv"], capture_output=True)
    elif verbose:
        print(f"  ✓ DT Flow fonts already installed ({len(otf_files)} fonts in {font_dir})")

    return len(installed)


# ── Template helpers ───────────────────────────────────────────────────────

def load_template() -> Presentation:
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE}")
    return Presentation(str(TEMPLATE))


def list_layouts(prs: Presentation) -> list[str]:
    return [l.name for l in prs.slide_masters[0].slide_layouts]


def get_layout(prs: Presentation, name: str):
    for layout in prs.slide_masters[0].slide_layouts:
        if layout.name == name:
            return layout
    available = "\n  ".join(list_layouts(prs))
    raise ValueError(f"Layout '{name}' not found.\nAvailable:\n  {available}")


def clear_sample_slides(prs: Presentation) -> None:
    """Remove all sample slides from the template, keeping master + layouts."""
    sldIdLst = prs.slides._sldIdLst
    rId_attr = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    rIds = [el.get(rId_attr) for el in list(sldIdLst)]
    for rId in rIds:
        if rId:
            try:
                prs.part.drop_rel(rId)
            except KeyError:
                pass
    sldIdLst.clear()


def add_slide(prs: Presentation, layout_name: str):
    """Add a slide and return (slide, name_to_idx).

    name_to_idx maps each layout placeholder's semantic name (lowercase)
    to its stable placeholder format index. Filling by idx is reliable;
    filling by instance name is not (instance names differ from layout names).
    """
    layout = get_layout(prs, layout_name)
    slide = prs.slides.add_slide(layout)
    name_to_idx = {
        ph.name.lower().strip(): ph.placeholder_format.idx
        for ph in layout.placeholders
    }
    return slide, name_to_idx


# ── Placeholder fill helpers ───────────────────────────────────────────────

def _get_ph(slide, ph_name: str, name_to_idx: dict):
    """Return the placeholder matching ph_name, or None."""
    # Primary: look up idx from the layout's semantic name, then find by idx
    idx = name_to_idx.get(ph_name.lower().strip())
    if idx is not None:
        for ph in slide.placeholders:
            if ph.placeholder_format.idx == idx:
                return ph
    # Fallback: direct instance-name match
    for ph in slide.placeholders:
        if ph.name.lower().strip() == ph_name.lower().strip():
            return ph
    return None


def fill(slide, ph_name: str, text: str, n2i: dict) -> bool:
    """Set plain text on a named placeholder. Returns True if found."""
    ph = _get_ph(slide, ph_name, n2i)
    if ph is None:
        return False
    try:
        ph.text = str(text)
    except Exception as e:
        print(f"    ⚠ fill('{ph_name}'): {e}", file=sys.stderr)
    return True


def fill_bullets(slide, ph_name: str, items: list, n2i: dict) -> bool:
    """Fill a placeholder with a bulleted list. Returns True if found."""
    ph = _get_ph(slide, ph_name, n2i)
    if ph is None:
        return False
    if not items:
        return True
    try:
        tf = ph.text_frame
        tf.text = str(items[0])
        for item in items[1:]:
            p = tf.add_paragraph()
            p.text = str(item)
    except Exception as e:
        print(f"    ⚠ fill_bullets('{ph_name}'): {e}", file=sys.stderr)
    return True


def fill_first(slide, candidates: list[str], value, n2i: dict) -> bool:
    """Try placeholder names in order; fill the first one found."""
    for name in candidates:
        if _get_ph(slide, name, n2i) is not None:
            if isinstance(value, list):
                return fill_bullets(slide, name, value, n2i)
            return fill(slide, name, value, n2i)
    return False


def fill_content(slide, ph_name: str, value, n2i: dict) -> bool:
    """Fill a content placeholder — handles both str and list[str]."""
    if isinstance(value, list):
        return fill_bullets(slide, ph_name, value, n2i)
    return fill(slide, ph_name, str(value), n2i)


# ── Layout handlers ────────────────────────────────────────────────────────

def handle_title_slide(prs, spec):
    layout = spec.get("layout", "Title slide_1 speaker")
    slide, n = add_slide(prs, layout)
    # Layout has: title (idx 0), subtitle (idx 1), name 1 (idx 22/23), company 1 (idx 24)
    fill_first(slide, ["title", "Title 3"], spec.get("title", ""), n)
    fill_first(slide, ["subtitle"], spec.get("subtitle", ""), n)
    fill_first(slide, ["name 1"], spec.get("presenter_name", ""), n)
    fill_first(slide, ["company 1"], spec.get("presenter_company", ""), n)
    return slide


def handle_section_header(prs, spec):
    slide, n = add_slide(prs, "Section Header")
    fill_first(slide, ["Title 1", "title"], spec.get("title", ""), n)
    return slide


def handle_eyebrow_content(prs, spec):
    layout = spec.get("layout", "Title+content+eyebrow_left")
    slide, n = add_slide(prs, layout)
    fill_first(slide, ["title"],   spec.get("title", ""),   n)
    fill_first(slide, ["eyebrow"], spec.get("eyebrow", ""), n)
    fill_content(slide, "content placeholder", spec.get("content", []), n)
    return slide


def handle_title_content(prs, spec):
    layout = spec.get("layout", "Title+content_left")
    slide, n = add_slide(prs, layout)
    fill_first(slide, ["title"], spec.get("title", ""), n)
    fill_content(slide, "content placeholder", spec.get("content", []), n)
    return slide


def handle_icon_cards(prs, spec):
    cards = spec.get("cards", [])
    count = 4 if len(cards) >= 4 else 3
    if len(cards) < 3:
        print(f"  ⚠ handle_icon_cards: {len(cards)} card(s) provided; minimum layout is 3 cards. Padding empty.", file=sys.stderr)
    layout = spec.get("layout", f"{count} icon cards+title")
    slide, n = add_slide(prs, layout)
    fill_first(slide, ["title"], spec.get("title", ""), n)
    for i, card in enumerate(cards[:count], 1):
        fill_first(slide, [f"header {i}"],  card.get("header",  ""), n)
        fill_first(slide, [f"card {i}"],    card.get("body",    ""), n)
        fill_first(slide, [f"subcopy {i}"], card.get("subcopy", ""), n)
    return slide


def handle_text_columns(prs, spec):
    cols = spec.get("columns", [])
    count = max(2, min(len(cols), 6))
    if count not in (2, 3, 4, 6):
        print(f"  ⚠ handle_text_columns: {len(cols)}-column layout not supported (valid: 2, 3, 4, 6). Falling back to 3; column(s) {count+1}+ discarded.", file=sys.stderr)
        count = 3
    layout = spec.get("layout", f"{count} text columns")
    slide, n = add_slide(prs, layout)
    fill_first(slide, ["title"], spec.get("title", ""), n)
    for i, col in enumerate(cols[:count], 1):
        fill_first(slide, [f"header {i}"],  col.get("header",  ""), n)
        fill_first(slide, [f"card {i}"],    col.get("body",    ""), n)
        fill_first(slide, [f"subcopy {i}"], col.get("subcopy", ""), n)
    return slide


def handle_quote(prs, spec):
    slide, n = add_slide(prs, "Quote")
    fill_first(slide, ["title", "Title 1", "content placeholder"],
               spec.get("quote", ""), n)
    fill_first(slide, ["subtitle", "name 1", "company 1"],
               spec.get("attribution", ""), n)
    return slide


def handle_customer_story(prs, spec):
    layout = spec.get("layout", "Customer story")
    slide, n = add_slide(prs, layout)
    fill_first(slide, ["title", "Title 1"],                    spec.get("title", ""),   n)
    fill_content(slide, "content placeholder",                  spec.get("content", []), n)
    fill_first(slide, ["subtitle"],                             spec.get("subtitle", ""), n)
    return slide


def handle_blank(prs, spec):
    layout = spec.get("layout", "Blank_graphic")
    slide, _ = add_slide(prs, layout)
    return slide


def handle_thank_you(prs, spec):
    slide, _ = add_slide(prs, "Thank you slide")
    return slide


def handle_generic(prs, spec):
    """Fallback: add the slide and fill any explicitly listed placeholders."""
    layout_name = spec.get("layout", "Title+content_left")
    slide, n = add_slide(prs, layout_name)
    for ph_name, text in spec.get("placeholders", {}).items():
        fill_content(slide, ph_name, text, n)
    return slide


# ── Dispatch ───────────────────────────────────────────────────────────────

HANDLERS = {
    "Title Slide":              handle_title_slide,
    "Title slide_1 speaker":    handle_title_slide,
    "Title slide_2 speakers":   handle_title_slide,
    "Title slide_3 speakers":   handle_title_slide,
    "Title slide_4 speakers":   handle_title_slide,
    "Section Header":                            handle_section_header,
    "Title+content+eyebrow_left":                handle_eyebrow_content,
    "Title+content+eyebrow_centered":            handle_eyebrow_content,
    "Title+content+eyebrow_middle aligned_left": handle_eyebrow_content,
    "Title+content+eyebrow_middle aligned_centered": handle_eyebrow_content,
    "Title+content_left":                        handle_title_content,
    "Title+content_centered":                    handle_title_content,
    "1_Title+content_left_2column":              handle_title_content,
    "3 icon cards+title":   handle_icon_cards,
    "4 icon cards+title":   handle_icon_cards,
    "icon cards+title":     handle_icon_cards,
    "2 text columns":       handle_text_columns,
    "3 text columns":       handle_text_columns,
    "4 text columns":       handle_text_columns,
    "6 text columns":       handle_text_columns,
    "Quote":                handle_quote,
    "Customer story":       handle_customer_story,
    "Customer story_stats": handle_customer_story,
    "Customer story_quote": handle_customer_story,
    "Blank_graphic":        handle_blank,
    "Blank_black":          handle_blank,
    "Thank you slide":      handle_thank_you,
}


def dispatch(prs, spec: dict):
    layout = spec.get("layout", "")
    handler = HANDLERS.get(layout)
    if handler:
        return handler(prs, spec)
    for key, fn in HANDLERS.items():
        if layout.startswith(key):
            return fn(prs, spec)
    print(f"  ⚠ No handler for '{layout}' — using generic fallback", file=sys.stderr)
    return handle_generic(prs, spec)


# ── Generator ──────────────────────────────────────────────────────────────

def generate(spec_data: dict, output_path: Path) -> None:
    prs = load_template()
    clear_sample_slides(prs)

    slides_spec = spec_data.get("slides", [])
    if not slides_spec:
        print("Warning: spec contains no slides.", file=sys.stderr)

    failures = 0
    for i, slide_spec in enumerate(slides_spec):
        # Skip comment-only entries
        if set(slide_spec.keys()) <= {"_comment"}:
            continue
        layout = slide_spec.get("layout", "(none)")
        try:
            dispatch(prs, slide_spec)
            print(f"  ✓  [{i+1:2d}] {layout}")
        except Exception as e:
            print(f"  ✗  [{i+1:2d}] {layout} — {e}", file=sys.stderr)
            failures += 1

    if failures:
        print(f"\n⚠ {failures} slide(s) failed. Saving partial output.", file=sys.stderr)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))
    print(f"\nSaved → {output_path}")
    if failures:
        sys.exit(1)


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--list-layouts":
        prs = load_template()
        print(f"{'Index':>5}  Layout name")
        print(f"{'─'*5}  {'─'*45}")
        for i, name in enumerate(list_layouts(prs)):
            print(f"{i:5d}  {name}")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "--install-fonts":
        n = ensure_dtflow_fonts(verbose=True)
        if n == 0:
            print("No new fonts installed (already up to date).")
        return

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    if not spec_path.exists():
        print(f"Spec file not found: {spec_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(sys.argv[2]) if len(sys.argv) >= 3 \
        else spec_path.parent / f"deck-{date.today():%Y-%m-%d}.pptx"

    with open(spec_path, encoding="utf-8") as f:
        spec_data = json.load(f)

    ensure_dtflow_fonts()
    print(f"Template : {TEMPLATE.name}")
    print(f"Spec     : {spec_path}")
    print(f"Output   : {output_path}")
    print()
    generate(spec_data, output_path)


if __name__ == "__main__":
    main()
