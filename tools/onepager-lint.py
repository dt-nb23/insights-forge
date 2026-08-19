#!/usr/bin/env python3
"""
tools/onepager-lint.py — Insights Forge one-pager HTML lint

Checks HTML one-pager files against the design system rules in
skills/exec-onepager/reference/layout-system.md:

  1. Required structural sections are present (header, footer, :root block).
  2. The canonical :root tokens from layout-system.md are all declared
     (the design system says to copy the :root block verbatim).
  3. Font declarations include the Arial fallback ('DTFlow', Arial, sans-serif).
  4. No color values outside the design system's palette. Any hex value that
     appears in layout-system.md (in :root or in component CSS) is allowed;
     anything else is flagged as an off-palette color.

Usage:
    python3 tools/onepager-lint.py <file.html> [<file2.html> ...]
    python3 tools/onepager-lint.py  # scans all *.html in project root

Exit code 0 = all named files exist and are clean.
Exit code 1 = violations found, or a named file does not exist.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYOUT_SYSTEM = ROOT / "skills" / "exec-onepager" / "reference" / "layout-system.md"

HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGBA_COLOR = re.compile(r"\brgba?\s*\([^)]*\)")
TOKEN_DECL = re.compile(r"(--[a-z0-9\-]+)\s*:")

# ── Design-system palette, parsed from layout-system.md ────────────────────

def load_design_system():
    """Return (required_tokens, allowed_hex, allowed_rgba) from layout-system.md.

    required_tokens: every custom property declared in the canonical :root block.
    allowed_hex/allowed_rgba: every color literal anywhere in layout-system.md —
    the design system's component CSS legitimately uses hex values outside :root,
    so the lint allows exactly that palette and nothing else.
    """
    if not LAYOUT_SYSTEM.exists():
        print(f"WARNING: {LAYOUT_SYSTEM.relative_to(ROOT)} not found — "
              f"token and palette checks skipped.", file=sys.stderr)
        return [], None, None

    text = LAYOUT_SYSTEM.read_text(encoding="utf-8")
    required_tokens = TOKEN_DECL.findall(_richest_root_block(text))
    allowed_hex = {h.lower() for h in HEX_COLOR.findall(text)}
    # Always-safe neutrals
    allowed_hex |= {"#fff", "#000", "#ffffff", "#000000"}
    allowed_rgba = {re.sub(r"\s+", "", r).lower() for r in RGBA_COLOR.findall(text)}
    return required_tokens, allowed_hex, allowed_rgba


REQUIRED_MARKERS = [
    ("header", re.compile(r"<header\b", re.IGNORECASE)),
    ("footer", re.compile(r"<footer\b", re.IGNORECASE)),
    (":root block", re.compile(r":root\s*\{")),
]

FONT_FALLBACK = re.compile(r"\bArial\b", re.IGNORECASE)

# ── Helpers ─────────────────────────────────────────────────────────────────

def _richest_root_block(text: str) -> str:
    """Return the contents of the :root block with the most token declarations.

    Prose like "copy the `:root {}` block" can produce empty first matches, so
    the block that actually declares tokens wins.
    """
    candidates = re.findall(r":root\s*\{([^}]*)\}", text, re.DOTALL)
    if not candidates:
        return ""
    return max(candidates, key=lambda c: len(TOKEN_DECL.findall(c)))


def mask_root_blocks(css: str) -> str:
    """Replace :root { } block contents with spaces, preserving offsets/lines."""
    def _mask(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    return re.sub(r":root\s*\{[^}]*\}", _mask, css, flags=re.DOTALL)


def check_file(path: Path, required_tokens, allowed_hex, allowed_rgba) -> list[str]:
    issues = []
    html = path.read_text(encoding="utf-8", errors="replace")
    name = path.name

    # 1. Required structural markers
    for label, pattern in REQUIRED_MARKERS:
        if not pattern.search(html):
            issues.append(f"  MISSING: {label} not found in {name}")

    # 2. Canonical :root tokens (layout-system.md says copy the block verbatim)
    declared = set(TOKEN_DECL.findall(_richest_root_block(html)))
    for token in required_tokens:
        if token not in declared:
            issues.append(f"  MISSING TOKEN: {token} not declared in :root in {name}")

    # 3. Font fallback
    if not FONT_FALLBACK.search(html):
        issues.append(f"  FONT: no Arial fallback found in {name}; "
                      f"the canonical stack is 'DTFlow', Arial, sans-serif")

    # 4. Off-palette colors (anywhere in <style>, outside :root).
    # Skipped when the design system file is missing (allowed sets are None).
    if allowed_hex is None or allowed_rgba is None:
        return issues
    for style_match in re.finditer(r"<style[^>]*>(.*?)</style>", html,
                                   re.DOTALL | re.IGNORECASE):
        block = style_match.group(1)
        masked = mask_root_blocks(block)  # offsets preserved → stable line numbers
        for match in HEX_COLOR.finditer(masked):
            hex_val = match.group().lower()
            if hex_val not in allowed_hex:
                line_num = block[:match.start()].count("\n") + 1
                issues.append(
                    f"  OFF-PALETTE COLOR: {match.group()} in <style> near line "
                    f"{line_num} of the style block in {name}; not in the "
                    f"layout-system.md palette — use a design-system value or token"
                )
        for match in RGBA_COLOR.finditer(masked):
            rgba_val = re.sub(r"\s+", "", match.group()).lower()
            if rgba_val not in allowed_rgba:
                line_num = block[:match.start()].count("\n") + 1
                issues.append(
                    f"  OFF-PALETTE COLOR: {match.group()} in <style> near line "
                    f"{line_num} of the style block in {name}; not in the "
                    f"layout-system.md palette — use a design-system value or token"
                )

    return issues

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    if args:
        targets = [Path(p) for p in args]
    else:
        targets = sorted(ROOT.glob("*.html"))

    if not targets:
        print("No HTML files found.")
        sys.exit(0)

    required_tokens, allowed_hex, allowed_rgba = load_design_system()

    all_issues = []
    missing_files = 0
    for target in targets:
        if not target.exists():
            print(f"File not found: {target}", file=sys.stderr)
            missing_files += 1
            continue
        issues = check_file(target, required_tokens, allowed_hex, allowed_rgba)
        if issues:
            print(f"\n{target.name} — {len(issues)} issue(s):")
            for line in issues:
                print(line)
        else:
            print(f"{target.name} — OK")
        all_issues.extend(issues)

    if all_issues or missing_files:
        print(f"\n{len(all_issues)} total issue(s) found"
              + (f"; {missing_files} file(s) not found." if missing_files else "."))
        sys.exit(1)
    else:
        print("\nAll files clean.")
        sys.exit(0)

if __name__ == "__main__":
    main()
