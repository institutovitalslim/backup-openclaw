#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CRON_CMD="0 3 * * * cd $REPO_ROOT && ./scripts/run-backup-and-push-linux.sh >> $REPO_ROOT/snapshot/metadata/cron.log 2>&1"

TMP_FILE="$(mktemp)"
crontab -l 2>/dev/null | grep -v 'run-backup-and-push-linux.sh' > "$TMP_FILE" || true
printf '%s\n' "$CRON_CMD" >> "$TMP_FILE"
crontab "$TMP_FILE"
rm -f "$TMP_FILE"

echo "Cron diario instalado para 03:00 em $REPO_ROOT"
