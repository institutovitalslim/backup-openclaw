#!/usr/bin/env python3
import json
import os
import subprocess
import time
from pathlib import Path

SHEET_ID = os.getenv("ZAPI_HISTORY_SHEET_ID", "1QXvRhElCx1t7mxMAwGkcvh5V7YyKLjP9zozSGH7LHnM")
RANGE = os.getenv("ZAPI_HISTORY_CONTEXT_RANGE", "contexto_paciente!A1:E1000")
OUT_PATH = Path(os.getenv("CLARA_EXCLUSIONS_FILE", "/root/.openclaw/workspace/ops/zapi_bridge/clara_exclusions.json"))


def load_existing():
    if not OUT_PATH.exists():
        return {"phones": {}, "updated_at": None}
    try:
        data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"phones": {}, "updated_at": None}
        if not isinstance(data.get("phones"), dict):
            data["phones"] = {}
        return data
    except Exception:
        return {"phones": {}, "updated_at": None}


def main():
    out = subprocess.check_output(["gog", "sheets", "get", SHEET_ID, RANGE, "--json"], text=True)
    values = json.loads(out).get("values", [])
    if not values:
        raise SystemExit("no values from sheet")
    header = values[0]
    rows = [dict(zip(header, r)) for r in values[1:] if r]
    state = load_existing()
    phones = state.setdefault("phones", {})
    synced = 0
    for row in rows:
        phone = ''.join(ch for ch in str(row.get('phone', '')) if ch.isdigit())
        summary = str(row.get('summary', ''))
        if not phone:
            continue
        if 'Paciente ' not in summary:
            continue
        existing = phones.get(phone)
        if isinstance(existing, dict) and existing.get('source') == 'manual':
            continue
        phones[phone] = {
            "name": row.get("chat_name") or row.get("sender_name") or "",
            "reason": "patient_bridge_known",
            "source": "bridge_contexto_paciente",
            "updated_at": int(time.time())
        }
        synced += 1
    state["updated_at"] = int(time.time())
    OUT_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "synced": synced, "path": str(OUT_PATH)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
