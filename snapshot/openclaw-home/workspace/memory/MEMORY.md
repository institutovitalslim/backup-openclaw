# MEMORY.md - Memory Index

## Structure
- context/ - memoria relativamente estavel: decisoes, licoes, pessoas, negocio e pendencias.
- projects/ - um arquivo por projeto ativo.
- content/ - voz, ideias, rascunhos, campanhas e memoria editorial.
- integrations/ - mapa de canais, credenciais, automacoes e acessos.
- playbooks/ - SOPs, checklists e rotinas repetiveis.
- research/ - benchmark, estudos e referencia duravel.
- feedback_loops/ - aprendizado por feedback por dominio.
- sessions/ - diario operacional bruto.
- tactical/ - memoria temporaria e explicitamente expiravel.

## Core Files
- context/decisions.md
- context/lessons.md
- context/people.md
- context/business-context.md
- context/pending.md
- integrations/telegram-map.md
- integrations/credentials-map.md

## Loading Rule
- Inicializacao minima: SOUL.md, USER.md, IDENTITY.md, memory/sessions/YYYY-MM-DD.md
- Sessao principal: ler tambem memory/MEMORY.md
- O restante deve ser recuperado por busca semantica sob demanda

## Retrieval Priority
1. memory/sessions/ para contexto imediato
2. memory/feedback_loops/ para preferencia e aprendizagem
3. memory/context/ para regras e contexto estavel
4. memory/projects/ para trabalho ativo
5. memory/content/ e memory/integrations/ para contexto especializado

## Expansion Space
Pastas prontas para novos conhecimentos:
- content/campaigns/
- content/drafts/
- content/ideas/
- content/voice/
- playbooks/
- research/
- projects/
- integrations/
- tactical/
