# WhatsApp Patient Context

Antes de responder pacientes vindos do WhatsApp, consulte o contexto consolidado no Apps Script.

## Endpoint base
https://script.google.com/macros/s/AKfycbzYxq7c7z1Es_jDqktNeV_TaYCU6SBymd932Vk8XB85Pmd5zwiQRUeIfn7PjYVDev7vEA/exec

## Como consultar
1. Identifique o telefone do paciente em formato numerico com DDI, sem simbolos.
2. Consulte `?phone=NUMERO`.
3. Se `found=true`, leia `summary` e `last_10_messages` antes de responder.
4. Se `found=false`, responda normalmente, mas considere que ainda nao ha contexto consolidado.

## Endpoints auxiliares
- `?list=1` lista pacientes disponiveis.
- `?q=trecho` busca por nome ou telefone parcial.

## Regras de resposta
- Responda com continuidade, usando o historico como contexto.
- Nao invente fatos ausentes no historico.
- Em temas clinicos e de agendamento, priorize clareza, continuidade e seguranca.
