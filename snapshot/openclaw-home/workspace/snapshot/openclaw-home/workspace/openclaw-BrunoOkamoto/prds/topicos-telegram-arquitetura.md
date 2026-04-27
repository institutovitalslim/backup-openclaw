# Guia Completo: Tópicos no Telegram + Arquitetura de Agentes

**Objetivo:** Ensinar a criar e organizar tópicos no Telegram, configurar agentes para responder sem menção, e entender as diferenças arquiteturais entre **um agente MAIN compartilhado** vs **agentes isolados por tópico**.

---

## 📱 Parte 1: Criando Tópicos no Telegram

### O que são Tópicos (Topics)?

Tópicos são **threads organizadas dentro de um grupo**. Cada tópico funciona como um canal separado, mas todos estão no mesmo grupo.

**Quando usar:**
- Separar projetos diferentes
- Organizar conversas por assunto (suporte, dev, ideias)
- Ter agentes especializados por contexto

### Passo a Passo: Criar Grupo com Tópicos

#### 1. Criar o Grupo

1. Abra o Telegram
2. Menu → **Novo Grupo**
3. Nome: `Amora HQ` (ou o que preferir)
4. Adicione pelo menos 1 pessoa (você mesmo pode ser suficiente)
5. Finalize a criação

#### 2. Transformar em Supergrupo

1. Abra as **configurações do grupo** (clique no nome)
2. **Tipo do Grupo** → **Grupo Público** (ou mantenha privado)
3. Defina um `@username` para o grupo (ex: `@amorahq_bruno`)
4. O Telegram automaticamente transforma em **Supergrupo**

> ⚠️ **Importante:** Só supergrupos suportam tópicos!

#### 3. Ativar Tópicos

1. Configurações do grupo → **Tópicos**
2. Toggle **"Ativar Tópicos"**
3. O Telegram cria automaticamente o tópico **"Geral"** (id: `1`)

#### 4. Criar Tópicos Adicionais

1. Na tela do grupo, clique no **ícone de tópicos** (canto superior)
2. **"Criar Tópico"**
3. Dê um nome: `Curso OpenClaw`, `Suporte`, `Dev`, etc.
4. Escolha um ícone/emoji
5. Pronto! Cada tópico tem um **ID único** (ex: `2638`, `2640`)

---

## 🤖 Parte 2: Adicionando Agentes aos Tópicos

### Opção A: Adicionar o Bot ao Grupo

1. Vá em **@BotFather**
2. `/mybots` → escolha seu bot
3. **Bot Settings → Group Privacy → Desativar "Privacy Mode"**
   - Isso permite o bot ver **todas as mensagens** do grupo
4. Adicione o bot ao grupo: `@seubotaqui`
5. Torne ele **administrador** (necessário para agir em tópicos)

### Opção B: Usar Bot Existente (sem admin)

Se o bot NÃO for admin, ele só responde quando **marcado** (`@bot mensagem`).

---

## ⚙️ Parte 3: Configurando Agentes para Responder SEM Menção

Por padrão, bots do Telegram só respondem quando mencionados. Para habilitar **resposta automática em tópicos específicos**, você precisa configurar no `config.yaml`.

### Estrutura do Config

```yaml
agents:
  - id: amora-main
    model: anthropic/claude-sonnet-4-6
    thinking: off
    workspaceDir: /root/.openclaw/workspace-amora
    
    activation:
      surfaces:
        - surface: telegram
          mode: mention  # Padrão global: só quando marcada
          
          overrides:
            # Tópico "Curso OpenClaw" — responde TUDO
            - chat: "telegram:-1003873964847:topic:2638"
              mode: all
            
            # Tópico "Suporte" — responde TUDO
            - chat: "telegram:-1003873964847:topic:2640"
              mode: all
            
            # Tópico "Geral" — só quando marcada
            - chat: "telegram:-1003873964847:topic:1"
              mode: mention
```

### Como Descobrir o Chat ID

1. Mande uma mensagem **no tópico** marcando o bot
2. No terminal da VPS: `openclaw logs --tail 50`
3. Procure por: `chat_id: "telegram:-1003873964847:topic:2638"`
4. Copie esse ID e cole no config

### Aplicar a Config

```bash
openclaw gateway restart
```

Agora a Amora responde **automaticamente** nos tópicos configurados com `mode: all`.

---

