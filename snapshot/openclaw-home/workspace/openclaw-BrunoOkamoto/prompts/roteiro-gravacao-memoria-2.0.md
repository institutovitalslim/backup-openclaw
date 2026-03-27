# Roteiro de Gravação — "Memória 2.0"
**Aula nova separada | ~20 min | Atualização Março 2026**

---

## Setup antes de gravar

- Abrir terminal com workspace limpo (sessão nova)
- Ter aberto: VS Code com `memory/` visível, terminal lateral
- Deixar `memory/sessions/` com 2–3 arquivos visíveis (para mostrar o diário)
- Desativar notificações

---

## BLOCO 1 — Abertura (1:30 min)

**[CÂMERA FRONTAL]**

> "Galera, memória 2.0. Se você assistiu a aula de fundação, lembra que a gente configurou o sistema de memória, os arquivos decisions, lessons, pending… e na hora de testar o memory search, travou pedindo chave de API do OpenAI.
>
> Duas coisas aconteceram desde então. Primeiro: esse bug foi corrigido. O memory search agora funciona nativamente, sem precisar de nenhuma chave externa. Segundo: eu aprendi — usando o meu próprio agente todo dia — que a estrutura de pastas que a gente criou na primeira aula funciona, mas tem uns ajustes que fazem diferença enorme.
>
> Essa aula cobre os dois. É curta. Uns 20 minutos. E você vai sair com o sistema de memória do seu agente rodando de verdade."

---

## BLOCO 2 — O que o agente carrega vs. busca (4 min)

**[CÂMERA FRONTAL → COMPARTILHA TELA: terminal]**

> "Antes de qualquer coisa, preciso deixar isso muito claro, porque muda como você pensa na estrutura:"

**[MOSTRAR NA TELA: digitar `/status` no agente e mostrar output]**

> "Toda sessão nova, o agente carrega automaticamente 5 coisas:
> SOUL.md, USER.md, AGENTS.md, MEMORY.md — e as notas de hoje e ontem.
>
> Só isso. Mais nada.
>
> Tudo o mais — decisions, lessons, projetos, integrações — fica FORA do contexto. O agente vai buscar quando precisar. Isso é a busca semântica, e já vou mostrar como funciona."

**[MOSTRAR: estrutura de pastas no VS Code]**

> "O MEMORY.md — o índice — é o único arquivo que está sempre presente. E ele não guarda conteúdo. Ele aponta onde o conteúdo está. Olha aqui o meu:"

**[MOSTRAR: MEMORY.md aberto — seções com links para os arquivos de memória]**

> "É um mapa. Não é o território."

---

## BLOCO 3 — Estrutura de subpastas (4 min)

**[COMPARTILHA TELA: VS Code, árvore de pastas memory/]**

> "Na aula de fundação a gente criou tudo na raiz da pasta memory. Decisions.md, lessons.md, pending.md, tudo junto. Funciona — mas quando o volume cresce, a busca semântica começa a trazer contexto misturado.
>
> O que eu uso hoje:"

**[MOSTRAR: tree da pasta memory/ no terminal]**

```
memory/
├── context/
│   ├── decisions.md
│   ├── lessons.md
│   ├── people.md
│   └── business-context.md
├── projects/
│   ├── metricaas.md
│   ├── comunidade-ai.md
│   └── mission-control-apis.md
├── content/
│   ├── voice/linkedin.md
│   └── voice/youtube.md
├── integrations/
│   ├── telegram-map.md
│   └── credentials-map.md
└── sessions/
    ├── 2026-03-14.md
    └── 2026-03-12-mission-control.md
```

> "Subpastas por categoria. A lógica é simples: quando eu pergunto 'qual o status do Metricaas?', o agente busca em projects/ e encontra exatamente o arquivo certo. Se tivesse tudo num projects.md gigante, ele traria contexto do MGM, da Comunidade IA, de tudo junto.
>
> Projetos separados por arquivo. Isso é a mudança mais importante."

**[MOSTRAR: abrir metricaas.md — conteúdo real do arquivo]**

> "Cada projeto tem: status atual, próximas ações, pendências. O agente atualiza quando você pede. Na próxima sessão, ele encontra tudo aqui."

---

## BLOCO 4 — Como a busca semântica funciona (4 min)

**[CÂMERA FRONTAL → COMPARTILHA TELA: terminal com agente]**

