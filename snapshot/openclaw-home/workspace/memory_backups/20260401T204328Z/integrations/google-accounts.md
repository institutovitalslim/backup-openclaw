# google-accounts.md - Google Accounts Map

Este arquivo define o papel de cada conta Google usada pelo OpenClaw.
Use esta nota para evitar confundir a conta de envio do bot com a conta operacional da clinica.

## Conta de envio do bot
- Conta: medicalemagrecimento@gmail.com
- Papel: envio de e-mails do bot OpenClaw
- Regra: sempre usar esta conta para mensagens enviadas pelo bot
- Estado atual: configurada como GOG_ACCOUNT no runtime em 2026-03-24

## Conta operacional da clinica
- Conta: institutovitalslim@gmail.com
- Papel: acesso operacional aos recursos Google da clinica
- Uso esperado: consulta de e-mails, agendas, lembretes e ferramentas Google como Google Ads, Google Tag Manager e Google Analytics
- Regra: manter esta conta conectada para administracao e consulta

## Observacoes
- As duas contas podem coexistir no gog keyring.
- Conta de envio e conta de gestao nao devem ser tratadas como a mesma coisa.
- Ao enviar e-mail em nome do bot, priorizar medicalemagrecimento@gmail.com.
- Ao consultar recursos da clinica, priorizar institutovitalslim@gmail.com quando o contexto for operacional.
