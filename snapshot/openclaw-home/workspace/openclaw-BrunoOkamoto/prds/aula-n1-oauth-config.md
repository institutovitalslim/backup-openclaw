# PRD — Aula N-1: Configurar Credenciais — API Key Anthropic + OpenAI

> **Nível:** Iniciante / Setup  
> **Duração estimada:** 15–20 minutos  
> **Pré-requisito:** OpenClaw instalado, acesso à internet
> **Atualizado:** Anthropic bloqueou OAuth para planos Pro — novo fluxo recomendado

---

## 🎯 Objetivo da Aula

Ao final desta aula, o aluno será capaz de:

1. Entender por que o fluxo OAuth/`setup-token` da Anthropic **não funciona mais** para a maioria dos alunos
2. Configurar a Anthropic via **API Key direta** (fluxo correto e recomendado)
3. Gerar e configurar API Keys na **OpenAI Platform** (OAuth ainda funciona aqui)
4. Configurar as credenciais no OpenClaw via `openclaw config`
5. Verificar se a configuração está funcionando com `openclaw status`
6. Diagnosticar e resolver os **erros mais comuns** de autenticação

---

## 🚨 AVISO IMPORTANTE — Leia Antes de Começar

> **A Anthropic bloqueou OAuth para planos Pro.**

Se você tem uma assinatura Claude Pro ($20/mês), **o fluxo `setup-token` / `openclaw setup-token` NÃO FUNCIONA MAIS para você.** Isso afeta a maioria dos alunos e é a dúvida #1 do curso (~20 ocorrências nos fóruns).

**Sintoma:** Você tenta rodar `openclaw setup-token` (ou o fluxo OAuth da Anthropic no wizard), parece funcionar, mas na primeira mensagem pro bot aparece erro "OAuth flow not supported for Pro plans" ou "Unauthorized".

**Solução:** Ignorar completamente o fluxo OAuth e usar uma **API Key direta**, que é o que vamos aprender nessa aula.

> ⚠️ **Não é bug do OpenClaw.** A Anthropic mudou a política deles. O OpenClaw se adaptou, mas o wizard de onboarding ainda pode mostrar a opção OAuth — **ignore e use API Key**.

---

## 📋 Script de Gravação — Seção por Seção

### 🎬 ABERTURA (0:00 – 2:00)

**[Bruno na tela, tom direto]**

> "Fala, pessoal! Aula N-1 do curso OpenClaw — configurar credenciais. Essa aula existe porque é aqui que a maioria das pessoas trava."

> "E eu preciso te avisar sobre uma mudança importante: a Anthropic, que faz o Claude, bloqueou o login OAuth para planos Pro. Sim — se você paga $20/mês de assinatura do Claude, o fluxo antigo não funciona mais. Vou te mostrar o jeito certo, que é mais simples na verdade."

> "Se você já tentou configurar, viu algum erro de 'setup-token' ou 'OAuth', ou simplesmente nunca conseguiu fazer o Claude responder — essa aula resolve isso de vez."

---

### 📚 SEÇÃO 1: Por Que o Fluxo Antigo Quebrou (2:00 – 5:00)

**[Tela mostrando diagrama ou slide]**

> "Antes da mudança, a Anthropic tinha um fluxo onde você podia conectar o OpenClaw via OAuth — basicamente, você autorizava o acesso pela interface web, sem precisar de uma API Key. Parecia mais conveniente."

> "Mas em 2026, a Anthropic decidiu que esse fluxo OAuth só funciona para planos API (pay-per-use). Pra planos Pro ($20/mês) — que é o que a maioria tem — eles bloquearam. Motivo? Prevenção de abuso e separação clara entre 'assinatura pra usar no chat' vs 'acesso programático via API'."

**[Pausa para ênfase]**

> "Então a situação hoje é:"

| Situação | Funciona? | O que fazer |
|----------|-----------|-------------|
| Plano Pro ($20/mês) + OAuth | ❌ Bloqueado | Criar API Key separada |
| Plano gratuito da Anthropic + OAuth | ❌ Bloqueado | Criar API Key com billing |
| API Key direta (qualquer plano) | ✅ Funciona | O que vamos fazer |

