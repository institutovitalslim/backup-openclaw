# Roteiro de Gravação — "Skills: O Sistema de Superpoderes do Seu Agente"
**Aula dedicada | ~25 min | Módulo 6 reformulado**

---

## Setup antes de gravar

- Terminal aberto com workspace da Amora visível
- VS Code mostrando `skills/` com subpastas reais (content/, analytics/, operations/)
- ClawHub aberto no browser: clawhub.com
- GitHub aberto com um exemplo de skill de terceiro
- Notificações desativadas

---

## BLOCO 1 — Abertura: Por que 1 agente > múltiplos agentes (2 min)

**[CÂMERA FRONTAL]**

> "Quando a galera começa a usar OpenClaw de verdade, invariavelmente cai na mesma armadilha: começa a criar agente pra tudo.
>
> Agente de conteúdo. Agente de métricas. Agente de email. Agente de calendário.
>
> Parece que faz sentido. Na prática, é um pesadelo.
>
> Por quê? Porque cada agente tem seu próprio contexto. Você pede pra um criar um post, e outro não sabe que o post foi criado. Você toma uma decisão com um, o outro não sabe. Você vira o gerente de 8 agentes burros ao invés de ter 1 assistente inteligente.
>
> A forma certa é outra: **1 agente com múltiplos superpoderes.** Cada superpoder é uma skill.
>
> É exatamente isso que essa aula cobre."

---

## BLOCO 2 — O que é uma skill (3 min)

**[COMPARTILHA TELA: VS Code, abre skills/ no workspace]**

> "Uma skill é basicamente um manual de instruções + ferramentas que você dá pro seu agente.
>
> Estrutura mínima:"

**[MOSTRAR: tree de uma skill real, ex: skills/content/carrossel-linkedin/]**

```
skills/
└── content/
    └── carrossel-linkedin/
        └── SKILL.md
```

> "É só um arquivo SKILL.md. O agente lê esse arquivo quando vai executar a skill, entende o que pode fazer, e executa.
>
> Quando eu digo 'cria um carrossel de LinkedIn', o agente vai lá, lê a skill, e segue o processo definido. Não improvisa. Não alucina formato. Segue o que tá escrito.
>
> Isso é o ponto central: **skill = processo documentado que o agente executa de forma consistente.**"

**[MOSTRAR: abrir um SKILL.md real — conteúdo resumido]**

> "O arquivo tem: descrição do que a skill faz, quando usar, quais inputs ela precisa, e o passo a passo de execução. Pode ter exemplos, regras de qualidade, o que for necessário."

---

## BLOCO 3 — Como organizar skills em pastas (3 min)

**[COMPARTILHA TELA: VS Code, árvore completa de skills/]**

> "Organização importa. Minha estrutura:"

**[MOSTRAR: tree das skills/ reais]**

```
skills/
├── content/          ← tudo que produz conteúdo
│   ├── carrossel-instagram/
│   ├── carrossel-linkedin/
│   └── yt-hype/
├── analytics/        ← métricas e dados
│   ├── chartmogul/
│   └── ga4/
├── operations/       ← operações recorrentes
│   ├── notion-api/
│   ├── crisp-wrapup/
│   └── planner-adhd/
└── research/         ← pesquisa e inteligência
    ├── deep-research-protocol/
    └── blogwatcher/
```

> "Categorias claras. Quando vou criar uma skill nova, primeiro me pergunto: qual categoria? Se não existe categoria pra ela, pode ser que seja uma categoria nova — ou que eu precisaria criar antes.
>
> Por que isso importa? Porque quando você tem 20, 30 skills, sem organização você perde tempo achando o que tem disponível. E mais importante: o agente também fica confuso.
>
> A regra que uso: **cada skill resolve uma coisa bem feita.** Skill de carrossel de Instagram ≠ skill de carrossel de LinkedIn — porque o formato, tom e estrutura são completamente diferentes."

---

## BLOCO 4 — Como pedir pro agente executar uma skill (2 min)

**[CÂMERA FRONTAL → COMPARTILHA TELA: terminal com agente]**

> "Duas formas:"

**[DEMO AO VIVO: digitar os dois exemplos]**

> "Forma simples — você só pede:"

```
"Cria um carrossel de LinkedIn sobre o crescimento do Metricaas"
```

> "O agente identifica que existe a skill de carrossel LinkedIn, lê o SKILL.md automaticamente, e executa.
>
> Forma explícita — quando quer garantir qual skill usar:"

```
"Usa a skill carrossel-linkedin pra criar um carrossel sobre..."
```

