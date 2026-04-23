#!/bin/bash
set -euo pipefail
export OP_SERVICE_ACCOUNT_TOKEN=$(grep '^OP_SERVICE_ACCOUNT_TOKEN=' /root/.openclaw/.op.service-account.env | cut -d= -f2-)
export HOME=/root
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
cd /root/.openclaw/workspace
exec /usr/bin/python3 /root/.openclaw/workspace/ops/zapi_bridge/daily_clara_analysis.py >> /var/log/daily_clara_analysis.log 2>&1
