# decisions.md - Decisoes Irreversiveis

Este arquivo guarda coisas que nao podem mudar sem conversa explicita.
Use para regras permanentes do agente, da operacao e da seguranca.

## O que entra aqui
- Politicas de credenciais
- Regras de deploy ou aprovacao
- Limites de seguranca e privacidade
- Regras operacionais que o agente nunca deve quebrar

## Exemplos de categoria
- Todas as credenciais ficam no 1Password.
- Deploy so apos aprovacao.
- O agente nao envia resposta externa sem contexto suficiente.

## Decisoes Ativas
- O agente principal roda em uma VPS OpenClaw no workspace remoto `/root/.openclaw/workspace` em `root@187.77.58.193`. Para qualquer ajuste de memoria, playbook, integracao, catalogo, comportamento ou validacao do agente principal, priorizar sempre a VPS como fonte operacional real; mudancas apenas no workspace local do Windows nao garantem efeito sobre a Clara. (2026-03-26)
- Todas as credenciais sensiveis devem ficar no 1Password do projeto; copias locais devem ser removidas ou rotacionadas quando possivel. (2026-03-06)
- O e-mail padrao de envio do bot OpenClaw e medicalemagrecimento@gmail.com. Sempre que o agente enviar e-mails em nome do bot, deve usar esta conta. (2026-03-24)
- A conta institutovitalslim@gmail.com deve permanecer conectada para leitura e gestao de recursos Google da clinica, incluindo Gmail, Agenda, lembretes e acessos operacionais como Google Ads, Google Tag Manager e Google Analytics. (2026-03-24)
- Canva MCP esta configurado como capacidade permanente do agente no servidor, via mcporter com o nome canva. Para pedidos de criacao de materiais de marketing no Canva, o agente deve priorizar este fluxo oficial antes de alternativas manuais ou nao oficiais. (2026-03-25)
- Para tarefas no Canva, o agente deve usar prioritariamente o servidor canva via MCP e nao via browser remoto. Browser, Cloudflare Tunnel, scraping ou login web so devem ser usados como fallback se o fluxo MCP falhar de forma confirmada. (2026-03-25)
- O servidor principal do OpenClaw opera com `agents.defaults.timeoutSeconds = 600` para reduzir falhas em tarefas longas de marketing/Canva.

## 2026-03-26 - WhatsApp outbound rule
- Neste servidor, contexto de WhatsApp nao implica canal de envio ativo. Se o usuario pedir para mandar WhatsApp e nao houver rota outbound documentada/validada, responder com a limitacao e oferecer o texto do lembrete ou outro canal; nunca converter numero de WhatsApp em destino Telegram.
- A conta `medicalemagrecimento@gmail.com` deve ser acessada na VPS por `gog` OAuth para Gmail. Nao usar senha/local file/browser login no Gmail como caminho padrao, porque o Google bloqueia esse fluxo no ambiente headless. (2026-03-28)
