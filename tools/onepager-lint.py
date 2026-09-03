#!/usr/bin/env python3
"""
tools/onepager-lint.py — Insights Forge one-pager brand-GATE lint

Mechanically verifies the brand gate defined in
skills/exec-onepager/steps/3-brand-gate.md (backed by
memory/long-term/brand/brand-spec.md §6-8 and skills/brand-humanizer/SKILL.md)
against a one-pager HTML file. Gates 2 (plan fidelity) and 6 (handoff) are
judgment calls and stay manual; everything below is what a script can check.

Checked groups
  GATE1-FIT       headless-Chrome print renders to exactly one page
  GATE1-BUDGET    visible copy vs. the reference one-pager's character count
                  (skills/exec-onepager/reference/reference-onepager.html,
                  which fits one Letter page): more than 15% over is a WARN
                  that usually predicts overflow — the Chrome-free signal
                  when GATE1-FIT cannot run
  GATE3-DASH      no em/en dashes in visible copy (.foot-src excluded — its
                  required citation format itself mandates an em dash)
  GATE3-PHRASE    disallowed phrasings ("Dynatrace Server", "plugin", ...)
  GATE3-TM        first mention of Dynatrace/OneAgent/Smartscape/Grail
                  carries the registered-trademark symbol; "Davis" never does
  GATE3-CASE      sentence-case headings (.beat-name, .mast-title, .p-name,
                  .p-eyebrow, .d-name); brand product names, months,
                  acronyms, and common third-party product names (Jira,
                  ServiceNow, Microsoft Teams, ...) are allowed mid-heading;
                  pass --proper-noun for anything else (the client name)
  GATE3-COMMA     missing serial comma (heuristic)
  GATE3-AI        AI-writing lexicon survivors (delve, crucial, leverage, ...)
  GATE3-SPELL     British spellings (analyse, behaviour, optimisation, ...)
  GATE4-*         accessibility: aria-hidden on decoration, list/table/note
                  roles, section labels, .beat labelledby resolution,
                  font-size minimums, white-on-teal contrast
  GATE5-SRC       .foot-src citation format "[Source] — domain (retrieved
                  YYYY-MM-DD)" with a real, non-future date
  GATE5-DOMAIN    cited domains appear in the action plan (--action-plan)
  GATE5-FOOTER    footer carries "© <current-year> Dynatrace, LLC." and
                  "Confidential"
  DESIGN-TOKEN    every var(--x) referenced is declared in :root
  DESIGN-PALETTE  colors resolve to the layout-system.md palette (rgba with
                  any alpha is allowed when its RGB triplet is on palette)
  DESIGN-FONT     Arial fallback present ('DTFlow', Arial, sans-serif)
  DESIGN-STRUCT   header, footer, and :root block present
  DESIGN-ASSET    every local asset reference (<img src>, CSS url()) resolves
                  from the HTML file's own directory — catches a wrong ../
                  depth, the usual breakage now that one-pagers live five
                  levels deep in the engagement folder

Severities
  FAIL  mechanically certain violation
  WARN  heuristic — confirm by hand before "fixing"
  INFO  context only (e.g. em/rem font sizes are not statically verifiable)

Every finding is one grep-able line:
  GATE3-DASH FAIL <file>:<line> — <message>
Line 0 means the finding applies to the file as a whole.

Usage:
    python3 tools/onepager-lint.py <file.html> [<file2.html> ...]
    python3 tools/onepager-lint.py                 # scans *.html and html/*.html
    python3 tools/onepager-lint.py --proper-noun Forge --proper-noun Keptn ...
    python3 tools/onepager-lint.py --action-plan <ENGAGEMENT_PATH>/action-plan.md ...

Gate 1 needs a Chrome binary: $ONEPAGER_CHROME, then Google Chrome / Chrome
Canary in /Applications, then chromium / google-chrome on PATH.

Exit codes:
  0  no FAILs
  1  one or more FAILs
  2  usage error (bad flag, missing input file, missing --action-plan file)
  3  gate 1 unverifiable (no Chrome / render failed); all other groups
     were still checked and reported
"""

import argparse
import datetime
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYOUT_SYSTEM = ROOT / "skills" / "exec-onepager" / "reference" / "layout-system.md"
REFERENCE_ONEPAGER = ROOT / "skills" / "exec-onepager" / "reference" / "reference-onepager.html"
# GATE1-BUDGET: visible-copy character count allowed relative to the reference
# one-pager (which fits one Letter page at the print zoom). Above this ratio the
# page almost always overflows; below it only a render can confirm the fit.
BUDGET_TOLERANCE = 1.15

# ── Patterns ────────────────────────────────────────────────────────────────

HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGBA_COLOR = re.compile(r"\brgba?\s*\(([^)]*)\)")
TOKEN_DECL = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;}]+)")
VAR_REF = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)\s*(?:,[^)]*)?\)")
FONT_FALLBACK = re.compile(r"\bArial\b", re.IGNORECASE)

