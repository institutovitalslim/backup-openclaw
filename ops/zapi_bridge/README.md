# Z-API → Clara Bridge

Bridge HTTP local para:
1. receber webhook da Z-API
2. fan-out opcional para o Apps Script atual
3. chamar a Clara via OpenClaw Gateway HTTP
4. responder de volta pelo Z-API

## Decisão técnica validada

O caminho confiável para invocar a Clara **não é** `openclaw agent` via CLI.
O caminho validado é o **Gateway HTTP local** com:

- `POST /v1/responses` ou `POST /v1/chat/completions`
- `x-openclaw-session-key` estável por paciente/número
- `x-openclaw-model: openai/gpt-5.4`

### Por que o header de modelo é obrigatório aqui

Sem forçar o modelo disponível, o OpenClaw pode tentar o default do agente, falhar na primeira tentativa e entrar no fallback que injeta:

> Continue where you left off. The previous model attempt failed or timed out.

Isso parecia “prompt contaminado”, mas a causa raiz era **fallback automático de modelo**.

## Arquivos

- `zapi_clara_bridge.py` — serviço HTTP simples em Python stdlib
- `zapi_bridge.env.example` — template de variáveis de ambiente
- `~/.config/systemd/user/zapi-clara-bridge.service` — unit file user-level

## Variáveis de ambiente

### OpenClaw
- `OPENCLAW_GATEWAY_TOKEN` **obrigatória**
- `OPENCLAW_GATEWAY_URL` default: `http://127.0.0.1:18789/v1/responses`
- `OPENCLAW_AGENT_REF` default: `openclaw/main`
- `OPENCLAW_MODEL_OVERRIDE` default: `openai/gpt-5.4`
- `OPENCLAW_SESSION_PREFIX` default: `bridge:zapi`

### Z-API
- `ZAPI_CLIENT_TOKEN` **obrigatória**
- `ZAPI_BASE_URL` **ou** (`ZAPI_INSTANCE_ID` + `ZAPI_TOKEN`)
- `ZAPI_SEND_TEXT_PATH` default: `/send-text`

### Fan-out / segurança
- `APPS_SCRIPT_FANOUT_URL` opcional
- `BRIDGE_SHARED_SECRET` opcional

### Runtime
- `BRIDGE_HOST` default: `127.0.0.1`
- `BRIDGE_PORT` default: `8787`
- `DEDUP_TTL_SECONDS` default: `600`
- `HTTP_TIMEOUT_SECONDS` default: `90`

## Subida manual

```bash
cd /root/.openclaw/workspace
export OPENCLAW_GATEWAY_TOKEN='...'
export ZAPI_INSTANCE_ID='...'
export ZAPI_TOKEN='...'
export ZAPI_CLIENT_TOKEN='...'
export APPS_SCRIPT_FANOUT_URL='https://script.google.com/macros/s/.../exec'
python3 ops/zapi_bridge/zapi_clara_bridge.py
```

## Health check

```bash
curl http://127.0.0.1:8787/healthz
```

## Teste local do webhook

```bash
curl -X POST http://127.0.0.1:8787/webhook \
  -H 'Content-Type: application/json' \
  -d '{
    "messageId": "test-1",
    "phone": "557186968887",
    "text": {"message": "Oi, preciso remarcar minha consulta."}
  }'
```

## Regras do serviço

- ignora mensagens `fromMe`
- ignora grupos
- ignora payload sem telefone
- ignora payload não-textual/vazio
- deduplica por `messageId`
- respeita `NO_REPLY`
- responde com sessão estável por telefone (`bridge:zapi:<telefone>`)

## Subida via systemd user-level

```bash
cp /root/.openclaw/workspace/ops/zapi_bridge/zapi_bridge.env.example \
   /root/.openclaw/workspace/ops/zapi_bridge/zapi_bridge.env

# editar os valores reais
systemctl --user daemon-reload
systemctl --user enable --now zapi-clara-bridge.service
systemctl --user status zapi-clara-bridge.service
```

## Próximo passo recomendado

Apontar o webhook da Z-API para:

- `https://<host-ou-proxy>/webhook`

mantendo o Apps Script como fan-out paralelo, não como substituto.