> "A boa notícia: a API Key é mais simples de entender e mais flexível. Você controla exatamente quanto gasta. Vamos configurar isso agora."

---

### 💳 SEÇÃO 1.5: E se eu tenho assinatura Pro? (5:00 – 7:30)

**[Tela: browser em console.anthropic.com]**

> "Antes de continuar — se você paga pelo Claude Pro, precisa entender algo importante."

> "Sua assinatura Pro ($20/mês) e o acesso via API são **coisas separadas**. Sua assinatura dá acesso ao chat em claude.ai — não à API. São sistemas de billing diferentes."

> "Pra usar o OpenClaw com o Claude, você precisa:"
> 1. Acessar console.anthropic.com (diferente de claude.ai)
> 2. Adicionar um método de pagamento SEPARADO (ou créditos)
> 3. Criar uma API Key

> "Sim, parece injusto pagar duas vezes. Mas é assim que a Anthropic estruturou. A boa notícia: com controle fino de modelo (Haiku para tarefas simples, Sonnet para interação), o gasto real da API costuma ser $5-15/mês — muito menos que a assinatura Pro."

> "Se você quer EVITAR pagar a mais: pode migrar do Pro para API-only. Cancela o Pro, usa só a API. Você perde o acesso ao claude.ai, mas o OpenClaw funciona melhor assim de qualquer forma."

---

### 🔑 SEÇÃO 2: Gerando sua API Key na Anthropic (7:30 – 11:00)

**[Tela: Browser abrindo console.anthropic.com]**

> "Vamos criar a API Key. Acesse **console.anthropic.com** — atenção: é o **console**, não o claude.ai."

**[Mostrar navegação no painel]**

> "Depois que você logar, clique em **'API Keys'** no menu lateral (ou Settings → API Keys)."

> "Clique em **'Create Key'**."

**[Mostrar o formulário]**

> "Dê um nome pra sua chave — recomendo `openclaw-pessoal`. Isso ajuda a gerenciar depois."

> "**ATENÇÃO agora!** A chave vai aparecer na tela. Parece com `sk-ant-api03-XXXXXX...`"

**[Box de AVISO na tela]**

> "**COPIE AGORA.** Essa é sua única chance de ver a chave completa. Depois disso, a Anthropic não mostra mais. Salva num gerenciador de senhas (1Password, Bitwarden) ou num lugar seguro."

> "Mas antes de sair feliz — verifique se tem billing ativo. Vai em **Settings → Billing** e confirma que tem um cartão cadastrado ou créditos. Sem billing, a chave funciona mas toda chamada retorna erro 402."

---

### 🔑 SEÇÃO 3: Gerando sua API Key na OpenAI (11:00 – 13:30)

**[Tela: Browser abrindo platform.openai.com]**

> "Agora vamos pra OpenAI. Aqui é mais direto — OAuth ainda funciona, mas API Key também. Vamos usar API Key pra manter consistência."

> "Acesse **platform.openai.com/api-keys** e clique em **'Create new secret key'**."

> "Dê um nome, confirma, e copie a chave. Começa com `sk-proj-` ou `sk-`."

> "Mesma regra: **copie agora**, não aparece de novo."

> "Verifique crédito em **Billing → Usage**. OpenAI precisa de crédito ou free trial ativo pra funcionar."

---

### ⚙️ SEÇÃO 4: Configurando o OpenClaw com `openclaw config` (13:30 – 17:00)

**[Tela: Terminal aberto]**

> "Agora que temos as chaves, vamos configurar. Abre o terminal e digita:"

```bash
openclaw config
```

> "Isso abre o assistente interativo. Selecione Anthropic, cole sua API Key quando pedir."

> "Depois selecione OpenAI (se tiver configurado também) e cole a chave."

**[IMPORTANTE — mostrar isso]**

> "Atenção: se o wizard mostrar uma opção 'OAuth' ou 'Setup Token' para a Anthropic — **ignore**. Escolha sempre 'API Key'. Eu sei que parece contraditório o próprio OpenClaw mostrar essa opção, mas ela não funciona mais para a maioria das contas."

---

### ✅ SEÇÃO 5: Testando com `openclaw status` (17:00 – 19:00)

