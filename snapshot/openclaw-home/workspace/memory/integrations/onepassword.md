# onepassword.md - 1Password

- O bot deve usar apenas `OP_SERVICE_ACCOUNT_TOKEN`.
- O vault padrao para leituras por titulo e `openclaw`, salvo override em `OPENCLAW_1P_DEFAULT_VAULT`.
- Nunca usar `op signin`, `op account add`, senha-mestra, Touch ID ou aprovacao manual.
- Se `OP_SERVICE_ACCOUNT_TOKEN` nao estiver carregado, o bot deve reportar falta de ambiente e parar.
- Para ler itens diretamente, preferir `/root/.openclaw/bin/op-safe-read.sh`.
- Segredos continuam sendo injetados em `/root/.openclaw/.env.runtime` via `op inject`.