## 🏗️ Parte 4: Arquitetura de Agentes — MAIN vs Isolados

Aqui está a **decisão mais importante** do curso: como organizar seus agentes?

---

### 🔵 Arquitetura 1: **UM Agente MAIN Compartilhado**

**Como funciona:**
- **1 agente** (`amora-main`) responde em **múltiplos tópicos**
- Todos os tópicos compartilham:
  - Mesmo **workspace**
  - Mesma **memória** (`MEMORY.md`, `memory/2026-02-25.md`)
  - Mesmos **crons** (heartbeats, lembretes)
  - Mesmo **SOUL.md**, **USER.md**, **TOOLS.md**

**Exemplo de config:**

```yaml
agents:
  - id: amora-main
    workspaceDir: /root/.openclaw/workspace-amora
    activation:
      surfaces:
        - surface: telegram
          mode: mention
          overrides:
            - chat: "telegram:-1003873964847:topic:2638"  # Curso
              mode: all
            - chat: "telegram:-1003873964847:topic:2640"  # Suporte
              mode: all
            - chat: "telegram:-1003873964847:topic:1"     # Geral
              mode: mention
```

#### ✅ Vantagens

1. **Continuidade total** — A Amora lembra de TUDO que aconteceu em todos os tópicos
2. **Economia de recursos** — 1 processo, 1 workspace, 1 memória
3. **Crons únicos** — Heartbeats, lembretes, backups rodam 1 vez só
4. **Contexto cruzado** — "Aquele arquivo que você criou no tópico X" funciona
5. **Facilidade de setup** — Só um agente pra configurar

#### ❌ Desvantagens

1. **Contexto poluído** — Conversas de tópicos diferentes se misturam no histórico
2. **Sem isolamento** — Se alguém faz merda num tópico, afeta todo o workspace
3. **Contexto explode rápido** — Múltiplos tópicos ativos = 100k tokens em dias
4. **Privacidade zero** — A Amora pode citar coisas de um tópico privado em outro público
5. **Comportamento único** — Não dá pra ter "Amora Técnica" vs "Amora Criativa"

#### 🎯 Quando usar

- **Você é o único humano** usando os tópicos
- Quer **continuidade total** entre conversas
- Tópicos são **variações do mesmo contexto** (projetos relacionados)
- Não se importa com **memory bleed** entre tópicos

---

### 🟢 Arquitetura 2: **Agentes Isolados por Tópico**

**Como funciona:**
- **Cada tópico tem seu próprio agente** (`amora-curso`, `amora-suporte`, `amora-dev`)
- Cada agente tem:
  - **Workspace separado** (`/workspace-curso`, `/workspace-suporte`)
  - **Memória isolada** (cada um tem seu `MEMORY.md`)
  - **Crons independentes** (cada um pode ter heartbeats diferentes)
  - **SOUL.md customizado** (comportamento especializado)

**Exemplo de config:**

```yaml
agents:
  # Agente do tópico "Curso OpenClaw"
  - id: amora-curso
    model: anthropic/claude-sonnet-4-6
    workspaceDir: /root/.openclaw/workspace-curso
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:-1003873964847:topic:2638"
              mode: all
  
  # Agente do tópico "Suporte"
  - id: amora-suporte
    model: anthropic/claude-haiku-4-5  # Mais barato
    workspaceDir: /root/.openclaw/workspace-suporte
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:-1003873964847:topic:2640"
              mode: all
  
  # Agente do tópico "Dev"
  - id: amora-dev
    model: anthropic/claude-opus-4-6  # Mais poderoso
    thinking: on
    workspaceDir: /root/.openclaw/workspace-dev
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:-1003873964847:topic:2641"
              mode: all
```

#### ✅ Vantagens

1. **Isolamento total** — Cada tópico tem sua própria sandbox
2. **Especialização** — Agente de suporte usa Haiku (barato), Dev usa Opus (poderoso)
3. **SOUL.md customizado** — "Amora Professora" no curso, "Amora DevOps" no suporte
4. **Privacidade** — Dados de um tópico **nunca vazam** para outro
5. **Contexto limpo** — Cada agente só vê mensagens do seu tópico
6. **Controle granular** — Crons diferentes por agente (ex: heartbeat só no suporte)
7. **Escalabilidade** — Adicionar novo tópico = novo agente, sem poluir os existentes

#### ❌ Desvantagens

