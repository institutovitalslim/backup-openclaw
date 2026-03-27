# 📋 PRD MASTER — Regravação & Atualização do Curso OpenClaw
> Versão: 1.0 · Data: 06/03/2026 · Autor: Amora (curso-openclaw)
> Status: **AGUARDANDO APROVAÇÃO DO BRUNO**

---

## 1. CONTEXTO E OBJETIVO

O curso OpenClaw foi estruturado em **12 módulos (M0-M11)** + **5 aulas extras (A-E)** + **6 aulas de troubleshooting (N1-N6)** entre 15/02 e 06/03/2026.

Desde a gravação das primeiras aulas, o OpenClaw lançou **3 releases significativas** (2026.2.12, 2026.2.21, 2026.3.2) com **breaking changes críticos** que invalidam partes do conteúdo existente.

Além disso, foram coletadas **~2000 mensagens dos grupos** de alunos (24/02 a 06/03), gerando um ranking das **Top 10 dúvidas** que precisam ser endereçadas nas aulas.

**Objetivo:** Produzir um plano completo de regravação, atualização e criação de novas aulas, garantindo que o curso reflita a versão 2026.3.2+ e cubra as dores reais dos alunos.

---

## 2. INVENTÁRIO COMPLETO DE AULAS

### 2.1 Módulos Principais (12)
| # | Módulo | Duração | Status Material | Status Gravação |
|---|--------|---------|-----------------|-----------------|
| M0 | Abertura | 10min | ✅ PRD pronto | ❓ Verificar |
| M1 | Setup (VPS + Instalação) | 25min | ✅ PRD pronto | ✅ **GRAVADA** (Aula 1 — 04/03) |
| M2 | Segurança | 15min | ✅ PRD pronto | ❌ NÃO GRAVADA |
| M3 | Identidade | 25min | ✅ PRD pronto | ❌ NÃO GRAVADA |
| M4 | Memória | 25min | ✅ PRD pronto | ❌ NÃO GRAVADA |
| M5 | Integrações | 25min | ✅ PRD pronto | ❌ NÃO GRAVADA |
| M6 | Skills | 15min | ✅ PRD pronto | ❌ NÃO GRAVADA |
| M7 | Proatividade | 15min | ✅ PRD pronto | ❌ NÃO GRAVADA |
| M8 | Multi-Agentes | 20min | ✅ PRD pronto | ❌ NÃO GRAVADA |
| M9 | Immune System | 20min | ✅ PRD pronto | ❌ NÃO GRAVADA |
| M10 | Mission Control | 10min | ✅ PRD pronto | ❌ NÃO GRAVADA |
| M11 | Wrap-up | 10min | ✅ PRD pronto | ❌ NÃO GRAVADA |

### 2.2 Aulas Gravadas (04/03/2026)
| # | Tema Real Gravado | Corresponde a | Precisa Regravar? |
|---|-------------------|---------------|-------------------|
| Aula 1 | Como instalar pela VPS e remover o Docker | M1 Setup | ⚠️ **SIM** — falta `tools.profile full` |
| Aula 2 | Como usar assinatura Claude/OpenAI no OpenClaw | N-1 OAuth | ⚠️ **PARCIAL** — OAuth Anthropic bloqueado |
| Aula 3 | Como configurar agentes pra executar tarefas | N-3 Config Set | ✅ OK (cobre o `config set`) |
| Aula 4 | O que acontece quando agente para de responder | N-4/N-5 Debug | ⚠️ **PARCIAL** — faltam cenários |

### 2.3 Aulas Extras (Material pronto, não gravadas)
| # | Tema | Material | Status Gravação |
|---|------|----------|-----------------|
| Extra A | Integração de Ferramentas | ✅ PRD + Prompt + HTML + PDF | ❌ NÃO GRAVADA |
| Extra B | Debug na VPS com Claude Code | ✅ PRD + Prompt + HTML + PDF | ❌ NÃO GRAVADA |
| Extra C | Tópicos no Telegram | ✅ PRD + Prompt + HTML + PDF | ❌ NÃO GRAVADA |
| Extra D | Automações Evolutivas | ✅ PRD + Prompt + HTML + PDF | ❌ NÃO GRAVADA |
| Extra E | Contexto & Memória | ✅ PRD + Prompt + HTML + PDF | ❌ NÃO GRAVADA |

