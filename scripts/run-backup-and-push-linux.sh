#!/usr/bin/env bash
set -euo pipefail

unset GH_TOKEN

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

./scripts/backup-openclaw-linux.sh "${1:-/root/.openclaw}"

git add README.md scripts snapshot .gitattributes .gitignore

if git diff --cached --quiet; then
  echo "Sem alteracoes para publicar."
  exit 0
fi

git commit -m "Daily OpenClaw backup $(date -u +%F)"
git push origin main
