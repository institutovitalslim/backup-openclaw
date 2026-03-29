# 1password-access.md - Playbook

## Regra principal
- 1Password no OpenClaw e "service account only".

## Fluxo correto
1. Verificar se `OP_SERVICE_ACCOUNT_TOKEN` esta carregado.
2. Usar `/root/.openclaw/bin/op-safe-read.sh` para `item get`, `read` ou `inject`.
3. Em `item get`, informar `--vault` ou deixar o wrapper aplicar o vault padrao `openclaw`.
4. Se o item nao estiver acessivel, informar falta de permissao ou vault incorreto.

## Fluxo proibido
- Nao pedir senha-mestra.
- Nao iniciar `op signin`.
- Nao solicitar aprovacao no app desktop.
- Nao sugerir Touch ID em servidor.
- Service account atual do OpenClaw: `OpenClaw Connect - IVS`; nao voltar para `openclaw-gateway-sa`.
