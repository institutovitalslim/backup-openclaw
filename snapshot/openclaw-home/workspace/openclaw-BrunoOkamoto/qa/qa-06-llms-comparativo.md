# ❓ Q&A — Comparativo de LLMs (Claude, ChatGPT e outros)

> Guia de referência: qual modelo usar, quanto custa, o que recomendamos.

---

## Qual modelo devo usar no OpenClaw?

**Nossa recomendação geral:**

| Situação | Modelo recomendado | Por quê |
|---|---|---|
| Conversa do dia a dia | Claude Sonnet ou GPT-4o | Ótimo equilíbrio qualidade/custo |
| Tarefas automáticas (crons, lembretes) | Claude Haiku ou GPT-4o mini | Muito barato, rápido o suficiente |
| Análises complexas, decisões importantes | Claude Opus | Máxima qualidade, use com moderação |
| Quando Claude está bloqueado | GPT-4o | Excelente alternativa |

---

## Comparativo de Preços e Planos

### Claude (Anthropic)

| Plano | Preço aprox. | O que inclui |
|---|---|---|
| Claude.ai Free | Grátis | Uso limitado no chat (não serve pro OpenClaw) |
| Claude.ai Pro | ~R$ 100/mês | Uso no chat — **não conecta diretamente ao OpenClaw** |
| Claude.ai Max | ~R$ 550/mês | Uso intenso no chat — **não conecta diretamente ao OpenClaw** |
| **API Anthropic** | Pay-per-use | ✅ **O que funciona no OpenClaw** |

**Custo real da API (estimativa mensal com uso moderado):**
- Haiku (automações): ~R$ 2–10/mês
- Sonnet (uso diário): ~R$ 20–80/mês
- Opus (uso intenso): ~R$ 100–300/mês

> ⚠️ **Atenção sobre bloqueios:** A Anthropic está bloqueando algumas contas novas no momento. Não temos controle sobre isso. Se a sua conta foi bloqueada, use o ChatGPT como alternativa — o curso ensina os dois jeitos e ambos funcionam muito bem.

---

### ChatGPT / OpenAI

| Plano | Preço aprox. | O que inclui |
|---|---|---|
| ChatGPT Free | Grátis | Uso limitado no chat (não serve pro OpenClaw) |
| ChatGPT Plus | ~R$ 100/mês | GPT-4o no chat — **não conecta diretamente ao OpenClaw** |
| ChatGPT Pro | ~R$ 1.000/mês | Uso intenso + o1 pro — **não conecta diretamente ao OpenClaw** |
| **API OpenAI** | Pay-per-use | ✅ **O que funciona no OpenClaw** |

**Custo real da API (estimativa mensal com uso moderado):**
- GPT-4o mini (automações): ~R$ 2–8/mês
- GPT-4o (uso diário): ~R$ 15–60/mês
- o1 (análises complexas): ~R$ 80–250/mês

---

## Qual a diferença entre assinar o Claude.ai e usar a API?

**Analogia simples:**

- **Assinar o Claude.ai/ChatGPT** = Comer num restaurante. Você usa o cardápio deles, no ambiente deles.
- **Usar a API** = Comprar os ingredientes e cozinhar em casa. Você integra onde quiser.

O OpenClaw é como a sua cozinha — ele precisa dos **ingredientes** (API), não do restaurante pronto.

---

## Posso usar outros modelos além de Claude e ChatGPT?

Sim! O OpenClaw suporta vários provedores:

| Modelo | Provedor | Destaque |
|---|---|---|
| Gemini | Google | Bom pra contextos muito longos |
| Mistral | Mistral AI | Opção europeia, boa privacidade |
| Llama (local) | Ollama | **Grátis**, roda na sua máquina |
| Deepseek | Deepseek | Muito barato, boa qualidade |

**Para descobrir o que está disponível:**
Cole esse prompt no seu bot:

```
Quais modelos de IA o OpenClaw suporta atualmente?
Me recomenda qual seria o melhor pro meu uso com base no que você sabe sobre mim.
Considera tanto qualidade quanto custo.
```

---

## Como trocar o modelo que meu bot usa?

Cole esse prompt no seu bot:

```
Quero trocar o modelo que você usa para [MODELO QUE QUER].
Me guia:
1. Como pego a API key do novo provedor?
2. Como atualizo a configuração?
3. Como testo se ficou funcionando?
Explica passo a passo sem usar comandos de terminal difíceis.
```

---

*Última atualização: Fev/2026 — Preços aproximados, consulte sempre o site oficial dos provedores.*
