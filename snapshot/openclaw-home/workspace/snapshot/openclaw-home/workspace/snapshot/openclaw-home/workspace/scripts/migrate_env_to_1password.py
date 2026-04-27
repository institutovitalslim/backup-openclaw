#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ENV_PATH = Path('~/.openclaw/.env').expanduser()

if not ENV_PATH.exists():
    raise SystemExit(f"Env file not found: {ENV_PATH}")

raw = {}
for line in ENV_PATH.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    if '=' not in line:
        continue
    key, value = line.split('=', 1)
    raw[key.strip()] = value.strip()

services = [
    {
        "env_key": "OPENAI_API_KEY",
        "title": "OpenAI API Key",
        "username": "openai",
        "hostname": "api.openai.com",
        "tags": ["openclaw", "openai", "api"],
        "notes": "Env var: OPENAI_API_KEY"
    },
    {
        "env_key": "ANTHROPIC_API_KEY",
        "title": "Anthropic API Key",
        "username": "anthropic",
        "hostname": "api.anthropic.com",
        "tags": ["openclaw", "anthropic", "api"],
        "notes": "Env var: ANTHROPIC_API_KEY"
    },
    {
        "env_key": "TELEGRAM_BOT_TOKEN",
        "title": "Telegram Bot Token",
        "username": "telegram",
        "hostname": "api.telegram.org",
        "tags": ["openclaw", "telegram"],
        "notes": "Env var: TELEGRAM_BOT_TOKEN"
    },
    {
        "env_key": "MATON_API_KEY",
        "title": "Maton API Key",
        "username": "maton",
        "hostname": "gateway.maton.ai",
        "tags": ["openclaw", "maton", "api"],
        "notes": "Env var: MATON_API_KEY"
    },
    {
        "env_key": "ZAPI_INSTANCE_ID",
        "title": "Z-API Instance ID",
        "username": "zapi",
        "hostname": "api.z-api.io",
        "tags": ["openclaw", "zapi"],
        "notes": "Env var: ZAPI_INSTANCE_ID"
    },
    {
        "env_key": "ZAPI_TOKEN",
        "title": "Z-API Token",
        "username": "zapi",
        "hostname": "api.z-api.io",
        "tags": ["openclaw", "zapi"],
        "notes": "Env var: ZAPI_TOKEN"
    },
    {
        "env_key": "ZAPI_CLIENT_TOKEN",
        "title": "Z-API Client Token",
        "username": "zapi",
        "hostname": "api.z-api.io",
        "tags": ["openclaw", "zapi"],
        "notes": "Env var: ZAPI_CLIENT_TOKEN"
    }
]

missing = [s["env_key"] for s in services if s["env_key"] not in raw]
if missing:
    print("[WARN] Missing keys:", ", ".join(sorted(set(missing))))

result = subprocess.run([
    "op", "item", "list", "--vault", "openclaw", "--format", "json"
], capture_output=True, text=True, check=True)
existing_titles = {item["title"] for item in json.loads(result.stdout or "[]")}

created = []
skipped = []

def run_create(payload):
    subprocess.run([
        "op", "item", "create", "--vault", "openclaw", "-"
    ], input=json.dumps(payload), text=True, check=True, stdout=subprocess.DEVNULL)

for svc in services:
    value = raw.get(svc["env_key"])
    if not value:
        skipped.append((svc["title"], "missing env"))
        continue
    if svc["title"] in existing_titles:
        skipped.append((svc["title"], "already exists"))
        continue
    payload = {
        "title": svc["title"],
        "category": "API_CREDENTIAL",
        "tags": svc.get("tags", []),
        "fields": [
            {
                "id": "notesPlain",
                "type": "STRING",
                "purpose": "NOTES",
                "label": "notesPlain",
                "value": svc["notes"]
            },
            {
                "id": "username",
                "type": "STRING",
                "label": "username",
                "value": svc["username"]
            },
            {
                "id": "credential",
                "type": "CONCEALED",
                "label": "credential",
                "value": value
            },
            {
                "id": "type",
                "type": "MENU",
                "label": "type",
                "value": "token"
            },
            {
                "id": "hostname",
                "type": "STRING",
                "label": "hostname",
                "value": svc.get("hostname", "")
            }
        ],
        "sections": [
            {
                "label": "Metadata",
                "fields": [
                    {
                        "type": "STRING",
                        "label": "Env Var",
                        "value": svc["env_key"]
                    }
                ]
            }
        ]
    }
    run_create(payload)
    created.append(svc["title"])

print("[INFO] Created", len(created), "items")
for title in created:
    print(" -", title)
if skipped:
    print("[INFO] Skipped:")
    for title, reason in skipped:
        print(f" - {title}: {reason}")
