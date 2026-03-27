# ❓ Q&A — Infraestrutura Básica (Porta, SSH, Conexão)

> Linguagem simples. Sem terminal. Cole o prompt no seu bot e ele resolve.

---

## "Apareceu 'address already in use' ou 'port in use'"

**O que aconteceu:** Tem outro programa usando a mesma porta que o OpenClaw quer usar. É como duas pessoas tentando usar a mesma cadeira ao mesmo tempo.

**O que fazer:**
Cole esse prompt no seu bot:

```
Apareceu um erro de "port already in use" ou "address already in use".
Me ajuda a resolver:
1. Qual porta está em conflito?
2. Qual processo está usando essa porta?
3. Como resolver — parar o processo que está atrapalhando ou mudar a porta do OpenClaw?
4. Como confirmar que resolveu?
```

---

## "O bot não conecta / 'localhost refused connection'"

**O que aconteceu:** O gateway (o programa principal do OpenClaw) provavelmente não está rodando, ou está em uma porta diferente da que você está tentando acessar.

**O que fazer:**
Cole esse prompt no seu bot (se tiver acesso por outro canal):

```
Estou com problema de conexão — "connection refused" no localhost.
Me ajuda a diagnosticar:
1. O gateway do OpenClaw está rodando?
2. Em qual porta ele deveria estar?
3. Como verificar o status sem usar muito o terminal?
4. Como reiniciar o gateway de forma segura?
```

**Se não conseguir acessar o bot de jeito nenhum:** Tente acessar o painel do OpenClaw pelo Mission Control ou pelo link que você configurou no setup.

---

## "Apareceu 'command not found' quando tento usar algo"

**O que aconteceu:** O programa que você quer usar não está instalado, ou o caminho não está configurado corretamente.

**O que fazer:**
Cole esse prompt no seu bot:

```
Apareceu "command not found" quando tentei usar [NOME DO COMANDO].
Me ajuda:
1. Esse comando deveria estar instalado no OpenClaw?
2. Como instalar se não estiver?
3. Como verificar se está no caminho certo?
```

---

## "Não sei como acessar meu servidor remotamente"

**O que aconteceu:** Você precisa se conectar à sua VPS de qualquer lugar com segurança.

**O que fazer:**
Cole esse prompt no seu bot:

```
Preciso acessar meu servidor remotamente de forma segura.
Me explica de forma bem simples:
1. O que é um túnel SSH e pra que serve?
2. Como configuro acesso seguro via Tailscale ou Cloudflare Tunnel?
3. Qual é mais fácil pra iniciante?
4. Me guia pelo processo de configuração passo a passo.
```

**Dica:** Tailscale é a opção mais simples pra iniciantes — instala em 5 minutos e funciona como uma VPN pessoal gratuita.

---

## "Minha VPS está lenta / usando muita memória"

**O que fazer:**
Cole esse prompt no seu bot:

```
Minha VPS parece estar lenta ou usando muita memória/CPU.
Me ajuda a diagnosticar:
1. Quais processos estão consumindo mais recursos?
2. Tem algum agente ou cron rodando desnecessariamente?
3. O que posso fazer pra reduzir o consumo?
4. Quando faz sentido fazer upgrade da VPS?
```

---

*Última atualização: Fev/2026*
