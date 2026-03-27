# MEMORY.md — Index

This file is the front door for memory. It stays concise and points to the topic-specific files under `memory/`.

## Structure
- `memory/decisions.md` — permanent decisions/commitments.
- `memory/lessons.md` — strategic + tactical lessons.
- `memory/projects.md` — snapshot of active initiatives.
- `memory/people.md` — key contacts and context.
- `memory/pending.md` — items awaiting Tiaro’s input.

*(Populate the individual files; do not duplicate content here.)*

## Feedback Loops
- `memory/feedback_loops/decisions/<domain>.md` - regras estaveis por dominio.
- `memory/feedback_loops/lessons/<domain>.md` - padroes curados por dominio.
- `memory/feedback_loops/feedback/<domain>.jsonl` - eventos recentes com FIFO para `content`, `tasks`, `recommendations` e `digest`.
- `memory/feedback_loops/indexes/promotion_log.jsonl` - auditoria de promocoes.

## Semantic Retrieval
- Inicializacao minima: `SOUL.md`, `USER.md`, `IDENTITY.md` e `memory/YYYY-MM-DD.md`.
- Para contexto extra, usar busca semantica antes de abrir arquivos completos.
- Reindexacao manual: `openclaw memory index --force`.
- Status do indice: `openclaw memory status --json`.
- Busca: `openclaw memory search --query "..."`.
