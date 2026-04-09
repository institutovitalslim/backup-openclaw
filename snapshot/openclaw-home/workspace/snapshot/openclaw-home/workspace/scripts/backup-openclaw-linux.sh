#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_HOME="${1:-/root/.openclaw}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SNAPSHOT_ROOT="$REPO_ROOT/snapshot/openclaw-home"
METADATA_ROOT="$REPO_ROOT/snapshot/metadata"
CONFIG_ROOT="$SNAPSHOT_ROOT/config"
WORKSPACE_ROOT="$SNAPSHOT_ROOT/workspace"

if [[ ! -d "$OPENCLAW_HOME" ]]; then
  echo "Diretorio OpenClaw nao encontrado: $OPENCLAW_HOME" >&2
  exit 1
fi

rm -rf "$SNAPSHOT_ROOT" "$METADATA_ROOT"
mkdir -p "$CONFIG_ROOT/cron" "$WORKSPACE_ROOT" "$METADATA_ROOT"

if [[ -f "$OPENCLAW_HOME/openclaw.json" ]]; then
  cp "$OPENCLAW_HOME/openclaw.json" "$CONFIG_ROOT/openclaw.json"
fi

if [[ -f "$OPENCLAW_HOME/cron/jobs.json" ]]; then
  cp "$OPENCLAW_HOME/cron/jobs.json" "$CONFIG_ROOT/cron/jobs.json"
fi

rsync -a --delete \
  --exclude='.git/' \
  --exclude='.openclaw/' \
  --exclude='**/node_modules/' \
  --exclude='**/venv/' \
  --exclude='**/__pycache__/' \
  --exclude='**/.pytest_cache/' \
  --exclude='**/.mypy_cache/' \
  --exclude='**/.next/' \
  --exclude='**/dist/' \
  --exclude='**/build/' \
  --exclude='**/*.pyc' \
  "$OPENCLAW_HOME/workspace/" "$WORKSPACE_ROOT/"

find "$SNAPSHOT_ROOT" -mindepth 1 | LC_ALL=C sort > "$METADATA_ROOT/inventory.txt"

python3 - "$OPENCLAW_HOME" "$SNAPSHOT_ROOT" "$METADATA_ROOT/summary.json" <<'PY'
import json
import sys
from datetime import datetime, timezone

openclaw_home, snapshot_root, summary_path = sys.argv[1:]
summary = {
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "openclaw_home": openclaw_home,
    "snapshot_root": snapshot_root,
    "backup_scope": [
        "openclaw.json",
        "cron/jobs.json",
        "workspace/"
    ],
    "restore_with": "./scripts/restore-openclaw-linux.sh",
}
with open(summary_path, "w", encoding="utf-8") as fh:
    json.dump(summary, fh, indent=2)
PY

cat > "$METADATA_ROOT/excluded-paths.txt" <<'EOF'
workspace/.git/
workspace/.openclaw/
workspace/**/node_modules/
workspace/**/venv/
workspace/**/__pycache__/
workspace/**/.pytest_cache/
workspace/**/.mypy_cache/
workspace/**/.next/
workspace/**/dist/
workspace/**/build/
workspace/**/*.pyc
EOF

echo "Backup concluido em $SNAPSHOT_ROOT"
