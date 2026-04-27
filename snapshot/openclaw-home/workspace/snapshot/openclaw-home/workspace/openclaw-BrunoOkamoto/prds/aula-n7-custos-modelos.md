# PRD — Aula N-7: Quanto Custa e Qual Modelo Usar

> **Nível:** Intermediário  
> **Duração estimada:** 15 minutos  
> **Pré-requisito:** OpenClaw instalado e funcionando, pelo menos um provider configurado

---

## 🎯 Objetivo da Aula

Ao final desta aula, o aluno será capaz de:

1. Entender a diferença entre **assinatura** e **API Key** e quando usar cada uma
2. Comparar os principais modelos de IA por **preço e capacidade**
3. Escolher o modelo certo para cada tipo de tarefa (economizando até 95%)
4. Configurar **modelos diferentes por função** (heartbeat, chat, análise)
5. Estimar o **gasto mensal real** do seu setup
6. Colocar **limites de gasto** para nunca ser surpreendido

---

## 📋 Script de Gravação — Seção por Seção

### 🎬 ABERTURA (0:00 – 1:00)

**[Bruno na tela, tom direto]**

> "Fala, pessoal! Aula N-7 — custos e modelos. Essa é a aula que vai te salvar de um susto na fatura."

> "Já vi aluno gastar $200 num único dia de teste. Já vi outro rodando o mesmo setup por $8/mês. A diferença? Escolha de modelo. Em 15 minutos você vai entender tudo."

---

### 💳 SEÇÃO 1: Assinatura vs API Key — Qual Usar? (1:00 – 4:30)

**[Tela: slide comparativo]**

> "Primeira decisão: você vai usar assinatura mensal ou API Key com pay-per-use?"

**[Mostrar na tela:]**

| | Assinatura (Claude Pro) | API Key (Pay-per-use) |
|---|---|---|
| **Custo fixo** | $20/mês sempre | $0 se não usar |
| **Controle de gasto** | ❌ Nenhum | ✅ Total |
| **Funciona com OpenClaw** | ❌ Não mais (OAuth bloqueado) | ✅ Sim |
| **Ideal para** | Uso pessoal no chat | Agentes, automação |
| **Risco de surpresa** | Baixo (fixo) | Médio sem limites |

> "A resposta é quase sempre: **API Key**. A assinatura Pro foi pensada para uso humano — você abrindo o chat e conversando. O OpenClaw faz chamadas programáticas, que precisam de API Key."

> "Com API Key, você paga exatamente pelo que usa. Num mês que você viaja e quase não usa o agente, paga menos. Num mês de projeto intenso, paga mais — mas você tem controle."

---

### 📊 SEÇÃO 2: Tabela de Modelos e Preços (4:30 – 8:00)

**[Tela: tabela comparativa]**

> "Agora vamos falar de dinheiro concreto. Os modelos são cobrados por tokens — pedaços de texto de ~4 caracteres. O preço é por 1 milhão de tokens."

| Modelo | Preço Input (M tokens) | Preço Output (M tokens) | Velocidade | Qualidade |
|--------|----------------------|------------------------|------------|-----------|
| **Claude Opus 4** | $15 | $75 | Lento | ⭐⭐⭐⭐⭐ |
| **Claude Sonnet 4.5** | $3 | $15 | Médio | ⭐⭐⭐⭐ |
| **Claude Haiku 4.5** | $0.80 | $4 | Rápido | ⭐⭐⭐ |
| **GPT-4o** | $2.50 | $10 | Médio | ⭐⭐⭐⭐ |
| **Gemini 3.1 Pro** | $1.25 | $5 | Médio | ⭐⭐⭐⭐ |
| **Mistral Small** | $0.10 | $0.30 | Muito rápido | ⭐⭐ |

> "Uma mensagem típica usa ~500 tokens de input + ~200 tokens de output. Vamos fazer a conta:"

> "Com Opus 4: $15/M × 0.0005M + $75/M × 0.0002M = $0.0075 + $0.015 = **$0.022 por mensagem**"
> "Com Haiku 4.5: $0.80/M × 0.0005M + $4/M × 0.0002M = $0.0004 + $0.0008 = **$0.0012 por mensagem**"

> "Diferença: **18x mais barato** com Haiku para a mesma tarefa simples."

---

### 🎯 SEÇÃO 3: Qual Modelo Para Cada Situação? (8:00 – 11:00)

**[Tela: cards de recomendação]**

> "A estratégia é: use o modelo MÍNIMO que resolve o problema."

**Heartbeats e Crons:**

> "Heartbeat é quando o agente acorda sozinho pra checar emails, calendário, notificações. Essas tarefas são simples — verificar, categorizar, decidir se precisa te avisar."
> "**Use Haiku** — $0.005 por execução vs $0.10 com Opus. Com 20 heartbeats por dia, são $0.10/dia com Haiku vs $2/dia com Opus. Em um mês: $3 vs $60. A mesma tarefa."

**Interação Diária (mensagens no Telegram):**

> "Quando você manda uma mensagem pro agente e quer uma resposta útil — pesquisa, organização, análise leve."
> "**Use Sonnet** — o melhor custo-benefício. Rápido o suficiente, inteligente o suficiente, preço razoável."

**Análise Complexa:**

> "Quando você precisa analisar um documento longo, tomar uma decisão difícil, ou escrever algo importante."
> "**Use Opus** — mas só quando precisa. Não use Opus pra checar o clima."

**Alternativas econômicas:**

> "Gemini 3.1 Pro a $1.25/M é uma excelente alternativa ao Sonnet pra quem quer economizar. Mistral Small é absurdamente barato e bom pra tarefas muito simples de classificação."

---

### ⚙️ SEÇÃO 4: Como Configurar Modelo por Função (11:00 – 13:00)

