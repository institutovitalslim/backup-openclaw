#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from html import unescape
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.request import HTTPCookieProcessor, Request, build_opener


MEDIA_RE = re.compile(r"https://[^\s\"'<>]+?\.(?:mp4|m3u8|mp3|pdf)", re.IGNORECASE)
TITLE_RE = re.compile(r"<p[^>]*>(.*?)</p>", re.IGNORECASE | re.DOTALL)


@dataclass
class SystemeClient:
    base_url: str
    opener: Any

    def request_json(self, path: str, *, referer: str | None = None) -> Any:
        request = Request(
            urljoin(self.base_url, path),
            headers=self._headers(referer=referer),
        )
        with self.opener.open(request) as response:
            return json.loads(response.read().decode("utf-8"))

    def request_text(self, path: str, *, referer: str | None = None) -> str:
        request = Request(
            urljoin(self.base_url, path),
            headers=self._headers(referer=referer),
        )
        with self.opener.open(request) as response:
            return response.read().decode("utf-8", "ignore")

    def post_json(self, path: str, payload: dict[str, Any], *, referer: str | None = None) -> str:
        request = Request(
            urljoin(self.base_url, path),
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(referer=referer, content_type="application/json"),
            method="POST",
        )
        with self.opener.open(request) as response:
            return response.read().decode("utf-8", "ignore")

    def _headers(self, *, referer: str | None, content_type: str | None = None) -> dict[str, str]:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": self.base_url,
            "User-Agent": "openclaw-course-map/1.0",
        }
        if referer:
            headers["Referer"] = referer
        if content_type:
            headers["Content-Type"] = content_type
        return headers


def build_client(base_url: str) -> SystemeClient:
    cookie_jar = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cookie_jar))
    return SystemeClient(base_url=base_url.rstrip("/"), opener=opener)


def extract_text_title(html: str) -> str | None:
    match = TITLE_RE.search(html)
    if not match:
        return None
    text = re.sub(r"<[^>]+>", " ", match.group(1))
    text = re.sub(r"\s+", " ", unescape(text)).strip()
    return text or None


def normalize_mojibake(text: str) -> str:
    if "Ãƒ" not in text:
        return text
    try:
        return text.encode("latin-1").decode("utf-8")
    except UnicodeError:
        return text


def extract_media_urls(html: str) -> list[str]:
    decoded = html.replace("\\/", "/")
    decoded = decoded.replace("\\u0022", "\"")
    decoded = decoded.replace("\\u003C", "<")
    decoded = decoded.replace("\\u003E", ">")
    decoded = decoded.replace("\\n", " ")
    decoded = decoded.encode("utf-8").decode("unicode_escape")
    return sorted({normalize_mojibake(url) for url in MEDIA_RE.findall(decoded)})


def lecture_payload_to_map_entry(
    *,
    base_url: str,
    course_path: str,
    module_name: str,
    lecture: dict[str, Any],
    lecture_html: str,
) -> dict[str, Any]:
    lecture_id = lecture["id"]
    lecture_name = normalize_mojibake(lecture["name"])
    lecture_url = f"{base_url}/school/course/{course_path}/lecture/{lecture_id}"
    media_urls = extract_media_urls(lecture_html)
    resource_urls = [url for url in media_urls if not re.search(r"\.(?:mp4|m3u8|mp3)$", url, re.IGNORECASE)]
    video_urls = [url for url in media_urls if re.search(r"\.(?:mp4|m3u8|mp3)$", url, re.IGNORECASE)]
    return {
        "module_name": normalize_mojibake(module_name),
        "lecture_id": lecture_id,
        "lecture_name": lecture_name,
        "lecture_url": lecture_url,
        "available": lecture.get("available"),
        "completed": lecture.get("completed"),
        "page_title": normalize_mojibake(extract_text_title(lecture_html) or "") or None,
        "video_urls": video_urls,
        "resource_urls": resource_urls,
    }


def render_markdown(course: dict[str, Any], modules: list[dict[str, Any]], entries: list[dict[str, Any]]) -> str:
    lines = [
        f"# {course['name']}",
        "",
        f"- Instructor: {course.get('instructorName') or 'Unknown'}",
        f"- Access: {course.get('dominantAccessType') or 'unknown'}",
        f"- Progress: {course.get('progress', 0)}",
        f"- Modules: {len(modules)}",
        f"- Lectures: {len(entries)}",
        "",
        "## Modules",
        "",
    ]
    by_module: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        by_module.setdefault(entry["module_name"], []).append(entry)
    for module in modules:
        module_name = module["name"]
        lines.append(f"### {module_name}")
        lines.append("")
        for entry in by_module.get(module_name, []):
            lines.append(f"- Lecture: {entry['lecture_name']}")
            lines.append(f"  URL: {entry['lecture_url']}")
            if entry["video_urls"]:
                lines.append(f"  Video: {entry['video_urls'][0]}")
            if len(entry["video_urls"]) > 1:
                for extra in entry["video_urls"][1:]:
                    lines.append(f"  Video extra: {extra}")
            if entry["resource_urls"]:
                for resource in entry["resource_urls"]:
                    lines.append(f"  Resource: {resource}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--course-path", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--slug", default="systeme-course-map")
    args = parser.parse_args()

    client = build_client(args.base_url)
    client.post_json(
        "/api/security/login",
        {"email": args.email, "password": args.password, "remember": True},
        referer=f"{args.base_url.rstrip('/')}/login",
    )

    course = client.request_json(
        f"/api/membership/course/{args.course_path}",
        referer=f"{args.base_url.rstrip('/')}/school/course/{args.course_path}",
    )
    menu = client.request_json(
        f"/api/membership/course/{course['id']}/menu",
        referer=f"{args.base_url.rstrip('/')}/school/course/{args.course_path}",
    )

    entries: list[dict[str, Any]] = []
    for module in menu:
        module_name = module["name"]
        for lecture in module.get("lectures", []):
            lecture_html = client.request_text(
                f"/api/membership/lecture/{lecture['id']}",
                referer=f"{args.base_url.rstrip('/')}/school/course/{args.course_path}/lecture/{lecture['id']}",
            )
            entries.append(
                lecture_payload_to_map_entry(
                    base_url=args.base_url.rstrip("/"),
                    course_path=args.course_path,
                    module_name=module_name,
                    lecture=lecture,
                    lecture_html=lecture_html,
                )
            )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.slug}.json"
    md_path = output_dir / f"{args.slug}.md"

    payload = {
        "course": {
            "id": course["id"],
            "name": course["name"],
            "instructor_name": course.get("instructorName"),
            "dominant_access_type": course.get("dominantAccessType"),
            "progress": course.get("progress"),
            "course_path": args.course_path,
            "base_url": args.base_url.rstrip("/"),
        },
        "modules": menu,
        "lectures": entries,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(course, menu, entries), encoding="utf-8")

    print(json.dumps({"json_path": str(json_path), "md_path": str(md_path), "lecture_count": len(entries)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

