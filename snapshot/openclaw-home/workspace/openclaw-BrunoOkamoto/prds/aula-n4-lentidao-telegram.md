# PRD — Aula N-4: Lentidão do Bot no Telegram
## Debug e Otimização de Performance

**Módulo:** N — Troubleshooting  
**Nível:** Intermediário / Debug  
**Duração estimada:** 15–20 minutos  
**Instrutor:** Bruno  
**Formato:** Screenshare + narração (sem câmera)

---

## 🎯 Objetivo da Aula

Ao final, o aluno vai saber:
1. Diagnosticar por que o bot está lento (modelo, VPS ou Telegram?)
2. Identificar e resolver as 6 causas mais comuns de lentidão
3. Medir e monitorar o tempo de resposta via logs
4. Configurar o OpenClaw de forma otimizada para velocidade

---

## 🎬 ROTEIRO DE GRAVAÇÃO

### INTRO (0:00 – 1:30)

> **[Bruno fala, tela mostra o Telegram com bot demorando para responder]**

*"Você manda uma mensagem pro seu bot no Telegram... e fica olhando o cursor piscando. 5 segundos. 10 segundos. 30 segundos. Nada."*

*"Se isso aconteceu com você, você não está sozinho. É uma das reclamações mais comuns no curso. E o problema quase sempre tem solução rápida — mas é preciso saber onde olhar."*

*"Nesta aula, vamos aprender a diagnosticar a lentidão de forma sistemática. Vou mostrar as 6 causas mais comuns, como identificar cada uma, e a solução exata pra cada situação."*

*"Bora? Abre o terminal junto comigo."*

---

### BLOCO 1: DIAGNÓSTICO INICIAL — É O MODELO, A VPS OU O TELEGRAM? (1:30 – 4:00)

> **[Tela: terminal com `openclaw status` e depois logs do gateway]**

*"Antes de sair mexendo em config, a gente precisa entender o que está devagar. Existe uma sequência lógica aqui:"*

**[Mostre o fluxograma mentalmente enquanto fala:]**

*"Primeiro — o Telegram recebeu sua mensagem? O gateway processou ela? O modelo respondeu? Você recebeu a resposta?"*

*"Cada etapa pode ter um gargalo diferente. Vamos começar pelo mais fácil: o comando `openclaw status`."*

```bash
openclaw status
```

*"Esse comando mostra uso de CPU, RAM, e o estado dos processos ativos. Se a CPU tá em 100% ou a RAM tá quase zerada — você já tem sua resposta."*

*"Agora, pra ver onde o tempo está sendo gasto, a gente olha os logs do gateway:"*

```bash
# Logs em tempo real
openclaw gateway logs --follow

# Ou filtrar por tempo de resposta
openclaw gateway logs | grep "response_time"
```

*"Nos logs, você vai ver timestamps. Se o tempo entre 'received message' e 'sent to model' é grande — é processamento interno. Se o tempo entre 'model responded' e 'sent to telegram' é grande — é problema de rede ou webhook."*

*"Se ambos são rápidos mas o usuário não recebe — o problema é do Telegram mesmo. Raro, mas acontece."*

**[Pausa dramática]**

*"Agora que temos nosso toolkit de diagnóstico, vamos às causas. Tenho 6 pra te mostrar — da mais comum pra menos comum."*

---

### BLOCO 2: CAUSA 1 — CONTEXTO MUITO GRANDE (4:00 – 6:00)

> **[Tela: `/status` mostrando contexto alto, ex: 85%]**

*"Causa número 1, e de longe a mais comum: contexto cheio."*

*"Lembra que a Aula Extra E explica como o contexto funciona? Aqui está o impacto prático: quanto mais tokens no contexto, mais o modelo precisa processar a cada mensagem. Uma conversa com 80% do contexto usado pode ser 3 a 5 vezes mais lenta que uma conversa nova."*

*"É como um documento Word com 500 páginas abertas — toda operação fica pesada."*

*"Diagnóstico rápido:"*

```
# Qualquer canal (Telegram, WhatsApp, etc.)
/status
```

*"Se aparecer '75%+' — você encontrou sua causa."*

**Solução imediata:**

*"Você tem duas opções:"*

```
/compact   ← resume o histórico, libera espaço, mantém contexto
/new       ← começa sessão nova (perde histórico, começa do zero)
```

*"`/compact` é pra quando você quer continuar de onde parou. `/new` é pra quando quer um pizarro limpo."*

*"Pra evitar que isso aconteça no futuro, configure compactação automática:"*

