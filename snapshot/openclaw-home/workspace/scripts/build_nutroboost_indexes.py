#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


DATE_RE = re.compile(r"(\d{2}/\d{2}/\d{4})")


def classify(name: str) -> str:
    lower = name.lower()
    if "mentoria" in lower:
        return "mentorias"
    if "discuss" in lower or "casos clÃ­nicos" in lower or "casos clinicos" in lower:
        return "discussoes_de_casos"
    if "reuniÃ£o" in lower or "reuniao" in lower:
        return "reunioes"
    return "aulas_tecnicas"


def tokenize(name: str) -> list[str]:
    words = re.findall(r"\w+", name.lower(), flags=re.UNICODE)
    stop = {
        "de",
        "da",
        "do",
        "das",
        "dos",
        "e",
        "em",
        "a",
        "o",
        "as",
        "os",
        "mentoria",
        "discussÃ£o",
        "discussao",
        "casos",
        "clÃ­nicos",
        "clinicos",
    }
    return [w for w in words if len(w) >= 4 and w not in stop and not w.isdigit()]


def md_link(label: str, url: str) -> str:
    return f"[{label}]({url})"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    lectures = payload["lectures"]
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    by_type: dict[str, list[dict]] = defaultdict(list)
    by_date: dict[str, list[dict]] = defaultdict(list)
    by_keyword: dict[str, list[dict]] = defaultdict(list)

    for lecture in lectures:
        by_type[classify(lecture["lecture_name"])].append(lecture)
        date_match = DATE_RE.search(lecture["lecture_name"])
        if date_match:
            by_date[date_match.group(1)].append(lecture)
        for token in tokenize(lecture["lecture_name"]):
            by_keyword[token].append(lecture)

    simple_map_lines = ["# Nutroboost Video Index", ""]
    for lecture in lectures:
        simple_map_lines.append(f"- {lecture['lecture_name']}")
        simple_map_lines.append(f"  Aula: {lecture['lecture_url']}")
        if lecture["video_urls"]:
            simple_map_lines.append(f"  Video: {lecture['video_urls'][0]}")
    (out_dir / "nutroboost-video-index.md").write_text("\n".join(simple_map_lines) + "\n", encoding="utf-8")

    type_lines = ["# Nutroboost By Type", ""]
    for bucket in ["aulas_tecnicas", "discussoes_de_casos", "mentorias", "reunioes"]:
        items = by_type.get(bucket, [])
        if not items:
            continue
        type_lines.append(f"## {bucket}")
        type_lines.append("")
        for item in items:
            line = f"- {md_link(item['lecture_name'], item['lecture_url'])}"
            if item["video_urls"]:
                line += f" | video: {item['video_urls'][0]}"
            type_lines.append(line)
        type_lines.append("")
    (out_dir / "nutroboost-by-type.md").write_text("\n".join(type_lines), encoding="utf-8")

    date_lines = ["# Nutroboost By Date", ""]
    for date in sorted(by_date.keys(), key=lambda d: tuple(reversed(d.split("/")))):
        date_lines.append(f"## {date}")
        date_lines.append("")
        for item in by_date[date]:
            line = f"- {md_link(item['lecture_name'], item['lecture_url'])}"
            if item["video_urls"]:
                line += f" | video: {item['video_urls'][0]}"
            date_lines.append(line)
        date_lines.append("")
    (out_dir / "nutroboost-by-date.md").write_text("\n".join(date_lines), encoding="utf-8")

    keyword_lines = ["# Nutroboost By Keyword", ""]
    for keyword in sorted(k for k, v in by_keyword.items() if len(v) <= 12):
        keyword_lines.append(f"## {keyword}")
        keyword_lines.append("")
        for item in by_keyword[keyword]:
            line = f"- {md_link(item['lecture_name'], item['lecture_url'])}"
            if item["video_urls"]:
                line += f" | video: {item['video_urls'][0]}"
            keyword_lines.append(line)
        keyword_lines.append("")
    (out_dir / "nutroboost-by-keyword.md").write_text("\n".join(keyword_lines), encoding="utf-8")

    summary = {
        "lecture_count": len(lectures),
        "type_buckets": {k: len(v) for k, v in sorted(by_type.items())},
        "dated_entries": len(by_date),
        "keyword_entries": len(by_keyword),
    }
    (out_dir / "nutroboost-index-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

