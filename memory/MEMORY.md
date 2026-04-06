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
- research/: benchmark, estudos e referencias que valem consulta futura. Exemplos: eGFR/testosterona em centenarias → research/eGFR-testosterone-centenarians.md; implante subdérmico de oxandrolona pós-LCA → research/implante-oxandrolona-lca.md; paradoxo metabólico da menopausa → research/menopausa-paradoxo-metabolico.md; protocolo EV + duplas IM → research/protocolo-ev-03-soros-10-duplas.md; protocolo Recompilar 10/10 → research/protocolo-duplas-recompilar-10-10.md; CP e testosterona baixa → research/prostate-cancer-low-testosterone-mortality.md; triplo agonismo antiobesidade → research/triplo-agonismo-obesidade.md; fórmula Recompilar homem → research/formula-homem-recompilar-2cs-2025.md; tirzepatida Recompilar → research/tirze-recompilar-3meses-2025.md; targeting FSH aging → research/targeting-fsh-aging.md; estresse reducionista → research/estresse-reducionista-supernutricao.md; hipótese hormonal da avó → research/hipotese-hormonal-avo.md; comparação Glaser vs demais → research/testosterona-rebecca-glaser-comparativo.md; semaglutida e gestação → research/semaglutida-gestacao-2026.md; GH baixa dose → research/gh-baixa-dose-composicao-corporal.md; cabelo CS 2025 → research/cabelo-cs-2025.md; GLP-1 e Botox → research/glp1-botox-migranea-2026.md; duplas premium 2 meses → research/protocolo-duplas-premium-2meses-2025.md; fórmula retenção hídrica → research/formula-retencao-hidrica.md; hepteto fantástico → research/hepteto-fantastico.md; informativo líquidos biomeds → research/informativo-liquidos-biomeds.md; alopecia areata (Nutroboost) → research/alopecia-areata-blueprint.md. estudos Sinclair (longevidade) → research/sinclair-longevity-core-findings.md.

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

## Integracoes Criticas
- playbooks/openclaw-gateway-restart.md: como reiniciar e validar corretamente o gateway nesta VPS.
- memory/integrations/onepassword.md
- memory/playbooks/1password-access.md
- memory/integrations/canva.md
- memory/playbooks/canva-mcp-access.md
- memory/integrations/telegram-map.md: IDs dos grupos e topicos do Telegram, incluindo `Evolucao do Openclaw`.

- memory/playbooks/canva-marketing-workflow.md
- memory/content/campaigns/canva-marketing-brief-template.md
- memory/playbooks/marketing-production-routine.md
- memory/playbooks/carrossel-modelo-01.md: padrao editorial e visual do `Modelo 01` para carrosseis da Clara.
- memory/projects/dra-daniely-instagram.md: lote padrao de fotos reais da Dra Daniely e fluxo operacional para carrosseis no `Modelo 01`.
- memory/content/hooks-reels-carrosseis.md: framework dos 8 tipos de hook para reels e carrosseis; tabela de aplicacao por objetivo de post.
- memory/content/conselho-ivs-instagram-framework.md: veredicto do Conselho LLM sobre estrategia de conteudo Instagram do IVS; consensos, divergencias, pontos cegos (compliance CFM + presenca de camera), sistema integrado validado (Pilares → Hook → Storytelling) e proporcao semanal 4-2-1.

## Endogin Catalogo De Plataforma
- integrations/endogin.md: status do acesso e mapa base da plataforma.
- playbooks/endogin-course-catalog.md: ordem correta de consulta para modulos e videos.
- projects/endogin-platform.md: inventario estrutural da plataforma Endogin.
- projects/endogin-vendas.md: trilhas comerciais, SND, agendamento e prospeccao, com regra de entrega em formato de aula ensinavel e reporte no topico `Evolucao do Openclaw` (`thread 768`).
- projects/endogin-obesidade.md: trilhas de obesidade, tirzepatida, sarcopenia e emagrecimento.
- projects/endogin-trh.md: trilhas de TRH, menopausa, pellets e hormonios.
- projects/endogin-casos-clinicos.md: encontros, niveis e grupos de casos clinicos.
- projects/endogin-start.md: trilhas Start, SCALE, Caio Pires, Twoany, Regina e Surgical.
- projects/omie-study.md: estado atual do estudo do Omie na VPS.
- research/endogin-catalog-deep-index.md: indice tematico profundo para busca semantica.
- ../snapshot/endogin/course-structure.md: lista textual completa de modulos/produtos/aulas.
- ../snapshot/endogin/course-structure.json: fonte estrutural completa para filtros e automacao.

## Quarkclinic API
- integrations/quarkclinic-api.md: skill da API Quarkclinic na VPS, cliente seguro e estado atual do acesso.
- ../skills/quarkclinic-api/SKILL.md: instrucoes de uso da skill.
- ../skills/quarkclinic-api/references/api-docs.md: mapa enxuto de endpoints e autenticacao.

## Perplexity
- integrations/perplexity.md: estado validado da integracao/skill Perplexity na VPS, local da credencial no 1Password e endpoints uteis.

## Quarkclinic Plataforma
- integrations/quarkclinic.md: fluxos operacionais (atendimento, pacientes, financeiro, caixas e CRM) para uso completo do sistema pelo time de recepcao.

## Omie
- integrations/omie.md: panorama inicial dos módulos oficiais do ERP Omie (finanças, notas fiscais, estoque, vendas/CRM, serviços, IA, Omie.Hub, Omie.Cash, PDV, WhatsApp, prospecção) e próximos passos do estudo.
- projects/omie-study.md: status e roadmap do treinamento/curadoria do Omie.

- Skill Endogin Transcription: `/root/.openclaw/workspace/skills/endogin-transcription/SKILL.md`
