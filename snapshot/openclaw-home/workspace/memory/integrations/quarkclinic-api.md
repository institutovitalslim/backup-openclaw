# Integracao Quarkclinic API

- Skill operacional da VPS: `/root/.openclaw/workspace/skills/quarkclinic-api`
- Cliente principal: `/root/.openclaw/workspace/skills/quarkclinic-api/scripts/quarkclinic_api.py`
- Referencia enxuta da API: `/root/.openclaw/workspace/skills/quarkclinic-api/references/api-docs.md`
- Fonte documental oficial:
  - `https://api.quark.tec.br/clinic/ext/swagger-ui.html#/`
  - `https://api.quark.tec.br/clinic/ext/v2/api-docs`

## Como usar

- Validar credenciais sem expor segredos:
  - `python3 /root/.openclaw/workspace/skills/quarkclinic-api/scripts/quarkclinic_api.py --check`
- Fazer leitura simples:
  - `python3 /root/.openclaw/workspace/skills/quarkclinic-api/scripts/quarkclinic_api.py GET /v1/clinicas`
- Consultar agendamentos:
  - `python3 /root/.openclaw/workspace/skills/quarkclinic-api/scripts/quarkclinic_api.py GET /v1/agendamentos --query data_agendamento_inicio=01-03-2026 --query data_agendamento_fim=26-03-2026`
- Sugerir horarios livres proximos e tentar agendar:
  - `python3 /root/.openclaw/workspace/skills/quarkclinic-api/scripts/quarkclinic_booking_assistant.py --agenda-id 240623539 --unidade-id 227138348 --paciente-id 240621965 --convenio-id 148 --especialidade-id 67 --procedimento-id 240622606 --telefone "(71) 99896-8887" --data 27/03/2026 --hora-preferida 10:00 --book`
- Conferir homonimos antes do agendamento:
  - `python3 /root/.openclaw/workspace/skills/quarkclinic-api/scripts/quarkclinic_booking_assistant.py --agenda-id 240623539 --unidade-id 227138348 --paciente-id 240621965 --paciente-nome "Tiaro Fernandes Neves" --convenio-id 148 --especialidade-id 67 --procedimento-id 240622606 --telefone "(71) 99896-8887" --data 27/03/2026 --hora-preferida 10:00`

## Autenticacao

- Leitura usa `Auth-token`.
- Escrita usa `Auth-token`, `X-Chave-Key` e `X-Secret-Key`.
- Ordem de resolucao das credenciais:
  - variaveis de ambiente
  - `/root/.openclaw/quarkclinic.env`
  - item 1Password `Dados Acesso API Quarckclinic` se o `op` da VPS tiver acesso ao vault correto

## Estado Atual

- A skill esta instalada e validada na VPS.
- Existe um espelho do item `Dados Acesso API Quarckclinic` no vault `openclaw` da VPS.
- A skill agora prefere 1Password como fonte primaria e usa `/root/.openclaw/quarkclinic.env` apenas como fallback.
- `GET /v1/clinicas` foi validado com sucesso na VPS usando `1password:Dados Acesso API Quarckclinic`.
- O fluxo de agendamento precisa usar o inicio exato de um slot livre. Exemplo real: o pedido `10:00` falhou e `09:57` foi aceito para a mesma janela livre.
- A API de pacientes pode retornar busca ampla; por isso a skill filtra localmente e, quando houver homonimos, exige confirmacao por sobrenome/ID antes de marcar.
