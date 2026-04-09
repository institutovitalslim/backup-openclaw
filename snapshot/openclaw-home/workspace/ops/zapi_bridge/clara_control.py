#!/usr/bin/env python3
import json
import sys
import time
from pathlib import Path

STATE_PATH = Path("/root/.openclaw/workspace/ops/zapi_bridge/clara_control_state.json")


def load_state():
    if not STATE_PATH.exists():
        return {"paused": False, "manual_overrides": {}, "updated_at": None}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state):
    state["updated_at"] = int(time.time())
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_phone(v):
    return "".join(ch for ch in v if ch.isdigit())


def main():
    if len(sys.argv) < 2:
        print("uso: clara_control.py status|pause|resume|assume <telefone> [minutes]|release <telefone>")
        return 1
    cmd = sys.argv[1].lower()
    state = load_state()
    state.setdefault("manual_overrides", {})

    if cmd == "status":
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0
    if cmd == "pause":
        state["paused"] = True
        save_state(state)
        print("Clara pausada globalmente.")
        return 0
    if cmd == "resume":
        state["paused"] = False
        save_state(state)
        print("Clara reativada globalmente.")
        return 0
    if cmd == "assume":
        if len(sys.argv) < 3:
            print("informe o telefone")
            return 1
        phone = normalize_phone(sys.argv[2])
        minutes = int(sys.argv[3]) if len(sys.argv) >= 4 else 240
        until = int(time.time()) + minutes * 60 if minutes > 0 else None
        state["manual_overrides"][phone] = {"until": until, "note": "manual_override"}
        save_state(state)
        print(f"Clara pausada para {phone} por {minutes} min.")
        return 0
    if cmd == "release":
        if len(sys.argv) < 3:
            print("informe o telefone")
            return 1
        phone = normalize_phone(sys.argv[2])
        state["manual_overrides"].pop(phone, None)
        save_state(state)
        print(f"Clara reativada para {phone}.")
        return 0

    print("comando inválido")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
