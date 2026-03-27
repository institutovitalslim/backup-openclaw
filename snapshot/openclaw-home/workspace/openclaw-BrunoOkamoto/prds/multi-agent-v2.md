# PRD: Multi-Agent OS v2.0 — Arquitetura Avançada

> ⚠️ **Nota (19/02/2026):** Este PRD descreve a v2 como foi projetada. A estrutura `shared/` real foi reorganizada na Shared Memory v2 (ver `shared/projects/PRD-SHARED-V2.md`). Paths como `shared/context/`, `shared/governance/`, `shared/costs/`, `shared/audit/`, `shared/lessons/` e `TOOLS-SHARED.md` foram consolidados em `shared/tools/`, `shared/assets/`, `shared/projects/`, `shared/decisions.md` e `shared/lessons.md`.

> Para quando seu agente único virou gargalo. Jogue no agente principal.

## 1. Contexto: Por Que Evoluir?

### Problemas do modelo v1 (1 agente hub + workers)

| Problema | Sintoma |
|----------|---------|
| **Gargalo central** | Agente principal coordena E executa — fica lento |
| **Context rot** | Threads longas = respostas piores (degradação antes do limite) |
| **Zero governance** | Sem tracking de custo, sem audit, sem digest |
| **Sem especialização** | Um agente tentando ser bom em tudo = medíocre em tudo |
| **Escala quebrada** | Adicionar mais workers não resolve se o hub é o bottleneck |

### A solução: Hierarquia com Bosses

Em vez de 1 agente fazendo tudo, você cria uma **organização**:

```
Você (CEO)
    ↓
Agente Principal (Chief of Staff) — coordena, não executa
    ↓
Bosses (por domínio) — gerenciam seus workers
    ↓
Workers (especializados) — executam tarefas
```

---

## 2. Arquitetura v2

### Hierarquia

```
Você (CEO)
    ↓ fala com
Agente Principal (Chief of Staff, L4)
    — Não executa tasks
    — Coordena bosses
    — Governance + daily digest
    — Traduz suas prioridades
    ↓
┌──────────────┬──────────────┬──────────────┐
│  Boss A      │  Boss B      │  Boss C      │
│  (domínio 1) │  (domínio 2) │  (domínio 3) │
│  Sonnet, L2  │  Sonnet, L2  │  Sonnet, L2  │
│  Topic próprio│  Topic próprio│  Topic próprio│
└──────┬───────┴──────┬───────┴──────┬───────┘
       ↓              ↓              ↓
    Workers         Workers        Workers
    (L1, Haiku/    (L1, Haiku/    (L1, Haiku/
     Sonnet)        Sonnet)        Sonnet)
```

### O que muda do v1 para v2

| Aspecto | v1 | v2 |
|---------|----|----|
| **Papel do agente principal** | COO — faz tudo | CoS — coordena, não executa |
| **Delegação** | Hub → Workers direto | CoS → Bosses → Workers |
| **Governance** | Nenhuma | Dia 1: cost tracking, audit, digest |
| **Comunicação** | Tudo passa pelo hub | Você fala direto com bosses via topics |
| **Escala** | Limitada (hub = gargalo) | Cada boss é autônomo no seu domínio |
| **Custo** | Descontrolado | Kill switch + tracking por agente |

---

## 3. Definindo Seus Bosses

### Como decidir quais bosses criar

Responda: **"Quais são os 3-5 grandes domínios do meu trabalho?"**

**Exemplos por perfil:**

| Perfil | Boss A | Boss B | Boss C | Boss D |
|--------|--------|--------|--------|--------|
| **SaaS Founder** | Conteúdo | Produto/Ops | Dev | Analytics |
| **Freelancer** | Projetos | Prospecção | Admin/Financeiro | — |
| **Creator** | Conteúdo | Comunidade | Monetização | Analytics |
| **Startup** | Growth | Engineering | Customer Success | Data |
| **Agência** | Clientes | Produção | Comercial | Ops |

### Regras para criar bosses

1. **Máximo 5 bosses** para começar (complexidade cresce exponencialmente)
2. **Cada boss = 1 domínio claro** — se você não consegue descrever em 1 frase, é grande demais
3. **Boss ≠ Worker** — boss COORDENA workers, não executa tudo sozinho
4. **Comece com 2-3** — adicione conforme necessidade real, não especulativa

---

## 4. Workers: Watcher vs Maker

Nem todo worker precisa ficar "ligado". Dois tipos:

### Watcher (Fica de plantão)
- Tem heartbeat ativo (30-60 min)
- Reage a eventos sem o boss pedir
- Custo: ~$1-2/mês cada
- **Exemplo:** Monitor de comunidade, scraper de dados, coletor de métricas

