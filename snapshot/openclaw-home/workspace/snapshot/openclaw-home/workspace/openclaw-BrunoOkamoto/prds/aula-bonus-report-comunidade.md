# PRD — Aula Bônus: Report de Comunidade com IA

> **Nível:** Intermediário
> **Duração estimada:** 15–18 minutos
> **Pré-requisito:** OpenClaw instalado, pelo menos um grupo conectado ao MyGroupMetrics (ou qualquer fonte de dados de mensagens)

---

## 🎯 Objetivo da Aula

Ao final desta aula, o aluno vai entender que o OpenClaw pode:

1. Conectar em qualquer banco de dados com mensagens (Supabase, API REST)
2. Analisar automaticamente o humor, as dúvidas e os padrões da comunidade
3. Gerar um relatório visual completo — HTML + PDF — sem escrever uma linha de código manualmente
4. Entregar esse relatório todo na sua caixa de entrada, toda semana, sem interação

**Ângulo da aula:** O resultado primeiro. O código é só a prova de que é simples.

---

## 📋 Script de Gravação — Seção por Seção

---

### 🎬 ABERTURA (0:00 – 1:30)

**[Bruno na tela com o PDF do report aberto ao lado]**

> "Fala, pessoal. Olha esse PDF aqui."

> "Esse relatório chegou pra mim ontem, de manhã, sem eu pedir nada. Ele me mostra: humor da comunidade essa semana, quais dúvidas mais repetiram, que horas o grupo mais ativa, quem são os alunos que mais ajudam os outros."

> "14.725 mensagens analisadas. Quatro grupos de WhatsApp. Quatro semanas de dados. E eu não fiz absolutamente nada."

> "Nessa aula eu vou te mostrar como eu fiz isso — e mais importante: como você vai fazer igual para a sua comunidade."

---

### 📊 SEÇÃO 1: O problema que isso resolve (1:30 – 4:00)

**[Bruno na câmera, tom de conversa]**

> "Deixa eu te fazer uma pergunta rápida."

> "Você tem grupo de WhatsApp de alunos, clientes, comunidade? Quantas mensagens por semana? 200? 500? 2.000?"

> "Agora me diz: você consegue responder essas perguntas sem abrir o grupo agora?"

**[Mostrar na tela — slide com as 4 perguntas]**

> "Qual foi o humor da comunidade essa semana — as pessoas estão animadas ou frustradas?"
> "Qual dúvida apareceu mais de três vezes nos últimos 7 dias?"
> "Que horas do dia o grupo mais engaja — quando eu devo fixar comunicados?"
> "Quem são os membros que mais ajudam os outros — meus potenciais moderadores?"

> "A maioria dos criadores não consegue responder nenhuma das quatro. Porque essas respostas estão enterradas em milhares de mensagens."

> "O OpenClaw lê tudo isso, analisa e entrega as respostas toda segunda de manhã."

---

### 🔁 SEÇÃO 2: Como funciona em 3 passos (4:00 – 7:00)

**[Tela: diagrama simples com 3 blocos]**

> "O processo inteiro tem três partes. E cada parte o agente faz sozinho."

**Passo 1 — Buscar os dados**

> "O agente se conecta na sua base de dados — no meu caso é o Supabase do MyGroupMetrics. Busca todas as mensagens dos últimos 30 dias. Com paginação, porque bancos de dados grandes devolvem os dados em pedaços."

> "Resultado: 14.725 mensagens num arquivo JSON na memória do agente."

**Passo 2 — Analisar**

> "Com os dados em mãos, o agente aplica análises. Sentimento: quais mensagens são positivas, quais são negativas, com exemplos reais para você entender por quê. Tópicos: o que mais aparece — instalação, erros, cases de sucesso, custos. Padrões: horários, dias da semana, quem responde mais, quem some."

> "Tudo isso sem biblioteca de machine learning. Python puro, dicionário de palavras calibrado para o seu contexto."

**Passo 3 — Entregar**

> "O agente gera um HTML completo — dark theme, gráficos em CSS, 14 seções — converte em PDF pelo Chrome e manda direto no Telegram. Eu recebo o arquivo aqui, e posso mandar pros alunos se quiser."

---

### 🧠 SEÇÃO 3: A Skill — a memória do processo (7:00 – 10:00)

**[Tela: o arquivo SKILL.md aberto no editor]**

> "Agora vou te mostrar a parte mais importante. Não é o código — é a Skill."

> "Toda vez que o agente acorda pra gerar o relatório, ele lê esse arquivo aqui. A Skill é a memória do processo — está documentado onde buscar os dados, como analisar, qual formato gerar, onde salvar, como entregar."

> "Se eu não tivesse isso, o agente esqueceria tudo entre uma sessão e outra. Com a Skill, ele sempre faz igual. Toda semana. Sem variação."

**[Mostrar a estrutura do SKILL.md]**

