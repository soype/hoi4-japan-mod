#!/usr/bin/env python3
"""Build the mod's japan.txt focus override from the installed vanilla file.

The mod only changes one focus in Japan's national focus tree. HOI4 has no
reliable way to patch a single focus definition, so the whole file has to be
overridden. To keep the git diff reviewable, the vanilla file is not tracked.
This script copies the installed file and swaps in the modified focus block
from src/focus/JAP_strike_the_southern_road.txt.

Usage:
    python3 tools/build_focus.py
    python3 tools/build_focus.py /path/to/vanilla/japan.txt
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FOCUS_ID = "JAP_strike_the_southern_road"
REPO_ROOT = Path(__file__).resolve().parent.parent
REPLACEMENT = REPO_ROOT / "src" / "focus" / f"{FOCUS_ID}.txt"
OUTPUT = REPO_ROOT / "common" / "national_focus" / "japan.txt"

# The mod lives at <game>/mod/<mod_name>/, so the vanilla file is two levels up.
DEFAULT_VANILLA = REPO_ROOT.parent.parent / "common" / "national_focus" / "japan.txt"


def find_focus_block(lines: list[str]) -> tuple[int, int]:
    """Return [start, end) line indexes of the focus block with FOCUS_ID."""
    start = None
    for index, line in enumerate(lines):
        if not re.match(r"^\s*focus\s*=\s*\{", line):
            continue
        if index + 1 >= len(lines):
            continue
        if re.match(r"^\s*id\s*=\s*" + re.escape(FOCUS_ID) + r"\s*$", lines[index + 1]):
            start = index
            break

    if start is None:
        raise SystemExit(f"Could not find focus {FOCUS_ID} in the vanilla file.")

    depth = 0
    for index in range(start, len(lines)):
        depth += lines[index].count("{") - lines[index].count("}")
        if depth == 0:
            return start, index + 1

    raise SystemExit(f"Unbalanced braces while reading focus {FOCUS_ID}.")


def main() -> None:
    vanilla = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_VANILLA
    if not vanilla.is_file():
        raise SystemExit(
            f"Vanilla focus file not found: {vanilla}\n"
            "Pass the path explicitly: python3 tools/build_focus.py /path/to/japan.txt"
        )
    if not REPLACEMENT.is_file():
        raise SystemExit(f"Replacement focus file not found: {REPLACEMENT}")

    vanilla_lines = vanilla.read_text(encoding="utf-8-sig").splitlines(keepends=True)
    replacement_lines = REPLACEMENT.read_text(encoding="utf-8-sig").splitlines(keepends=True)

    if not any(f"id = {FOCUS_ID}" in line for line in replacement_lines):
        raise SystemExit(f"{REPLACEMENT} does not define {FOCUS_ID}.")

    start, end = find_focus_block(vanilla_lines)
    output_lines = vanilla_lines[:start] + replacement_lines + vanilla_lines[end:]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(output_lines), encoding="utf-8-sig")

    print(f"Read vanilla focus file: {vanilla}")
    print(f"Replaced {FOCUS_ID} (lines {start + 1}-{end}).")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
