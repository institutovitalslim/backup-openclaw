#!/usr/bin/env python3
import argparse
import json
import os
import runpy
import sys
from pathlib import Path

BRIDGE_PATH = Path(__file__).resolve().parent / "zapi_clara_bridge.py"
bridge = runpy.run_path(str(BRIDGE_PATH))

normalize_phone = bridge["normalize_phone"]
send_zapi_text = bridge["send_zapi_text"]
manual_assume = bridge["manual_assume"]
manual_release = bridge["manual_release"]
load_control_state = bridge["load_control_state"]


def cmd_assume(args):
    phone = normalize_phone(args.phone)
    state = manual_assume(phone, note=args.note)
    print(json.dumps({"ok": True, "phone": phone, "state": state}, ensure_ascii=False, indent=2))


def cmd_release(args):
    phone = normalize_phone(args.phone)
    state = manual_release(phone)
    print(json.dumps({"ok": True, "phone": phone, "state": state}, ensure_ascii=False, indent=2))


def cmd_status(args):
    state = load_control_state()
    if args.phone:
        phone = normalize_phone(args.phone)
        active = phone in (state.get("manual_overrides") or {})
        print(json.dumps({"ok": True, "phone": phone, "manual_override": active, "state": state}, ensure_ascii=False, indent=2))
        return
    print(json.dumps({"ok": True, "state": state}, ensure_ascii=False, indent=2))


def cmd_send(args):
    phone = normalize_phone(args.phone)
    status, body = send_zapi_text(phone, args.message)
    print(json.dumps({"ok": 200 <= status < 300, "phone": phone, "status": status, "body": body}, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Manual operations for Clara via Z-API bridge")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("assume")
    p.add_argument("phone")
    p.add_argument("--note", default="telegram_manual")
    p.set_defaults(func=cmd_assume)

    p = sub.add_parser("release")
    p.add_argument("phone")
    p.set_defaults(func=cmd_release)

    p = sub.add_parser("status")
    p.add_argument("phone", nargs="?")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("send")
    p.add_argument("phone")
    p.add_argument("message")
    p.set_defaults(func=cmd_send)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
