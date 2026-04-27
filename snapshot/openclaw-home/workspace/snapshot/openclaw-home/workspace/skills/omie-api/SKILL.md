---
name: omie-api
description: Use this skill for Omie ERP tasks, including financeiro (contas a pagar/receber, boletos, fluxo de caixa), servicos (OS, contratos, NFS-e), estoque (produtos, movimentacoes, compras) e CRM (contas, contatos, oportunidades, pipeline). Provides a safe client for API requests to https://app.omie.com.br/api/.
---

# Omie API Skill

Use this skill when the user asks to consultar, integrar, auditar, extrair ou atualizar dados do ERP Omie.

## Workflow

1. For endpoint selection or parameter details, read [references/api-docs.md](references/api-docs.md).
2. Prefer the bundled client instead of handwritten HTTP calls:

```bash
# Check connection
python3 scripts/omie_api.py --check

# Financeiro
python3 scripts/omie_api.py call financas/contapagar ListarContasPagar '{"pagina":1,"registros_por_pagina":20}'
python3 scripts/omie_api.py call financas/contareceber ListarContasReceber '{"pagina":1,"registros_por_pagina":20}'
python3 scripts/omie_api.py call financas/contareceberboleto ObterBoleto '{"nCodTitulo":123}'
python3 scripts/omie_api.py call financas/extrato ListarExtrato '{"dDtInicio":"01/01/2026","dDtFim":"31/03/2026"}'
python3 scripts/omie_api.py call financas/resumo ObterResumo '{}'

# Servicos
python3 scripts/omie_api.py call servicos/os ListarOS '{"pagina":1,"registros_por_pagina":20}'
python3 scripts/omie_api.py call servicos/os IncluirOS @nova-os.json --write-ok
python3 scripts/omie_api.py call servicos/contrato ListarContratos '{"pagina":1,"registros_por_pagina":20}'

# Estoque
python3 scripts/omie_api.py call estoque/consulta ListarPosEstoque '{"pagina":1,"registros_por_pagina":20}'
python3 scripts/omie_api.py call estoque/ajuste IncluirAjusteEstoque @ajuste.json --write-ok
python3 scripts/omie_api.py call geral/produtos ListarProdutos '{"pagina":1,"registros_por_pagina":20}'

# CRM
python3 scripts/omie_api.py call crm/contas ListarContas '{"pagina":1,"registros_por_pagina":20}'
python3 scripts/omie_api.py call crm/oportunidades ListarOportunidades '{"pagina":1,"registros_por_pagina":20}'
python3 scripts/omie_api.py call crm/contatos ListarContatos '{"pagina":1,"registros_por_pagina":20}'

# Cadastros Gerais
python3 scripts/omie_api.py call geral/clientes ListarClientes '{"pagina":1,"registros_por_pagina":20}'
python3 scripts/omie_api.py call geral/clientes IncluirCliente @cliente.json --write-ok
python3 scripts/omie_api.py call geral/categorias ListarCategorias '{"pagina":1,"registros_por_pagina":20}'
python3 scripts/omie_api.py call geral/contacorrente ListarContasCorrentes '{"pagina":1,"registros_por_pagina":20}'
```

3. Default to read-only requests. For write operations (Incluir, Alterar, Excluir), require explicit user intent and pass `--write-ok`.
4. All list endpoints are paginated. Always start with page 1 and check total_de_paginas for more data.
5. On the VPS, treat `/root/.openclaw/workspace` as the operational source of truth.

## Credential Sources

The client resolves credentials in this order:

1. Environment variables already present in the shell.
2. `/root/.openclaw/secure/omie_api.env` or the file pointed to by `OMIE_ENV_FILE`.
3. 1Password item `Acesso API OMIE` if `op` is authenticated and reachable.

Supported environment variables:

- `OMIE_APP_KEY`
- `OMIE_APP_SECRET`
- `OMIE_BASE_URL` (default: `https://app.omie.com.br/api/`)

## Safety Rules

- Do not print secrets back to the user.
- Do not mutate ERP data unless the user explicitly asked for the change.
- Write operations (IncluirContaPagar, IncluirOS, IncluirCliente, etc.) require `--write-ok` flag.
- Financial operations (baixa de titulos, exclusao de lancamentos) require double confirmation.
- Never delete financial records without explicit user confirmation.
- All list endpoints are paginated — always inform user of total pages/records.

## Common Queries

### Financeiro
```bash
# Listar contas a pagar pendentes
python3 scripts/omie_api.py call financas/contapagar ListarContasPagar '{"pagina":1,"registros_por_pagina":50,"filtrar_por_status":"ABERTO"}'

# Listar contas a receber
python3 scripts/omie_api.py call financas/contareceber ListarContasReceber '{"pagina":1,"registros_por_pagina":50}'

# Resumo financeiro
python3 scripts/omie_api.py call financas/resumo ObterResumo '{}'

# Gerar boleto
python3 scripts/omie_api.py call financas/contareceberboleto GerarBoleto '{"nCodTitulo":123}' --write-ok
```

### Servicos
```bash
# Listar OS abertas
python3 scripts/omie_api.py call servicos/os ListarOS '{"pagina":1,"registros_por_pagina":50}'

# Faturar OS
python3 scripts/omie_api.py call servicos/osp FaturarOS '{"nCodOS":123}' --write-ok
```

### Estoque
```bash
# Posicao de estoque
python3 scripts/omie_api.py call estoque/consulta ListarPosEstoque '{"pagina":1,"registros_por_pagina":50}'

# Movimentacoes
python3 scripts/omie_api.py call estoque/movestoque ListarMovimentos '{"pagina":1,"registros_por_pagina":50}'
```

### CRM
```bash
# Pipeline de oportunidades
python3 scripts/omie_api.py call crm/oportunidades ListarOportunidades '{"pagina":1,"registros_por_pagina":50}'

# Criar oportunidade
python3 scripts/omie_api.py call crm/oportunidades UpsertOportunidade @oportunidade.json --write-ok
```

## Empresa Configurada

- **Razao Social**: Medical Emagrecimento LTDA (Instituto Vital Slim)
- **CNPJ**: 40.289.526/0001-58
- **Cidade**: Lauro de Freitas/BA
- **Codigo Empresa Omie**: 6737587523

## Troubleshooting

- **401/403**: Verificar APP_KEY e APP_SECRET no 1Password ou env file.
- **Resposta vazia**: Confirmar que os parametros de paginacao estao corretos.
- **Timeout**: A API Omie tem limite de 3 requisicoes/segundo. O script ja faz throttle automatico.
- **Campo obrigatorio**: Consultar [references/api-docs.md](references/api-docs.md) para campos obrigatorios de cada endpoint.