> "O agente vai direto pra aquela skill específica.
>
> **Importante:** o agente só usa a skill se ela estiver na pasta skills/ do workspace. Ele não inventa. Se a skill não existe, ele ou improvisa — o que é menos consistente — ou te diz que não tem aquela skill."

---

## BLOCO 5 — Todo processo repetitivo vira skill (3 min)

**[CÂMERA FRONTAL]**

> "Essa é a mentalidade que muda o jogo.
>
> Toda vez que você faz a mesma coisa mais de duas vezes com seu agente, você tem um candidato a skill.
>
> Exemplos concretos:"

**[MOSTRAR NA TELA — lista simples]**

> "- Você toda semana pede um relatório de métricas → skill de weekly-metrics
> - Você toda vez que grava um vídeo pede título, descrição e tags → skill yt-hype
> - Você toda vez que tem uma reunião pede um brief de prep → skill meeting-prep
> - Você todo mês analisa o churn → skill churn-analysis
>
> Por que transformar em skill e não só repetir o prompt?
>
> Porque quando está na skill, o processo está documentado, testado, tem critérios de qualidade definidos. Você não precisa lembrar de detalhe. O agente não improvisa. E quando você quiser melhorar o processo, muda a skill — e muda pra sempre.
>
> Pensa assim: **um prompt é um pedido. Uma skill é um processo.**"

---

## BLOCO 6 — Sub-agentes executam skills específicas (2 min)

**[CÂMERA FRONTAL]**

> "Quando você usa sub-agentes — que é quando o agente principal delega uma tarefa pra um agente isolado rodar em background — a melhor prática é: o sub-agente tem um escopo claro e executa uma skill específica.
>
> Errado:"

**[MOSTRAR NA TELA]**

> ❌ "Spawna um agente pra 'cuidar do conteúdo'"

> "Certo:"

> ✅ "Spawna um agente pra executar a skill carrossel-linkedin com esse input"

> "A diferença: o agente solto vai tomar decisões aleatórias. O agente com skill tem um processo definido, inputs claros, e output previsível.
>
> Sub-agentes são ótimos pra tarefas paralelas e longas. Mas sempre com escopo fechado. Um sub-agente sem skill é um freelancer sem briefing."

---

## BLOCO 7 — Backup das suas skills (2 min)

**[COMPARTILHA TELA: terminal]**

> "Suas skills são ativos. Se você perder o workspace, perde todo o processo que documentou.
>
> Duas formas de backup:"

**[MOSTRAR: comando git]**

> "A mais simples: Git. Seu workspace já é um repositório. Commita e faz push:"

```bash
cd ~/seu-workspace
git add skills/
git commit -m "backup skills $(date +%Y-%m-%d)"
git push
```

> "Repositório privado no GitHub, acesso só seu.
>
> Segunda opção: script de backup automático. Você configura uma cron pra rodar de madrugada e fazer push automaticamente. Tem um script de exemplo no workspace de referência do curso.
>
> A regra de ouro: **skill que não está no Git não existe.** Um crash de disco, um workspace corrompido — e você perde meses de processo documentado. Não deixa isso acontecer."

---

## BLOCO 7b — Demo real: skill de Meta Ads (2 min)

**[COMPARTILHA TELA: VS Code → skills/analytics/meta-ads/SKILL.md]**

> "Antes de falar de segurança, quero mostrar como uma skill de analytics real funciona na prática.
>
> Essa é a skill de Meta Ads que rodo todo dia pra acompanhar as vendas da Pixel Educação — a empresa do curso. Vou abrir o SKILL.md:"

**[MOSTRAR: SKILL.md aberto — credenciais com XXXX]**

> "Olha aqui: o token do Meta e o ID da conta estão como `XXXX`. Nunca no código — sempre via 1Password. O agente busca em runtime.
>
> O que ela gera? Um dashboard como esse:"

**[MOSTRAR: arquivo exemplo-output-meta-ads.html no browser]**

> "Receita total, split por produto — OpenClaw Minicurso separado do Micro-SaaS PRO — taxa de reembolso, ROAS das campanhas. Gerado automaticamente, enviado pro Telegram todo dia às 8h.
>
> Isso é o que uma skill bem feita entrega. Você descreve o processo uma vez — e o agente executa toda vez que você pedir, ou no horário que você configurar."

---

## BLOCO 8 — Skills de terceiros: como usar com segurança (4 min)

**[COMPARTILHA TELA: clawhub.com aberto no browser]**

> "O ClawHub é o marketplace de skills da comunidade OpenClaw. Você encontra skills prontas pra instalar.
>
> Mas antes de instalar qualquer coisa, uma regra inviolável:"

**[CÂMERA FRONTAL — tom sério]**

