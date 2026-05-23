#!/usr/bin/env python3
"""Smoke-test both skill packages against realistic article excerpts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = {
    "zh_article_excerpt": {
        "path": PROJECT_ROOT / "tests" / "fixtures" / "zh_article_excerpt.txt",
        "profile": "zh",
    },
    "en_article_excerpt": {
        "path": PROJECT_ROOT / "tests" / "fixtures" / "en_article_excerpt.txt",
        "profile": "en",
    },
    "zh_article_excerpt_mixed": {
        "path": PROJECT_ROOT / "tests" / "fixtures" / "zh_article_excerpt.txt",
        "profile": "mixed",
    },
}
SKILLS = {
    "codex": PROJECT_ROOT / "skills" / "codex" / "word-counter" / "scripts" / "word_counter.py",
    "claude": PROJECT_ROOT
    / "skills"
    / "claude"
    / ".claude"
    / "skills"
    / "word-counter"
    / "scripts"
    / "word_counter.py",
}


def run_counter(script: Path, fixture: Path, profile: str) -> dict[str, object]:
    proc = subprocess.run(
        [sys.executable, str(script), "--profile", profile, "--format", "json", str(fixture)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def main() -> int:
    failures: list[str] = []

    for fixture_name, fixture_config in FIXTURES.items():
        baseline = None
        print(f"\n== {fixture_name} ({fixture_config['profile']}) ==")
        for skill_name, script in SKILLS.items():
            payload = run_counter(script, fixture_config["path"], fixture_config["profile"])
            print(
                f"{skill_name:6} total={payload['selected_total']:<4} "
                f"formula={payload['selected_formula']}"
            )
            if baseline is None:
                baseline = payload
            elif payload != baseline:
                failures.append(f"{fixture_name}: {skill_name} output differs from baseline")

    if failures:
        print("\nSmoke test failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("\nSmoke test passed: Codex and Claude skill outputs are identical.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
