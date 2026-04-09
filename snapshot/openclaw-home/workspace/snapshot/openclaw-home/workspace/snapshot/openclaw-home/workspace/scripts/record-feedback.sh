#!/usr/bin/env bash
set -euo pipefail

ROOT="${FEEDBACK_ROOT:-/root/.openclaw/workspace/memory/feedback_loops}"
DATE="${DATE:-$(date +%F)}"

if [[ $# -lt 5 ]]; then
  echo "Usage: $0 <domain> <decision> <weight> <context> <reason> [tags_csv] [applies_to_csv]" >&2
  exit 1
fi

DOMAIN="$1"
DECISION="$2"
WEIGHT="$3"
CONTEXT="$4"
REASON="$5"
TAGS_CSV="${6:-}"
APPLIES_TO_CSV="${7:-}"

read -r -a TAGS <<<"$(printf '%s' "$TAGS_CSV" | tr ',' ' ')"
read -r -a APPLIES_TO <<<"$(printf '%s' "$APPLIES_TO_CSV" | tr ',' ' ')"

python3 /root/.openclaw/workspace/scripts/feedback_loops.py \
  --root "$ROOT" \
  append \
  --date "$DATE" \
  --domain "$DOMAIN" \
  --context "$CONTEXT" \
  --decision "$DECISION" \
  --reason "$REASON" \
  --tags "${TAGS[@]}" \
  --source manual \
  --applies-to "${APPLIES_TO[@]}" \
  --weight "$WEIGHT"