**[Tela: Terminal]**

> "Para verificar se tudo está certo, rode:"

```bash
openclaw status
```

> "Você vai ver algo assim:"

```
✅ OpenClaw Status
─────────────────────────────
Provider: Anthropic (Claude)
Model:    claude-sonnet-4-5
API Key:  sk-ant-...api03 (valid)
Status:   Connected

Provider: OpenAI
Model:    gpt-4o
API Key:  sk-proj-...XxXx (valid)  
Status:   Connected
─────────────────────────────
All providers configured ✓
```

> "Se aparecer 'Connected' — perfeito! Se aparecer erro, próxima seção."

---

### 🔧 SEÇÃO 6: Erros Comuns e Como Resolver (19:00 – 22:00)

**[Tela: Slides com erros]**

**[Erro 1 — TOP 1 do curso]**

> "**'OAuth flow not supported' ou 'setup-token only'** — esse é o erro #1 no fórum. Causa: você usou o fluxo OAuth ou `openclaw setup-token`. Solução: rode `openclaw config` de novo, escolha 'API Key' (não OAuth), cole sua chave do console.anthropic.com."

**[Erro 2]**

> "**'Invalid API Key'** — a chave está errada, expirada ou foi revogada. Vai no console do provider, cria uma nova, reconfigura."

**[Erro 3]**

> "**'HTTP 402 — Payment Required'** — você tem a chave certa mas não tem billing ativo. Anthropic: vai em console.anthropic.com → Billing → adiciona cartão. OpenAI: platform.openai.com → Billing → adiciona crédito."

**[Erro 4]**

> "**Rate limit (HTTP 429)** vs credencial inválida (HTTP 401) — são coisas diferentes! Rate limit é temporário, espera uns minutos. Credencial inválida é permanente, precisa reconfigurar."

---

### 🎯 ENCERRAMENTO (22:00 – 23:00)

> "Resumo da aula: o fluxo OAuth da Anthropic não funciona mais para planos Pro — use sempre API Key. A OpenAI ainda funciona com OAuth mas API Key é mais simples. Configuramos com `openclaw config`, verificamos com `openclaw status`."

> "Se você tem assinatura Pro — vai precisar de billing separado na API para usar o OpenClaw. Vale a pena: com uso inteligente de modelos, você gasta menos que o Pro e tem muito mais controle."

> "Na próxima aula, a gente começa a usar de verdade. Mas antes, faz o exercício prático!"

---

## 🛠️ Passo a Passo Técnico Detalhado

### 1. Gerar API Key — Anthropic

