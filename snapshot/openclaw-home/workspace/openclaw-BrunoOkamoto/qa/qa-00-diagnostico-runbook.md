# 🚨 Runbook de Diagnóstico — "Meu bot não está funcionando"

> Use este guia ANTES de qualquer outra coisa. Resolve 90% dos problemas.
> Sem terminal. Só prompts.

---

## Passo 1 — Meu bot está respondendo?

**Se SIM:** Vá para o Passo 2.

**Se NÃO:**
- Espere 2 minutos e tente de novo (pode ser instabilidade temporária)
- Tente enviar uma mensagem simples: `oi`
- Se ainda não responder: acesse o painel Mission Control ou reinicie o gateway pelo link que você configurou no setup

---

## Passo 2 — Peça um diagnóstico ao bot

Cole esse prompt:

```
Faz um diagnóstico rápido pra mim agora:
1. O gateway está funcionando? (/status)
2. Tem algum erro recente nos logs?
3. O modelo de IA está respondendo?
4. Alguma automação ou cron com problema?
Me diz o que encontrar em linguagem simples.
```

---

## Passo 3 — Identifique o sintoma e vá para o Q&A certo

| O que está acontecendo | Arquivo de ajuda |
|---|---|
| Bot não responde / lento / respostas pioraram | → qa-03-contexto-memoria.md |
| Erro 401, token inválido, problema de API key | → qa-01-auth-modelo.md |
| Qualquer pessoa usa meu bot / bot não responde no grupo | → qa-02-telegram.md |
| "Port in use", "command not found", não conecta | → qa-04-infra-basica.md |
| Dúvida sobre modelos / custo / Claude bloqueado | → qa-06-llms-comparativo.md |
| Dúvida sobre como o sistema funciona | → qa-05-arquitetura.md |

---

## Prompt Universal de Emergência

Se não souber o que está errado, cole isso:

```
Estou com um problema no OpenClaw e não sei exatamente o que é.
Sintoma: [DESCREVA O QUE ESTÁ ACONTECENDO]

Por favor:
1. Me ajuda a identificar a causa
2. Me diz o que fazer em linguagem simples
3. Me guia passo a passo pra resolver
4. Confirma quando estiver resolvido
```

---

## ⚠️ Regra de Ouro

**Não tente resolver no chute.**

A sequência correta sempre é:
1. Diagnosticar primeiro (o que está errado?)
2. Entender a causa (por quê aconteceu?)
3. Aplicar solução (como corrigir?)
4. Confirmar que resolveu (funcionou?)

Pular etapas cria problemas novos em cima do antigo.

---

*Se nada resolver: descreva seu problema detalhadamente no grupo de suporte com:*
- *O que você tentou fazer*
- *O que aconteceu (print do erro se tiver)*
- *O que você já tentou*

---

*Última atualização: Fev/2026*
