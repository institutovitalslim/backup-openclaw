# Project: OpenClaw Memory

## Status
- fase: ativo
- prioridade: alta
- dono: OpenClaw

## Objetivo
Organizar a memoria do OpenClaw com estrutura curada, busca semantica, feedback loops, snapshot seguro e revisoes periodicas.

## Escopo Atual
- estrutura context/projects/content/integrations/sessions/tactical
- feedback loops por dominio
- snapshot para memory_backups/
- revisao quinzenal
- consolidacao mensal
- prune conservador
- indexacao semantica sob demanda

## Ganhos Ja Obtidos
- memoria mais organizada
- separacao entre bruto e curado
- backups fora da arvore indexada
- melhor base para crescimento de conhecimento

## Riscos / Cuidados
- evitar referencias legadas espalhadas em prompts e docs
- evitar indexar backups
- evitar prune agressivo

## Backlog
- revisar referencias antigas restantes
- enriquecer playbooks e research
- criar padroes por projeto ativo
- reduzir ainda mais ruido no indice semantico

## Proximos Passos
1. continuar limpeza de referencias legadas
2. transformar playbooks em SOPs reais
3. semear research com benchmark e referencias uteis

## Revisao Quinzenal - 2026-04-01
- Snapshot gerado em `memory_backups/20260401T204328Z`.
- Revisadas notas recentes em `memory/sessions/` e consolidado o estado validado da integracao Perplexity em `memory/integrations/perplexity.md`.
- `memory/context/lessons.md` atualizado com a licao de retestar Perplexity antes de declarar indisponibilidade.
- `memory/feedback_loops/indexes/feedback_summary.md` revisado: ha promocao registrada para `feedback_loops/lessons/content.md`; nao houve promocao nova para decisions nesta revisao.
- Prune conservador em dry-run retornou `candidates=0`.
- Reindexacao executada com `openclaw memory index --force`.
