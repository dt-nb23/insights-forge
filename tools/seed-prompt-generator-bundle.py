#!/usr/bin/env python3
"""Unpack/pack the Component source embedded in a Claude Artifact bundle export.

The Seed Prompt Generator's .html files are Claude Artifact bundle exports:
a small harness plus an asset dictionary, with the actual application source
sitting as a single JSON-escaped string inside a
<script type="__bundler/template"> block. This tool extracts that string to
a readable file for editing, and re-inserts an edited version to produce a
new bundle.
"""
import argparse
import json
import re
import sys

TEMPLATE_OPEN = '<script type="__bundler/template">'
TEMPLATE_CLOSE = '</script>'


def find_template_line(lines):
    for i, line in enumerate(lines):
        if line.strip() == TEMPLATE_OPEN:
            if lines[i + 2].strip() != TEMPLATE_CLOSE:
                raise ValueError(
                    f"Expected {TEMPLATE_CLOSE!r} on line {i + 3}, found {lines[i + 2]!r}. "
                    "Bundle structure has changed since this tool was written."
                )
            return i + 1
    raise ValueError(f"No {TEMPLATE_OPEN!r} line found in {sys.argv}.")


def unpack(bundle_path, out_path):
    with open(bundle_path, encoding='utf-8') as f:
        lines = f.readlines()
    idx = find_template_line(lines)
    decoded = json.loads(lines[idx])
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(decoded)
    print(f"Unpacked {bundle_path!r} line {idx + 1} -> {out_path!r} ({len(decoded)} chars)")


def pack(bundle_path, src_path, out_path):
    with open(bundle_path, encoding='utf-8') as f:
        lines = f.readlines()
    idx = find_template_line(lines)
    with open(src_path, encoding='utf-8') as f:
        src = f.read()
    encoded = json.dumps(src)
    # The browser's HTML tokenizer scans for a literal `</script` sequence
    # inside ANY <script> element's raw text — including this one, which is
    # "just data" to us but not to the tokenizer. A literal `</script>`
    # anywhere in the decoded source (there are many, e.g. from nested
    # <style>/<script> tags in the app's own markup) would prematurely close
    # this wrapping <script type="__bundler/template"> tag and corrupt the
    # file. Escaping the slash keeps it valid JSON while breaking the match.
    encoded = re.sub(r'</(script)', r'<\\/\1', encoded, flags=re.IGNORECASE)
    lines[idx] = encoded + '\n'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Packed {src_path!r} into {bundle_path!r} line {idx + 1} -> {out_path!r}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='cmd', required=True)

    up = sub.add_parser('unpack', help='Extract the Component source to a readable file')
    up.add_argument('bundle_path')
    up.add_argument('out_path')

    pk = sub.add_parser('pack', help='Re-insert an edited Component source into a new bundle')
    pk.add_argument('bundle_path', help='Original bundle to use as the shell/asset source')
    pk.add_argument('src_path', help='Edited, readable Component source file')
    pk.add_argument('out_path', help='Path to write the new bundle file')

    args = p.parse_args()
    if args.cmd == 'unpack':
        unpack(args.bundle_path, args.out_path)
    elif args.cmd == 'pack':
        pack(args.bundle_path, args.src_path, args.out_path)


if __name__ == '__main__':
    main()
