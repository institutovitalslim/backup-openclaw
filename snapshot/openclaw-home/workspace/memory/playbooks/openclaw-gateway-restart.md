# OpenClaw Gateway Restart

## Regra
- Nesta VPS, o gateway roda como user service do systemd, nao como unit de sistema.
- O comando correto de reinicio e `systemctl --user restart openclaw-gateway.service`.
- Nao usar `systemctl restart openclaw-gateway.service`, porque a unit nao existe no escopo de sistema.

## Validacao Rapida
1. `systemctl --user is-active openclaw-gateway.service`
2. `systemctl --user --no-pager --full status openclaw-gateway.service`
3. `openclaw health`

## Pistas Operacionais
- Unit file: `/root/.config/systemd/user/openclaw-gateway.service`
- Drop-in: `/root/.config/systemd/user/openclaw-gateway.service.d/10-1password-service-account.conf`
- ExecStartPre atual: `/root/.openclaw/bin/refresh-runtime-from-1password.sh`
- Processo principal observado apos restart: `openclaw` pai de `openclaw-gateway`

## Confirmacao Validada Em 2026-03-31
- `systemctl --user restart openclaw-gateway.service` funcionou.
- `openclaw health` respondeu com Telegram ok.
- Logs do gateway mostraram `agent model: anthropic/claude-sonnet-4-6` apos o restart.
