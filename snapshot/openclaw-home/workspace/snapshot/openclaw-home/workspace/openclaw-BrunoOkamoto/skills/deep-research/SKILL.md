---
name: deep-research-protocol
description: >
  Protocolo estruturado de pesquisa profunda com múltiplas fontes, síntese e relatório
  acionável. Use quando o Bruno pedir pesquisa detalhada, análise de mercado, investigação
  de tema ou benchmarking. Acionar quando: "pesquisa sobre", "deep research", "investiga",
  "analisa o mercado de", "benchmark", "quero entender melhor", "pesquisa profunda",
  "me dá um overview de", "análise de concorrentes". Para pesquisas complexas (>30min),
  spawnar como sub-agent.
metadata:
  author: amora-cos
  version: 1.0.0
  domain: shared
  owner: main
---

# Deep Research Protocol — Skill de Pesquisa Profunda

## O que é

Protocolo estruturado para pesquisa profunda. Combina múltiplas fontes, sintetiza findings, e entrega relatório acionável.

## Protocolo de Pesquisa

### 1. Enquadramento (2 min)
- Qual a pergunta exata?
- Qual decisão essa pesquisa vai informar?
- Qual nível de profundidade? (Quick scan vs Deep dive)

### 2. Coleta Multi-fonte

**Fontes primárias (usar nesta ordem):**
1. `web_search` — busca geral (Brave)
2. `web_fetch` — extrair conteúdo de URLs relevantes
3. **Perplexity** — busca com AI-powered answers e citações (API key no 1Password: "Perplexity API")
   ```bash
   PERPLEXITY_API_KEY=$(op item get "Perplexity API" --vault "Amora Vault" --field credential --reveal)
   node /root/.openclaw/workspace/skills/perplexity/scripts/search.mjs "query"
   ```
4. Knowledge Base — se tiver conteúdo relevante já ingestado

**Fontes especializadas:**
- Reddit/HackerNews — opinião de comunidade técnica
- Twitter/X — sinais em tempo real
- YouTube — análises longas e tutoriais
- GitHub — repos e projetos open source

### 3. Síntese

Para cada fonte:
- **Fato** — o que é confirmável
- **Opinião** — o que é interpretação
- **Sinal** — o que sugere tendência

### 4. Relatório

**Formato padrão:**

```markdown
# [Tema] — Deep Research
Data: DD/MM/YYYY

## TL;DR (3-5 bullets)

## Contexto
[Por que estamos pesquisando isso]

## Findings
### [Subtema 1]
- Finding + fonte
### [Subtema 2]
- Finding + fonte

## Análise
[Cruzamento dos findings, padrões identificados]

## Recomendação
[O que fazer com essa informação]

## Fontes
[Lista de URLs consultadas]
```

### 5. Salvamento
- Salvar em `memory/research-YYYY-MM-DD-[slug].md`
- Se relevante pra Knowledge Base → ingestar

## Níveis de Profundidade

| Nível | Tempo | Fontes | Output |
|-------|-------|--------|--------|
| Quick scan | 5-10 min | 3-5 URLs | 1 parágrafo + bullets |
| Standard | 15-30 min | 8-12 URLs | Relatório 1-2 páginas |
| Deep dive | 30-60 min | 15-20+ URLs | Relatório 3-5 páginas |

## Quando spawnar sub-agent

Se a pesquisa é deep dive (>30min) ou Bruno quer continuar trabalhando enquanto pesquisa roda:
- Spawnar via `sessions_spawn` com task detalhada
- Sub-agent entrega relatório quando pronto
- Amora review e envia pro Bruno

## Vieses a evitar

- Confirmation bias — buscar contra-argumentos ativamente
- Recency bias — verificar se tendências são reais ou hype
- Survivorship bias — buscar casos de fracasso, não só sucesso
- Authority bias — expert disse ≠ é verdade
