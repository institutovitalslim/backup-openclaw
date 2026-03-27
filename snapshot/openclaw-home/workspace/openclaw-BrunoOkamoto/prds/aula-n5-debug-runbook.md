# PRD — Aula N-5: Debug Passo a Passo — Runbook Padrão de Diagnóstico

**Módulo:** N — Troubleshooting & Manutenção  
**Aula:** N-5  
**Duração estimada:** 25–30 minutos  
**Nível:** Intermediário / Avançado  
**Formato:** Screencast com terminal ao vivo + slides de apoio  

---

## Objetivo da Aula

Ao final desta aula, o aluno saberá seguir um runbook sistemático de 5 etapas para diagnosticar e resolver qualquer problema no OpenClaw — seja um bot silencioso, credenciais inválidas, configuração quebrada ou um erro desconhecido que precisa ser escalado.

---

## Roteiro de Gravação

### [00:00–02:00] Abertura

**Script (Bruno fala):**

> "Olá, pessoal! Nesta aula vamos falar de algo que todo mundo precisa em algum momento: debug. O OpenClaw é robusto, mas coisas acontecem — um bot para de responder, uma chave de API expira, o gateway trava. E quando isso acontece sem você saber por onde começar... vira caos.
>
> Então hoje eu vou te dar o meu runbook pessoal. Cinco etapas, em ordem. Você segue do começo ao fim e, na minha experiência, isso resolve 95% dos problemas. Vamos lá."

**O que mostrar na tela:**
- Diagrama das 5 etapas (slide de abertura)
- Terminal limpo, pronto para uso

---

### [02:00–06:00] Etapa 1: Triagem Inicial — O Bot Responde?

**Script:**

> "A primeira etapa é a triagem. Antes de mexer em qualquer coisa, você precisa entender _o que_ exatamente está errado. Existem três cenários distintos, e cada um aponta para um caminho diferente.
>
> **Cenário A: O bot está completamente silencioso.** Você mandou mensagem, esperou, nada aconteceu. Isso quase sempre significa que o gateway não está rodando. O gateway é o processo que fica escutando as mensagens e roteando para o modelo de IA. Se ele cair, o bot simplesmente para de existir. A solução é imediata — vamos ver na Etapa 2.
>
> **Cenário B: O bot responde, mas com uma mensagem de erro.** Ótimo! Isso significa que o gateway está de pé. Agora você precisa _ler_ a mensagem de erro. Parece óbvio, mas muita gente entra em pânico e sai reiniciando tudo sem ler o que está escrito. O erro geralmente te diz exatamente o que fazer: chave inválida, rate limit atingido, arquivo de configuração com problema.
>
> **Cenário C: O bot responde, mas lento — muito lento.** Esse é um problema de performance, não de configuração. Eu cobri isso na aula N-4. Se o seu bot está demorando 30 segundos para responder, pula para lá. Aqui a gente foca em erros, não em lentidão.
>
> Então antes de continuar: qual dos três cenários você está vivendo? Isso define tudo."

**O que mostrar na tela:**
- Fluxograma de decisão: Silencioso / Erro / Lento
- Demonstração: mandar mensagem no Telegram e mostrar cada tipo de resposta (ou ausência dela)

---

### [06:00–12:00] Etapa 2: Verificar o Gateway

**Script:**

> "Se o bot está silencioso, começa aqui. O comando é simples:"

```bash
openclaw gateway status
```

> "Esse comando te diz se o processo do gateway está rodando ou não. Se a saída mostrar algo como `stopped` ou `inactive`, você sabe o problema. Reinicia:

```bash
openclaw gateway restart
```

> "Se o gateway estava parado, provavelmente ele volta e o bot começa a funcionar imediatamente. Testa rápido — manda um 'olá' lá.
>
> Mas e se o gateway reinicia, mas o problema persiste? Aí você precisa olhar os logs. Os logs do OpenClaw ficam em:

```bash
~/.openclaw/logs/gateway.log
```

> "Para ver as últimas linhas em tempo real, usa:

```bash
tail -f ~/.openclaw/logs/gateway.log
```

> "Agora, o que você está procurando nos logs? Existem quatro sinais de alerta que eu sempre busco:
>
> **1. `auth error` ou `unauthorized`** — Significa que a API key não está sendo aceita. Vai direto para a Etapa 3.
>
> **2. `rate limit exceeded`** — Você esgotou o limite de requisições do seu plano. Pode ser um pico de uso, um loop acidental, ou o plano precisando ser upgradado. Espere alguns minutos e tente novamente.
>
> **3. `context error` ou `context length exceeded`** — A conversa ficou longa demais para o modelo processar. Você precisa limpar o histórico da sessão ou ajustar o limite de contexto na configuração.
>
> **4. `connection refused` ou `timeout`** — Problema de rede ou o endpoint da API está fora. Verifica sua conexão e o status da API do seu provedor (Anthropic, OpenAI, etc.).
>
> Vou mostrar ao vivo como ler um log real e identificar esses sinais."