1. **Zero continuidade** — Agentes não sabem o que aconteceu em outros tópicos
2. **Custo maior** — Múltiplos processos rodando (mais RAM, mais API calls)
3. **Crons duplicados** — Se 3 agentes têm heartbeat, rodam 3x
4. **Setup complexo** — Precisa criar workspace + config pra cada agente
5. **Sem compartilhamento** — Arquivo criado no tópico X não existe no Y

#### 🎯 Quando usar

- **Múltiplos humanos** usando tópicos diferentes
- Precisa de **privacidade entre tópicos** (cliente A vs cliente B)
- Quer **comportamentos especializados** (suporte vs desenvolvimento)
- Tópicos têm **contextos completamente diferentes**
- Quer **modelos diferentes por tópico** (Haiku no suporte, Opus no dev)

---

## 📊 Comparação Direta

| Aspecto | MAIN Compartilhado | Agentes Isolados |
|---------|-------------------|------------------|
| **Memória** | Compartilhada entre tópicos | Isolada por tópico |
| **Workspace** | 1 único workspace | 1 workspace por agente |
| **SOUL.md** | Comportamento global | Personalizado por tópico |
| **USER.md** | 1 humano, contexto unificado | Pode ter USER.md diferente |
| **TOOLS.md** | Ferramentas globais | Ferramentas por agente |
| **Crons** | Rodam 1x (compartilhados) | Rodam N vezes (por agente) |
| **Heartbeats** | 1 heartbeat global | 1 heartbeat por agente |
| **Contexto** | Cruza entre tópicos | Nunca cruza |
| **Privacidade** | Zero — tudo vaza | Total — isolamento completo |
| **Custo (API)** | Mais barato | Mais caro |
| **Custo (RAM)** | 1 processo | N processos |
| **Setup** | Simples (1 agente) | Complexo (N agentes) |
| **Uso ideal** | Projetos relacionados | Contextos isolados |

---

## 🛠️ Parte 5: Configuração Avançada

### Híbrido: MAIN + Agentes Especializados

Você pode **misturar** as duas arquiteturas:

```yaml
agents:
  # Agente MAIN — responde no privado e no "Geral"
  - id: amora-main
    workspaceDir: /root/.openclaw/workspace-amora
    activation:
      surfaces:
        - surface: telegram
          mode: mention  # Padrão: só quando marcada
          overrides:
            - chat: "telegram:1983085858"  # Privado com Bruno
              mode: all
  
  # Agente especializado — só no tópico "Curso"
  - id: amora-curso
    model: anthropic/claude-sonnet-4-6
    workspaceDir: /root/.openclaw/workspace-curso
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:-1003873964847:topic:2638"
              mode: all
  
  # Agente especializado — só no tópico "Suporte"
  - id: amora-suporte
    model: anthropic/claude-haiku-4-5
    workspaceDir: /root/.openclaw/workspace-suporte
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:-1003873964847:topic:2640"
              mode: all
```

**Vantagens:**
- MAIN mantém contexto pessoal (privado com você)
- Agentes especializados ficam isolados
- Melhor dos dois mundos

---

## 🧠 Parte 6: Impacto na Memória e Contexto

### Cenário 1: MAIN Compartilhado

**Estrutura de memória:**

```
/root/.openclaw/workspace-amora/
├── MEMORY.md               ← Contexto global (lido em TODAS sessões)
├── memory/
│   ├── 2026-02-25.md       ← Log diário (mistura TODOS os tópicos)
│   ├── 2026-02-26.md
```

**Quando a Amora responde no tópico "Curso":**
1. Lê `MEMORY.md` (contexto global)
2. Lê `memory/2026-02-25.md` (conversas de TODOS os tópicos)
3. Responde com **contexto completo**

**Problema:**
- Se você falou sobre "projeto secreto X" no tópico "Dev" de manhã
- E alguém pergunta no tópico "Curso" à tarde
- A Amora **pode citar o projeto secreto** (memory bleed)

---

### Cenário 2: Agentes Isolados

**Estrutura de memória:**

```
/root/.openclaw/workspace-curso/
├── MEMORY.md               ← Contexto APENAS do curso
├── memory/
│   ├── 2026-02-25.md       ← Log APENAS do tópico Curso

/root/.openclaw/workspace-suporte/
├── MEMORY.md               ← Contexto APENAS do suporte
├── memory/
│   ├── 2026-02-25.md       ← Log APENAS do tópico Suporte
```

