#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$REPO_ROOT/logs"
LOG_FILE="$LOG_DIR/cron.log"
mkdir -p "$LOG_DIR"
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"
if [[ -f "/root/.openclaw/.op.service-account.env" ]]; then
  set -a && source /root/.openclaw/.op.service-account.env && set +a
fi
exec >>"$LOG_FILE" 2>&1
echo "[$(date -u +%FT%TZ)] Iniciando backup OpenClaw via cron"
cd "$REPO_ROOT"
./scripts/run-backup-and-push-linux.sh "${1:-/root/.openclaw}"
echo "[$(date -u +%FT%TZ)] Backup OpenClaw concluido"
