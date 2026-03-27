# ❓ Q&A — Telegram (Config, Allowlist, Privacidade)

> Linguagem simples. Sem terminal. Cole o prompt no seu bot e ele resolve.

---

## "Qualquer pessoa consegue mandar mensagem pro meu bot e ele responde"

**O que aconteceu:** Seu bot está configurado como "aberto" — qualquer pessoa que descobrir o username dele pode usar. É como deixar a porta da sua casa aberta.

**O que fazer:**
Cole esse prompt no seu bot:

```
Meu bot está respondendo qualquer pessoa. Preciso restringir isso.
Me ajuda a:
1. Descobrir qual é o meu ID numérico do Telegram
2. Configurar o dmPolicy para "allowlist" 
3. Adicionar meu ID na lista de permitidos
4. Confirmar que ficou certo testando
Explica tudo passo a passo.
```

---

## "Meu bot não me responde mais depois que configurei a allowlist"

**O que provavelmente aconteceu:** Você colocou a allowlist mas esqueceu de incluir o SEU próprio ID — ou digitou errado.

**O que fazer:**
Cole esse prompt no seu bot (via outro canal, como chat direto se tiver):

```
Não consigo mais mandar mensagem pro meu bot principal. 
Acho que me tranquei fora da allowlist.
Me ajuda a verificar:
1. Qual é o meu ID do Telegram? (me diz como descobrir)
2. Como vejo quem está na allowlist atual?
3. Como adiciono meu ID corretamente?
```

**Como descobrir seu ID do Telegram:** Mande `/start` para @userinfobot no Telegram — ele te responde com seu ID numérico.

---

## "Bot não funciona em grupo / tópico"

**O que fazer:**
Cole esse prompt no seu bot:

```
Meu bot não está respondendo no grupo/tópico do Telegram.
Me ajuda a verificar:
1. O Privacy Mode do bot está desativado? (precisa estar desativado pra funcionar em grupo)
2. O ID do grupo está na configuração de canais permitidos?
3. Tem alguma configuração de "allowFrom" ou "allowedIds" que precisa atualizar?
Me guia passo a passo.
```

**Dica rápida:** No BotFather, envie `/mybots` → selecione seu bot → `Bot Settings` → `Group Privacy` → `Turn off`. Isso resolve 80% dos problemas em grupo.

---

## "Apareceu um erro com allowedIds ou allowFrom — o que mudou?"

**O que aconteceu:** O OpenClaw atualizou o formato da configuração. Versões antigas usavam `allowedIds` ou `allowFrom` — a versão atual usa `dmPolicy: "allowlist"` com `allowedUsers`.

**O que fazer:**
Cole esse prompt no seu bot:

```
Minha configuração do Telegram tem "allowedIds" ou "allowFrom" que parecem ser de uma versão antiga.
Me ajuda a:
1. Identificar qual formato estou usando
2. Migrar para o formato atual (dmPolicy + allowedUsers)
3. Verificar se a config ficou correta
4. Reiniciar o gateway pra aplicar
```

---

## "Como adiciono mais pessoas pra poderem usar meu bot?"

**O que fazer:**
Cole esse prompt no seu bot:

```
Quero adicionar uma nova pessoa para poder usar meu bot.
O ID do Telegram dela é: [COLOQUE O ID AQUI]
Me guia como adicionar ela na allowlist corretamente.
```

**Como a pessoa descobre o ID dela:** Ela manda `/start` pro @userinfobot no Telegram.

---

*Última atualização: Fev/2026*
