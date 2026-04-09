#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

load_1password_service_account() {
  if [[ -n "${OP_SERVICE_ACCOUNT_TOKEN:-}" ]]; then
    return 0
  fi
  if [[ -f "/root/.openclaw/.op.service-account.env" ]]; then
    set -a && source /root/.openclaw/.op.service-account.env && set +a
  fi
}

read_github_token() {
  if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    printf '%s' "$GITHUB_TOKEN"
    return 0
  fi
  command -v op >/dev/null 2>&1 || return 1
  load_1password_service_account
  op read 'op://openclaw/token github/password' 2>/dev/null
}

git_push_with_1password_token() {
  local remote_url token auth_header
  remote_url="$(git remote get-url origin)"
  if [[ ! "$remote_url" =~ ^https://github\.com/ ]]; then
    git push origin main
    return
  fi
  token="$(read_github_token || true)"
  if [[ -z "$token" ]]; then
    git push origin main
    return
  fi
  auth_header="$(printf '%s' "x-access-token:${token}" | base64 | tr -d '\r\n')"
  git -c http.https://github.com/.extraheader="AUTHORIZATION: basic ${auth_header}" push origin main
}

./scripts/backup-openclaw-linux.sh "${1:-/root/.openclaw}"
git add README.md scripts snapshot
if git diff --cached --quiet; then
  echo "Sem alteracoes para publicar."
  exit 0
fi
git commit -m "Daily OpenClaw backup $(date -u +%F)"
git_push_with_1password_token
