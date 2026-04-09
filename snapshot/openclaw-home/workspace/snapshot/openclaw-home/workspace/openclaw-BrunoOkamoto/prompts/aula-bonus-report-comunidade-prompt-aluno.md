# Prompt do Aluno — Aula Bônus: Report de Comunidade

> Copie, adapte as partes entre colchetes e mande para o seu agente OpenClaw.

---

## Prompt Principal

```
Quero criar um relatório semanal automático das mensagens da minha comunidade.

**Minha fonte de dados:**
[Descreva onde ficam as mensagens. Exemplos:
- "Tenho um Supabase com tabela 'messages'. Campos: created_at, content, user_name, chat_id"
- "Uso o MyGroupMetrics — meu user_owner é [seu ID]"
- "Tenho acesso à API do Crisp com workspace_id [seu ID]"
- "Tenho um CSV exportado do grupo — posso fazer upload"]

**Grupos/canais a analisar:**
[Liste os grupos ou canais. Exemplos:
- "Grupo WhatsApp Alunos — chat_id: 120363xxxxxxxx"
- "Canal Telegram Clientes — @meucanal"
- "Workspace Crisp — todos os tickets"]

**Credenciais:**
[As credenciais estão no 1Password? Se sim, informe o nome do item e o vault.
Se não, me avise que eu te oriento a guardar antes de continuar.]

**O que quero no relatório:**
- Sentimento geral da semana (positivo / negativo / neutro)
- Dúvidas e temas mais frequentes
- Horários de pico de atividade
- Quem mais ajuda os outros (possíveis embaixadores)
- Comparação com as semanas anteriores

**Formato de entrega:**
- HTML dark theme com gráficos visuais
- Convertido em PDF
- Enviado aqui no Telegram toda segunda às 9h

**O que preciso que você faça:**
1. Criar uma Skill em skills/research/report-[nome-comunidade]/ com todo o processo documentado
2. Testar a conexão com minha fonte de dados
3. Gerar o primeiro relatório agora para eu ver como fica
4. Criar o cron para rodar automaticamente toda segunda às 9h

GUARDRAIL: apenas leitura nos dados. Nenhuma escrita, atualização ou deleção sem minha autorização explícita.
```

---

## Variações por Fonte de Dados

### Se você usa MyGroupMetrics (Supabase MGM)

```
Minha fonte de dados é o Supabase do MyGroupMetrics.
As credenciais estão no 1Password com o nome "Supabase MGM", vault "Amora Vault".
Campos relevantes da tabela interactions: created_at, message, user_name, chat_id, response_to.

Meus grupos:
- [Nome do grupo 1] — chat_id: [ID do grupo no WhatsApp]
- [Nome do grupo 2] — chat_id: [ID do grupo no WhatsApp]

Meu group_owner no banco é: [seu ID de usuário no MGM]
```

### Se você usa Crisp

```
Minha fonte de dados é o Crisp.
As credenciais (website_id e token) estão no 1Password como "Crisp API", vault "Amora Vault".
Quero analisar todas as conversas dos últimos 30 dias do workspace.
```

### Se você tem Supabase próprio

```
Tenho um Supabase próprio.
URL e service_key estão no 1Password como "[Nome do Item]", vault "[Nome do Vault]".
Tabela: [nome da tabela]
Campos: [created_at ou equivalente], [campo de texto], [campo de usuário], [campo de grupo/canal se houver]
```

### Se você tem só um CSV

```
Tenho um arquivo CSV com o histórico do grupo.
Vou fazer upload agora. Depois de analisar, quero que você crie um processo para eu poder atualizar o CSV toda semana e gerar o novo relatório.
Campos no CSV: [liste as colunas]
```

---

## O que esperar depois de mandar o prompt

O agente vai:

1. **Confirmar a conexão** — vai testar o acesso à sua fonte de dados e te dizer quantas mensagens encontrou
2. **Criar a Skill** — vai documentar todo o processo em `skills/research/report-[nome]/SKILL.md`
3. **Gerar o primeiro relatório** — HTML + PDF direto no chat para você ver e aprovar
4. **Criar o cron** — vai verificar se segunda às 9h está livre e configurar o agendamento

Se algo não funcionar (credencial errada, estrutura de tabela diferente), o agente vai te pedir as informações que faltam antes de continuar.

---

## Dicas

**Calibre o sentimento para o seu nicho**

Depois do primeiro relatório, se os percentuais não parecerem certos, peça:
```
O sentimento positivo está alto demais / baixo demais. 
Me mostra quais mensagens foram classificadas como positivas e negativas.
Quero ajustar o dicionário de palavras.
```

**Adicione tópicos específicos da sua área**

```
Quero que o relatório identifique também mensagens sobre [seu tópico específico].
Palavras-chave: [lista de palavras]
```

**Mude a frequência**

```
Em vez de semanal, quero relatório mensal — todo dia 1 às 8h.
Ajusta o cron para: 0 8 1 * *
```