**Quando amora-curso responde:**
1. Lê `MEMORY.md` do workspace-curso
2. Lê `memory/2026-02-25.md` do workspace-curso
3. **Não tem acesso** ao workspace-suporte

**Benefício:**
- Zero vazamento de contexto
- Cada agente só sabe o que aconteceu no seu tópico

---

## 🔄 Parte 7: Impacto nos Crons

### MAIN Compartilhado

```yaml
# /root/.openclaw/config.yaml
cron:
  jobs:
    - name: "Heartbeat Global"
      schedule:
        kind: every
        everyMs: 1800000  # 30 min
      payload:
        kind: systemEvent
        text: "Read HEARTBEAT.md if it exists..."
      sessionTarget: main
      delivery:
        mode: announce
        channel: telegram
        to: "1983085858"  # Privado com Bruno
```

**Como funciona:**
- Roda **1 vez a cada 30 min**
- Usa o **workspace global** (`/workspace-amora`)
- Pode checar coisas de **todos os tópicos** (emails, calendário, etc.)
- Economiza API calls (1 heartbeat vs 3)

---

### Agentes Isolados

```yaml
cron:
  jobs:
    # Heartbeat do agente "Curso"
    - name: "Heartbeat Curso"
      schedule:
        kind: every
        everyMs: 3600000  # 60 min
      payload:
        kind: agentTurn
        message: "Checar se tem novas perguntas no curso"
        agentId: amora-curso
      sessionTarget: isolated
      delivery:
        mode: announce
        channel: telegram
        to: "-1003873964847:topic:2638"
    
    # Heartbeat do agente "Suporte"
    - name: "Heartbeat Suporte"
      schedule:
        kind: every
        everyMs: 1800000  # 30 min
      payload:
        kind: agentTurn
        message: "Checar tickets pendentes"
        agentId: amora-suporte
      sessionTarget: isolated
      delivery:
        mode: announce
        channel: telegram
        to: "-1003873964847:topic:2640"
```

**Como funciona:**
- Cada agente tem **seu próprio heartbeat**
- Rodam em **workspaces separados**
- **Mais API calls**, mas **contexto focado**

---

## 🧪 Parte 8: Casos de Uso Reais

### Caso 1: Freelancer com Múltiplos Clientes

**Problema:** Precisa separar contexto de cada cliente (privacidade).

**Solução:** Agentes isolados

```yaml
agents:
  - id: amora-cliente-a
    workspaceDir: /workspace-cliente-a
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:-1003873964847:topic:2638"
              mode: all
  
  - id: amora-cliente-b
    workspaceDir: /workspace-cliente-b
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:-1003873964847:topic:2640"
              mode: all
```

**Benefícios:**
- Cliente A **nunca vê** dados do Cliente B
- SOUL.md customizado por cliente (ex: "Fale formal com Cliente A")
- Modelos diferentes (Haiku pra suporte, Opus pra dev)

---

### Caso 2: Projetos Pessoais Relacionados

**Problema:** Você trabalha em 3 projetos, mas são todos seus (ex: blog, app, curso).

**Solução:** MAIN compartilhado

```yaml
agents:
  - id: amora-main
    workspaceDir: /workspace-amora
    activation:
      surfaces:
        - surface: telegram
          mode: mention
          overrides:
            - chat: "telegram:-1003873964847:topic:1"    # Blog
              mode: all
            - chat: "telegram:-1003873964847:topic:2"    # App
              mode: all
            - chat: "telegram:-1003873964847:topic:3"    # Curso
              mode: all
```

**Benefícios:**
- Amora lembra de TUDO (contexto cruzado útil)
- "Aquela ideia do app que falamos ontem" funciona no tópico do blog
- Economiza recursos (1 processo)

---

### Caso 3: Híbrido — Pessoal + Profissional

**Problema:** Você quer **privacidade** entre trabalho e vida pessoal.

**Solução:** Híbrido

```yaml
agents:
  # Agente pessoal — privado + tópico "Vida"
  - id: amora-pessoal
    workspaceDir: /workspace-pessoal
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:1983085858"                # Privado
              mode: all
            - chat: "telegram:-1003873964847:topic:1"    # Tópico "Vida"
              mode: all
  
  # Agente profissional — tópico "Trabalho"
  - id: amora-trabalho
    model: anthropic/claude-opus-4-6
    workspaceDir: /workspace-trabalho
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:-1003873964847:topic:2"    # Tópico "Trabalho"
              mode: all
```

