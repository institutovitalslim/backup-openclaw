#!/usr/bin/env bash
set -euo pipefail
BASE="/root/.openclaw/workspace/ops/llm-audit"
/usr/bin/python3 "$BASE/audit_llm_overrides_v3.py" > "$BASE/latest_report_v3.json" 2> "$BASE/latest_report_v3.log" || {
  printf '⚠️ Auditoria de LLM encontrou modelo proibido em produção. Verifique %s e %s.\n' "$BASE/latest_report_v3.json" "$BASE/latest_report_v3.log" >> "$BASE/alerts.log"
}