**[Tela: Terminal]**

> "O OpenClaw permite configurar modelos diferentes por função. Isso é poderoso."

```bash
# Modelo padrão para interações do dia a dia
openclaw config set model anthropic/claude-sonnet-4-5

# Modelo específico para heartbeats (econômico)
openclaw config set heartbeat.model anthropic/claude-haiku-4-5

# Modelo para análises pesadas (opcional, usar com moderação)
openclaw config set analysis.model anthropic/claude-opus-4
```

> "Dessa forma, o agente usa Haiku automaticamente nas 20 execuções de heartbeat do dia, Sonnet quando você manda mensagem, e Opus só quando você pedir uma análise profunda."

> "Para verificar a configuração atual:"

```bash
openclaw config get model
openclaw config get heartbeat.model
```

---

### 💰 SEÇÃO 5: Exemplo Real de Gasto Mensal (13:00 – 14:30)

**[Tela: breakdown de custos]**

> "Vamos montar um setup real e calcular:"

| Uso | Quantidade/mês | Modelo | Custo estimado |
|-----|---------------|--------|----------------|
| Heartbeats (2x/hora, 16h/dia) | ~960 execuções | Haiku | ~$5 |
| Mensagens diárias (10/dia) | ~300 mensagens | Sonnet | ~$4 |
| Análises semanais | ~4 análises longas | Opus | ~$3 |
| Crons e automações | ~200 execuções | Haiku | ~$2 |
| **Total estimado** | | | **~$14/mês** |

> "Setup moderado, agente funcionando 24/7 com heartbeats ativos: **$14 a $25/mês**. Se você usar intensamente, pode chegar a $40. Mas com controle de modelos, é muito difícil passar disso sem querer."

> "Compare com: Claude Pro ($20/mês) sem funcionar no OpenClaw. Ou um assistente humano part-time ($500+/mês). Por $15-40/mês você tem um agente AI funcionando 24h."

---

### 🚨 SEÇÃO 6: Troubleshooting — "Minha Conta Zerou" (14:30 – 15:00)

**[Tela: como colocar limites]**

> "Isso acontece quando um loop de código ou skill mal configurada faz milhares de chamadas sem querer. Como se proteger:"

**Na Anthropic:**
```
console.anthropic.com → Settings → Billing → Usage Limits
→ "Monthly spend limit" → Defina um valor (ex: $50)
→ "Notification threshold" → Defina um alerta (ex: $25)
```

**No OpenClaw:**
```bash
# Limitar requests por hora (proteção contra loops)
openclaw config set rateLimit.requestsPerHour 100

# Ver gasto estimado acumulado do mês
openclaw usage report
```

> "Configure esses limites **antes** de começar a usar intensamente. É o cinto de segurança — você espera não precisar, mas vai ficar feliz que existe."

---

## 🛠️ Configuração Recomendada Para Iniciantes

```bash
# Setup básico e econômico para começar
openclaw config set model anthropic/claude-sonnet-4-5
openclaw config set heartbeat.model anthropic/claude-haiku-4-5

# Verificar configuração
openclaw config get model
openclaw config get heartbeat.model
```

E no console.anthropic.com:
- Monthly spend limit: $50
- Notification at: $25

---

## 📊 Tabela Completa de Modelos (Referência Rápida)

| Modelo | Input/Output ($/M) | Uso Ideal | Evitar Para |
|--------|-------------------|-----------|-------------|
| Claude Opus 4 | $15/$75 | Análise profunda, decisões críticas | Heartbeats, respostas simples |
| Claude Sonnet 4.5 | $3/$15 | Interação diária, escrita, research | Tarefas repetitivas em volume |
| Claude Haiku 4.5 | $0.80/$4 | Heartbeats, crons, classificação | Análises complexas |
| GPT-4o | $2.50/$10 | Alternativa ao Sonnet, código | — |
| Gemini 3.1 Pro | $1.25/$5 | Alternativa econômica ao Sonnet | — |
| Mistral Small | $0.10/$0.30 | Classificação simples, routing | Qualquer tarefa que exige raciocínio |

---

## ✅ Checklist Final do Aluno

- [ ] Entende a diferença entre assinatura e API Key
- [ ] Modelo padrão configurado: `openclaw config set model anthropic/claude-sonnet-4-5`
- [ ] Modelo de heartbeat configurado: `openclaw config set heartbeat.model anthropic/claude-haiku-4-5`
- [ ] Limite de gasto configurado no console.anthropic.com
- [ ] Notificação de gasto configurada (threshold)
- [ ] `openclaw usage report` testado e funcionando

---

## ❓ Dúvidas Frequentes

**1. Posso trocar de modelo a qualquer hora?**

> Sim. `openclaw config set model NOVO-MODELO` e pronto. Válido a partir da próxima mensagem.

**2. O Mistral é muito mais barato — por que não usar sempre?**

> Qualidade inferior para raciocínio complexo. Para heartbeats simples funciona; para conversas e análise, perda de qualidade é perceptível. Use Haiku como mínimo para interações.

**3. Gemini é confiável para uso com OpenClaw?**

> Sim, desde a v2026.3.2. Boa alternativa econômica. Não tem as mesmas capacidades de ferramentas do Claude para casos complexos, mas para uso geral é excelente.

**4. Como saber exatamente quanto gastei?**

> `openclaw usage report` mostra breakdown por modelo. Console da Anthropic mostra em tempo real com gráficos.

**5. Haiku é "burro"?**

> Não! Para tarefas estruturadas (checar emails, classificar mensagens, responder perguntas simples), Haiku é excelente. Ele fica atrás em raciocínio multi-step e criatividade. Para 80% das tarefas de automação, é mais que suficiente.