**O que mostrar na tela:**
- `openclaw gateway status` com saída de stopped/running
- `openclaw gateway restart` e output
- `tail -f ~/.openclaw/logs/gateway.log` com exemplos de cada tipo de erro destacados

---

### [12:00–17:00] Etapa 3: Verificar Credenciais

**Script:**

> "Chegamos na causa mais comum de problemas: credenciais. A API key expirou, foi rotacionada, ou simplesmente foi copiada errada. Começa com o diagnóstico:

```bash
openclaw status
```

> "Esse comando lista todos os modelos configurados e o status de cada um. Você vai ver algo como:

```
Models configured:
  ✓ anthropic/claude-opus-4   [active]
  ✗ openai/gpt-4o             [auth error]
```

> "Se algum modelo está com `auth error`, a chave está inválida ou ausente.
>
> O teste mais simples é mandar uma mensagem curta — literalmente 'olá' — e ver o que acontece. Se você receber `401 Unauthorized` nos logs, a chave está errada. Se receber `429 Too Many Requests`, é rate limit.
>
> Esses dois erros parecem iguais para o usuário — o bot não responde — mas a solução é completamente diferente:
>
> - **401 / auth error:** Você precisa reautenticar. A chave está inválida.
> - **429 / rate limit:** A chave é válida, mas você usou demais. Espere e tente de novo.
>
> Para reautenticar, vai no painel do provedor, gera uma nova chave, e atualiza no OpenClaw:

```bash
openclaw config set api_key <sua-nova-chave>
openclaw gateway restart
```

> "Depois do restart, testa novamente. Na minha experiência, 60% dos problemas que chegam no suporte se resolvem aqui."

**O que mostrar na tela:**
- `openclaw status` com exemplos de modelos ativos e com erro
- Comparação visual: 401 vs 429 nos logs
- Demonstração de como atualizar a chave e reiniciar

---

### [17:00–22:00] Etapa 4: Verificar Configuração

**Script:**

> "Se chegou até aqui e ainda não resolveu, o problema está na configuração. O OpenClaw tem um comando novo que eu recomendo fortemente usar _antes_ de qualquer restart:

```bash
openclaw config validate
```

> "Esse comando lê o seu `openclaw.json`, verifica a sintaxe, e aponta exatamente onde está o erro — com número de linha e tudo. Muito melhor do que reiniciar e ficar olhando pra uma tela branca tentando adivinhar.
>
> Os erros mais comuns que eu vejo no `openclaw.json`:
>
> **1. Vírgula sobrando ou faltando** — JSON é impiedoso. Uma vírgula a mais no final de um objeto já quebra tudo.
>
> **2. Campo obrigatório ausente** — `model`, `channel`, ou `token` faltando no bloco de configuração.
>
> **3. Referência a arquivo que não existe** — O `openclaw.json` apontando para um AGENTS.md num caminho que não existe.
>
> Falando em AGENTS.md: esse arquivo também pode causar problemas. Os erros mais comuns são:
>
> - **Indentação quebrada** — O AGENTS.md usa markdown. Um bloco de código mal fechado pode bagunçar o parsing.
> - **Referência circular** — Uma skill que importa outra que importa a primeira.
> - **Instrução conflitante** — Duas regras que se contradizem. O modelo fica preso tentando obedecer as duas.
>
> Skills também podem ter conflito. Se você adicionou uma skill nova e o bot começou a se comportar de forma estranha, testa removendo a skill temporariamente para isolar o problema.
>
> Depois de corrigir qualquer coisa no arquivo de configuração, sempre valida antes de reiniciar:

```bash
openclaw config validate && openclaw gateway restart
```

> "O `&&` garante que o restart só acontece se a validação passar. Boa prática."

**O que mostrar na tela:**
- `openclaw config validate` com saída de sucesso e com erro
- Exemplos de `openclaw.json` quebrado vs correto (diff lado a lado)
- Exemplo de AGENTS.md com problema de formatação

---

### [22:00–27:00] Etapa 5: Escalar o Problema

**Script:**

> "Se você chegou até aqui e ainda não conseguiu resolver, o problema é mais complexo. Não é vergonha nenhuma — o importante agora é pedir ajuda da forma certa.
>
> Tem uma ferramenta específica para isso:

```bash
openclaw doctor
```

