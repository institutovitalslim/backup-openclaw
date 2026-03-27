# MEMORY.md ??? Memory Index

## Structure
- `context/` ??? memoria relativamente estavel: decisoes, licoes, pessoas, negocio e pendencias.
- `projects/` ??? um arquivo por projeto ativo.
- `content/` ??? voz, ideias, rascunhos e campanhas.
- `integrations/` ??? mapa de canais, credenciais e integracoes.
- `playbooks/` ??? SOPs e checklists operacionais.
- `research/` ??? benchmarks, estudos e referencia duravel.
- `feedback_loops/` ??? aprendizado por feedback granular, lessons e decisions por dominio.
- `sessions/` ??? diario operacional, um arquivo por dia ou tema recente.
- `tactical/` ??? memoria temporaria e explicitamente expiravel.
- `backups/` ??? snapshots de seguranca antes de consolidacoes ou reorganizacoes.

## Core Paths
- `context/decisions.md`
- `context/lessons.md`
- `context/people.md`
- `context/business-context.md`
- `context/pending.md`
- `integrations/telegram-map.md`
- `integrations/credentials-map.md`

## Session Rule
- Inicializacao minima: `SOUL.md`, `USER.md`, `IDENTITY.md` e `memory/sessions/YYYY-MM-DD.md`.
- Em sessao principal, ler tambem `memory/MEMORY.md`.
- Use busca semantica sob demanda para o restante.

## Feedback Loops
- `feedback_loops/decisions/<domain>.md`
- `feedback_loops/lessons/<domain>.md`
- `feedback_loops/feedback/<domain>.jsonl`
- `feedback_loops/indexes/promotion_log.jsonl`