> "Leia o código. Sempre.
>
> Uma skill tem acesso ao seu workspace, pode rodar comandos, pode ler arquivos. Skill maliciosa pode exfiltrar credenciais, deletar dados, executar qualquer coisa.
>
> O protocolo manual básico:"

**[COMPARTILHA TELA: terminal]**

```bash
git clone https://github.com/usuario/skill-nome /tmp/review-skill
cat /tmp/review-skill/SKILL.md
grep -r "curl" /tmp/review-skill/
grep -r "rm -rf" /tmp/review-skill/
grep -r "eval" /tmp/review-skill/
```

> "Funciona. Mas tem uma forma melhor.
>
> O Adrylan — um dos alunos mais avançados do curso — criou uma skill que audita outras skills. Ela é baseada no OWASP ASI Top 10 de 2026, no scanner Snyk e no Aguara. Nove categorias de verificação: prompt injection, exfiltração de dados, código malicioso, credenciais hardcoded, engenharia social...
>
> Você instala ela uma vez — e a partir daí, toda vez que encontrar uma skill nova, você cola o conteúdo e pede: 'audita essa skill'. O agente roda o checklist completo e te dá um relatório: limpo, atenção ou crítico.
>
> O SKILL.md completo tá no material bônus no Drive. **É a primeira skill que você deve instalar — antes de qualquer outra.**"

---

## BLOCO 9 — Skills do Claude Code funcionam no OpenClaw? (2 min)

**[CÂMERA FRONTAL]**

> "Pergunta frequente: tenho skills do Claude Code, funcionam no OpenClaw?
>
> Resposta curta: depende.
>
> Skills do Claude Code — os arquivos CLAUDE.md — têm um formato diferente. São instruções pro agente de como se comportar num projeto de código específico. Não são o mesmo conceito de skill do OpenClaw.
>
> Para adaptar:
> 1. O conteúdo de instrução geralmente é aproveitável — você pega o contexto e regras e coloca num SKILL.md do OpenClaw
> 2. Scripts bash que o Claude Code usa geralmente rodam no OpenClaw sem modificação — o ambiente de execução é compatível
> 3. O que não funciona direto são integrações específicas do Claude Code (MCP servers, por exemplo) — aí precisa adaptar pro equivalente OpenClaw
>
> Na prática: se você tem um prompt elaborado que usa no Claude Code, vira um SKILL.md no OpenClaw. O comportamento vai ser equivalente."

---

## BLOCO 10 — Encerramento (1 min)

**[CÂMERA FRONTAL]**

> "Resumindo:
>
> Um agente com skills > múltiplos agentes. Contexto unificado, processo consistente.
>
> Cada processo repetitivo vira skill. Prompt é pedido, skill é processo.
>
> Sub-agente sem skill = freelancer sem briefing. Sempre dê escopo claro.
>
> Backup no Git. Skills são ativos, trate como código.
>
> Skill de terceiro: leia o código antes. Sempre.
>
> O material completo — lista de skills por perfil, checklist de segurança e o prompt de instalação — tá no Drive, link na descrição."

---

## Checklist pré-gravação

- [ ] VS Code com `skills/` aberto mostrando categorias reais
- [ ] `skills/analytics/meta-ads/SKILL.md` aberto (credenciais como XXXX)
- [ ] `reports/misc/exemplo-output-meta-ads.html` aberto no browser (dashboard de vendas)
- [ ] Terminal pronto pra demo do clone + grep de segurança
- [ ] clawhub.com aberto no browser
- [ ] SKILL.md da skill-audit pronto pra mostrar (material bônus)
- [ ] Script de backup git pronto no terminal
- [ ] Notificações desativadas

## Timings aproximados

| Bloco | Conteúdo | Tempo |
|-------|----------|-------|
| 1 | Abertura: 1 agente > múltiplos | 2:00 |
| 2 | O que é uma skill | 3:00 |
| 3 | Organização em pastas | 3:00 |
| 4 | Como pedir pra executar | 2:00 |
| 5 | Todo processo vira skill | 3:00 |
| 6 | Sub-agentes + skills | 2:00 |
| 7 | Backup no Git | 2:00 |
| 7b | Demo real: skill Meta Ads | 2:00 |
| 8 | Skills de terceiros + skill-audit bônus | 4:00 |
| 9 | Claude Code → OpenClaw | 2:00 |
| 10 | Encerramento | 1:00 |
| **Total** | | **~26 min** |

## Links para colocar na descrição

- ClawHub: https://clawhub.com
- Skills por perfil (PDF): Drive → Curso OpenClaw → aula-06-skills → skills-by-profile.pdf
- Prompt de instalação: Drive → aula-06-skills → prompts → modulo-06-skills.md
