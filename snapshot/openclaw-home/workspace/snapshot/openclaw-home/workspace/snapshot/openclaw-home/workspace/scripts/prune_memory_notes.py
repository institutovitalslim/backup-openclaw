#!/usr/bin/env python3
"""Prune explicitly tactical memory notes.

Safety-first policy:
- only deletes files under memory/tactical/
- or files containing the explicit marker "Retention: tactical-30d"
- default mode is dry-run
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


MARKER = "Retention: tactical-30d"
SAFE_DIR_NAME = "tactical"


@dataclass
class Candidate:
    path: Path
    reason: str
    age_days: int


def is_candidate(path: Path, memory_root: Path, cutoff: datetime) -> Candidate | None:
    if not path.is_file():
        return None

    if path.name in {"decisions.md", "lessons.md", "pending.md", "people.md", "projects.md"}:
        return None

    try:
        rel = path.relative_to(memory_root)
    except ValueError:
        return None

    if rel.parts and rel.parts[0] == "feedback_loops":
        return None
    if rel.parts and rel.parts[0] == "backups":
        return None

    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    if mtime >= cutoff:
        return None

    age_days = int((datetime.now(timezone.utc) - mtime).total_seconds() // 86400)

    if SAFE_DIR_NAME in rel.parts:
        return Candidate(path=path, reason="under memory/tactical/", age_days=age_days)

    try:
        head = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:20]
    except OSError:
        return None

    if any(MARKER in line for line in head):
        return Candidate(path=path, reason=f"contains marker '{MARKER}'", age_days=age_days)

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune explicitly tactical memory notes")
    parser.add_argument("--memory-root", default="/root/.openclaw/workspace/memory")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--apply", action="store_true", help="Delete candidates")
    args = parser.parse_args()

    memory_root = Path(args.memory_root)
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)

    candidates: list[Candidate] = []
    for path in memory_root.rglob("*.md"):
        candidate = is_candidate(path, memory_root, cutoff)
        if candidate:
            candidates.append(candidate)

    print(f"mode={'apply' if args.apply else 'dry-run'}")
    print(f"memory_root={memory_root}")
    print(f"days={args.days}")
    print(f"candidates={len(candidates)}")

    for candidate in sorted(candidates, key=lambda c: str(c.path)):
        print(f"{candidate.path} | age_days={candidate.age_days} | reason={candidate.reason}")
        if args.apply:
            candidate.path.unlink(missing_ok=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

