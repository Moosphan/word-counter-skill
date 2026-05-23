#!/usr/bin/env python3
"""Build release archives for the Codex and Claude Code skill packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = PROJECT_ROOT / "dist"
PACKAGES = [
    {
        "name": "codex-word-counter-skill",
        "source": PROJECT_ROOT / "skills" / "codex" / "word-counter",
        "arc_root": Path("word-counter"),
    },
    {
        "name": "claude-code-word-counter-skill",
        "source": PROJECT_ROOT / "skills" / "claude" / ".claude",
        "arc_root": Path(".claude"),
    },
]


def sha256_for_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def zip_tree(source: Path, arc_root: Path, target: Path) -> None:
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, arc_root / path.relative_to(source))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package the skill release artifacts.")
    parser.add_argument("--version", required=True, help="Version label used in archive names.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the dist directory before packaging.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.clean and DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "sync_skill_runtime.py")],
        check=True,
    )

    manifest: dict[str, object] = {"version": args.version, "artifacts": []}

    for package in PACKAGES:
        source = package["source"]
        if not source.exists():
            raise FileNotFoundError(f"Missing package source: {source}")
        archive_name = f"{package['name']}-{args.version}.zip"
        target = DIST_DIR / archive_name
        zip_tree(source, package["arc_root"], target)
        manifest["artifacts"].append(
            {
                "name": archive_name,
                "sha256": sha256_for_file(target),
                "source": str(source.relative_to(PROJECT_ROOT)),
            }
        )
        print(f"built {target.relative_to(PROJECT_ROOT)}")

    manifest_path = DIST_DIR / f"release-manifest-{args.version}.json"
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
    print(f"wrote {manifest_path.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
