#!/usr/bin/env bash
set -euo pipefail

if [[ -f "/root/.openclaw/.op.service-account.env" ]]; then
  set -a && source /root/.openclaw/.op.service-account.env && set +a
fi

: "${OP_SERVICE_ACCOUNT_TOKEN:?OP_SERVICE_ACCOUNT_TOKEN is required}"
PUBKEY="$(op read 'op://openclaw/OpenClaw VPS Backup SSH Key/public key')"

mkdir -p /root/.ssh
chmod 700 /root/.ssh
touch /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

if ! grep -Fqx "$PUBKEY" /root/.ssh/authorized_keys; then
  printf '%s\n' "$PUBKEY" >> /root/.ssh/authorized_keys
  echo "Chave SSH adicionada."
else
  echo "Chave SSH ja presente."
fi
