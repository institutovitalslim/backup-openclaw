#!/usr/bin/env bash
set -euo pipefail
BASE="/root/.openclaw/workspace/ops/llm-audit"
REPORT="$BASE/latest_report_v3.json"
LOG="$BASE/latest_report_v3.log"
ALERTS="$BASE/alerts.log"
STAMP="$BASE/last_alert_fingerprint.txt"
/usr/bin/python3 "$BASE/audit_llm_overrides_v3.py" > "$REPORT" 2> "$LOG" || {
  fingerprint="$(sha256sum "$LOG" | awk '{print $1}')"
  last=""
  [ -f "$STAMP" ] && last="$(cat "$STAMP")"
  if [ "$fingerprint" != "$last" ]; then
    printf '%s\n' "$fingerprint" > "$STAMP"
    printf '⚠️ Auditoria de LLM encontrou modelo proibido em produção. Verifique %s e %s.\n' "$REPORT" "$LOG" >> "$ALERTS"
    /usr/bin/python3 - <<'PY'
from message import send
send(channel='telegram', target='971050173', message='⚠️ Auditoria de LLM encontrou modelo proibido em produção. Verifique latest_report_v3.json e latest_report_v3.log no diretório /root/.openclaw/workspace/ops/llm-audit/.')
PY
  fi
}
