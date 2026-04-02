# Canva MCP

## Status
- Configurado via mcporter no host.
- Nome do servidor MCP: canva.
- Endpoint: https://mcp.canva.com/mcp.
- Auth: OAuth por usuario.
- Callback local do host: http://127.0.0.1:43100/callback.

## Como usar
- Quando o pedido envolver criar, editar, exportar ou localizar designs no Canva, usar a skill mcporter.
- Preferir comandos como:
  - mcporter list canva --schema
  - mcporter call canva.<tool> ...
- Se houver erro de autenticacao, executar mcporter config login canva --reset.

## Notas operacionais
- O Canva MCP e por usuario; nao existe service account global.
- A autenticacao depende de browser e callback local do host.
- Nesta maquina, o callback pode exigir tunel SSH local quando o login for iniciado a partir da VPS.

## Regra de Execucao
- Para tarefas no Canva, usar primeiro o servidor canva via MCP.
- Nao usar browser remoto como caminho padrao.
- Browser/manual so entra como fallback se o MCP falhar de forma confirmada para a tarefa.
