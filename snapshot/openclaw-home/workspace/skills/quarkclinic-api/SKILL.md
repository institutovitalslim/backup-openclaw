---
name: quarkclinic-api
description: Use this skill for Quarkclinic or Quarckclinic API tasks, including reading pacientes, agendamentos, agendas, profissionais, clinicas, procedimentos, contas e orcamentos from https://api.quark.tec.br/clinic/ext/. It provides a safe client for Auth-token based requests and guarded write operations that also require X-Chave-Key and X-Secret-Key.
---

# Quarkclinic API Skill

Use this skill when the user asks to consultar, integrar, auditar, extrair ou atualizar dados da API do Quarkclinic/Quarckclinic.

## Workflow

1. For endpoint selection or parameter details, read [references/api-docs.md](references/api-docs.md).
2. Prefer the bundled client instead of handwritten HTTP calls:

```bash
python3 scripts/quarkclinic_api.py --check
python3 scripts/quarkclinic_api.py GET /v1/pacientes --query page=1
python3 scripts/quarkclinic_api.py GET /v1/agendamentos --query data_agendamento_inicio=01-03-2026 --query data_agendamento_fim=26-03-2026
python3 scripts/quarkclinic_booking_assistant.py --agenda-id 240623539 --unidade-id 227138348 --paciente-id 240621965 --convenio-id 148 --especialidade-id 67 --procedimento-id 240622606 --telefone "(71) 99896-8887" --data 27/03/2026 --hora-preferida 10:00
python3 scripts/quarkclinic_booking_assistant.py --agenda-id 240623539 --unidade-id 227138348 --paciente-id 240621965 --paciente-nome "Tiaro Fernandes Neves" --convenio-id 148 --especialidade-id 67 --procedimento-id 240622606 --telefone "(71) 99896-8887" --data 27/03/2026 --hora-preferida 10:00
```

3. For agendamento, always check `/horarios-livres` first. Quarkclinic expects the exact start of a free interval, not an arbitrary minute inside that interval. Use `scripts/quarkclinic_booking_assistant.py` to suggest or attempt exact slots automatically.
4. Before booking, check for homonyms. If more than one patient matches the same name, ask for confirmation by surname and then use the confirmed patient ID.
5. Default to read-only requests. For `POST`, `PATCH`, `PUT`, or `DELETE`, require explicit user intent and pass `--write-ok`.
6. If a requested time is busy, suggest the closest free starts from the same date before giving up.
7. On the VPS, treat `/root/.openclaw/workspace` as the operational source of truth.

## Credential Sources

The client resolves credentials in this order:

1. Environment variables already present in the shell.
2. `/root/.openclaw/quarkclinic.env` or the file pointed to by `QUARKCLINIC_ENV_FILE`.
3. 1Password item `Dados Acesso API Quarckclinic` if `op` is authenticated and the item is reachable from the configured vault.

Supported environment variables:

- `QUARKCLINIC_AUTH_TOKEN`
- `QUARKCLINIC_X_CHAVE_KEY`
- `QUARKCLINIC_X_SECRET_KEY`
- `QUARKCLINIC_BASE_URL`
- `QUARKCLINIC_OP_ITEM`
- `QUARKCLINIC_OP_VAULT`

If the VPS service account cannot read the 1Password item yet, keep a synced file at `/root/.openclaw/quarkclinic.env` with the variables above.

## Safety Rules

- Do not print secrets back to the user.
- Do not mutate clinic data unless the user explicitly asked for the change.
- Agendamento creation and status changes require `Auth-token`, `X-Chave-Key`, and `X-Secret-Key`.
- Some list endpoints are paginated and default to page 1 with up to 100 records.
- Agendamento listing is limited to a 30-day scheduling window.

## Common Calls

Read-only:

```bash
python3 scripts/quarkclinic_api.py GET /v1/clinicas
python3 scripts/quarkclinic_api.py GET /v1/agendas
python3 scripts/quarkclinic_api.py GET /v1/profissionais
python3 scripts/quarkclinic_api.py GET /v1/procedimentos
python3 scripts/quarkclinic_api.py GET /v1/usuarios
python3 scripts/quarkclinic_api.py GET /v1/pacientes --query page=1
python3 scripts/quarkclinic_api.py GET /v1/contas/receber --query dataInicio=01-03-2026 --query dataFim=26-03-2026
```

Write operations:

```bash
python3 scripts/quarkclinic_api.py POST /v1/pacientes --write-ok --body @novo-paciente.json
python3 scripts/quarkclinic_api.py POST /v1/agendamentos --write-ok --body @agendamento.json
python3 scripts/quarkclinic_booking_assistant.py --agenda-id 240623539 --unidade-id 227138348 --paciente-id 240621965 --convenio-id 148 --especialidade-id 67 --procedimento-id 240622606 --telefone "(71) 99896-8887" --data 27/03/2026 --hora-preferida 10:00 --book
python3 scripts/quarkclinic_booking_assistant.py --agenda-id 240623539 --unidade-id 227138348 --paciente-id 240621965 --paciente-nome "Tiaro Fernandes Neves" --confirm-paciente-id 240621965 --convenio-id 148 --especialidade-id 67 --procedimento-id 240622606 --telefone "(71) 99896-8887" --data 27/03/2026 --hora-preferida 10:00 --book
```

## Troubleshooting

- Run `python3 scripts/quarkclinic_api.py --check` to confirm which credential source is active.
- If a user asks for a time like `10:00` but the free interval is `09:57 - 10:10`, use `09:57` for the actual `POST` and present nearby alternatives.
- If more than one patient matches the same name, present the candidate list with surname, ID and identifying fields before attempting the booking.
- If 1Password fails on the VPS, check whether the item is available to the service-account vault configured in `QUARKCLINIC_OP_VAULT`.
- If the API returns `401`, confirm the `Auth-token`.
- If a write request fails before sending, confirm `X-Chave-Key` and `X-Secret-Key`.
