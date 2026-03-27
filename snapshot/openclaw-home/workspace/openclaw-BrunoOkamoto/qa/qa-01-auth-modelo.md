# ❓ Q&A — Auth & Modelo (API, Claude, Troca de Provedor)

> Linguagem simples. Sem terminal. Cole o prompt no seu bot e ele resolve.

---

## "Meu bot parou de responder / ficou lento de repente"

**O que provavelmente aconteceu:** O serviço do Claude (Anthropic) colocou sua conta em cooldown temporário. É normal — acontece quando há muitas chamadas em pouco tempo.

**O que fazer:**
Cole esse prompt no seu bot:

```
Verifica o status do gateway pra mim. Quero saber: 
1. Se o modelo configurado está respondendo
2. Se tem algum erro de autenticação ou cooldown
3. O que você recomenda fazer agora
```

**Se o bot também não responder:** Espere 5–10 minutos e tente de novo. O cooldown é automático e passa sozinho.

---

## "Apareceu erro 401 — o que significa isso?"

**Em linguagem simples:** O bot tentou se identificar pro serviço de IA e a senha estava errada ou vencida. É como tentar entrar numa festa com um convite expirado.

**O que fazer:**
Cole esse prompt no seu bot:

```
Apareceu um erro 401 de autenticação. Me ajuda a diagnosticar:
1. A chave de API está configurada corretamente?
2. O .env está sendo lido pelo gateway?
3. O serviço do systemd tem algum override antigo que pode estar sobrescrevendo a chave nova?
Me diz o que encontrar e o que devo corrigir.
```

---

## "Não sei se devo usar API key ou assinar o plano Claude.ai"

**Diferença simples:**

| | Assinatura Claude.ai | API Key (Anthropic) |
|---|---|---|
| **Pra quê serve** | Usar o chat no site/app | Conectar ao OpenClaw |
| **Preço** | R$ 100–550/mês | Paga pelo uso (R$ 0,10–R$ 5 por 1M tokens) |
| **Funciona no OpenClaw?** | ❌ Não diretamente | ✅ Sim |

**Resumo:** Para usar no OpenClaw, você precisa da **API Key** (console.anthropic.com), não da assinatura do chat.

**⚠️ Aviso importante sobre bloqueios:** Algumas contas da Anthropic estão sendo bloqueadas no momento. Não temos controle sobre isso — é uma decisão deles. Se sua conta foi bloqueada, o curso ensina como usar o **ChatGPT (OpenAI) como alternativa**. Muitos alunos estão usando assim sem problema.

---

## "Quero trocar do Claude para o ChatGPT (ou vice-versa)"

**O que fazer:**
Cole esse prompt no seu bot:

```
Quero trocar o modelo que você usa. Me guia passo a passo:
1. Como pego minha API key da OpenAI (ou Anthropic)
2. Como atualizo o .env com a nova chave
3. Como configuro o modelo no openclaw.json
4. Como reinicio o gateway pra aplicar a mudança
Explica como se eu nunca tivesse feito isso antes.
```

---

## "Quanto custa usar o Claude / ChatGPT no OpenClaw?"

**Referência de preços (Fev/2026 — consulte sempre o site oficial):**

| Modelo | Plano | Preço aprox/mês |
|---|---|---|
| Claude Haiku | API | Muito barato (~R$ 1–5) |
| Claude Sonnet | API | Moderado (~R$ 15–50) |
| Claude Opus | API | Caro (~R$ 80–200) |
| GPT-4o mini | API | Muito barato (~R$ 1–5) |
| GPT-4o | API | Moderado (~R$ 20–80) |

**Nossa recomendação:**
- Use **Haiku ou GPT-4o mini** para tarefas automáticas (lembretes, crons)
- Use **Sonnet ou GPT-4o** para conversas do dia a dia
- Reserve o **Opus** para quando realmente precisar de profundidade

**Dica:** Com otimização, a maioria dos alunos gasta entre R$ 20–80/mês.

---

*Última atualização: Fev/2026*