> "O `doctor` faz uma checagem completa do ambiente: versão do OpenClaw, integridade dos arquivos de configuração, status dos modelos, permissões de arquivo, variáveis de ambiente. Ele gera um relatório que você pode compartilhar.
>
> Mas antes de postar no grupo de suporte, existe uma etiqueta importante: **nunca compartilhe suas chaves de API.** O `openclaw doctor` automaticamente mascara credenciais no output, mas se você for copiar logs manualmente, revise antes.
>
> O que coletar antes de pedir ajuda:
>
> **1. Versão do OpenClaw:**

```bash
openclaw --version
```

> **2. Output do `openclaw doctor`** (já com credenciais mascaradas)
>
> **3. Os últimos 50 logs do gateway:**

```bash
tail -50 ~/.openclaw/logs/gateway.log
```

> **4. Sua config sem credenciais:**

```bash
openclaw config export --mask-secrets
```

> "Com essas quatro coisas, qualquer pessoa do suporte consegue te ajudar em minutos. Sem isso, a conversa vira um interrogatório e demora muito mais.
>
> No grupo de suporte, cole tudo em um único bloco de código, descreva o que você fez antes do problema aparecer, e qual das 5 etapas do runbook você já executou. Isso economiza o tempo de todo mundo."

**O que mostrar na tela:**
- `openclaw doctor` com output completo
- `openclaw --version`
- `openclaw config export --mask-secrets`
- Template de post no grupo de suporte

---

### [27:00–30:00] Encerramento — Tabela de Erros & Primeiros Socorros

**Script:**

> "Antes de terminar, dois recursos que você vai querer ter sempre à mão.
>
> O primeiro é a tabela de erros mais comuns — está no material de apoio desta aula. Cola no favoritos.
>
> O segundo é o checklist de primeiros socorros: cinco comandos que resolvem 80% dos problemas. Quando o bot parar de funcionar, roda esses cinco na ordem, e na maioria das vezes um deles já resolve:

```bash
# 1. Ver status geral
openclaw status

# 2. Ver status do gateway
openclaw gateway status

# 3. Reiniciar o gateway
openclaw gateway restart

# 4. Validar configuração
openclaw config validate

# 5. Diagnóstico completo
openclaw doctor
```

> "Salva isso. Imprime se precisar. É o seu kit de ferramentas de debug.
>
> Nos vemos na próxima aula. Se tiver dúvida, o grupo de suporte está lá."

---

## Tabela de Erros Mais Comuns

| Erro | Sintoma | Causa | Solução |
|------|---------|-------|---------|
| `401 Unauthorized` | Bot silencioso ou erro na resposta | API key inválida ou expirada | Gerar nova chave, `openclaw config set api_key <nova>`, restart |
| `429 Too Many Requests` | Bot silencioso por um período | Rate limit atingido | Aguardar 1-5 minutos, reduzir frequência de uso |
| `Gateway stopped` | Bot completamente silencioso | Processo do gateway travou ou crashou | `openclaw gateway restart` |
| `Context length exceeded` | Erro após conversa longa | Histórico de conversa muito extenso | Limpar histórico ou ajustar `max_context` na config |
| `Connection refused` | Erro de conexão nos logs | Rede instável ou endpoint fora | Verificar internet, checar status do provedor |
| `JSON parse error` | Gateway falha ao iniciar | `openclaw.json` com erro de sintaxe | `openclaw config validate`, corrigir JSON |
| `File not found` | Gateway falha ao iniciar | Caminho de arquivo inexistente na config | Verificar todos os caminhos no `openclaw.json` |
| `Skill conflict` | Comportamento errático do bot | Duas skills com instruções conflitantes | Remover skill recém-adicionada, isolar problema |
| `AGENTS.md parse error` | Bot ignora instruções | AGENTS.md mal formatado (bloco de código aberto) | Fechar todos os blocos de código no AGENTS.md |
| `Model not found` | Erro ao processar mensagem | Nome do modelo incorreto na config | Verificar nomenclatura exata no `openclaw status` |

---

## Checklist de Primeiros Socorros

- [ ] `openclaw status` — ver estado geral dos modelos
- [ ] `openclaw gateway status` — confirmar se o gateway está rodando
- [ ] `openclaw gateway restart` — reiniciar o gateway
- [ ] `openclaw config validate` — validar o arquivo de configuração
- [ ] `openclaw doctor` — diagnóstico completo do ambiente

---

## Notas de Produção

- **Ambiente de gravação:** Terminal com fonte grande (16px+), tema escuro
- **Mostrar erros reais:** Preparar arquivos de configuração propositalmente quebrados para demonstração
- **Pausar nos momentos-chave:** Após cada comando, aguardar o output aparecer completamente antes de falar
- **Material de apoio:** HTML desta aula deve estar linkado na descrição do vídeo
- **Thumbnail:** Imagem com "5 etapas" e ícone de bug/ferramentas
