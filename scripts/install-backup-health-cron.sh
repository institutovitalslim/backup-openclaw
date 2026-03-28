#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HEALTH_CHECK_SCRIPT="$REPO_ROOT/scripts/check-backup-health.sh"

mkdir -p "$REPO_ROOT/logs"
chmod +x "$HEALTH_CHECK_SCRIPT"

CRON_CMD="30 4 * * * $HEALTH_CHECK_SCRIPT >/dev/null 2>&1"

TMP_FILE="$(mktemp)"
crontab -l 2>/dev/null | grep -v 'check-backup-health.sh' > "$TMP_FILE" || true
printf '%s\n' "$CRON_CMD" >> "$TMP_FILE"
crontab "$TMP_FILE"
rm -f "$TMP_FILE"

echo "Cron de health-check instalado diariamente as 04:30 em $REPO_ROOT"