REQUIRED_MARKERS = [
    ("header", re.compile(r"<header\b", re.IGNORECASE)),
    ("footer", re.compile(r"<footer\b", re.IGNORECASE)),
    (":root block", re.compile(r":root\s*\{")),
]

# Gate 3b — disallowed phrasings (brand-spec.md §7), word-boundary, any case.
BANNED_PHRASES = [
    (re.compile(r"\bdynatrace\s+server\b", re.I), '"Dynatrace Server" — use "Dynatrace Cluster"'),
    (re.compile(r"\bplugin\b", re.I), '"plugin" — use "extension"'),
    (re.compile(r"\badd-on\b", re.I), '"add-on" — use "extension"'),
    (re.compile(r"\bout-of-the-box\b", re.I), '"out-of-the-box" — use "ready-made"'),
    (re.compile(r"\bdynatrace\s+interface\b", re.I), '"Dynatrace interface" — use "Dynatrace web UI"'),
]

# Gate 3c — registered trademarks needing ® on first visible mention.
TRADEMARKS = ["Dynatrace", "OneAgent", "Smartscape", "Grail"]

# Gate 3d — heading classes the gate names, and the proper-noun allowlist
# (brand-spec.md §7 product terms; acronyms and months are matched by pattern).
HEADING_CLASSES = {"beat-name", "mast-title", "p-name", "p-eyebrow", "d-name"}
BRAND_WORDS = {
    "Dynatrace", "OneAgent", "Smartscape", "Grail", "AppEngine",
    "AutomationEngine", "ActiveGate", "Hub", "SaaS", "Keptn", "Davis",
}
# Third-party product and platform names that legitimately keep their capital
# mid-heading ("Approve Jira and Microsoft Teams integration"). Client names
# are never hard-coded here — pass them with --proper-noun.
COMMON_PROPER_NOUNS = {
    "Jira", "ServiceNow", "Slack", "Microsoft", "Teams", "PagerDuty",
    "Opsgenie", "GitHub", "GitLab", "Bitbucket", "Jenkins", "Azure",
    "Google", "Kubernetes", "OpenShift", "OpenTelemetry", "Salesforce",
    "Snowflake", "Splunk", "Datadog", "Grafana", "Prometheus", "Terraform",
    "Ansible", "Okta", "Confluence", "Notebooks", "Workflows", "Guardian",
}
# Allowed only in their product-name pairing: word -> required neighbor.
BRAND_PAIR_AFTER = {"Intelligence": "Dynatrace", "Monitoring": "Full-Stack"}
BRAND_PAIR_BEFORE = {"Full-Stack": "Monitoring"}
MONTHS = {
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
}
ACRONYM = re.compile(r"[A-Z]{2,}$")
HEADING_WORD = re.compile(r"[A-Za-z][A-Za-z0-9'’\-]*")

# Gate 3e — missing serial comma (heuristic).
SERIAL_COMMA = re.compile(r"\w+, \w+ (and|or) \w+")

# Gate 3f — AI-writing lexicon (brand-humanizer §7/§23; longest match first).
AI_LEXICON = re.compile(
    r"\b(stands as a testament|in order to|due to the fact that|cutting-edge"
    r"|delve|crucial|leverage|foster|showcase|underscores|underscore"
    r"|landscape|testament|seamless|robust)\b", re.I)

# Gate 3g — British spellings (brand-spec §6: American English).
BRITISH = re.compile(
    r"\b(analyse|behaviour|optimisation|colour|organisation|prioritise"
    r"|utilisation)\w*\b", re.I)

# Gate 4 class sets.
DECORATIVE_CLASSES = {"stripe", "foot-bar", "grad-bar", "mast-divider", "arrow", "proof-div"}
LIST_CLASSES = {"stats", "tiles", "chips", "phases", "steps", "decisions"}

# Gate 5a — citation segment format: [Source] — domain (retrieved YYYY-MM-DD)
SRC_SEGMENT = re.compile(r".+ — (\S+\.\S+) \(retrieved (\d{4})-(\d{2})-(\d{2})\)", re.S)

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}

# Design — local asset references inside CSS url(...) values.
ASSET_URL = re.compile(r"url\(\s*['\"]?([^'\")]+?)['\"]?\s*\)")
REMOTE_PREFIXES = ("http://", "https://", "data:", "//", "#", "blob:")

TEAL = "#49c2b3"
WHITE_VALUES = {"#fff", "#ffffff", "white"}


# ── Minimal DOM ─────────────────────────────────────────────────────────────

class Node:
    __slots__ = ("tag", "attrs", "classes", "children", "parent", "line")

    def __init__(self, tag, attrs, line):
        self.tag = tag
        self.attrs = dict(attrs)
        self.classes = set((self.attrs.get("class") or "").split())
        self.children = []   # Node and TextNode, in document order
        self.parent = None
        self.line = line


class TextNode:
    __slots__ = ("text", "line", "parent")

    def __init__(self, text, line, parent):
        self.text = text
        self.line = line
        self.parent = parent


