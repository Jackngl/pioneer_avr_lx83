#!/usr/bin/env python3
"""Simple helper to bump the integration version everywhere."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
from typing import Final


ROOT: Final = pathlib.Path(__file__).resolve().parents[1]
MANIFEST_PATH: Final = ROOT / "custom_components" / "pioneer_avr_lx83" / "manifest.json"
VERSION_FILE: Final = ROOT / "VERSION"
CHANGELOG_PATH: Final = ROOT / "CHANGELOG.md"

SEMVER_RE: Final = re.compile(r"^\d+\.\d+\.\d+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bump project version.")
    parser.add_argument(
        "version",
        type=str,
        help="New semantic version (major.minor.patch)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=dt.date.today().isoformat(),
        help="Release date used in CHANGELOG (default: today)",
    )
    parser.add_argument(
        "--notes",
        type=str,
        default="- Describe your changes here",
        help="Initial bullet for the changelog entry.",
    )
    return parser.parse_args()


def ensure_semver(version: str) -> None:
    if not SEMVER_RE.match(version):
        raise ValueError(f"Version '{version}' is not valid semantic versioning.")


def update_manifest(version: str) -> None:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    data["version"] = version
    MANIFEST_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def update_version_file(version: str) -> None:
    VERSION_FILE.write_text(version + "\n", encoding="utf-8")


def update_changelog(version: str, release_date: str, notes: str) -> None:
    changelog = CHANGELOG_PATH.read_text(encoding="utf-8")
    entry = (
        f"## [{version}] - {release_date}\n\n"
        f"{notes if notes.startswith('-') else '- ' + notes}\n\n"
    )
    if "## [" in changelog:
        # Insert entry right after the intro block.
        split_idx = changelog.find("## [", 1)
        header = changelog[:split_idx]
        rest = changelog[split_idx:]
        CHANGELOG_PATH.write_text(f"{header}{entry}{rest}", encoding="utf-8")
    else:
        CHANGELOG_PATH.write_text(changelog + "\n" + entry, encoding="utf-8")


def main() -> None:
    args = parse_args()
    ensure_semver(args.version)
    update_manifest(args.version)
    update_version_file(args.version)
    update_changelog(args.version, args.date, args.notes)
    print(f"Version bumped to {args.version}")
    print("Remember to review CHANGELOG.md and commit the changes, then run:")
    print(f"  git tag -a v{args.version} -m 'Release v{args.version}' && git push --tags")


if __name__ == "__main__":
    main()
