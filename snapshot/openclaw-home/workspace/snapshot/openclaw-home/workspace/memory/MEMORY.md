# MEMORY.md - Mapa da Memoria

Regra de ouro:
MEMORY.md e o mapa, nao o territorio.
Ele aponta para onde cada coisa esta. Nao deve duplicar o conteudo dos arquivos especializados.

## O que vai em cada lugar
- context/decisions.md: decisoes irreversiveis e regras permanentes do agente.
- context/lessons.md: erros, aprendizados e padroes; licoes estrategicas ficam, licoes taticas expiram.
- context/people.md: equipe, parceiros, fornecedores e como interagir com cada pessoa.
- context/business-context.md: contexto do negocio, operacao e prioridades duraveis.
- context/pending.md: coisas esperando decisao, aprovacao ou retorno do Tiaro.
- projects/<nome>.md: status individual de cada projeto ativo.
- content/voice/<plataforma>.md: tom de voz por canal.
- content/ideas/: ideias de conteudo ainda nao desenvolvidas.
- content/drafts/: rascunhos de posts, newsletters, scripts e copys.
- content/campaigns/: memoria de campanhas, lancamentos e narrativas temporais.
- integrations/: mapa de ferramentas, acessos, grupos, topicos e credenciais.
- feedback_loops/: feedback granular, lessons curadas e decisions permanentes por dominio.
- sessions/YYYY-MM-DD.md: log bruto do dia ou do tema, sem curadoria.
- tactical/: memoria temporaria com expiracao explicita.
- playbooks/: SOPs, checklists e rotinas operacionais.
- research/: benchmark, estudos e referencias que valem consulta futura.

## Criterio rapido para salvar
- Se nao pode mudar sem conversa: context/decisions.md
- Se e um erro, aprendizado ou padrao reaproveitavel: context/lessons.md
- Se esta esperando o Tiaro: context/pending.md
- Se e status ou historico de um projeto: projects/<nome>.md
- Se e estilo de escrita por canal: content/voice/<plataforma>.md
- Se e registro bruto do que aconteceu: sessions/YYYY-MM-DD.md

## Session Initialization Rule
Carregar apenas:
- SOUL.md
- USER.md
- IDENTITY.md
- memory/sessions/YYYY-MM-DD.md
- memory/MEMORY.md

Usar busca semantica ou leitura pontual para o restante.

## Expansao sem bagunca
Quando surgir conhecimento novo, criar dentro da mesma logica:
- novo projeto: memory/projects/<nome>.md
- novo canal de conteudo: memory/content/voice/<plataforma>.md
- nova integracao: memory/integrations/<ferramenta>.md
- novo playbook: memory/playbooks/<tema>.md
- nova pesquisa duravel: memory/research/<tema>.md

MEMORY.md deve continuar curto e funcionar como indice.