class DocParser(HTMLParser):
    """Builds a tolerant element tree; captures <style> contents separately.

    Visible-text checks read TextNodes (entities decoded by convert_charrefs;
    attributes and comments never become TextNodes). CSS checks read
    self.styles (raw, undecoded — HTMLParser keeps style/script in CDATA mode).
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#document", [], 1)
        self.stack = [self.root]
        self.styles = []  # (start_line, css_text)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.getpos()[0])
        node.parent = self.stack[-1]
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, attrs, self.getpos()[0])
        node.parent = self.stack[-1]
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        parent = self.stack[-1]
        if parent.tag == "style":
            self.styles.append((self.getpos()[0], data))
            return
        if parent.tag == "script":
            return
        parent.children.append(TextNode(data, self.getpos()[0], parent))


def iter_nodes(node):
    for child in node.children:
        if isinstance(child, Node):
            yield child
            yield from iter_nodes(child)


def iter_text(node, _under_hidden_tags=("style", "script")):
    """Yield TextNodes under node in document order (style/script never
    contain TextNodes by construction)."""
    for child in node.children:
        if isinstance(child, TextNode):
            yield child
        else:
            yield from iter_text(child)


def element_text(node):
    return "".join(t.text for t in iter_text(node))


def has_ancestor_class(node, cls):
    cur = node.parent
    while cur is not None:
        if isinstance(cur, Node) and cls in cur.classes:
            return True
        cur = cur.parent
    return False


def line_of(text_node, offset):
    return text_node.line + text_node.text[:offset].count("\n")


# ── CSS helpers ─────────────────────────────────────────────────────────────

def mask_preserving_lines(text, pattern, flags=0):
    """Blank out pattern matches with spaces so offsets and lines survive."""
    return re.sub(pattern,
                  lambda m: re.sub(r"[^\n]", " ", m.group(0)),
                  text, flags=flags)


def mask_css_comments(css):
    return mask_preserving_lines(css, r"/\*.*?\*/", re.DOTALL)


def mask_root_blocks(css):
    return mask_preserving_lines(css, r":root\s*\{[^{}]*\}", re.DOTALL)


def parse_css_rules(css, base_line):
    """Yield (selector, declarations_text, decl_start_offset, line) for leaf
    rules. Grouping rules (@media, ...) yield only their leaf children."""
    rules = []
    stack = []  # [selector, open_index, has_nested_rules]
    last = 0
    for i, ch in enumerate(css):
        if ch == "{":
            stack.append([css[last:i].strip(), i, False])
            last = i + 1
        elif ch == "}":
            if stack:
                sel, start, nested = stack.pop()
                if not nested:
                    line = base_line + css[:start].count("\n")
                    rules.append((sel, css[start + 1:i], start + 1, line))
                if stack:
                    stack[-1][2] = True
            last = i + 1
        elif ch == ";":
            last = i + 1
    return rules


def parse_decls(decl_text):
    out = []
    for part in decl_text.split(";"):
        if ":" in part:
            prop, _, val = part.partition(":")
            out.append((prop.strip().lower(), val.strip()))
    return out


def hex_to_triplet(hex_val):
    v = hex_val.lstrip("#")
    if len(v) in (3, 4):
        v = "".join(c * 2 for c in v[:3])
    if len(v) >= 6:
        try:
            return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            return None
    return None


def rgba_triplet(args_text):
    nums = re.findall(r"[\d.]+", args_text)
    if len(nums) < 3:
        return None
    try:
        return tuple(int(float(n)) for n in nums[:3])
    except ValueError:
        return None


def load_palette():
    """Allowed RGB triplets from every color literal in layout-system.md,
    plus white and black. Returns None when the file is missing."""
    if not LAYOUT_SYSTEM.exists():
        return None
    text = LAYOUT_SYSTEM.read_text(encoding="utf-8")
    triplets = set()
    for h in HEX_COLOR.findall(text):
        t = hex_to_triplet(h)
        if t:
            triplets.add(t)
    for m in RGBA_COLOR.finditer(text):
        t = rgba_triplet(m.group(1))
        if t:
            triplets.add(t)
    triplets.add((255, 255, 255))
    triplets.add((0, 0, 0))
    return triplets


# ── Issue container ─────────────────────────────────────────────────────────

class Report:
    def __init__(self, path):
        self.path = path
        self.issues = []  # (code, severity, line, message)

    def add(self, code, severity, line, message):
        self.issues.append((code, severity, line, message))

    def emit(self):
        counts = {"FAIL": 0, "WARN": 0, "INFO": 0}
        for code, sev, line, msg in self.issues:
            counts[sev] += 1
            print(f"{code} {sev} {self.path}:{line} — {msg}")
        return counts


# ── Gate 1 — one-page constraint ────────────────────────────────────────────

def find_chrome():
    candidates = []
    env = os.environ.get("ONEPAGER_CHROME")
    if env:
        candidates.append(env)
    candidates += [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    ]
    for cand in candidates:
        if Path(cand).is_file() and os.access(cand, os.X_OK):
            return cand
    for name in ("chromium", "google-chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


def gate1_page_count(chrome, path):
    """Return (page_count, error). error is a string when unverifiable."""
    with tempfile.TemporaryDirectory(prefix="onepager-lint-") as tmp:
        pdf = Path(tmp) / "out.pdf"
        cmd = [chrome, "--headless", "--disable-gpu",
               f"--print-to-pdf={pdf}", "--no-pdf-header-footer",
               path.resolve().as_uri()]
        try:
            proc = subprocess.run(cmd, capture_output=True, timeout=120)
        except (subprocess.TimeoutExpired, OSError) as exc:
            return None, f"chrome did not complete: {exc}"
        if not pdf.exists():
            tail = (proc.stderr or b"").decode(errors="replace").strip().splitlines()
            detail = f" ({tail[-1]})" if tail else ""
            return None, f"chrome produced no PDF{detail}"
        pages = len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))
        if pages == 0:
            return None, "could not count pages in the rendered PDF"
        return pages, None


def check_gate1(report, chrome, path):
    """Returns True when the gate was verifiable."""
    if chrome is None:
        report.add("GATE1-FIT", "INFO", 0,
                   "gate 1 unverifiable — run the manual print preview "
                   "(no Chrome found; set $ONEPAGER_CHROME)")
        return False
    pages, err = gate1_page_count(chrome, path)
    if err:
        report.add("GATE1-FIT", "INFO", 0,
                   f"gate 1 unverifiable — run the manual print preview ({err})")
        return False
    if pages > 1:
        report.add("GATE1-FIT", "FAIL", 0,
                   f"renders to {pages} pages; the one-pager must fit one page "
                   f"— cut content, do not compress type or padding")
    return True


def content_chars(doc):
    """Visible-copy character count: every text node except the sources
    block (fixed-format citations) and the <title> (not rendered on the
    page), whitespace-collapsed."""
    total = 0
    for tn in iter_text(doc.root):
        if has_ancestor_class(tn, "foot-src"):
            continue
        if isinstance(tn.parent, Node) and tn.parent.tag == "title":
            continue
        total += len(" ".join(tn.text.split()))
    return total


def load_reference_budget():
    """Character count of the reference one-pager, or None if it is missing."""
    if not REFERENCE_ONEPAGER.exists():
        return None
    doc = DocParser()
    doc.feed(REFERENCE_ONEPAGER.read_text(encoding="utf-8", errors="replace"))
    doc.close()
    chars = content_chars(doc)
    return chars or None


def check_budget(report, doc, ref_chars, gate1_verifiable):
    """GATE1-BUDGET — the Chrome-free fit signal. Never a FAIL: a character
    count is a proxy, and only a render proves the page."""
    if ref_chars is None:
        report.add("GATE1-BUDGET", "INFO", 0,
                   f"{REFERENCE_ONEPAGER.relative_to(ROOT)} not found — "
                   f"content-budget check skipped")
        return
    chars = content_chars(doc)
    ratio = chars / ref_chars
    if ratio > BUDGET_TOLERANCE:
        report.add("GATE1-BUDGET", "WARN", 0,
                   f"visible copy is {chars} characters, {int((ratio - 1) * 100)}% "
                   f"over the reference one-pager ({ref_chars}) — this much text "
                   f"usually overflows one Letter page; cut before trusting any "
                   f"render, and never compress type or padding to fit")
    elif not gate1_verifiable:
        report.add("GATE1-BUDGET", "INFO", 0,
                   f"visible copy is {chars} characters ({int(ratio * 100)}% of "
                   f"the reference one-pager) — inside the content budget, but "
                   f"only the manual print preview confirms the one-page fit")


# ── Gate 3 — brand text rules ───────────────────────────────────────────────

def visible_text_nodes(doc):
    return list(iter_text(doc.root))


def check_dashes(report, text_nodes):
    for tn in text_nodes:
        if has_ancestor_class(tn, "foot-src"):
            continue  # the required citation format itself mandates an em dash
        for m in re.finditer(r"[—–]", tn.text):
            which = "em dash (U+2014)" if m.group() == "—" else "en dash (U+2013)"
            report.add("GATE3-DASH", "FAIL", line_of(tn, m.start()),
                       f"{which} in visible text — replace with a period, "
                       f"comma, colon, or parentheses")


def check_banned_phrases(report, text_nodes):
    for tn in text_nodes:
        for pattern, msg in BANNED_PHRASES:
            for m in pattern.finditer(tn.text):
                report.add("GATE3-PHRASE", "FAIL", line_of(tn, m.start()),
                           f"disallowed phrasing {msg}")


def check_trademarks(report, text_nodes):
    # Build one document-order string with an offset -> (node, local) map.
    pieces, parts, offset = [], [], 0
    for tn in text_nodes:
        pieces.append((offset, tn))
        parts.append(tn.text)
        offset += len(tn.text) + 1
    doc_text = "\n".join(parts)

    def locate(pos):
        node = pieces[0][1] if pieces else None
        start = 0
        for piece_start, tn in pieces:
            if piece_start > pos:
                break
            node, start = tn, piece_start
        return line_of(node, min(pos - start, len(node.text))) if node else 0

    for mark in TRADEMARKS:
        for m in re.finditer(rf"\b{mark}\b", doc_text):
            following = doc_text[m.end():m.end() + 6]
            if mark == "Dynatrace" and following.startswith(", LLC"):
                continue  # legal-entity name in the required footer boilerplate
            if not following.startswith("®"):
                report.add("GATE3-TM", "FAIL", locate(m.start()),
                           f"first visible mention of {mark} must be {mark}® "
                           f"(later mentions may drop the symbol)")
            break  # only the first product mention is checked

    for m in re.finditer(r"\bDavis®", doc_text):
        report.add("GATE3-TM", "FAIL", locate(m.start()),
                   'do not add ® to "Davis" — brand-spec.md flags the mark '
                   "as unconfirmed")


def check_heading_case(report, doc, proper_nouns):
    extra = set(proper_nouns)

    def allowed(word, prev_word, next_word):
        if word in BRAND_WORDS or word in MONTHS or word in extra:
            return True
        if word in COMMON_PROPER_NOUNS:
            return True
        if ACRONYM.fullmatch(word):
            return True
        if BRAND_PAIR_AFTER.get(word) == prev_word:
            return True
        if BRAND_PAIR_BEFORE.get(word) == next_word:
            return True
        return False

    for node in iter_nodes(doc.root):
        if not (node.classes & HEADING_CLASSES):
            continue
        text = " ".join(element_text(node).split())
        if not text:
            continue
        words = HEADING_WORD.findall(text)
        shown = text if len(text) <= 60 else text[:57] + "..."
        run = []  # consecutive non-initial capitalized words not on allowlist

        def flush(run):
            if len(run) >= 2:
                report.add("GATE3-CASE", "FAIL", node.line,
                           f'heading "{shown}" is title case: consecutive '
                           f"capitalized words {', '.join(run)} — gate 3 "
                           f"requires sentence case")
            elif len(run) == 1:
                report.add("GATE3-CASE", "WARN", node.line,
                           f'heading "{shown}" capitalizes "{run[0]}" '
                           f"mid-heading — if it is a proper noun, pass "
                           f"--proper-noun {run[0]}")

        for i, word in enumerate(words):
            if i == 0:
                continue
            prev_word = words[i - 1]
            next_word = words[i + 1] if i + 1 < len(words) else ""
            if word[0].isupper() and not allowed(word, prev_word, next_word):
                run.append(word)
            else:
                flush(run)
                run = []
        flush(run)


def check_serial_comma(report, text_nodes):
    for tn in text_nodes:
        for m in SERIAL_COMMA.finditer(tn.text):
            report.add("GATE3-COMMA", "WARN", line_of(tn, m.start()),
                       f'possible missing serial comma: "{m.group()}" — '
                       f'brand-spec §6 wants "owner, timeframe, and cost"')


def check_ai_lexicon(report, text_nodes):
    for tn in text_nodes:
        for m in AI_LEXICON.finditer(tn.text):
            report.add("GATE3-AI", "WARN", line_of(tn, m.start()),
                       f'AI-writing lexicon: "{m.group()}" — confirm it '
                       f"survived the brand-humanizer pre-pass on purpose")


def check_british_spelling(report, text_nodes):
    for tn in text_nodes:
        for m in BRITISH.finditer(tn.text):
            report.add("GATE3-SPELL", "WARN", line_of(tn, m.start()),
                       f'British spelling: "{m.group()}" — brand-spec §6 '
                       f"requires American English")


# ── Gate 4 — accessibility ──────────────────────────────────────────────────

def check_aria_hidden(report, doc):
    for node in iter_nodes(doc.root):
        decorative = bool(node.classes & DECORATIVE_CLASSES) or \
            (node.tag == "div" and "cmap-head" in node.classes)
        if decorative and node.attrs.get("aria-hidden") != "true":
            cls = next(iter(node.classes & (DECORATIVE_CLASSES | {"cmap-head"})))
            report.add("GATE4-HIDDEN", "FAIL", node.line,
                       f'decorative <{node.tag} class="{cls}"> needs '
                       f'aria-hidden="true"')


def check_list_roles(report, doc):
    for node in iter_nodes(doc.root):
        if not (node.classes & LIST_CLASSES):
            continue
        cls = next(iter(node.classes & LIST_CLASSES))
        if node.attrs.get("role") != "list":
            report.add("GATE4-LIST", "FAIL", node.line,
                       f'.{cls} group needs role="list"')
        for child in node.children:
            if isinstance(child, Node) and child.attrs.get("role") != "listitem":
                report.add("GATE4-LIST", "FAIL", child.line,
                           f'child <{child.tag}> of .{cls} needs role="listitem"')


def check_table_roles(report, doc):
    for node in iter_nodes(doc.root):
        if "ptable" not in node.classes:
            continue
        if node.attrs.get("role") != "table":
            report.add("GATE4-TABLE", "FAIL", node.line,
                       '.ptable needs role="table"')
        roles = {d.attrs.get("role") for d in iter_nodes(node)}
        for needed in ("row", "columnheader", "cell"):
            if needed not in roles:
                report.add("GATE4-TABLE", "FAIL", node.line,
                           f'.ptable has no descendant with role="{needed}"')


def check_note_roles(report, doc):
    for node in iter_nodes(doc.root):
        for cls in ("stake", "h2h-side"):
            if cls in node.classes:
                if node.attrs.get("role") != "note":
                    report.add("GATE4-NOTE", "FAIL", node.line,
                               f'.{cls} panel needs role="note"')
                if not node.attrs.get("aria-label"):
                    report.add("GATE4-NOTE", "FAIL", node.line,
                               f".{cls} panel needs an aria-label")


def check_section_labels(report, doc):
    for node in iter_nodes(doc.root):
        if node.tag != "section":
            continue
        if "tldr" in node.classes and not node.attrs.get("aria-label"):
            report.add("GATE4-LABEL", "FAIL", node.line,
                       "section.tldr needs an aria-label")
        if "takeaway" in node.classes and not (
                node.attrs.get("aria-label") or node.attrs.get("aria-labelledby")):
            report.add("GATE4-LABEL", "FAIL", node.line,
                       "section.takeaway needs aria-label or aria-labelledby")


def check_beat_labels(report, doc):
    ids = {n.attrs.get("id") for n in iter_nodes(doc.root) if n.attrs.get("id")}
    for node in iter_nodes(doc.root):
        if node.tag != "section" or "beat" not in node.classes:
            continue
        ref = node.attrs.get("aria-labelledby")
        if not ref:
            report.add("GATE4-BEAT", "FAIL", node.line,
                       "section.beat needs aria-labelledby pointing at its "
                       ".beat-name id")
            continue
        for token in ref.split():
            if token not in ids:
                report.add("GATE4-BEAT", "FAIL", node.line,
                           f'section.beat aria-labelledby="{token}" is '
                           f"dangling — no element has that id")


def iter_css_sources(doc):
    """Yield (selector_context, declarations, line) for every style-block leaf
    rule and every style="" attribute. selector_context is the CSS selector
    for rules, or the element's class string for inline styles."""
    for start_line, css in doc.styles:
        masked = mask_css_comments(css)
        for sel, decl_text, _off, line in parse_css_rules(masked, start_line):
            yield sel, parse_decls(decl_text), line
    for node in iter_nodes(doc.root):
        style = node.attrs.get("style")
        if style:
            context = node.attrs.get("class", node.tag)
            yield context, parse_decls(mask_css_comments(style)), node.line