```json
{
  "sessions": {
    "main": {
      "autoCompact": {
        "enabled": true,
        "thresholdPercent": 75
      }
    }
  }
}
```

---

### BLOCO 3: CAUSA 2 — MODELO MUITO PESADO (6:00 – 8:00)

> **[Tela: arquivo de config com modelo configurado]**

*"Causa número 2: você tá usando um canhão pra matar formiga."*

*"Claude Opus é o modelo mais inteligente. Mas 'mais inteligente' também significa 'mais lento e mais caro'. Se você configurou Opus pra absolutamente tudo — pra responder 'oi, tudo bem?' E pra rodar crons de notificação — você está pagando caro e esperando mais do que precisa."*

*"A regra de ouro é:"*

- **Sonnet** → conversas normais, o dia a dia
- **Haiku** → crons, alertas automáticos, tarefas simples e repetitivas  
- **Opus** → análise profunda, código complexo, quando qualidade > velocidade

*"Como configurar isso no openclaw.json:"*

```json
{
  "sessions": {
    "main": {
      "model": "claude-sonnet-4-6"
    }
  },
  "crons": {
    "defaultModel": "claude-haiku-4-5"
  }
}
```

*"E pra trocar o modelo na hora, sem editar config:"*

```
/model sonnet    ← muda pra Sonnet nessa sessão
/model haiku     ← muda pra Haiku
```

*"Você vai sentir a diferença na prática. Haiku responde em 1-2 segundos. Opus pode demorar 10-15s pra análises complexas. Use o certo pra cada trabalho."*

---

### BLOCO 4: CAUSA 3 — VPS FRACA (8:00 – 9:30)

> **[Tela: `openclaw status` mostrando CPU/RAM, ou `htop`]**

*"Causa número 3: o servidor em si tá engasgado."*

*"A maioria dos alunos do curso começa com um VPS de entrada — 1GB RAM, 1 vCPU compartilhada. Isso funciona pro início, mas quando você começa a empilhar: gateway rodando, crons ativos, skills pesadas, heartbeats frequentes — pode não ter headroom suficiente."*

*"Como diagnosticar:"*

```bash
openclaw status      # visão geral do OpenClaw
htop                 # uso em tempo real de CPU/RAM
free -h              # memória disponível
df -h                # espaço em disco (swap issue)
```

*"Sinais de alerta:"*
- RAM disponível < 200MB
- CPU consistently > 80%
- Swap sendo usado (isso é péssimo pra performance)

*"Soluções, em ordem de custo:"*

1. **Grátis:** Otimize o que tá rodando (próximas causas)
2. **~$5/mês:** Upgrade pra 2GB RAM (Hetzner, DigitalOcean, etc.)
3. **Reorganize:** Mova crons pesados pra horários de menos carga

---

### BLOCO 5: CAUSA 4 — MUITOS CRONS SIMULTÂNEOS (9:30 – 11:00)

> **[Tela: config de crons, vários com mesmo horário]**

*"Causa número 4: todos os seus crons acordam ao mesmo tempo."*

*"Imagina que você tem 5 crons configurados. Todos pra às 09:00. O sistema acorda, tenta rodar os 5 ao mesmo tempo, todos fazem chamadas pro modelo, todos competem pelo mesmo CPU e memória. A sessão principal fica esperando na fila."*

*"Diagnóstico: liste seus crons ativos:"*

```bash
openclaw cron list
```

*"Se você ver vários com horários idênticos ou muito próximos — encontrou o problema."*

*"Solução: escalone os horários:"*

```json
{
  "crons": [
    { "name": "daily-summary", "schedule": "0 9 * * *" },
    { "name": "weather-check", "schedule": "5 9 * * *" },
    { "name": "news-digest", "schedule": "10 9 * * *" },
    { "name": "task-reminder", "schedule": "15 9 * * *" }
  ]
}
```

*"Separe ao menos 5 minutos entre crons pesados. Ou espalhe ao longo do dia — nem tudo precisa ser às 9h."*

---

### BLOCO 6: CAUSA 5 — SKILLS PESADAS (11:00 – 12:30)

> **[Tela: AGENTS.md ou config de skills]**

*"Causa número 5: skills que demoram pra carregar em todo turno."*

*"Algumas skills leem arquivos grandes, fazem chamadas de rede, ou executam código pesado toda vez que são invocadas. Se você tem skills assim configuradas pra carregar automaticamente em cada mensagem — você está pagando esse custo em todo request."*

*"Diagnóstico: olhe o seu AGENTS.md ou configuração de skills:"*

```bash
# Quais skills estão sendo carregadas automaticamente?
cat /root/.openclaw/workspace-*/AGENTS.md | grep -i skill
```

