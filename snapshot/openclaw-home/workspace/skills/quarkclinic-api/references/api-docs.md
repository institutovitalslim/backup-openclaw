# Quarkclinic API Reference

Source of truth:
- Swagger UI: [https://api.quark.tec.br/clinic/ext/swagger-ui.html#/](https://api.quark.tec.br/clinic/ext/swagger-ui.html#/)
- OpenAPI JSON: [https://api.quark.tec.br/clinic/ext/v2/api-docs](https://api.quark.tec.br/clinic/ext/v2/api-docs)

Base URL:

```text
https://api.quark.tec.br/clinic/ext
```

Authentication:

- Most read endpoints require `Auth-token`.
- Common write endpoints also require `X-Chave-Key` and `X-Secret-Key`.
- The Swagger description states that all requests must include the client access token in the `Auth-Token` header. The path-level parameter names are shown as `Auth-token`, so the client sends `Auth-token` consistently.

Core tags in the spec:

- `agenda`
- `agendamento`
- `conta-pagar`
- `conta-receber`
- `financeiro`
- `lancamento`
- `negociacao`
- `orcamento`
- `organizacao`
- `paciente`
- `partner`
- `procedimento`
- `produto`
- `profissional`
- `usuario`

Useful read endpoints:

- `GET /v1/clinicas`
- `GET /v1/agendas`
- `GET /v1/agendas/{id}`
- `GET /v1/agendas/{id}/horarios-livres`
- `GET /v1/agendamentos`
- `GET /v1/agendamentos/{id}`
- `GET /v1/pacientes`
- `GET /v1/pacientes/{id}`
- `GET /v1/procedimentos`
- `GET /v1/profissionais`
- `GET /v1/usuarios`
- `GET /v1/orcamentos`
- `GET /v1/contas/receber`
- `GET /v1/contas/pagar`
- `GET /v1/financeiro/formas-pagamento`
- `GET /v1/financeiro/formas-recebimento`

Useful write endpoints:

- `POST /v1/pacientes`
- `POST /v1/agendamentos`
- `PATCH /v1/agendamentos/{id}/confirmar`
- `PATCH /v1/agendamentos/{id}/cancelar`
- `POST /v1/agendamentos/{id}/mudar-status`

Important request notes:

- List endpoints are paginated; page 1 is default and the docs mention up to 100 records per page.
- `GET /v1/agendamentos` requires:
  - `data_agendamento_inicio` in `dd-MM-yyyy`
  - `data_agendamento_fim` in `dd-MM-yyyy`
- The agendamento date window is limited to 30 days.
- `GET /v1/contas/pagar` and `GET /v1/contas/receber` accept date filters such as `dataInicio` and `dataFim`.

Practical examples:

```bash
python3 scripts/quarkclinic_api.py GET /v1/clinicas
python3 scripts/quarkclinic_api.py GET /v1/pacientes --query page=1
python3 scripts/quarkclinic_api.py GET /v1/agendamentos --query data_agendamento_inicio=01-03-2026 --query data_agendamento_fim=26-03-2026
python3 scripts/quarkclinic_api.py GET /v1/contas/receber --query dataInicio=01-03-2026 --query dataFim=26-03-2026
python3 scripts/quarkclinic_api.py POST /v1/pacientes --write-ok --body @novo-paciente.json
```
