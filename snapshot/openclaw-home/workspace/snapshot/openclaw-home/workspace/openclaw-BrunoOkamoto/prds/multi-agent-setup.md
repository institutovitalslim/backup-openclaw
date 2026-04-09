# PRD: Setup Multi-Agentes

> ⚠️ **Nota (19/02/2026):** Refs a `shared/TEAM.md` refletem a v2 original. Na estrutura real, equipe está em `shared/people.md` e agentes nos workspace files.

> Para quando um agente não é suficiente. Jogue no agente principal.

## Contexto

Quando as responsabilidades crescem, um único agente fica sobrecarregado. A solução: múltiplos agentes especializados, coordenados por um principal (hub).

## Arquitetura

```
Gateway (1 servidor)
├── Agente Principal (Opus) ← hub, coordena tudo
├── Agente de Conteúdo (Sonnet) ← produção, drafts
├── Agente Scraper (Sonnet) ← coleta de dados
└── [Outros conforme necessidade]
```

## Leveling System (Kevin Simback)

Todo agente novo começa em L1 e sobe conforme ganha confiança:

| Nível | Nome | Autonomia | Revisão |
|-------|------|-----------|---------|
| L1 | Observer | Zero — output sempre revisado | Cada entrega |
| L2 | Contributor | Baixa — pode sugerir, não executar | Semanal |
| L3 | Operator | Média — executa dentro de guidelines | Semanal |
| L4 | Trusted | Alta — autonomia quase total | Quinzenal |

**Regras:**
- Promoção via performance review semanal
- Rebaixamento é possível (se qualidade cair)
- NUNCA "rushar" um agente pra L3+ sem histórico

## Shared Context

Criar pasta `shared/` acessível por todos os agentes:

```
shared/
├── TEAM.md          ← Registry: quem faz o quê, nível, status
├── outputs/         ← Resultados compartilhados
└── lessons/         ← Aprendizados do time
```

**TEAM.md exemplo:**
```markdown
| Agente | Papel | Nível | Modelo | Status |
|--------|-------|-------|--------|--------|
| Amora | COO / Hub | L4 | Opus | Ativo |
| Content | Produção | L1 | Sonnet | Ativo |
| Scraper | Coleta | L1 | Sonnet | Ativo |
```

## Economia

- **Agente principal:** Opus (interação, decisões)
- **Agentes de execução:** Sonnet (crons, tarefas rotineiras)
- **Heartbeats:** Haiku (economia ~90%)
- Regra: agente que não precisa de Opus NÃO deve usar Opus

## Coordenação

- Agente principal é o HUB — usuário fala só com ele
- Agentes secundários não têm binding Telegram
- Hub model > Mesh model (aprendizado cruzado entre domínios distintos não funciona)
- Sub-agents (sessions_spawn) para tasks paralelas
- **Após spawnar sub-agents: use `sessions_yield`** para encerrar o turno limpo e receber os resultados na próxima mensagem (v2026.3.12+)

## Novidades 3.13

### sessions_yield — Novo Tool de Orquestração

A versão 2026.3.13 adicionou o tool `sessions_yield`, que permite ao agente principal **encerrar o turno atual imediatamente** após spawnar sub-agentes, recebendo os resultados como próxima mensagem.

```json
// Fluxo antes (3.12 e anterior):
// 1. Agent spawna sub-agent
// 2. Agent continua "rodando" (esperando, processando)
// 3. Sub-agent termina e anuncia

// Fluxo com sessions_yield (3.13+):
// 1. Agent spawna sub-agent
// 2. Agent chama sessions_yield → turno encerra
// 3. Sub-agent termina → próximo turno começa com resultado
```

**Por que importa:** O orquestrador agora pode encerrar a sessão limpa, sem ficar "preso" enquanto sub-agents trabalham. Reduz consumo de tokens e melhora a coordenação.

**Exemplo prático:**
```
Após spawnar 3 sub-agents para tarefas paralelas, o hub chama
sessions_yield para sair do turno. Os resultados chegam como
a próxima mensagem — tudo organizado.
```

> ✅ **Não requer config extra.** O tool `sessions_yield` já está disponível após atualizar para v2026.3.13.

## Novidades 3.2

### ACP Dispatch — Enabled by Default
A partir da versão 3.2, o ACP (Agent Communication Protocol) dispatch está **habilitado por padrão**. Não é mais necessário habilitar manualmente no config.

```json
// ANTES (3.1 e anterior):
{
  "acp": {
    "dispatch": true
  }
}

// AGORA (3.2+): não precisa mais desta config
// ACP dispatch já está ativo automaticamente
```

> ✅ Se você tem essa config antiga, pode remover — não causa problema, mas é redundante.

### sessions_spawn com Attachments
`sessions_spawn` agora suporta envio de **attachments** (arquivos, imagens, buffers) diretamente ao spawnar um sub-agente:

```json
{
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Analise este relatório e me dê um resumo executivo.",
    "attachments": [
      {
        "type": "file",
        "path": "/workspace/relatorio-mensal.pdf"
      }
    ]
  }
}
```

Casos de uso: passar PDFs pra análise, imagens pra processamento, arquivos de dados pra transformação — tudo numa única chamada sem etapas extras.

## Tarefas

1. Definir quais agentes você precisa (max 2-3 pra começar)
2. Criar config de cada agente com SOUL.md próprio
3. Configurar shared/TEAM.md
4. Definir modelos (Opus vs Sonnet)
5. Fazer primeiro test drive com task simples
6. Review após 1 semana → decidir promoção

## Resultado Esperado

Time de 2-3 agentes coordenados, cada um com papel claro e nível definido.
