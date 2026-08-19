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
from pptx.chart.data import ChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from lxml import etree

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE     = PROJECT_ROOT / "Dynatrace_Brand_Insights-Forge.pptx"
FONTS_DIR    = PROJECT_ROOT / "DTFlow"
ASSETS_DIR   = PROJECT_ROOT / "assets"

# Brand constants — brand-spec.md §2 (theme colors) and §5 (chart series)
_OVERLAY_COLOR = RGBColor(0x1A, 0x24, 0x40)   # Deep navy #1A2440

BRAND_CHART_COLORS = [
    RGBColor(0x49, 0xC2, 0xB3),  # Teal      — Accent 1
    RGBColor(0x3B, 0xAC, 0xF0),  # Light blue — Accent 2
    RGBColor(0x19, 0x66, 0xFF),  # Royal blue — Accent 3
    RGBColor(0x5E, 0x28, 0xE5),  # Purple    — Accent 4
    RGBColor(0x8D, 0x1C, 0xDC),  # Violet    — Accent 5
    RGBColor(0xC9, 0x3F, 0xDB),  # Magenta   — Accent 6
]

# Named wave asset shortcuts (files live in assets/)
WAVE_ASSETS = {
    "wave-bg":  ASSETS_DIR / "wave-bg.png",   # cover / closing
    "wave-ask": ASSETS_DIR / "wave-ask.png",  # decision-required accent slides
}


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


# ── Visual helpers — wave backgrounds, overlays, chart colors ─────────────

def _slide_dimensions(slide):
    """Return (width, height) in EMUs from the presentation."""
    prs = slide.part.package.presentation
    return prs.slide_width, prs.slide_height


def _move_shape_in_spTree(slide, shape, position: int) -> None:
    """Reposition a shape element in the slide's spTree to control z-order.

    position=2 is just after the bg/bgRef elements (bottom of the stack).
    """
    spTree = slide.shapes._spTree
    spTree.remove(shape._element)
    spTree.insert(position, shape._element)


def _set_fill_alpha(shape, opacity: float) -> None:
    """Set opacity on a shape whose fill is already set to solid().

    opacity: 0.0 (transparent) → 1.0 (fully opaque).
    OOXML alpha is expressed in thousandths-of-a-percent: 100% = 100000.
    """
    alpha_val = str(int(opacity * 100000))
    spPr = shape._element.spPr
    solidFill = spPr.find(".//" + qn("a:solidFill"))
    if solidFill is None:
        return
    # Try srgbClr first, then sysClr / schemeClr
    for tag in (qn("a:srgbClr"), qn("a:sysClr"), qn("a:schemeClr")):
        clr = solidFill.find(tag)
        if clr is not None:
            # Remove any existing alpha child, then add a fresh one
            for existing in clr.findall(qn("a:alpha")):
                clr.remove(existing)
            alpha_elem = etree.SubElement(clr, qn("a:alpha"))
            alpha_elem.set("val", alpha_val)
            return


def add_wave_background(slide, wave: str, overlay_opacity: float = 0.80) -> None:
    """Insert a wave PNG as a full-slide background with a dark overlay.

    wave: a key from WAVE_ASSETS ("wave-bg", "wave-ask") or a path string.
    overlay_opacity: 0.0–1.0. Default 0.80 (body-text dark slides).
                     Use 0.65–0.70 for title-only dark slides (cover, closing).
                     Use 0.80–0.85 for dark slides with body text.

    Z-order after this call (bottom → top):
        [0] spTree background elements (<p:bg>, <p:bgRef>)
        [1] wave PNG picture
        [2] dark overlay rectangle
        [3+] all existing slide content shapes (placeholders etc.)
    """
    slide_w, slide_h = _slide_dimensions(slide)

    # Resolve the wave asset path
    if wave in WAVE_ASSETS:
        wave_path = WAVE_ASSETS[wave]
    else:
        wave_path = Path(wave)
        if not wave_path.is_absolute():
            wave_path = PROJECT_ROOT / wave_path

    if not wave_path.exists():
        print(f"  ⚠ wave asset not found: {wave_path} — skipping wave background",
              file=sys.stderr)
        return

    # 1. Wave PNG — inserted last so we can move it immediately
    pic = slide.shapes.add_picture(str(wave_path), 0, 0, slide_w, slide_h)
    _move_shape_in_spTree(slide, pic, 2)  # just above bg/bgRef

    # 2. Dark overlay — full-slide rectangle with semi-transparency
    # Use a textbox as the rectangle primitive (cleanest in python-pptx)
    from pptx.util import Emu
    overlay = slide.shapes.add_textbox(Emu(0), Emu(0), slide_w, slide_h)
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = _OVERLAY_COLOR
    overlay.line.fill.background()  # no border
    _set_fill_alpha(overlay, overlay_opacity)
    _move_shape_in_spTree(slide, overlay, 3)  # just above the wave image


