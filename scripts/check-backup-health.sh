#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

MAX_BACKUP_AGE_HOURS="${MAX_BACKUP_AGE_HOURS:-30}"
MAX_LOG_AGE_HOURS="${MAX_LOG_AGE_HOURS:-30}"

SNAPSHOT_ROOT="$REPO_ROOT/snapshot/openclaw-home"
SUMMARY_FILE="$REPO_ROOT/snapshot/metadata/summary.json"
CRON_LOG="$REPO_ROOT/logs/cron.log"
HEALTH_LOG="$REPO_ROOT/logs/backup-health.log"

mkdir -p "$REPO_ROOT/logs"

failures=()
now_epoch="$(date +%s)"

record_failure() {
  failures+=("$1")
}

file_age_hours() {
  local path="$1"
  local mtime
  mtime="$(stat -c %Y "$path")"
  echo $(( (now_epoch - mtime) / 3600 ))
}

check_exists() {
  local path="$1"
  local label="$2"
  if [[ ! -e "$path" ]]; then
    record_failure "${label} ausente: ${path}"
    return 1
  fi
  return 0
}

check_exists "$SNAPSHOT_ROOT" "snapshot root" || true
check_exists "$SUMMARY_FILE" "summary" || true
check_exists "$CRON_LOG" "cron log" || true

if [[ -f "$SUMMARY_FILE" ]]; then
  summary_age="$(file_age_hours "$SUMMARY_FILE")"
  if (( summary_age > MAX_BACKUP_AGE_HOURS )); then
    record_failure "ultimo backup muito antigo: ${summary_age}h"
  fi
fi

if [[ -f "$CRON_LOG" ]]; then
  cron_log_age="$(file_age_hours "$CRON_LOG")"
  if (( cron_log_age > MAX_LOG_AGE_HOURS )); then
    record_failure "log do cron muito antigo: ${cron_log_age}h"
  fi

  recent_log="$(tail -n 80 "$CRON_LOG" 2>/dev/null || true)"

  if ! printf '%s\n' "$recent_log" | grep -q "Backup OpenClaw concluido"; then
    record_failure "trecho recente do log nao contem confirmacao de conclusao"
  fi

  if printf '%s\n' "$recent_log" | grep -Eq "Repository rule violations|failed to push some refs|Permission denied|fatal:"; then
    record_failure "trecho recente do log contem erro de push ou autenticacao"
  fi
fi

if [[ -d "$SNAPSHOT_ROOT" ]]; then
  while IFS= read -r forbidden; do
    record_failure "arquivo sensivel presente no snapshot: ${forbidden}"
  done < <(find "$SNAPSHOT_ROOT" \( -name 'client_secret_gog_desktop.json' -o -path '*/tmp/*' \) -print)
fi

head_commit_time="$(git log -1 --format=%ct 2>/dev/null || echo 0)"
if [[ "$head_commit_time" =~ ^[0-9]+$ ]] && (( head_commit_time > 0 )); then
  head_age_hours=$(( (now_epoch - head_commit_time) / 3600 ))
  if (( head_age_hours > MAX_BACKUP_AGE_HOURS )); then
    record_failure "ultimo commit de backup muito antigo: ${head_age_hours}h"
  fi
else
  record_failure "nao foi possivel ler o ultimo commit git"
fi

status="OK"
if (( ${#failures[@]} > 0 )); then
  status="FAIL"
fi

timestamp="$(date -u +%FT%TZ)"
{
  echo "[${timestamp}] backup-health=${status}"
  if (( ${#failures[@]} == 0 )); then
    echo "checks: snapshot, summary, cron log recente, commit recente, arquivos proibidos"
  else
    printf 'failures:\n'
    printf -- '- %s\n' "${failures[@]}"
  fi
} | tee -a "$HEALTH_LOG"

if (( ${#failures[@]} > 0 )); then
  exit 1
fi
