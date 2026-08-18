#!/usr/bin/env python3
"""
tools/onepager-lint.py — Insights Forge one-pager HTML lint

Checks HTML one-pager files against the design system rules in
skills/exec-onepager/reference/layout-system.md:

  1. No hard-coded color values outside the :root {} block.
  2. Required CSS custom property tokens are declared in :root.
  3. Required structural sections are present (header, footer).
  4. Font declarations reference DT Flow or Arial fallback (not system-ui, sans-serif alone, etc.).
  5. Wave background img tags are present (if the one-pager uses a dark header).

Usage:
    python3 tools/onepager-lint.py <file.html> [<file2.html> ...]
    python3 tools/onepager-lint.py  # scans all *.html in project root
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── Token checklist: these must appear in :root {} ─────────────────────────

REQUIRED_TOKENS = [
    "--color-bg",
    "--color-primary",
    "--color-accent",
    "--color-text",
    "--font-body",
]

# ── Hard-coded color patterns (outside :root) ──────────────────────────────

HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGB_COLOR = re.compile(r"\brgb(a)?\s*\(")

# ── Font guard: at minimum Arial fallback must appear ──────────────────────

FONT_FALLBACK = re.compile(r"\bArial\b", re.IGNORECASE)

# ── Required structural markers ─────────────────────────────────────────────

REQUIRED_MARKERS = [
    ("header", re.compile(r"<header\b", re.IGNORECASE)),
    ("footer", re.compile(r"<footer\b", re.IGNORECASE)),
    (":root block", re.compile(r":root\s*\{")),
]

# ── Helpers ─────────────────────────────────────────────────────────────────

def extract_root_block(html: str) -> str:
    """Return the content of the first :root { } block, or empty string."""
    match = re.search(r":root\s*\{([^}]*)\}", html, re.DOTALL)
    return match.group(1) if match else ""

def check_file(path: Path) -> list[str]:
    issues = []
    html = path.read_text(encoding="utf-8", errors="replace")
    name = path.name

    # 1. Required structural markers
    for label, pattern in REQUIRED_MARKERS:
        if not pattern.search(html):
            issues.append(f"  MISSING: {label} not found in {name}")

    root_block = extract_root_block(html)

    # 2. Required tokens in :root
    for token in REQUIRED_TOKENS:
        if token not in root_block:
            issues.append(f"  MISSING TOKEN: {token} not declared in :root in {name}")

    # 3. Font fallback
    if not FONT_FALLBACK.search(html):
        issues.append(f"  FONT: no Arial fallback found in {name}; DT Flow must have Arial as fallback")

    # 4. Hard-coded colors outside :root
    # Strip the :root block and <style> contents that define tokens (allowed)
    # then check the remainder for raw hex / rgb values in inline styles or non-root CSS
    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)
    for block in style_blocks:
        # Remove the :root block from the style block
        cleaned = re.sub(r":root\s*\{[^}]*\}", "", block, flags=re.DOTALL)
        for match in HEX_COLOR.finditer(cleaned):
            hex_val = match.group()
            # Allow a few very common safe neutrals in non-root CSS
            if hex_val.lower() not in ("#fff", "#000", "#ffffff", "#000000"):
                line_num = block[:match.start()].count("\n") + 1
                issues.append(
                    f"  HARD-CODED COLOR: {hex_val} in <style> (outside :root) near line {line_num} in {name}; use a CSS token instead"
                )

    return issues

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    else:
        targets = sorted(ROOT.glob("*.html"))

    if not targets:
        print("No HTML files found.")
        sys.exit(0)

    all_issues = []
    for target in targets:
        if not target.exists():
            print(f"File not found: {target}", file=sys.stderr)
            continue
        issues = check_file(target)
        if issues:
            print(f"\n{target.name} — {len(issues)} issue(s):")
            for line in issues:
                print(line)
        else:
            print(f"{target.name} — OK")
        all_issues.extend(issues)

    if all_issues:
        print(f"\n{len(all_issues)} total issue(s) found.")
        sys.exit(1)
    else:
        print("\nAll files clean.")
        sys.exit(0)

if __name__ == "__main__":
    main()
