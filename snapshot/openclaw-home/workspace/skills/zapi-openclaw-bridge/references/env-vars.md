# Environment Variables

Typical variables for a Z-API ↔ OpenClaw bridge:

## Z-API
- `ZAPI_BASE_URL`
- `ZAPI_INSTANCE_ID`
- `ZAPI_TOKEN`
- `ZAPI_CLIENT_TOKEN`
- `ZAPI_WEBHOOK_TOKEN`

## OpenClaw
- `OPENCLAW_GATEWAY_URL`
- `OPENCLAW_GATEWAY_TOKEN`
- `OPENCLAW_MODEL`
- `OPENCLAW_SESSION_PREFIX`

## Concierge files
- `CLARA_SYSTEM_PROMPT_FILE`
- `CLARA_CONTROL_FILE`
- `CLARA_LEADS_FILE`
- `CLARA_ACTIVATION_PHRASE`

## Optional business integrations
- `QUARKCLINIC_BASE_URL`
- `QUARKCLINIC_AUTH_TOKEN`
- `CLARA_NOTIFY_PHONE`
- `APPS_SCRIPT_FANOUT_URL`

## Rule
Document variables in examples, but never commit live secrets.
