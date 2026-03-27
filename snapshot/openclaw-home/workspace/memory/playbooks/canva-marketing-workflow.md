# Playbook: Canva Marketing Workflow

## Objetivo
Usar o Canva MCP para transformar uma ideia de marketing em uma peca pronta, com consistencia de tom e menor atrito operacional.

## Sequencia recomendada
1. Ler o tom de voz relevante em memory/content/voice/<plataforma>.md.
2. Se o usuario quiser reaproveitar algo existente, buscar com:
   - mcporter call canva.search-designs ...
3. Se o usuario quiser algo novo, gerar candidatos com:
   - mcporter call canva.generate-design ...
4. Se houver candidato aprovado, materializar com:
   - mcporter call canva.create-design-from-candidate ...
5. Se precisar subir imagem/logo, usar:
   - mcporter call canva.upload-asset-from-url ...
6. Se precisar entrega final, exportar com:
   - mcporter call canva.export-design ...

## Heuristica por plataforma
- Instagram: mensagem curta, impacto visual, CTA claro.
- LinkedIn: clareza, autoridade, aplicacao pratica, sem excesso corporativo.

## Estrutura de briefing recomendada
- objetivo da peca
- plataforma
- publico
- oferta ou mensagem central
- CTA
- ativos disponiveis (logo, foto, paleta, brand kit)
- restricoes (evitar termos, cores, estilo)

## Prompt base para gerar peca
Crie uma peca para {plataforma} com tom {tom}. Objetivo: {objetivo}. Publico: {publico}. Mensagem central: {mensagem}. CTA: {cta}. Visual: {direcao_visual}.

## Regras
- Sempre preencher user_intent nas calls do Canva.
- Se o usuario mencionar template, primeiro buscar design/template compativel antes de gerar do zero.
- Quando houver mais de um candidato, resumir as diferencas de angulo visual antes de escolher.