def check_font_sizes(report, doc):
    saw_relative = False
    for sel, decls, line in iter_css_sources(doc):
        for prop, val in decls:
            if prop not in ("font-size", "font"):
                continue
            for m in re.finditer(r"(\d+(?:\.\d+)?)(px|em|rem)\b", val):
                size, unit = float(m.group(1)), m.group(2)
                if unit != "px":
                    saw_relative = True
                    continue
                if size < 9:
                    report.add("GATE4-FONT", "FAIL", line,
                               f"font-size {m.group(0)} in rule '{sel}' — "
                               f"gate 4 floor is 9px (labels) / 10px (body)")
                elif size < 10 and not re.search(
                        r"eyebrow|lbl|label|foot|meta|head|num|days", sel, re.I):
                    report.add("GATE4-FONT", "WARN", line,
                               f"font-size {m.group(0)} in rule '{sel}' — "
                               f"9px is only allowed for eyebrow/label/footer "
                               f"text; confirm this is one")
    if saw_relative:
        report.add("GATE4-FONT", "INFO", 0,
                   "em/rem font sizes present — minimum-size floor is not "
                   "statically verifiable; check rendered output")


def check_white_on_teal(report, doc):
    tokens = {}
    for _line, css in doc.styles:
        for m in re.finditer(r":root\s*\{([^{}]*)\}", mask_css_comments(css), re.S):
            for name, val in TOKEN_DECL.findall(m.group(1)):
                tokens[name] = val.strip()

    def resolve(value, depth=0):
        if depth > 3:
            return value
        new = VAR_REF.sub(lambda m: tokens.get(m.group(1), m.group(0)), value)
        return resolve(new, depth + 1) if new != value else new

    for sel, decls, line in iter_css_sources(doc):
        has_teal_bg = any(prop.startswith("background")
                          and TEAL in resolve(val).lower()
                          for prop, val in decls)
        has_white_text = any(prop == "color"
                             and resolve(val).strip().lower() in WHITE_VALUES
                             for prop, val in decls)
        if has_teal_bg and has_white_text:
            report.add("GATE4-CONTRAST", "WARN", line,
                       f"rule '{sel}' sets white text on {TEAL} brand teal — "
                       f"fails WCAG AA; use rgba(255,255,255,0.8) on a dark "
                       f"background instead")


