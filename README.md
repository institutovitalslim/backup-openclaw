# Backup do OpenClaw / Codex Workplace

Este repositorio foi preparado para manter um backup versionavel da estrutura essencial do seu workplace, com foco principal no ambiente Linux da VPS em `/root/.openclaw` e suporte auxiliar ao ambiente Windows em `C:\Users\tiaro\.codex`.

O objetivo e restaurar rapidamente a configuracao principal em outra VPS ou computador, sem depender do estado local atual.

## Escopo principal: VPS Linux

O backup Linux foi reduzido para o escopo exato de redeploy:

- `openclaw.json`
- `cron/jobs.json`
- `workspace/`

Do workspace, ficam de fora apenas artefatos locais e dependencias reconstruiveis:

- `.git/`
- `.openclaw/`
- `node_modules/`
- `venv/`
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.next/`
- `dist/`
- `build/`
- `*.pyc`

## Escopo auxiliar: Windows

Tambem mantive scripts para snapshot do `CODEX_HOME` do Windows, com o mesmo principio de excluir autenticacao, sessoes e bancos temporarios.

## Estrutura

- `scripts/backup-openclaw-linux.sh`: gera um snapshot de `openclaw.json`, `cron/jobs.json` e `workspace/`
- `scripts/restore-openclaw-linux.sh`: restaura o snapshot Linux
- `scripts/run-backup-and-push-linux.sh`: gera backup e envia para o GitHub
- `scripts/install-cron-linux.sh`: instala o cron diario na VPS
- `scripts/backup-codex-windows.ps1`: gera um snapshot limpo em `snapshot/codex-home/`
- `scripts/restore-codex-windows.ps1`: restaura o snapshot para um novo `CODEX_HOME`
- `scripts/register-daily-backup-task.ps1`: registra uma tarefa diaria no Windows
- `scripts/publish-to-github.ps1`: publica ou atualiza este backup no repositorio remoto
- `snapshot/openclaw-home/`: copia versionavel das configuracoes e do workspace Linux
- `snapshot/codex-home/`: copia versionavel do ambiente Windows

## Como gerar o backup manualmente na VPS

```bash
./scripts/backup-openclaw-linux.sh
```

## Como registrar o backup diario na VPS

```bash
./scripts/install-cron-linux.sh
```

Por padrao, o cron roda todos os dias as `03:00` e executa `backup + commit + push`.

## Como restaurar em outra VPS Linux

1. Clone ou copie este repositorio para a nova maquina.
2. Execute:

```bash
./scripts/restore-openclaw-linux.sh
```

3. Refaça segredos e integracoes externas manualmente se necessario.

## Como gerar o backup manualmente no Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\backup-codex-windows.ps1
```

## Publicacao no GitHub

Se `git` estiver disponivel no ambiente:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\publish-to-github.ps1
```

Se o ambiente nao tiver `git`, este repositorio ainda continua util localmente e pode ser publicado depois em qualquer maquina com acesso ao GitHub.
