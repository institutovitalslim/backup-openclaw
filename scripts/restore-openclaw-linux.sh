#!/usr/bin/env bash
set -euo pipefail

TARGET_OPENCLAW_HOME="${1:-/root/.openclaw}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SNAPSHOT_ROOT="$REPO_ROOT/snapshot/openclaw-home"

if [[ ! -d "$SNAPSHOT_ROOT" ]]; then
  echo "Snapshot nao encontrado em $SNAPSHOT_ROOT" >&2
  exit 1
fi

mkdir -p "$TARGET_OPENCLAW_HOME/cron" "$TARGET_OPENCLAW_HOME/workspace"

if [[ -f "$SNAPSHOT_ROOT/config/openclaw.json" ]]; then
  cp "$SNAPSHOT_ROOT/config/openclaw.json" "$TARGET_OPENCLAW_HOME/openclaw.json"
fi

if [[ -f "$SNAPSHOT_ROOT/config/cron/jobs.json" ]]; then
  cp "$SNAPSHOT_ROOT/config/cron/jobs.json" "$TARGET_OPENCLAW_HOME/cron/jobs.json"
fi

rsync -a "$SNAPSHOT_ROOT/workspace/" "$TARGET_OPENCLAW_HOME/workspace/"

echo "Restore concluido em $TARGET_OPENCLAW_HOME"