# ── Gate 5 — sources block and footer ───────────────────────────────────────

def check_sources(report, doc, action_plan_text):
    today = datetime.date.today()
    found_block = False
    for node in iter_nodes(doc.root):
        if "foot-src" not in node.classes:
            continue
        # Only the outermost .foot-src container counts.
        if has_ancestor_class(node, "foot-src"):
            continue
        found_block = True
        text = " ".join(element_text(node).split())
        for segment in re.split(r"\s*·\s*", text):
            segment = segment.strip()
            if not segment:
                continue
            m = SRC_SEGMENT.fullmatch(segment)
            if not m:
                report.add("GATE5-SRC", "FAIL", node.line,
                           f'citation "{segment}" does not match '
                           f'"[Source] — domain (retrieved YYYY-MM-DD)"')
                continue
            domain, y, mo, d = m.group(1), *map(int, m.group(2, 3, 4))
            try:
                retrieved = datetime.date(y, mo, d)
            except ValueError:
                report.add("GATE5-SRC", "FAIL", node.line,
                           f'citation "{segment}" has an impossible retrieval '
                           f"date {m.group(2)}-{m.group(3)}-{m.group(4)}")
                continue
            if retrieved > today:
                report.add("GATE5-SRC", "FAIL", node.line,
                           f'citation "{segment}" has a future retrieval date '
                           f"{retrieved.isoformat()}")
                continue
            if action_plan_text is not None and \
                    domain.lower() not in action_plan_text:
                report.add("GATE5-DOMAIN", "WARN", node.line,
                           f"cited domain {domain} does not appear in the "
                           f"action plan — gate 5 forbids new external claims "
                           f"in Phase 3")
    if not found_block:
        report.add("GATE5-SRC", "INFO", 0,
                   "no .foot-src block found — confirm the one-pager uses no "
                   "externally sourced facts")