def apply_brand_chart_colors(chart) -> None:
    """Apply Dynatrace brand series colors (Accent 1–6) to every series.

    Removes the Office theme color reference so the explicit RGB wins
    regardless of what theme is embedded in the template.
    """
    for i, series in enumerate(chart.series):
        color = BRAND_CHART_COLORS[i % len(BRAND_CHART_COLORS)]
        try:
            series.format.fill.solid()
            series.format.fill.fore_color.rgb = color

            # Clear the theme color reference (<c:spPr><a:solidFill><a:schemeClr>)
            # so the explicit srgbClr we just wrote is not overridden by the theme.
            spPr = series._element.find(qn("c:spPr"))
            if spPr is not None:
                for sf in spPr.findall(".//" + qn("a:solidFill")):
                    for sc in sf.findall(qn("a:schemeClr")):
                        sf.remove(sc)
        except Exception as e:
            print(f"  ⚠ apply_brand_chart_colors series {i}: {e}", file=sys.stderr)


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


def handle_chart(prs, spec):
    """Add a slide with a branded chart built from spec data.

    Spec keys:
        layout        — slide layout name (default "Blank_graphic")
        title         — optional slide title (filled into the title placeholder)
        chart         — dict with:
            type          — XL_CHART_TYPE name string (default "BAR_CLUSTERED")
            categories    — list of category labels
            series        — list of {name, values} dicts
            left, top     — position in EMUs (default: left-aligned with some margin)
            width, height — size in EMUs (default: most of the slide)
    """
    layout = spec.get("layout", "Blank_graphic")
    slide, n = add_slide(prs, layout)

    if spec.get("title"):
        fill_first(slide, ["title", "Title 1", "Title 3"], spec["title"], n)

    chart_spec = spec.get("chart")
    if not chart_spec:
        print("  ⚠ handle_chart: no 'chart' key in spec — slide added but empty", file=sys.stderr)
        return slide

    # Resolve chart type — fall back to BAR_CLUSTERED on unknown strings
    type_name = chart_spec.get("type", "BAR_CLUSTERED").upper()
    chart_type = getattr(XL_CHART_TYPE, type_name, None)
    if chart_type is None:
        print(f"  ⚠ Unknown chart type '{type_name}' — falling back to BAR_CLUSTERED",
              file=sys.stderr)
        chart_type = XL_CHART_TYPE.BAR_CLUSTERED

    # Build ChartData
    chart_data = ChartData()
    categories = chart_spec.get("categories", [])
    chart_data.categories = categories
    for s in chart_spec.get("series", []):
        chart_data.add_series(s.get("name", ""), s.get("values", []))

    # Default position/size: small insets on all four sides (inches → EMUs)
    slide_w, slide_h = _slide_dimensions(slide)
    default_left   = Inches(0.5)
    default_top    = Inches(1.5)
    default_width  = slide_w - Inches(1.0)
    default_height = slide_h - Inches(2.0)

    x  = Emu(chart_spec["left"])   if "left"   in chart_spec else default_left
    y  = Emu(chart_spec["top"])    if "top"    in chart_spec else default_top
    cx = Emu(chart_spec["width"])  if "width"  in chart_spec else default_width
    cy = Emu(chart_spec["height"]) if "height" in chart_spec else default_height

    graphic_frame = slide.shapes.add_chart(chart_type, x, y, cx, cy, chart_data)
    apply_brand_chart_colors(graphic_frame.chart)
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
    "Chart":                handle_chart,
    "Thank you slide":      handle_thank_you,
}


def dispatch(prs, spec: dict):
    layout = spec.get("layout", "")
    handler = HANDLERS.get(layout)
    if handler:
        slide = handler(prs, spec)
    else:
        for key, fn in HANDLERS.items():
            if layout.startswith(key):
                slide = fn(prs, spec)
                break
        else:
            print(f"  ⚠ No handler for '{layout}' — using generic fallback", file=sys.stderr)
            slide = handle_generic(prs, spec)

    # Apply wave background after the slide's content is placed
    if slide is not None and spec.get("wave_background"):
        wave = spec["wave_background"]
        opacity = float(spec.get("wave_overlay_opacity", 0.80))
        add_wave_background(slide, wave, opacity)

    return slide


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
