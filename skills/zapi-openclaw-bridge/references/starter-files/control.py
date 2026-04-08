#!/usr/bin/env python3
import json
from pathlib import Path

CONTROL_FILE = Path("{{CONTROL_FILE}}")


def load_state() -> dict:
    if not CONTROL_FILE.exists():
        return {"paused": False, "manual_overrides": {}}
    return json.loads(CONTROL_FILE.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    CONTROL_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    print(load_state())