def check_footer(report, doc):
    year = datetime.date.today().year
    required = f"© {year} Dynatrace, LLC."
    footers = [n for n in iter_nodes(doc.root) if n.tag == "footer"]
    if not footers:
        footers = [n for n in iter_nodes(doc.root) if "footer" in n.classes]
    if not footers:
        report.add("GATE5-FOOTER", "FAIL", 0,
                   f'no footer element — one is required, carrying '
                   f'"{required}" and "Confidential"')
        return
    text = " ".join(" ".join(element_text(f).split()) for f in footers)
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    if required not in text:
        report.add("GATE5-FOOTER", "FAIL", footers[0].line,
                   f'footer must contain "{required}" (current year) — '
                   f"brand-spec §8")
    if "Confidential" not in text:
        report.add("GATE5-FOOTER", "FAIL", footers[0].line,
                   'footer must contain the "Confidential" classification '
                   "marker — brand-spec §8")


# ── Design group — tokens, palette, fonts, structure, assets ────────────────

def check_assets(report, doc, path):
    """DESIGN-ASSET — every local <img src> / CSS url() must resolve from the
    file's own directory."""
    base = path.resolve().parent
    refs = []
    for node in iter_nodes(doc.root):
        if node.tag in ("img", "source"):
            attr = node.attrs.get("src")
        elif node.tag == "link":
            attr = node.attrs.get("href")
        else:
            attr = None
        if attr:
            refs.append((attr, node.line))
        style = node.attrs.get("style")
        if style:
            for m in ASSET_URL.finditer(style):
                refs.append((m.group(1), node.line))
    for start_line, css in doc.styles:
        masked = mask_css_comments(css)
        for m in ASSET_URL.finditer(masked):
            refs.append((m.group(1), start_line + masked[:m.start()].count("\n")))

    seen = set()
    for ref, line in refs:
        ref = (ref or "").strip()
        if not ref or ref.startswith(REMOTE_PREFIXES):
            continue
        clean = ref.split("?", 1)[0].split("#", 1)[0]
        if not clean or clean in seen:
            continue
        seen.add(clean)
        if not (base / clean).exists():
            report.add("DESIGN-ASSET", "FAIL", line,
                       f"local asset {clean} does not resolve from the HTML "
                       f"file's directory — check the ../ depth (engagement "
                       f"folders are five levels below the repo root)")


