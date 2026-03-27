#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="${1:-/root/.openclaw/workspace}"
MEMORY_ROOT="$WORKSPACE_ROOT/memory"
BACKUP_ROOT="$WORKSPACE_ROOT/memory_backups"
STAMP="${2:-$(date -u +%Y%m%dT%H%M%SZ)}"
TARGET_DIR="$BACKUP_ROOT/$STAMP"

mkdir -p "$TARGET_DIR"

copy_if_exists() {
  local src="$1"
  local dst_dir="$2"
  if [[ -e "$src" ]]; then
    cp -R "$src" "$dst_dir/"
  fi
}

copy_if_exists "$WORKSPACE_ROOT/MEMORY.md" "$TARGET_DIR"
copy_if_exists "$MEMORY_ROOT/MEMORY.md" "$TARGET_DIR"
copy_if_exists "$MEMORY_ROOT/context" "$TARGET_DIR"
copy_if_exists "$MEMORY_ROOT/projects" "$TARGET_DIR"
copy_if_exists "$MEMORY_ROOT/integrations" "$TARGET_DIR"
copy_if_exists "$MEMORY_ROOT/content/voice" "$TARGET_DIR/content"
copy_if_exists "$MEMORY_ROOT/feedback_loops" "$TARGET_DIR"

printf '%s\n' "$TARGET_DIR"