```markdown
# HEARTBEAT.md (Watcher)
1. Ler WORKING.md — tem task? Sim → executar. Não → HEARTBEAT_OK
2. Checar [fonte de dados] por novidades
3. Se encontrou algo relevante → registrar em shared/outputs/
```

### Maker (Só existe quando tem trabalho)
- Sem heartbeat — boss usa `sessions_spawn` quando precisa
- Custo quando idle: **$0**
- **Exemplo:** Writer, editor, dev, analista de dados

```
Boss recebe pedido → spawna Maker com briefing → Maker entrega → Boss revisa
```

### Regra de decisão

> "Esse worker precisa reagir a algo sem que o boss peça?"
> → **Sim** = Watcher | **Não** = Maker

---

## 5. Governance (DESDE O DIA 1)

> A governance não é "depois que tiver funcionando". É a **fundação**.
> Sem ela, o sistema cresce sem visibilidade e o custo explode.

### 5.1 Cost Tracking

```
shared/costs/
├── YYYY-MM-DD.csv       ← log diário (agent_id, model, tokens_in, tokens_out, cost_usd)
└── monthly-summary.md   ← consolidado mensal
```

### 5.2 Audit Log

```
shared/audit/
└── YYYY-MM-DD.jsonl     ← {timestamp, agent, api, endpoint, operation: read|write}
```

### 5.3 Daily Digest (cron automático)

O CoS envia todo dia de manhã:

```
🍇 Daily Digest — DD/MM/YYYY

✅ Ontem: [X tasks por boss]
⚠️ Bloqueios: [lista]
💰 Custo: $X.XX dia | $X.XX mês
🔔 Alertas: [anomalias]

Boss A: [1 linha status]
Boss B: [1 linha status]
Boss C: [1 linha status]
```

### 5.4 Kill Switch

| Threshold | Ação |
|-----------|------|
| 2x custo esperado | ⚠️ Alerta no Telegram |
| 3x custo esperado | 🚨 Avisa você e PERGUNTA antes de pausar |

**NUNCA auto-kill** — sempre pedir confirmação humana.

### 5.5 Escalation Rules

| Situação | Quem decide |
|----------|-------------|
| Task dentro do domínio do boss | Boss decide sozinho |
| Envolve dinheiro real (pagamentos, refunds) | **Sempre pede aprovação** |
| Cross-boss (precisa de outro domínio) | CoS coordena |
| Urgente fora do horário | Notifica você |
| Erro/rollback necessário | Boss registra + avisa CoS |

---

## 6. Estrutura Compartilhada

```
shared/
├── TEAM.md                     ← Registry: quem faz o quê, nível, status
├── context/
│   ├── USER.md                 ← Canonical — todos herdam daqui
│   ├── TOOLS-SHARED.md         ← Integrações compartilhadas
│   └── business-context.md     ← Contexto do negócio
├── governance/
│   ├── DAILY-DIGEST-TEMPLATE.md
│   ├── CROSS-BOSS-PROTOCOL.md
│   ├── QUALITY-GATES.md
│   ├── ESCALATION-RULES.md
│   └── APPROVAL-LOG.md
├── costs/
│   └── YYYY-MM-DD.csv
├── audit/
│   └── YYYY-MM-DD.jsonl
├── templates/
│   ├── BOSS-WORKSPACE/         ← Template para novo boss (8 arquivos)
│   └── WORKER-WORKSPACE/       ← Template mínimo para worker
├── outputs/                    ← Entregas dos agentes
└── lessons/                    ← Lições cross-agent
```

### TEAM.md (Fonte de Verdade)

```markdown
# 🏢 Team Registry

| Agente | Papel | Nível | Modelo | Tipo | Status |
|--------|-------|-------|--------|------|--------|
| [nome] | CoS / Hub | L4 | Sonnet | Principal | Ativo |
| [boss-a] | Boss [domínio] | L2 | Sonnet | Boss | Ativo |
| [boss-b] | Boss [domínio] | L2 | Sonnet | Boss | Ativo |
| [worker-1] | [função] | L1 | Haiku | Watcher | Ativo |
| [worker-2] | [função] | L1 | Sonnet | Maker | Idle |
```

---

## 7. Comunicação

### Você → Bosses (Acesso Direto)

Cada boss tem topic próprio no Telegram. Você fala **direto** com qualquer boss:
- Topic do Boss A → Boss A responde
- Topic do Boss B → Boss B responde

O CoS **não intercepta** mensagens dos topics dos bosses.

### Boss → Boss (Cross-Domain)

Quando um boss precisa de outro:
1. Cria card/registro com @[outro-boss]
2. Reporta no daily digest
3. CoS coordena na próxima janela
4. Se urgente → boss menciona CoS diretamente