def check_design(report, doc, html, palette):
    for label, pattern in REQUIRED_MARKERS:
        if not pattern.search(html):
            report.add("DESIGN-STRUCT", "FAIL", 0, f"{label} not found")

    all_css = "\n".join(css for _line, css in doc.styles)
    inline_css = "\n".join(n.attrs.get("style", "")
                           for n in iter_nodes(doc.root) if n.attrs.get("style"))
    if not FONT_FALLBACK.search(all_css + "\n" + inline_css):
        report.add("DESIGN-FONT", "FAIL", 0,
                   "no Arial fallback found — the canonical stack is "
                   "'DTFlow', Arial, sans-serif")

    # Every var(--x) referenced must be declared in :root.
    declared = set()
    for _line, css in doc.styles:
        for m in re.finditer(r":root\s*\{([^{}]*)\}", mask_css_comments(css), re.S):
            declared.update(name for name, _val in TOKEN_DECL.findall(m.group(1)))
    seen = set()
    sources = [(line, mask_css_comments(css)) for line, css in doc.styles]
    sources += [(n.line, n.attrs.get("style", ""))
                for n in iter_nodes(doc.root) if n.attrs.get("style")]
    for base_line, css in sources:
        for m in VAR_REF.finditer(css):
            token = m.group(1)
            if token not in declared and token not in seen:
                seen.add(token)
                report.add("DESIGN-TOKEN", "FAIL",
                           base_line + css[:m.start()].count("\n"),
                           f"var({token}) is referenced but {token} is not "
                           f"declared in :root")

    # Palette: colors outside :root must resolve to the layout-system palette.
    if palette is None:
        report.add("DESIGN-PALETTE", "INFO", 0,
                   f"{LAYOUT_SYSTEM.relative_to(ROOT)} not found — palette "
                   f"check skipped")
        return
    for base_line, css in sources:
        masked = mask_root_blocks(css)
        for m in HEX_COLOR.finditer(masked):
            triplet = hex_to_triplet(m.group())
            if triplet and triplet not in palette:
                report.add("DESIGN-PALETTE", "WARN",
                           base_line + masked[:m.start()].count("\n"),
                           f"{m.group()} is not in the layout-system.md "
                           f"palette — use a design-system value or token, or "
                           f"confirm the deviation is deliberate")
        for m in RGBA_COLOR.finditer(masked):
            triplet = rgba_triplet(m.group(1))
            if triplet and triplet not in palette:
                report.add("DESIGN-PALETTE", "WARN",
                           base_line + masked[:m.start()].count("\n"),
                           f"{m.group().strip()} has an off-palette RGB "
                           f"triplet — any alpha is fine, but the base color "
                           f"must be a palette value")


