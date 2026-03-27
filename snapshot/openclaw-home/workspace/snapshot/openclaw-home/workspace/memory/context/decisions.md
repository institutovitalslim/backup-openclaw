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
- Todas as credenciais sensiveis devem ficar no 1Password do projeto; copias locais devem ser removidas ou rotacionadas quando possivel. (2026-03-06)
- O e-mail padrao de envio do bot OpenClaw e medicalemagrecimento@gmail.com. Sempre que o agente enviar e-mails em nome do bot, deve usar esta conta. (2026-03-24)
- A conta institutovitalslim@gmail.com deve permanecer conectada para leitura e gestao de recursos Google da clinica, incluindo Gmail, Agenda, lembretes e acessos operacionais como Google Ads, Google Tag Manager e Google Analytics. (2026-03-24)