> "Olha a estrutura: o que a skill faz, quando usar, os grupos que ela analisa com os IDs, como buscar as credenciais no 1Password — nunca senha hardcoded —, o processo passo a passo, e no final: guardrail. Só leitura. Zero escrita no banco sem autorização."

> "Isso aqui é o que transforma uma tarefa que eu fiz uma vez em um processo que roda para sempre."

---

### ⏰ SEÇÃO 4: O Cron — set and forget (10:00 – 12:30)

**[Tela: cron list no terminal ou na interface]**

> "Com a Skill pronta, criar o cron é a parte mais rápida."

> "Pedi pro agente: 'Cria um cron pra rodar essa skill toda segunda às 9h.' Ele verificou se o horário estava livre, configurou e pronto."

**[Mostrar a config do cron]**

> "Repara no detalhe: sessionTarget isolated. A tarefa roda numa sessão separada — não polui o histórico do meu chat principal. E o delivery: announce para o topic do Telegram. O resultado chega aqui, no grupo certo."

> "Desde que configurei, não precisei pensar mais nisso. Chega toda segunda. Leio em dois minutos. Tenho o panorama completo da semana."

---

### 🌍 SEÇÃO 5: Adapte para o seu contexto (12:30 – 15:30)

**[Bruno na câmera]**

> "Agora a pergunta que você está fazendo: 'Bruno, mas eu não tenho MyGroupMetrics. Isso funciona pra mim?'"

> "Sim. Você precisa de três coisas:"

**[Mostrar na tela — lista simples]**

> "Primeiro: uma fonte de dados com mensagens acessível por API — pode ser Supabase, Crisp, Zendesk, qualquer coisa que tenha endpoint REST."

> "Segundo: saber quais campos tem nessa tabela — criado_em, mensagem, usuário. Três campos já são suficientes."

> "Terceiro: pedir pro agente criar a Skill adaptada para o seu contexto."

**[Mostrar o prompt do aluno na tela]**

> "Tem um prompt no material da aula. Você copia, adapta com seus dados, manda pro agente. Ele vai criar a Skill, testar a conexão, gerar o primeiro relatório e montar o cron. Em menos de uma hora você tem o processo rodando."

> "Comunidade de clientes, grupo de alunos, canal de suporte — qualquer coisa que gere mensagens vira inteligência acionável."

---

### 🎯 FECHAMENTO (15:30 – 17:00)

**[Bruno na câmera, tom de encerramento]**

> "Deixa eu resumir o que aconteceu aqui."

> "Eu tinha 14.725 mensagens que eu nunca ia ler. Agora toda segunda de manhã eu sei exatamente o que está acontecendo na comunidade: o que trava os alunos, quem está evoluindo, quando o grupo pulsa, o que precisa de atenção."

> "Isso não é análise — é inteligência operacional. É a diferença entre gerir uma comunidade no escuro e gerir com dados."

> "O processo inteiro — conexão, análise, relatório, entrega — está documentado numa Skill de uma página. Roda automaticamente. Não depende de mim."

> "Na próxima aula a gente vai ver como criar Skills do zero para qualquer processo recorrente que você queira automatizar. Até lá."

---

## 🖥️ O que mostrar na tela (guia de screen)

| Momento | O que mostrar |
|---------|--------------|
| Abertura | PDF do report aberto — a câmera vê Bruno e o PDF lado a lado |
| Seção 1 | Slide com as 4 perguntas que a maioria não consegue responder |
| Seção 2 | Diagrama: 3 blocos (Buscar → Analisar → Entregar) |
| Seção 2 (detalhe) | Briefly: terminal mostrando "Total: 14.725 mensagens" |
| Seção 3 | SKILL.md aberto no editor — scroll lento |
| Seção 4 | `cron list` no terminal + config do cron |
| Seção 5 | Prompt do aluno (material da aula) na tela |
| Fechamento | Bruno na câmera, encerramento direto |

---

## ⚠️ Pontos de atenção para a gravação

- **Não entrar em detalhes de código Python** — mencionar que existe, mostrar brevemente se quiser, mas não explicar linha por linha
- **Mostrar o PDF real** na abertura — o impacto visual é o gancho
- **Pronunciar "MyGroupMetrics"** como contexto do caso, mas deixar claro que funciona com outras fontes
- **Mencionar paginação** apenas como "o agente sabe como buscar os dados em pedaços" — sem detalhes técnicos
- **Guardrail** — mencionar brevemente que a Skill tem regra de só leitura. Passa confiança para o aluno

---

## 📁 Arquivos da Aula

| Arquivo | Destino Drive |
|---------|--------------|
| HTML do material | Aulas extras / Materiais Aulas Extras / html/ |
| PDF do material | Aulas extras / Materiais Aulas Extras / pdf/ |
| Prompt do aluno | Aulas extras / Materiais Aulas Extras / |
| Exemplo de report (PDF) | Aulas extras / use-cases/ |