1. Acesse [console.anthropic.com](https://console.anthropic.com) (**não** claude.ai)
2. Faça login ou crie uma conta
3. No menu lateral: **Settings → API Keys** (ou clique no ícone de chave)
4. Clique em **"Create Key"**
5. Dê um nome descritivo (ex: `openclaw-pessoal`)
6. **COPIE A CHAVE IMEDIATAMENTE** — começa com `sk-ant-api03-`
7. Salve num gerenciador de senhas (ex: 1Password, Bitwarden)
8. Verifique billing: Settings → Billing → cartão cadastrado ✅

> ⚠️ **Se você tem plano Pro:** Você ainda precisa fazer esses passos. A assinatura Pro e a API são sistemas de billing separados.
> ⚠️ **A Anthropic só exibe a chave completa uma vez.** Após fechar o modal, não é possível visualizá-la novamente.

### 2. Gerar API Key — OpenAI

1. Acesse [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Faça login na sua conta OpenAI
3. Clique em **"Create new secret key"**
4. Dê um nome (ex: `openclaw`)
5. **COPIE A CHAVE IMEDIATAMENTE** — começa com `sk-proj-` ou `sk-`
6. Verifique crédito em **Billing → Usage**

### 3. Configurar o OpenClaw

```bash
# Iniciar o assistente de configuração
openclaw config

# Quando aparecer opção OAuth/setup-token para Anthropic → IGNORE
# Escolha sempre "API Key"
# Cole sua chave quando solicitado
```

### 4. Verificar a Configuração

```bash
# Verificar status de todos os providers
openclaw status

# Saída esperada:
# ✅ Provider: Anthropic — Status: Connected
# ✅ Provider: OpenAI — Status: Connected
```

### 5. Onde as Credenciais são Armazenadas

| Sistema Operacional | Caminho |
|--------------------|---------|
| Linux / macOS | `~/.openclaw/config.json` |
| Windows | `C:\Users\<SeuNome>\.openclaw\config.json` |

> 🔒 **Segurança:** Esse arquivo tem permissões restritas (modo 600 no Linux/Mac). **Nunca commite esse arquivo no git.**

---

## 🚨 Tabela de Erros Comuns + Solução

| Erro | Causa | Solução |
|------|-------|---------|
| `OAuth flow not supported` / `setup-token only` | ⭐ **TOP 1** — Usou OAuth com plano Pro | Rode `openclaw config`, escolha "API Key", cole chave do console.anthropic.com |
| `Invalid API Key` | Chave errada, expirada ou revogada | Verifique/recrie a chave no console. Rode `openclaw config` novamente. |
| `HTTP 401 Unauthorized` | Credencial inválida | Mesma solução do Invalid API Key. |
| `HTTP 402 Payment Required` | Sem billing ativo na Anthropic | console.anthropic.com → Billing → adicione cartão/créditos |
| `HTTP 429 Too Many Requests` | Rate limit atingido (não é problema de chave) | Espere 1-5 minutos. Considere upgrade de plano se recorrente. |
| `Insufficient credits` | Sem crédito na OpenAI | platform.openai.com → Billing → adicione crédito. |
| `API Key not configured` | Nunca rodou `openclaw config` | Rode `openclaw config` e configure as chaves. |
| Chave funciona mas agente não responde | tools.profile = messaging (v2026.3.2) | `openclaw config set tools.profile full` |
| `model_not_available` | Modelo não disponível na tier | Troque para claude-haiku-4-5 ou claude-sonnet-4-5 |

---

## ✅ Checklist Final do Aluno

- [ ] Conta criada/acessada em console.anthropic.com (**não** claude.ai)
- [ ] API Key da Anthropic gerada e salva com segurança
- [ ] Billing ativo na Anthropic (cartão ou créditos)
- [ ] (Opcional) API Key da OpenAI gerada e salva
- [ ] (Opcional) OpenAI: crédito verificado em Billing
- [ ] `openclaw config` executado — escolheu "API Key" (não OAuth)
- [ ] `openclaw status` mostrando "Connected" para os providers configurados
- [ ] Arquivo `~/.openclaw/config.json` NÃO está no git (verificado .gitignore)
- [ ] Primeiros testes realizados com sucesso

---

## ❓ Dúvidas Frequentes

**1. Tenho Claude Pro — preciso pagar a mais?**

> Sim, infelizmente. Sua assinatura Pro dá acesso ao claude.ai (interface web), não à API. Para usar o OpenClaw, você precisa de billing separado no console.anthropic.com. A boa notícia: com modelos econômicos (Haiku para tasks simples), o gasto real costuma ser $5-15/mês.

**2. Posso cancelar o Pro e usar só a API?**

> Sim! Para uso com OpenClaw, API-only é na verdade a configuração ideal. Você perde o acesso ao claude.ai (a interface web bonita), mas o OpenClaw substitui isso com muito mais poder.

**3. Por que ainda aparece a opção OAuth no OpenClaw?**

> O OpenClaw ainda mantém a opção por compatibilidade com planos API legados. Mas para a grande maioria dos alunos com planos Pro ou contas novas, **não funciona**. Sempre use API Key.

**4. Preciso configurar os dois providers (Anthropic E OpenAI)?**

> Não é obrigatório. Configure apenas os que pretende usar. Para o curso, recomendamos pelo menos o Anthropic (Claude).

**5. Como trocar a chave depois de configurada?**

> Rode `openclaw config` de novo e insira a nova chave. O valor anterior é sobrescrito.

**6. O OpenClaw armazena minhas chaves na nuvem?**

> Não. As chaves ficam apenas localmente em `~/.openclaw/config.json`. O OpenClaw não envia suas credenciais para nenhum servidor externo.
