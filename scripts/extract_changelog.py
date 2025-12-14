#!/usr/bin/env python3
"""Extract a changelog entry for the given version."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"
ENTRY_RE = re.compile(r"^## \[(?P<version>.+?)\].*$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract changelog entry for a version")
    parser.add_argument("version", type=str, help="Version to extract (e.g. 1.1.0)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    text = CHANGELOG.read_text(encoding="utf-8")
    match = ENTRY_RE.search(text)
    start = None
    end = None
    while match:
        if match.group("version") == args.version:
            start = match.start()
            break
        match = ENTRY_RE.search(text, match.end())
    if start is None:
        raise SystemExit(f"Version {args.version} not found in {CHANGELOG}")

    next_match = ENTRY_RE.search(text, start + 1)
    end = next_match.start() if next_match else len(text)
    entry = text[start:end].strip()
    sys.stdout.write(entry + "\n")


if __name__ == "__main__":
    main()