> "Agora o que mudou de verdade. Na aula antiga, o memory search exigia chave de API do OpenAI pra funcionar. Isso gerou muita confusão. Aluno configurava tudo certo, chegava nessa parte, travava.
>
> Não precisa mais. Funciona nativamente."

**[DEMO AO VIVO: abrir sessão nova no terminal]**

> "Deixa eu mostrar. Sessão nova — contexto zerado. Nenhum arquivo de projeto carregado."

**[DIGITAR: "qual o status atual do Metricaas?"]**

> "O agente vai buscar nos arquivos... olha aqui — ele usou o memory_search, encontrou o arquivo projects/metricaas.md, e trouxe exatamente o trecho relevante. Sem eu ter aberto nada manualmente."

**[MOSTRAR O OUTPUT — agente encontrando a info]**

> "Isso é busca semântica. Não é grep, não é palavra-chave exata. Ele entende o significado. Se eu perguntar 'como está meu SaaS de métricas', ele vai achar o mesmo arquivo.
>
> Dois tools por baixo dos panos:
> - `memory_search` — busca em tudo, traz os chunks mais relevantes
> - `memory_get` — lê só as linhas específicas que precisa
>
> Você não precisa chamar esses tools manualmente. O agente usa automaticamente quando você pergunta algo."

---

## BLOCO 5 — Como pedir para salvar (3 min)

**[CÂMERA FRONTAL]**

> "Maior erro de quem começa: achar que o agente vai lembrar sozinho.
>
> Não vai. Se não está em arquivo, não existe na próxima sessão.
>
> A diferença:"

**[MOSTRAR NA TELA — slide simples ou digitar no terminal]**

> "❌ 'Lembra disso' → morre quando você fechar a janela
> ✅ 'Salva em memory/context/decisions.md' → permanente"

**[DEMO AO VIVO: digitar uma decisão e pedir pra salvar]**

> "Vou tomar uma decisão agora: todas as integrações novas precisam ter documentação antes de ir pra produção. Vou pedir pra salvar:"

**[DIGITAR: "Ficou decidido: toda integração nova precisa ter documentação antes de ir pra produção. Salva em memory/context/decisions.md como decisão permanente."]**

**[MOSTRAR: agente abrindo o arquivo e salvando]**

> "Feito. Sessão nova, esse contexto vai estar lá.
>
> Critério rápido de onde salvar:
> - Decisão que não muda → context/decisions.md
> - Erro que não pode repetir → context/lessons.md
> - Status de projeto → projects/nome.md
> - Aguardando seu input → pending.md"

---

## BLOCO 6 — Encerramento (1:30 min)

**[CÂMERA FRONTAL]**

> "Recapitulando o que mudou:
>
> Um — busca semântica funciona nativamente, sem chave de API.
>
> Dois — subpastas por categoria. Projects com um arquivo por projeto. Context separado de integrations separado de sessions.
>
> Três — o agente só carrega automaticamente SOUL, USER, AGENTS, MEMORY e as sessões de hoje e ontem. Todo o resto é sob demanda.
>
> Quatro — para salvar, você precisa ser explícito. 'Salva em memory/context/decisions.md'. Sem isso, não existe.
>
> O material desta aula tá no Drive — tem o guia em PDF com a estrutura completa, o prompt pra você pedir pro agente reorganizar a memória, e o PRD atualizado. Linka na descrição.
>
> Qualquer dúvida, manda no grupo. Até a próxima."

---

## Checklist pré-gravação

- [ ] Sessão nova aberta no terminal (contexto zerado)
- [ ] VS Code com `memory/` visível e arquivos reais (metricaas.md, decisions.md)
- [ ] MEMORY.md aberto em outra aba
- [ ] Notificações desativadas
- [ ] Testou a demo do memory_search antes de gravar

## Timings aproximados

| Bloco | Conteúdo | Tempo |
|-------|----------|-------|
| 1 | Abertura | 1:30 |
| 2 | Carrega vs. busca | 4:00 |
| 3 | Estrutura de subpastas | 4:00 |
| 4 | Busca semântica (demo) | 4:00 |
| 5 | Como salvar (demo) | 3:00 |
| 6 | Encerramento | 1:30 |
| **Total** | | **~18 min** |

## Links para colocar na descrição

- Material do aluno (PDF): Drive → Curso OpenClaw → aula-04-memoria → modulo-04-memoria.pdf
- Prompt de implementação: Drive → aula-04-memoria → prompts → modulo-04-memoria.md
- PRD atualizado: Drive → aula-04-memoria → prd → memory-architecture.md