### 2.4 Aulas Troubleshooting (Material pronto, parcialmente gravadas)
| # | Tema | Material | Status |
|---|------|----------|--------|
| N-1 | OAuth & Configuração de API | ✅ PRD + HTML + PDF | ⚠️ GRAVADA (Aula 2) — precisa update |
| N-2 | Bot sem Shell (Sandboxing) | ✅ PRD + HTML + PDF | ❌ NÃO GRAVADA |
| N-3 | Config Set (tools.profile) | ✅ PRD + HTML + PDF | ✅ GRAVADA (Aula 3) |
| N-4 | Lentidão no Telegram | ✅ PRD + HTML + PDF | ⚠️ PARCIAL (Aula 4) |
| N-5 | Debug Runbook | ✅ PRD + HTML + PDF | ⚠️ PARCIAL (Aula 4) |
| N-6 | VPS vs Mac Mini | ✅ PRD + HTML + PDF | ❌ NÃO GRAVADA |

---

## 3. TOP 10 DÚVIDAS DOS ALUNOS (24/02 a 06/03/2026)

> Fonte: ~2000 mensagens dos grupos "Tira Dúvidas OpenClaw" + "OpenClaw Geral 1"

| # | Dúvida | Freq. | Aula que Cobre | Status |
|---|--------|-------|----------------|--------|
| 1 | 🔑 **OAuth/Token Anthropic — "Não consigo autenticar"** | ~20x | N-1 (OAuth) | ⚠️ Precisa atualizar (Anthropic bloqueou OAuth Pro) |
| 2 | 💥 **Contexto estourando — "Agente promete e some"** | ~15x | Extra E (Contexto) | ✅ Coberto no material |
| 3 | 💰 **Assinatura vs API — "Quanto vou gastar?"** | ~15x | ❌ NOVA AULA NECESSÁRIA | 🆕 Criar aula de Custos |
| 4 | 📹 **"Onde estão as aulas?" — Onboarding confuso** | ~12x | Não é aula — é UX da plataforma | 📋 Fix operacional |
| 5 | 📱 **Telegram: bot não responde no grupo** | ~12x | N-2 (Bot sem Shell) + Extra C (Tópicos) | ⚠️ Precisa seção específica |
| 6 | 🏗️ **Sub-agentes vs Sessões — "Quando usar?"** | ~10x | M8 (Multi-Agentes) | ✅ Coberto no material |
| 7 | 🖥️ **VPS vs Local — "Precisa de VPS?"** | ~10x | N-6 (VPS vs Mac Mini) | ✅ Coberto no material |
| 8 | ⚙️ **Modelo por tarefa — "Qual modelo usar?"** | ~10x | ❌ NOVA SEÇÃO NECESSÁRIA | 🆕 Adicionar em M1 ou nova aula |
| 9 | 📱 **Integração Google (Drive/Gmail/Calendar)** | ~10x | Extra A (Integrações) + M5 | ⚠️ Precisa atualizar com gog |
| 10 | 🔧 **"Meu agente não executa nada"** (tools.profile) | ~8x | N-3 (Config Set) | ✅ **COBERTO — Aula 3 gravada** |

### 3.1 Novas Aulas/Seções Derivadas das Dúvidas

