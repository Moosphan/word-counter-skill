#!/usr/bin/env python3
"""Copy the canonical runtime script into each skill package."""

from __future__ import annotations

import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = PROJECT_ROOT / "src" / "word_counter.py"
TARGETS = [
    PROJECT_ROOT / "skills" / "codex" / "word-counter" / "scripts" / "word_counter.py",
    PROJECT_ROOT
    / "skills"
    / "claude"
    / ".claude"
    / "skills"
    / "word-counter"
    / "scripts"
    / "word_counter.py",
]


def main() -> int:
    if not SOURCE_SCRIPT.exists():
        raise FileNotFoundError(f"Missing source script: {SOURCE_SCRIPT}")

    for target in TARGETS:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE_SCRIPT, target)
        print(f"synced {target.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

