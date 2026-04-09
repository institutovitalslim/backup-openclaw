#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

INBOX_FILE = Path("/root/.openclaw/workspace/ops/zapi_bridge/clara_manual_inbox.json")


def load() -> dict:
    if not INBOX_FILE.exists():
        return {"messages": [], "updated_at": None}
    return json.loads(INBOX_FILE.read_text(encoding="utf-8"))


def cmd_list(args):
    data = load()
    messages = data.get("messages") or []
    if args.phone:
        phone = ''.join(ch for ch in args.phone if ch.isdigit())
        messages = [m for m in messages if m.get("phone") == phone]
    if args.limit:
        messages = messages[-args.limit:]
    print(json.dumps({"messages": messages, "updated_at": data.get("updated_at")}, ensure_ascii=False, indent=2))


def cmd_latest(args):
    data = load()
    messages = data.get("messages") or []
    phone = ''.join(ch for ch in args.phone if ch.isdigit())
    filtered = [m for m in messages if m.get("phone") == phone]
    print(json.dumps(filtered[-1] if filtered else {}, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect manual inbound messages for Clara")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list")
    p.add_argument("--phone")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("latest")
    p.add_argument("phone")
    p.set_defaults(func=cmd_latest)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