# ── Main ────────────────────────────────────────────────────────────────────

def lint_file(path, display, chrome, palette, proper_nouns, action_plan_text,
              ref_chars=None):
    """Returns (counts_by_severity, gate1_verifiable)."""
    report = Report(display)
    html = path.read_text(encoding="utf-8", errors="replace")
    doc = DocParser()
    doc.feed(html)
    doc.close()

    gate1_ok = check_gate1(report, chrome, path)
    if path.resolve() != REFERENCE_ONEPAGER.resolve():
        check_budget(report, doc, ref_chars, gate1_ok)

    text_nodes = visible_text_nodes(doc)
    check_dashes(report, text_nodes)
    check_banned_phrases(report, text_nodes)
    check_trademarks(report, text_nodes)
    check_heading_case(report, doc, proper_nouns)
    check_serial_comma(report, text_nodes)
    check_ai_lexicon(report, text_nodes)
    check_british_spelling(report, text_nodes)

    check_aria_hidden(report, doc)
    check_list_roles(report, doc)
    check_table_roles(report, doc)
    check_note_roles(report, doc)
    check_section_labels(report, doc)
    check_beat_labels(report, doc)
    check_font_sizes(report, doc)
    check_white_on_teal(report, doc)

    check_sources(report, doc, action_plan_text)
    check_footer(report, doc)

    check_design(report, doc, html, palette)
    check_assets(report, doc, path)

    counts = report.emit()
    print(f"{display}: {counts['FAIL']} FAIL, {counts['WARN']} WARN, "
          f"{counts['INFO']} INFO")
    return counts, gate1_ok


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="onepager-lint.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", metavar="file.html",
                        help="one-pager HTML files (default: *.html and "
                             "html/*.html in the project root)")
    parser.add_argument("--proper-noun", action="append", default=[],
                        metavar="WORD",
                        help="extra proper noun allowed mid-heading by the "
                             "sentence-case check (repeatable)")
    parser.add_argument("--action-plan", metavar="PATH",
                        help="engagement action-plan.md; cited domains absent "
                             "from it are warned about (gate 5)")
    args = parser.parse_args(argv)

    if args.files:
        targets = [Path(p) for p in args.files]
    else:
        targets = sorted(ROOT.glob("*.html")) + sorted((ROOT / "html").glob("*.html"))

    missing = [t for t in targets if not t.is_file()]
    if missing:
        for t in missing:
            print(f"File not found: {t}", file=sys.stderr)
        sys.exit(2)
    if not targets:
        print("No HTML files found.")
        sys.exit(0)

    action_plan_text = None
    if args.action_plan:
        plan_path = Path(args.action_plan)
        if not plan_path.is_file():
            print(f"--action-plan file not found: {plan_path}", file=sys.stderr)
            sys.exit(2)
        action_plan_text = plan_path.read_text(
            encoding="utf-8", errors="replace").lower()

    chrome = find_chrome()
    palette = load_palette()
    ref_chars = load_reference_budget()
    totals = {"FAIL": 0, "WARN": 0, "INFO": 0}
    gate1_unverifiable = False
    for target in targets:
        counts, verifiable = lint_file(
            target, str(target), chrome, palette,
            args.proper_noun, action_plan_text, ref_chars)
        for key in totals:
            totals[key] += counts[key]
        if not verifiable:
            gate1_unverifiable = True

    print(f"Totals: {totals['FAIL']} FAIL, {totals['WARN']} WARN, "
          f"{totals['INFO']} INFO across {len(targets)} file(s)")
    if totals["FAIL"]:
        sys.exit(1)
    if gate1_unverifiable:
        sys.exit(3)
    sys.exit(0)


if __name__ == "__main__":
    main()