| Dúvida | Ação | Prioridade |
|--------|------|-----------|
| **Custos & Modelos** (#3 + #8) | Criar aula nova: "Quanto custa e qual modelo usar" | 🔴 ALTA |
| **Onboarding** (#4) | Não é aula — é link direto na landing page + mensagem de boas-vindas | 🟡 OPERACIONAL |
| **Telegram grupo** (#5) | Expandir N-2 com seção "Bot não responde no grupo" (BotFather privacy) | 🔴 ALTA |
| **Google Integration** (#9) | Atualizar Extra A com passo a passo gog CLI | 🟡 MÉDIA |

---

## 4. ANÁLISE DE MUDANÇAS — OpenClaw Fev/Mar 2026

### 4.1 Releases Analisadas
- **2026.2.12** (12/02)
- **2026.2.21** (21/02) — Gemini 3.1, Streaming Telegram, Discord Voice, Apple Watch
- **2026.3.2** (03/03) — **BREAKING CHANGES CRÍTICOS**

### 4.2 Mudanças que Afetam o Curso

| Mudança | Release | Impacto | Aulas Afetadas |
|---------|---------|---------|----------------|
| 🚨 **`tools.profile` default = messaging** | 3.2 | **CRÍTICO** — novas instalações não executam nada | M1, N-2, N-3 |
| 🔑 **`openclaw secrets` (64 targets)** | 3.2 | **ALTO** — substitui gestão manual de .env | M2, M9 |
| ✅ **`openclaw config validate`** | 3.2 | **MÉDIO** — novo comando útil pra ensinar | M1, M3 |
| 📺 **Telegram streaming = partial (default)** | 3.2 | **MÉDIO** — alunos veem "digitando" ao vivo | M1 (mencionar) |
| 🔒 **WebSocket loopback-only** | 3.2 | **MÉDIO** — painel remoto sem tunnel quebra | M2, Extra B |
| 🔒 **CVE CVSS 8.8 — 30k instâncias expostas** | 2.12 | **ALTO** — gateway em 0.0.0.0 sem firewall | M2 (motivação) |
| 📄 **PDF tool nativo** | 3.2 | **BAIXO** — feature nova, não quebra nada | M5 (mencionar) |
| 🧠 **Ollama embeddings pra memória** | 3.2 | **BAIXO** — alternativa local | M4 (mencionar) |
| 🤖 **ACP dispatch enabled por default** | 3.2 | **BAIXO** — sub-agents routing | M8 (mencionar) |
| 📱 **Gemini 3.1 support** | 2.21 | **BAIXO** — mais opção de modelo | M1 (tabela de modelos) |
| ⌚ **Apple Watch companion** | 2.21 | **INFO** — feature nova | M10 (mencionar) |
| 🎙️ **Audio echo transcript** | 3.2 | **INFO** — nova config | Extra C (mencionar) |

### 4.3 Impacto por Aula — O Que Mudou

| Aula | Status Atual | O que precisa mudar |
|------|-------------|---------------------|
| **M1 Setup** | ⚠️ REGRAVAR | + `openclaw config set tools.profile full` (OBRIGATÓRIO) · + `config validate` · + mencionar streaming visual · + tabela de modelos atualizada (Gemini 3.1) |
| **M2 Segurança** | ⚠️ REGRAVAR | + `openclaw secrets audit/apply` substitui .env manual · + CVE 30k instâncias como motivação · + WebSocket loopback · + ordem correta: dmPolicy ANTES do UFW |
| **M3 Identidade** | ✅ MANTER | + Apenas adicionar `config validate` como dica |
| **M4 Memória** | ✅ MANTER | + Mencionar Ollama embeddings como opção local |
| **M5 Integrações** | ⚠️ ATUALIZAR | + PDF tool nativo · + gog CLI passo a passo |
| **M6 Skills** | ✅ MANTER | Sem mudanças relevantes |
| **M7 Proatividade** | ✅ MANTER | Sem mudanças relevantes |
| **M8 Multi-Agentes** | ⚠️ ATUALIZAR | + ACP dispatch default · + sessions_spawn attachments |
| **M9 Immune System** | ⚠️ ATUALIZAR | + `openclaw secrets audit` no checklist · + `openclaw doctor` melhorado |
| **M10 Mission Control** | ✅ MANTER | + Mencionar Apple Watch |
| **M11 Wrap-up** | ✅ MANTER | Sem mudanças |
| **N-1 OAuth** | ⚠️ ATUALIZAR | + Anthropic bloqueou OAuth Pro · + novo fluxo via API Key |
| **N-2 Bot sem Shell** | ⚠️ ATUALIZAR | + `tools.profile full` como causa #1 · + BotFather privacy mode |
| **N-3 Config Set** | ✅ MANTER | ✅ Já cobre o necessário |
| **N-4 Lentidão** | ✅ MANTER | Sem mudanças |
| **N-5 Debug Runbook** | ✅ MANTER | Sem mudanças |
| **N-6 VPS vs Mac Mini** | ✅ MANTER | Sem mudanças |
| **Extra A Integrações** | ⚠️ ATUALIZAR | + gog CLI · + PDF tool nativo |
| **Extra B Debug VPS** | ✅ MANTER | Sem mudanças |
| **Extra C Tópicos** | ✅ MANTER | + Mencionar audio echo transcript |
| **Extra D Automações** | ✅ MANTER | Sem mudanças |
| **Extra E Contexto** | ✅ MANTER | Sem mudanças |

---

## 5. DECISÃO DE REGRAVAÇÃO

### 🔴 REGRAVAR (conteúdo desatualizado ou incompleto)
| Aula | Motivo | Prioridade |
|------|--------|-----------|
| **M1 Setup** (Aula 1) | Falta `tools.profile full` — alunos travam | 🔴 P0 |
| **M2 Segurança** | `openclaw secrets` muda todo o fluxo + CVE | 🔴 P0 |
| **N-1 OAuth** (Aula 2) | OAuth Anthropic bloqueado, precisa novo fluxo | 🔴 P1 |

### 🟡 ATUALIZAR MATERIAL (regravação opcional, mas docs precisam update)
| Aula | O que mudar no material | Regravar? |
|------|------------------------|-----------|
| **M5 Integrações** | PDF tool + gog CLI | Opcional |
| **M8 Multi-Agentes** | ACP dispatch + attachments | Opcional |
| **M9 Immune System** | `openclaw secrets audit` | Opcional |
| **N-2 Bot sem Shell** | tools.profile + BotFather | Recomendado |
| **Extra A Integrações** | gog CLI | Opcional |

### ✅ MANTER (sem mudanças necessárias)
M0, M3, M4, M6, M7, M10, M11, N-3, N-4, N-5, N-6, Extra B, Extra C, Extra D, Extra E

### 🆕 CRIAR NOVA AULA
| Aula | Tema | Justificativa | Prioridade |
|------|------|--------------|-----------|
| **N-7** | **Custos & Modelos — "Quanto vou gastar?"** | Top 3 dúvida dos alunos (~15x). Tabela clara: Assinatura vs API, custo por modelo, recomendação por uso, config de modelos baratos pra heartbeat/crons | 🔴 P1 |
| **N-8** | **Telegram: Bot não responde no grupo** | Top 5 dúvida (~12x). BotFather privacy, allowlist, dmPolicy vs groupPolicy, diagnóstico passo a passo | 🔴 P1 |

---

## 6. PLANO DE EXECUÇÃO — TASKS

### FASE 1: Atualizar Material Existente (Amora faz)
> ⏱️ Estimativa: 2-3 horas

| Task | Descrição | Depende de | Output |
|------|-----------|-----------|--------|
| T1.1 | Atualizar PRD M1 Setup com `tools.profile full` + `config validate` + streaming | — | PRD atualizado |
| T1.2 | Atualizar PRD M2 Segurança com `openclaw secrets` + CVE + WebSocket | — | PRD atualizado |
| T1.3 | Atualizar PRD N-1 OAuth com novo fluxo pós-bloqueio Anthropic | — | PRD atualizado |
| T1.4 | Atualizar PRD N-2 com tools.profile como causa #1 + BotFather privacy | — | PRD atualizado |
| T1.5 | Criar PRD N-7 (Custos & Modelos) do zero | — | PRD novo |
| T1.6 | Criar PRD N-8 (Telegram Bot em Grupo) do zero | — | PRD novo |
| T1.7 | Atualizar PRDs M5, M8, M9, Extra A com mudanças menores | — | PRDs atualizados |

### FASE 2: Aprovação do Bruno
> ⏱️ Estimativa: 30 min de revisão

| Task | Descrição | Depende de |
|------|-----------|-----------|
| T2.1 | Bruno revisa lista de mudanças (seção 4.3 acima) | T1.* |
| T2.2 | Bruno aprova/rejeita cada item | T2.1 |
| T2.3 | Bruno decide ordem de gravação | T2.2 |

### FASE 3: Gerar Deliverables (Amora faz)
> ⏱️ Estimativa: 3-4 horas

| Task | Descrição | Depende de | Output |
|------|-----------|-----------|--------|
| T3.1 | Gerar HTML atualizado de cada aula modificada | T2.2 | HTMLs |
| T3.2 | Gerar PDF de cada aula modificada | T3.1 | PDFs |
| T3.3 | Gerar/atualizar Prompts do aluno de cada aula modificada | T3.1 | Prompts .md |
| T3.4 | Gerar documento HTML+PDF consolidado (v2) com todas as aulas | T3.2 | curso-openclaw-completo-v2.html/pdf |
| T3.5 | Atualizar Base de Conhecimento no Notion com novos Q&A | T3.1 | Notion atualizado |

### FASE 4: Gravação (Bruno faz)
> ⏱️ Estimativa: depende do Bruno

| Task | O que gravar | PRD de referência | Prioridade |
|------|-------------|-------------------|-----------|
| T4.1 | **M1 Setup** (regravar) — incluir `tools.profile full` | PRD M1 atualizado | 🔴 P0 |
| T4.2 | **M2 Segurança** (gravar do zero) — `openclaw secrets` + CVE | PRD M2 atualizado | 🔴 P0 |
| T4.3 | **N-1 OAuth** (regravar) — novo fluxo pós-bloqueio | PRD N-1 atualizado | 🔴 P1 |
| T4.4 | **N-7 Custos & Modelos** (nova) — tabela de custos, config modelos | PRD N-7 novo | 🔴 P1 |
| T4.5 | **N-8 Telegram Bot em Grupo** (nova) — BotFather + allowlist | PRD N-8 novo | 🔴 P1 |
| T4.6 | **N-2 Bot sem Shell** (gravar) — tools.profile + diagnóstico | PRD N-2 atualizado | 🟡 P2 |
| T4.7 | **M3-M11 restantes** (gravar do zero) | PRDs existentes | 🟡 P2 |
| T4.8 | **Extras A-E** (gravar) | PRDs existentes | 🟢 P3 |

### FASE 5: Pós-Produção
| Task | Descrição | Depende de |
|------|-----------|-----------|
| T5.1 | Upload dos vídeos na plataforma | T4.* |
| T5.2 | Vincular material (PDF/HTML/Prompt) a cada vídeo | T5.1 |
| T5.3 | Criar mensagem de boas-vindas com link direto pros vídeos | T5.1 |
| T5.4 | Atualizar landing page / Google Drive | T5.1 |

---

## 7. RESUMO EXECUTIVO

| Métrica | Valor |
|---------|-------|
| **Total de aulas no curso** | 23 (12 módulos + 5 extras + 6 troubleshooting) |
| **Aulas já gravadas** | 4 (Aulas 1-4 de 04/03) |
| **Aulas que precisam REGRAVAR** | 2 (M1 Setup, N-1 OAuth) |
| **Aulas que precisam GRAVAR do zero** | 19 |
| **Novas aulas a CRIAR** | 2 (N-7 Custos, N-8 Telegram Grupo) |
| **Total final** | **25 aulas** |
| **Material que precisa ATUALIZAR** | 7 PRDs + HTMLs + PDFs |
| **Material OK (sem mudança)** | 16 aulas |
| **Top dúvidas cobertas pelo curso** | 9/10 (após criar N-7 e N-8) |
| **Dúvida #4 (onboarding)** | Fix operacional, não aula |

---

## 8. PRÓXIMO PASSO IMEDIATO

**Bruno precisa:**
1. ✅ ou ❌ em cada item da seção 4.3 (O que mudou por aula)
2. Confirmar criação das 2 novas aulas (N-7 e N-8)
3. Definir ordem de gravação

**Assim que aprovar, eu:**
1. Atualizo todos os PRDs (Fase 1)
2. Gero HTML + PDF + Prompt de cada um (Fase 3)
3. Entrego pacote completo pronto pra gravar

---

## 9. ITENS FALTANTES IDENTIFICADOS NO DOUBLE CHECK

### 9.1 Material Existente Não Mencionado no PRD Original

| Item | Status | Ação |
|------|--------|------|
| **Módulo Bônus: Multi-Agent v2** | ✅ PRD + Prompt + HTML prontos (`prds/multi-agent-v2.md`, `prompts/modulo-bonus-multi-agent-v2.md`, `pdfs/modulo-bonus-multi-agent-v2.html`) | Faltava no inventário — adicionar como **Bônus 1** |
| **Ebook 20 Use Cases** | ✅ v7 pronta (`pdfs/ebook-20-use-cases-v7.html/pdf`) | Material de apoio — não é aula, é bônus de marketing/vendas |
| **PDFs por módulo (M0-M11)** | ✅ Todos gerados (`pdfs/modulo-00-abertura.pdf` até `modulo-11-wrapup.pdf`) | Prontos — verificar se precisam update com mudanças da 3.2 |
| **Templates (6 arquivos)** | ✅ SOUL, USER, AGENTS, IDENTITY, MEMORY, HEARTBEAT templates | Material de apoio dos módulos M3-M7 |
| **Use Cases (6 categorias)** | ✅ business, community, content, productivity, research, support | Material de apoio — complementa ebook |
| **Configs de exemplo** | ✅ `configs/cron-examples.md` + `configs/modelo-config.md` | Material de apoio dos módulos M5 e M1 |
| **10 Regras Invioláveis** | ✅ `docs/10-regras-inviolaveis.md` | Material de apoio do M11 (Wrap-up) — **verificar se regra #2 precisa update** (agora é `openclaw secrets`, não `.env`) |
| **Troubleshooting doc** | ✅ `docs/troubleshooting.md` (35+ problemas) | Material de apoio — **verificar se precisa update** |
| **Custos doc** | ✅ `docs/custos.md` | Material de apoio do M11 — **verificar se valores ainda batem** |
| **Guia Setup Automático** | ✅ `docs/guia-setup-automatico.md` | Speed run alternativo — **verificar se precisa `tools.profile`** |
| **Guia Sobrevivência** | ✅ `docs/guia-sobrevivencia-openclaw.html/pdf` | Novo — verificar conteúdo |
| **Pauta YouTube (podcast Rony)** | ✅ Pauta completa gerada (23/02) | Não é aula do curso — é conteúdo de marketing |
| **N-3 Config Set** | ⚠️ **NÃO TEM PRD PRÓPRIO** — só existe em `memory/2026-03-04-config-set.md` | Criar PRD dedicado se for virar aula separada, ou manter como parte da Aula 3 já gravada |
| **Base de Conhecimento Notion** | ✅ 14 seções publicadas | **Precisa atualizar** com mudanças da 3.2 |

### 9.2 Gaps Identificados

| Gap | Impacto | Ação Recomendada |
|-----|---------|-----------------|
| **N-3 não tem PRD formal** | Baixo (Aula 3 já gravada e funciona) | Documentar o fluxo `config set` no PRD do M1 atualizado |
| **PDFs dos módulos M0-M11 podem estar desatualizados** | Médio (alunos podem baixar PDF com info velha) | Regenerar após atualizar PRDs na Fase 1 |
| **10 Regras Invioláveis — regra #2 desatualizada** | Médio (menciona .env, agora é `openclaw secrets`) | Atualizar doc na Fase 1 |
| **`docs/custos.md` pode ter valores desatualizados** | Médio (preços de modelos mudam) | Verificar e atualizar com preços atuais |
| **`docs/guia-setup-automatico.md` falta `tools.profile full`** | Alto (aluno segue o speed run e trava) | Atualizar na Fase 1 |
| **`configs/modelo-config.md` pode faltar Gemini 3.1 e MiniMax** | Baixo | Atualizar com modelos novos |
| **Base Notion desatualizada com mudanças 3.2** | Alto (alunos consultam e recebem info velha) | Adicionar task T1.8 na Fase 1 |
| **Falta aula sobre WhatsApp** | Médio (dúvida #5 inclui WhatsApp) | Considerar seção em N-8 ou aula separada |

### 9.3 Tasks Adicionais (complementam a Fase 1)

| Task | Descrição | Prioridade |
|------|-----------|-----------|
| T1.8 | Atualizar Base de Conhecimento Notion (14 seções) com mudanças 3.2 | 🔴 ALTA |
| T1.9 | Atualizar `docs/10-regras-inviolaveis.md` (regra #2: .env → openclaw secrets) | 🟡 MÉDIA |
| T1.10 | Atualizar `docs/guia-setup-automatico.md` com `tools.profile full` | 🔴 ALTA |
| T1.11 | Verificar e atualizar `docs/custos.md` com preços atuais | 🟡 MÉDIA |
| T1.12 | Atualizar `configs/modelo-config.md` com Gemini 3.1 + MiniMax | 🟢 BAIXA |
| T1.13 | Regenerar PDFs M0-M11 após updates dos PRDs | 🟡 MÉDIA (Fase 3) |
| T1.14 | Adicionar Módulo Bônus (Multi-Agent v2) ao inventário oficial | 🟢 BAIXA |
| T1.15 | Atualizar `docs/troubleshooting.md` com problemas novos da 3.2 | 🟡 MÉDIA |

### 9.4 Contagem Atualizada

| Métrica | Antes | Depois do Double Check |
|---------|-------|----------------------|
| Total de aulas | 25 | **26** (+1 Bônus Multi-Agent v2) |
| Docs de apoio a atualizar | 0 | **6** (10 regras, custos, guia setup, modelo config, troubleshooting, Base Notion) |
| Tasks Fase 1 | 7 | **15** (+8 tasks de atualização de material de apoio) |
| Material de marketing/bônus | não listado | Ebook 20 Use Cases + Pauta YouTube |

---

## 10. RESUMO EXECUTIVO FINAL (PÓS DOUBLE CHECK)

**Tudo que precisa acontecer, em ordem:**

### 🔴 URGENTE (antes de gravar qualquer coisa)
1. Atualizar `guia-setup-automatico.md` com `tools.profile full`
2. Atualizar Base Notion com mudanças 3.2
3. Atualizar PRDs M1 + M2 + N-1 + N-2

### 🟡 IMPORTANTE (antes de publicar material)
4. Criar PRDs N-7 (Custos) + N-8 (Telegram Grupo)
5. Atualizar 10 Regras Invioláveis
6. Atualizar custos.md + troubleshooting.md
7. Regenerar todos PDFs

### 🟢 NICE TO HAVE
8. Adicionar Módulo Bônus ao inventário
9. Atualizar modelo-config.md
10. Verificar ebook use cases

---

*PRD gerado por Amora · curso-openclaw · 06/03/2026*
*Double check realizado: +8 tasks, +1 aula, +6 docs de apoio identificados*