**Benefícios:**
- Zero vazamento entre vida pessoal e trabalho
- Modelos diferentes (Haiku pessoal, Opus profissional)
- Comportamento especializado (SOUL.md diferente)

---

## 🚨 Parte 9: Armadilhas Comuns

### Armadilha 1: Misturar Chat IDs

**Erro:**
```yaml
- chat: "telegram:-1003873964847"  # ID do grupo (sem :topic:)
  mode: all
```

**Resultado:** Amora responde em **TODOS os tópicos** do grupo (caos).

**Correção:**
```yaml
- chat: "telegram:-1003873964847:topic:2638"  # ID específico do tópico
  mode: all
```

---

### Armadilha 2: Esquecer de Tornar o Bot Admin

**Erro:** Adicionar bot ao grupo mas **não dar permissão de admin**.

**Resultado:** Bot não consegue ler mensagens em tópicos (só no "Geral").

**Correção:**
1. Configurações do grupo → **Administradores**
2. Adicione o bot
3. Ative permissão: **"Gerenciar Tópicos"**

---

### Armadilha 3: Agentes Isolados Compartilhando Workspace

**Erro:**
```yaml
agents:
  - id: amora-curso
    workspaceDir: /workspace-amora  # ❌ Mesmo workspace
  - id: amora-suporte
    workspaceDir: /workspace-amora  # ❌ Mesmo workspace
```

**Resultado:** Agentes pisam um no outro (arquivos sobrescritos, memória compartilhada).

**Correção:**
```yaml
agents:
  - id: amora-curso
    workspaceDir: /workspace-curso  # ✅ Workspace isolado
  - id: amora-suporte
    workspaceDir: /workspace-suporte  # ✅ Workspace isolado
```

---

### Armadilha 4: Crons no Agente Errado

**Erro:** Criar cron para `amora-curso` mas tentar acessar dados de `amora-suporte`.

**Resultado:** Cron não encontra os arquivos (workspaces diferentes).

**Correção:** Certifique-se que o cron **usa o agentId correto**:

```yaml
cron:
  jobs:
    - name: "Checar curso"
      payload:
        kind: agentTurn
        message: "Checar novas perguntas"
        agentId: amora-curso  # ✅ Usa o workspace correto
```

---

## 📝 Parte 10: Checklist de Decisão

### Perguntas pra se fazer:

1. **Privacidade é crítica?**
   - ❌ Não → MAIN compartilhado
   - ✅ Sim → Agentes isolados

2. **Os tópicos têm contextos relacionados?**
   - ✅ Sim (ex: projetos pessoais) → MAIN compartilhado
   - ❌ Não (ex: clientes diferentes) → Agentes isolados

3. **Precisa de comportamentos especializados?**
   - ❌ Não → MAIN compartilhado
   - ✅ Sim (ex: Amora Professora vs DevOps) → Agentes isolados

4. **Quer economizar recursos (RAM/API)?**
   - ✅ Sim → MAIN compartilhado
   - ❌ Não → Agentes isolados

5. **Contexto cruzado é útil ou perigoso?**
   - Útil (ex: "lembra daquela ideia?") → MAIN compartilhado
   - Perigoso (ex: vazamento de dados) → Agentes isolados

---

## 🎯 Recomendação Final

**Para iniciantes:**
- Comece com **MAIN compartilhado**
- É mais simples, econômico, e "just works"
- Migre pra isolado quando sentir a dor (poluição de contexto, privacidade)

**Para avançados:**
- Use **agentes isolados** desde o início
- Custa mais, mas escala melhor
- Especialmente se trabalha com múltiplos clientes/projetos

**Para a maioria:**
- **Híbrido** é o sweet spot
- MAIN pra contexto pessoal
- Isolados pra contextos profissionais/privados

---

## 🛠️ Parte 11: Exemplo de Setup Completo

### Estrutura de Grupo

```
Amora HQ (Telegram Group)
├── 📌 Geral (id: 1) — só quando marcada
├── 📚 Curso OpenClaw (id: 2638) — agente isolado, responde tudo
├── 🛠️ Suporte (id: 2640) — agente isolado, responde tudo
└── 💬 Bruno Privado (chat: 1983085858) — MAIN, responde tudo
```