### Boss → Workers

- **Watcher:** Boss atualiza `WORKING.md` do worker → worker pega no próximo heartbeat
- **Maker:** Boss usa `sessions_spawn` com briefing completo

---

## 8. Economia de Modelos

| Tier | Modelo sugerido | Custo/mês estimado |
|------|----------------|-------------------|
| CoS (1x) | Sonnet | ~$30-50 |
| Bosses (3-5x) | Sonnet, heartbeat ativo | ~$5-8 cada |
| Watchers (3-5x) | Haiku, heartbeat 30-60min | ~$1-2 cada |
| Makers (5-10x) | Sonnet/Haiku, sob demanda | ~$0 quando idle |
| **Total estimado (3 bosses)** | | **~$60-80/mês** |
| **Total estimado (5 bosses)** | | **~$80-120/mês** |

### Regras de economia
- Worker que não precisa de Sonnet → **Haiku** (90% mais barato)
- Heartbeat de worker → **Haiku** (mesmo que o worker use Sonnet pra tasks)
- CoS NÃO precisa de Opus — Sonnet coordena bem
- Maker idle = **$0** — não existe custo se não é spawnado

---

## 9. Leveling System

| Nível | Nome | Autonomia | Review |
|-------|------|-----------|--------|
| L1 | Observer | Zero — output sempre revisado | Cada entrega |
| L2 | Contributor | Baixa — executa dentro de guidelines | Semanal |
| L3 | Operator | Média — autonomia com guardrails | Semanal |
| L4 | Trusted | Alta — quase total | Quinzenal |

**Regras:**
- Todo agente novo começa **L1**
- Promoção via performance review semanal
- Rebaixamento é possível (se qualidade cair)
- **NUNCA** rushar um agente pra L3+ sem histórico

### Performance Review (semanal, automática)

CoS roda review todo domingo com critérios:
1. **Responsividade** — respondeu dentro do SLA?
2. **Qualidade** — outputs precisaram de correção?
3. **Custo** — dentro do budget?
4. **Autonomia** — tomou boas decisões sozinho?

---

## 10. Migração: v1 → v2 (Passo a Passo)

### Etapa 0: Backup (1 hora)
- [ ] Backup completo do workspace atual
- [ ] Verificar que backup é restaurável
- [ ] Documentar estado atual (quais agentes, quais crons)

### Etapa 1: Foundation (1 dia)
- [ ] Promover agente principal: COO → Chief of Staff
- [ ] Atualizar SOUL.md com novo papel
- [ ] Criar `shared/` com toda a estrutura
- [ ] Criar templates de Boss e Worker
- [ ] Ativar governance: daily digest + kill switch

### Etapa 2: Primeiro Boss (2-3 dias)
- [ ] Criar workspace do Boss A (usar template)
- [ ] Configurar binding Telegram (topic próprio)
- [ ] Adicionar ao agents.list
- [ ] Criar 1-2 workers iniciais
- [ ] Testar spawn chain: CoS → Boss → Worker
- [ ] Validar que funciona antes de avançar

### Etapa 3: Segundo Boss (2-3 dias)
- [ ] Repetir processo do Boss A
- [ ] Testar comunicação cross-boss
- [ ] Validar daily digest com 2 bosses

### Etapa 4: Demais Bosses (1 dia cada)
- [ ] Seguir o mesmo padrão
- [ ] Máximo 1 boss novo por dia
- [ ] Sempre testar antes de avançar

### Etapa 5: Hardening (ongoing)
- [ ] Context sync automático (cron semanal)
- [ ] Memory lifecycle (cleanup de notas velhas)
- [ ] Performance reviews semanais
- [ ] Ajustar workers conforme uso real

---

## 11. Restauração de Emergência

Se algo der errado durante a migração:

```bash
openclaw gateway stop
cp -r ~/.openclaw/workspace ~/.openclaw/workspace-failed-v2/
cd ~/.openclaw
tar -xzf workspace-pre-v2-backup.tar.gz
openclaw gateway start
```

**Regra:** SEMPRE backup antes de cada etapa. Paranoia é feature, não bug.

---

## 12. Resultado Esperado

Ao final da implementação v2, você terá:

- ✅ CoS coordenando (não executando)
- ✅ 3-5 Bosses autônomos por domínio
- ✅ Workers especializados (Watchers + Makers)
- ✅ Governance completa desde o Dia 1
- ✅ Cost tracking com kill switch
- ✅ Daily digest automático
- ✅ Performance reviews semanais
- ✅ Acesso direto a qualquer boss via topic
- ✅ Custo controlado (~$60-120/mês)

---

*"Agents are 30% of the work. The other 70% is the immune system + governance."*