*"Soluções:"*

1. **Carregamento sob demanda:** Configure a skill pra carregar só quando necessário, não em todo turno
2. **Cache local:** Se a skill busca dados externos, adicione cache (ex: buscar clima só a cada 30min)
3. **Revise a lista:** Você realmente precisa de todas as skills ativas? Desative as que não usa

```json
{
  "skills": {
    "loadOnDemand": true,
    "autoload": ["weather"]
  }
}
```

---

### BLOCO 7: CAUSA 6 — HEARTBEATS MUITO FREQUENTES (12:30 – 13:30)

> **[Tela: configuração de heartbeat]**

*"Causa número 6: heartbeat acelerado demais."*

*"O heartbeat é a checagem periódica que o agente faz — email, calendário, notificações. Se você configurou isso pra checar a cada 5 minutos, você tem 12 invocações do modelo por hora. Em background. Competindo com suas conversas."*

*"Diagnóstico:"*

```bash
# Ver configuração atual de heartbeat
cat ~/.openclaw/config.json | grep -A 5 heartbeat
```

*"Solução — ajuste o intervalo:"*

```json
{
  "heartbeat": {
    "enabled": true,
    "intervalMinutes": 30,
    "model": "claude-haiku-4-5"
  }
}
```

*"Regra de ouro: heartbeat a cada 30 minutos é suficiente pra 95% dos casos. E sempre use Haiku pro heartbeat — é rápido e barato."*

---

### BLOCO 8: QUANDO O PROBLEMA É DO TELEGRAM (13:30 – 14:30)

> **[Tela: logs mostrando model response time vs delivery time]**

*"Existe uma sétima causa que não é culpa do seu setup: o Telegram em si."*

*"Eventualmente — especialmente em regiões mais afastadas dos datacenters do Telegram, ou durante picos de tráfego na plataforma — as mensagens demoram na rede antes de chegarem ao webhook. Ou antes de serem entregues de volta."*

*"Como identificar: os logs do gateway vão mostrar tempo de resposta normal do modelo, mas delay grande na entrega:"*

```
[15:23:01] Message received
[15:23:01] Sent to model
[15:23:04] Model responded (3s) ← normal
[15:23:09] Delivered to Telegram (5s) ← suspeito
```

*"Nesse caso, a solução de curto prazo é ativar o streaming parcial:"*

```json
{
  "channels": {
    "telegram": {
      "streaming": "partial"
    }
  }
}
```

*"Com streaming parcial, o usuário começa a ver o texto chegando enquanto o modelo ainda está gerando. A resposta completa pode demorar o mesmo tempo — mas a percepção de velocidade melhora muito. É a diferença entre 'o bot não respondeu' e 'o bot está digitando'."*

---

### RECAP E CONCLUSÃO (14:30 – 16:00)

> **[Tela: fluxograma de diagnóstico ou slides de resumo]**

*"Vamos recapitular o que vimos hoje:"*

*"Quando o bot estiver lento, siga esta ordem:"*

1. **`openclaw status`** → CPU/RAM OK?
2. **`/status` no chat** → contexto acima de 75%? → `/compact` ou `/new`
3. **Logs do gateway** → onde está o delay?
4. **Modelo** → Opus onde deveria ser Sonnet?
5. **Crons** → muitos no mesmo horário?
6. **Heartbeat** → intervalos muito curtos?
7. **Skills** → algo carregando em todo turno?
8. **Streaming** → ativar `partial` se o problema for percepção

*"A boa notícia: na maioria dos casos, o problema é contexto cheio ou modelo errado — e ambos se resolvem em menos de 2 minutos."*

*"Valeu, pessoal! Na próxima aula vamos falar sobre como configurar alertas pra te avisar antes que o bot fique lento. Até lá!"*

---

## 📋 CHECKLIST PRÉ-GRAVAÇÃO

- [ ] Terminal aberto com gateway rodando
- [ ] Bot configurado no Telegram (para demo)
- [ ] Arquivo `openclaw.json` de exemplo preparado
- [ ] Logs do gateway com exemplos reais de timing
- [ ] Screenshare em monitor com resolução 1920x1080
- [ ] Microfone testado, sem ruído de fundo
- [ ] Gravação de tela: OBS ou Loom

## 📁 ASSETS NECESSÁRIOS

- Fluxograma de diagnóstico (incluído no HTML da aula)
- Tabela de causas/soluções (incluída no HTML da aula)
- Exemplos de log do gateway (simulados se necessário)

---

*PRD gerado em: 2026-03-04 | Versão: 1.0*