### Config Completo

```yaml
# /root/.openclaw/config.yaml

agents:
  # Agente MAIN — privado com Bruno
  - id: amora-main
    model: anthropic/claude-sonnet-4-6
    thinking: off
    workspaceDir: /root/.openclaw/workspace-amora
    activation:
      surfaces:
        - surface: telegram
          mode: mention
          overrides:
            - chat: "telegram:1983085858"  # Privado
              mode: all

  # Agente do Curso — isolado
  - id: amora-curso
    model: anthropic/claude-sonnet-4-6
    thinking: off
    workspaceDir: /root/.openclaw/workspace-curso
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:-1003873964847:topic:2638"
              mode: all

  # Agente de Suporte — isolado, modelo barato
  - id: amora-suporte
    model: anthropic/claude-haiku-4-5
    thinking: off
    workspaceDir: /root/.openclaw/workspace-suporte
    activation:
      surfaces:
        - surface: telegram
          overrides:
            - chat: "telegram:-1003873964847:topic:2640"
              mode: all

cron:
  jobs:
    # Heartbeat MAIN — só pro Bruno
    - name: "Heartbeat Pessoal"
      schedule:
        kind: every
        everyMs: 1800000  # 30 min
      payload:
        kind: systemEvent
        text: "Read HEARTBEAT.md..."
      sessionTarget: main
      delivery:
        mode: announce
        channel: telegram
        to: "1983085858"
    
    # Heartbeat Curso — checks a cada 1h
    - name: "Heartbeat Curso"
      schedule:
        kind: every
        everyMs: 3600000
      payload:
        kind: agentTurn
        message: "Checar novas dúvidas no curso"
        agentId: amora-curso
      sessionTarget: isolated
      delivery:
        mode: announce
        channel: telegram
        to: "-1003873964847:topic:2638"
```

### Estrutura de Workspaces

```
/root/.openclaw/
├── workspace-amora/           # MAIN (pessoal)
│   ├── SOUL.md                # "Seja íntima, casual, use gírias"
│   ├── USER.md                # Contexto do Bruno
│   ├── MEMORY.md              # Memória pessoal
│   ├── memory/
│   │   └── 2026-02-25.md
│   └── HEARTBEAT.md           # Checks pessoais
│
├── workspace-curso/           # Agente isolado
│   ├── SOUL.md                # "Seja professora, didática, paciente"
│   ├── USER.md                # Perfil dos alunos
│   ├── MEMORY.md              # Dúvidas comuns, decisões do curso
│   ├── memory/
│   │   └── 2026-02-25.md
│   └── HEARTBEAT.md           # Checar novas perguntas
│
└── workspace-suporte/         # Agente isolado
    ├── SOUL.md                # "Seja técnica, objetiva, rápida"
    ├── USER.md                # Perfil dos clientes
    ├── MEMORY.md              # Tickets resolvidos, bugs conhecidos
    ├── memory/
    │   └── 2026-02-25.md
    └── HEARTBEAT.md           # Checar tickets pendentes
```

---

## 🎓 Conclusão

### Resumo do Resumo

**MAIN Compartilhado = Memória Total, Zero Privacidade**
- Use quando contexto cruzado é desejável
- Economiza recursos
- Ideal pra projetos pessoais relacionados

**Agentes Isolados = Privacidade Total, Zero Memória Cruzada**
- Use quando contexto cruzado é perigoso
- Custa mais recursos
- Ideal pra múltiplos clientes/contextos

**Híbrido = Melhor dos Dois Mundos**
- MAIN pra uso pessoal
- Isolados pra contextos profissionais
- Recomendado pra maioria dos casos

---

**Proximos Passos:**
1. Decidir qual arquitetura usar
2. Criar os tópicos no Telegram
3. Configurar o `config.yaml`
4. Testar cada tópico
5. Ajustar SOUL.md de cada agente
6. Configurar crons (se necessário)

**Dúvidas?**
- Revise a seção de **Checklist de Decisão**
- Teste com 1-2 tópicos primeiro
- Migre gradualmente se precisar mudar de arquitetura

---

**Última dica:** Não existe "arquitetura errada" — existe a que funciona **pra você**. Teste, aprenda, ajuste. É assim que se constrói um sistema sob medida.
