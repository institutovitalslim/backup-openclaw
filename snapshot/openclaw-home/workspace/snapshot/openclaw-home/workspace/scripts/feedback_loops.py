#!/usr/bin/env python3
"""Feedback loops helper.

Commands:
- init: create the feedback/lessons/decisions structure
- append: append a feedback event with FIFO retention
- consolidate: summarize monthly patterns and promote them
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


DOMAINS = ("content", "tasks", "recommendations", "digest")
DECISIONS = ("approve", "reject", "edit", "defer")
MAX_ENTRIES = 30


LESSONS_TEMPLATE = """# Lessons: {domain}

## Strategic

- Add durable patterns here.

## Tactical

- Add short-lived lessons here and review monthly.
"""


DECISIONS_TEMPLATE = """# Decisions: {domain}

- Add stable operational rules here.
"""


@dataclass
class Event:
    date: str
    domain: str
    context: str
    decision: str
    reason: str
    tags: list[str]
    source: str
    applies_to: list[str]
    weight: float

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "domain": self.domain,
            "context": self.context,
            "decision": self.decision,
            "reason": self.reason,
            "tags": self.tags,
            "source": self.source,
            "applies_to": self.applies_to,
            "weight": self.weight,
        }


def ensure_structure(root: Path) -> None:
    (root / "feedback").mkdir(parents=True, exist_ok=True)
    (root / "lessons").mkdir(parents=True, exist_ok=True)
    (root / "decisions").mkdir(parents=True, exist_ok=True)
    (root / "indexes").mkdir(parents=True, exist_ok=True)

    for domain in DOMAINS:
        feedback_path = root / "feedback" / f"{domain}.jsonl"
        lessons_path = root / "lessons" / f"{domain}.md"
        decisions_path = root / "decisions" / f"{domain}.md"

        feedback_path.touch(exist_ok=True)
        if not lessons_path.exists():
            lessons_path.write_text(LESSONS_TEMPLATE.format(domain=domain), encoding="utf-8")
        if not decisions_path.exists():
            decisions_path.write_text(DECISIONS_TEMPLATE.format(domain=domain), encoding="utf-8")

    summary_path = root / "indexes" / "feedback_summary.md"
    promotion_log_path = root / "indexes" / "promotion_log.jsonl"
    if not summary_path.exists():
        summary_path.write_text("# Feedback Summary\n\n", encoding="utf-8")
    promotion_log_path.touch(exist_ok=True)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            rows.append(json.loads(stripped))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    text = "\n".join(json.dumps(row, ensure_ascii=True) for row in rows)
    if text:
        text += "\n"
    path.write_text(text, encoding="utf-8")


def normalize_month(month: str | None) -> str:
    if month:
        datetime.strptime(month, "%Y-%m")
        return month
    return datetime.now(timezone.utc).strftime("%Y-%m")


def event_signature(row: dict) -> str:
    parts = [
        row.get("decision", ""),
        row.get("reason", "").strip().lower(),
        "|".join(sorted(row.get("tags", []))),
        "|".join(sorted(row.get("applies_to", []))),
    ]
    return " || ".join(parts)


def promotion_key(month: str, domain: str, level: str, signature: str) -> str:
    return f"{month}:{domain}:{level}:{signature}"


def load_promotion_keys(root: Path) -> set[str]:
    keys = set()
    for row in read_jsonl(root / "indexes" / "promotion_log.jsonl"):
        month = row.get("month")
        domain = row.get("domain")
        level = row.get("to")
        signature = row.get("signature")
        if month and domain and level and signature:
            keys.add(promotion_key(month, domain, level, signature))
    return keys


def append_markdown_section(path: Path, header: str, bullet_lines: list[str]) -> None:
    if not bullet_lines:
        return
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if header in text:
        return
    block = header + "\n\n" + "\n".join(f"- {line}" for line in bullet_lines) + "\n"
    path.write_text(text.rstrip() + "\n\n" + block, encoding="utf-8")


def cmd_init(args: argparse.Namespace) -> int:
    ensure_structure(Path(args.root))
    return 0


def cmd_append(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_structure(root)

    if args.domain not in DOMAINS:
        raise SystemExit(f"invalid domain: {args.domain}")
    if args.decision not in DECISIONS:
        raise SystemExit(f"invalid decision: {args.decision}")
    if not 0.0 <= args.weight <= 1.0:
        raise SystemExit("weight must be between 0.0 and 1.0")

    event = Event(
        date=args.date,
        domain=args.domain,
        context=args.context,
        decision=args.decision,
        reason=args.reason,
        tags=args.tags or [],
        source=args.source,
        applies_to=args.applies_to or [],
        weight=args.weight,
    )

    path = root / "feedback" / f"{args.domain}.jsonl"
    rows = read_jsonl(path)
    rows.append(event.to_dict())
    rows = rows[-MAX_ENTRIES:]
    write_jsonl(path, rows)
    return 0


def summarize_candidate(group_rows: list[dict]) -> str:
    sample = group_rows[0]
    tags = ", ".join(sample.get("tags", [])) or "no-tags"
    applies_to = ", ".join(sample.get("applies_to", [])) or "general scope"
    count = len(group_rows)
    avg_weight = sum(row.get("weight", 0.0) for row in group_rows) / max(count, 1)
    return (
        f"{sample.get('reason')} "
        f"(decision={sample.get('decision')}; count={count}; avg_weight={avg_weight:.2f}; "
        f"tags={tags}; applies_to={applies_to})"
    )


def cmd_consolidate(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_structure(root)
    month = normalize_month(args.month)
    existing_keys = load_promotion_keys(root)
    promotion_log_path = root / "indexes" / "promotion_log.jsonl"

    summary_lines = [f"# Feedback Summary", "", f"## {month}", ""]

    for domain in DOMAINS:
        rows = [
            row
            for row in read_jsonl(root / "feedback" / f"{domain}.jsonl")
            if str(row.get("date", "")).startswith(month)
        ]
        summary_lines.append(f"### {domain}")
        if not rows:
            summary_lines.append("")
            summary_lines.append("- No feedback entries for this month.")
            summary_lines.append("")
            continue

        groups: dict[str, list[dict]] = defaultdict(list)
        for row in rows:
            groups[event_signature(row)].append(row)

        lesson_bullets: list[str] = []
        decision_bullets: list[str] = []
        summary_lines.append("")
        summary_lines.append(f"- Entries: {len(rows)}")
        summary_lines.append(f"- Patterns: {len(groups)}")

        for signature, group_rows in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
            count = len(group_rows)
            max_weight = max(row.get("weight", 0.0) for row in group_rows)
            avg_weight = sum(row.get("weight", 0.0) for row in group_rows) / count
            candidate_text = summarize_candidate(group_rows)
            summary_lines.append(f"- Candidate: {candidate_text}")

            lesson_threshold = count >= 2 or max_weight >= 0.9
            decision_threshold = count >= 3 and avg_weight >= 0.75

            lesson_key = promotion_key(month, domain, "lesson", signature)
            if lesson_threshold and lesson_key not in existing_keys:
                lesson_bullets.append(candidate_text)
                log_row = {
                    "date": datetime.now(timezone.utc).date().isoformat(),
                    "month": month,
                    "domain": domain,
                    "from": "feedback",
                    "to": "lesson",
                    "signature": signature,
                    "reason": f"Auto-promoted from {count} matching feedback entrie(s)",
                    "source_entries": [
                        f"{row.get('date')}:{','.join(row.get('tags', [])) or 'no-tags'}"
                        for row in group_rows
                    ],
                }
                with promotion_log_path.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(log_row, ensure_ascii=True) + "\n")
                existing_keys.add(lesson_key)

            decision_key = promotion_key(month, domain, "decision", signature)
            if decision_threshold and decision_key not in existing_keys:
                decision_bullets.append(candidate_text)
                log_row = {
                    "date": datetime.now(timezone.utc).date().isoformat(),
                    "month": month,
                    "domain": domain,
                    "from": "lesson",
                    "to": "decision",
                    "signature": signature,
                    "reason": f"Auto-promoted from strong recurring pattern (count={count}, avg_weight={avg_weight:.2f})",
                    "source_entries": [
                        f"{row.get('date')}:{','.join(row.get('tags', [])) or 'no-tags'}"
                        for row in group_rows
                    ],
                }
                with promotion_log_path.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(log_row, ensure_ascii=True) + "\n")
                existing_keys.add(decision_key)

        append_markdown_section(
            root / "lessons" / f"{domain}.md",
            f"## Auto-promoted {month}",
            lesson_bullets,
        )
        append_markdown_section(
            root / "decisions" / f"{domain}.md",
            f"## Auto-promoted {month}",
            decision_bullets,
        )
        summary_lines.append("")

    (root / "indexes" / "feedback_summary.md").write_text(
        "\n".join(summary_lines).rstrip() + "\n",
        encoding="utf-8",
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Feedback loops helper")
    parser.add_argument(
        "--root",
        default="memory",
        help="Root directory for feedback memory (default: memory)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Create base structure")
    init_parser.set_defaults(func=cmd_init)

    append_parser = sub.add_parser("append", help="Append a feedback event")
    append_parser.add_argument("--date", required=True)
    append_parser.add_argument("--domain", required=True, choices=DOMAINS)
    append_parser.add_argument("--context", required=True)
    append_parser.add_argument("--decision", required=True, choices=DECISIONS)
    append_parser.add_argument("--reason", required=True)
    append_parser.add_argument("--tags", nargs="*", default=[])
    append_parser.add_argument("--source", default="manual")
    append_parser.add_argument("--applies-to", nargs="*", default=[])
    append_parser.add_argument("--weight", type=float, default=0.8)
    append_parser.set_defaults(func=cmd_append)

    consolidate_parser = sub.add_parser("consolidate", help="Consolidate monthly patterns")
    consolidate_parser.add_argument("--month", help="Month in YYYY-MM format")
    consolidate_parser.set_defaults(func=cmd_consolidate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

