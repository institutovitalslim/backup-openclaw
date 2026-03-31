# lessons.md - Erros e Aprendizados

Este arquivo guarda aprendizados que ajudam o agente a nao repetir erro.
Nao e para regras irreversiveis; e para padroes aprendidos.

## Estrategicas
Licoes permanentes ou de longa duracao.
Entram aqui quando o aprendizado continua valido mesmo fora do contexto imediato.

## Taticas
Licoes temporarias, workarounds e alertas operacionais.
Devem ser revistas e podem expirar em cerca de 30 dias quando perderem valor.

## Exemplos de categoria
- Nunca chamar API X sem cache quando o custo estiver alto.
- Esse fluxo quebra quando o token de runtime sobrescreve a chave valida.
- Antes de recomendar algo, conferir se ja esta em pending.md.

## Licoes Ativas
- Nenhuma licao curada registrada neste formato ainda.
- Capacidades novas como integracoes e workflows devem ser registradas em memory/integrations/ e memory/playbooks/, enquanto memory/MEMORY.md deve permanecer apenas como indice curto, sem incorporar o conteudo completo desses arquivos. (2026-03-25)
- Para tarefas no Canva, o agente pode cair no erro de tentar browser remoto e bater no Cloudflare. Se canva via MCP estiver autenticado, esse deve ser o caminho padrao; browser/manual so entra como fallback real. (2026-03-25)
- Em tarefas longas de Canva/carrossel, manter `agents.defaults.timeoutSeconds` em 600s no servidor principal.
- Manter `ripgrep` instalado na VPS para evitar desperdicio de tempo em buscas basicas do agente.
- Preservar compatibilidade do diario em `/root/.openclaw/workspace/memory/sessions/YYYY-MM-DD.md` quando o agente esperar esse caminho.
- Para `medicalemagrecimento@gmail.com`, nao tentar login web no Gmail em browser headless da VPS: o Google pode bloquear com This browser or app may not be secure. Usar `gog` OAuth para leitura/busca no Gmail e pedir ao Tiaro apenas o codigo TOTP quando o login do Omie exigir 2FA. (2026-03-28)
- No OpenClaw, a integracao com Claude/Anthropic deve ser feita por `ANTHROPIC_API_KEY` no `secrets.env`; nao contar com OAuth da Anthropic no gateway. (2026-03-31)
- No Windows do Tiaro, o Claude Desktop so libera `local sessions` sem erros depois que o Git for Windows (Git Bash) e o CLI `@anthropic-ai/claude-code` estiverem instalados e reconhecidos no PATH. (2026-03-31)
