#!/usr/bin/env python3
"""
tools/conformance-check.py — Insights Forge workspace conformance check

Checks:
  1. Repo-rooted file paths referenced in skill/agent files resolve.
     Only paths anchored at a known top-level directory are checked —
     bare filenames (current-context.md), engagement-relative paths, and
     domains (docs.dynatrace.com) are not repo references.
  2. No concrete client names appear in shared-tier files
     (memory/long-term/, skills/). The documented placeholder client
     'acme-corp' is allowed.
  3. Every critique lens agent (.claude/agents/*-lens.md) contains a
     "Hard exclusions" block. Non-lens sub-agents (e.g. the doc-freshness
     checker) are exempt.

Exit code 0 = clean. Exit code 1 = violations found (lists them).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── Check 1: referenced paths resolve ─────────────────────────────────────

SCAN_DIRS = ["skills", ".claude/agents"]
# Match backtick-quoted paths that look like local repo paths (no <placeholders>);
# leading '.' admits .claude/... references
PATH_RE = re.compile(r"`([a-z_\-\.][a-zA-Z0-9_/\-\.]+\.[a-z]+)`")
TEMPLATE_SKIP = re.compile(r"<[A-Z_]+>")
# Only paths anchored at a real top-level repo directory count as repo references
REPO_ROOTS = ("skills/", "memory/", "tools/", "docs/", ".claude/",
              "assets/", "html/", "plans/", "DTFlow/")
# Documented example paths that intentionally do not exist in the repo
EXAMPLE_PATH_RE = re.compile(r"memory/clients/(?!_template/)")

def check_paths():
    violations = []
    for scan_dir in SCAN_DIRS:
        for md in (ROOT / scan_dir).rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            for match in PATH_RE.finditer(text):
                ref = match.group(1)
                if TEMPLATE_SKIP.search(ref):
                    continue  # skip template placeholders like <ENGAGEMENT_PATH>
                if not ref.startswith(REPO_ROOTS):
                    continue  # bare filename, domain, or engagement-relative path
                if EXAMPLE_PATH_RE.match(ref):
                    continue  # example client paths (client folders are created at runtime)
                resolved = ROOT / ref
                if not resolved.exists():
                    violations.append(f"  MISSING PATH: {md.relative_to(ROOT)} → {ref}")
    return violations

# ── Check 2: no client names in shared tier ────────────────────────────────

SHARED_DIRS = ["memory/long-term", "skills"]
# Match concrete client paths like memory/clients/<name>/ where <name> is not a placeholder
CLIENT_PATH_RE = re.compile(r"memory/clients/(?!_template/)([a-z][a-z0-9\-]+)/")
# The documented placeholder client used in examples throughout the skills
PLACEHOLDER_CLIENTS = {"acme-corp", "client-name", "that-client-name"}

def check_no_client_names_in_shared():
    violations = []
    for scan_dir in SHARED_DIRS:
        for f in (ROOT / scan_dir).rglob("*"):
            if not f.is_file():
                continue
            if f.suffix not in (".md", ".py", ".json", ".html"):
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
            for match in CLIENT_PATH_RE.finditer(text):
                client = match.group(1)
                if client in PLACEHOLDER_CLIENTS:
                    continue
                violations.append(
                    f"  CLIENT NAME IN SHARED: {f.relative_to(ROOT)} contains '{client}'"
                )
    return violations

# ── Check 3: all agent files have Hard exclusions block ────────────────────

AGENTS_DIR = ROOT / ".claude" / "agents"

def check_agent_exclusions():
    violations = []
    # Only critique lenses receive engagement dispatches that must honor
    # out-of-scope exclusions; utility sub-agents (freshness checker) are exempt.
    for agent_file in sorted(AGENTS_DIR.glob("*-lens.md")):
        text = agent_file.read_text(encoding="utf-8")
        if "Hard exclusions" not in text and "out-of-scope exclusions" not in text.lower():
            violations.append(
                f"  MISSING EXCLUSIONS BLOCK: {agent_file.relative_to(ROOT)}"
            )
    return violations

# ── Main ───────────────────────────────────────────────────────────────────

def main():
    all_violations = []

    print("Check 1: referenced paths resolve...")
    v = check_paths()
    all_violations.extend(v)
    print(f"  {len(v)} violation(s).")

    print("Check 2: no client names in shared tier...")
    v = check_no_client_names_in_shared()
    all_violations.extend(v)
    print(f"  {len(v)} violation(s).")

    print("Check 3: agent files contain exclusions block...")
    v = check_agent_exclusions()
    all_violations.extend(v)
    print(f"  {len(v)} violation(s).")

    if all_violations:
        print(f"\n{len(all_violations)} conformance violation(s) found:\n")
        for line in all_violations:
            print(line)
        sys.exit(1)
    else:
        print("\nAll checks passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
