# PRD: Setup VPS na Hostinger (Bare Metal, sem Docker)

> Guia step-by-step para o Módulo 1 do curso.
> Bruno segue este roteiro na gravação.
> **Atualizado para OpenClaw v2026.3.2**

---

## Pré-requisitos

- Conta na Hostinger (https://www.hostinger.com)
- Conta na Anthropic (https://console.anthropic.com) com billing ativo
- Telegram instalado no celular

## Tempo estimado: 15-20 minutos

---

## Passo 1: Criar a VPS na Hostinger (3 min)

1. Acesse https://www.hostinger.com/vps-hosting
2. Escolha o plano mais barato (KVM 1 — suficiente pra OpenClaw)
   - 1 vCPU, 4GB RAM, 50GB SSD — mais que suficiente
3. **IMPORTANTE:** NÃO use o template Docker/One-Click do OpenClaw
4. Selecione **Ubuntu 24.04** como sistema operacional
5. Defina uma senha root forte (ou SSH key se souber)
6. Anote o IP da VPS

> **Por que não o One-Click Docker?**
> O Docker isola o agente num container — instalar skills, integrações e ferramentas extras fica muito mais complicado. Pra quem não é técnico, é uma barreira desnecessária. Instalando direto, tudo funciona como esperado.

---

## Passo 2: Conectar na VPS via SSH (2 min)

### No Mac/Linux:
```bash
ssh root@SEU_IP_DA_VPS
```
(digita a senha quando pedir)

### No Windows:
- Use o PuTTY ou o Windows Terminal
- Host: SEU_IP_DA_VPS
- User: root

### Primeira vez? A Hostinger tem terminal no painel:
- hPanel → VPS → Terminal (botão no topo)
- Funciona direto no navegador, sem instalar nada

> 💡 **Dica pro curso:** Mostrar as duas opções (terminal local + terminal do painel) pra atender quem não sabe usar SSH.

---

## Passo 3: Instalar o OpenClaw (3 min)

```bash
# Instalar OpenClaw (1 comando)
curl -fsSL https://openclaw.ai/install.sh | bash
```

Isso instala o Node.js (se necessário) e o OpenClaw.

Depois, rodar o wizard de configuração:

```bash
openclaw onboard --install-daemon
```

O wizard vai perguntar:

1. **Gateway mode:** → Escolher `Local`
2. **AI Provider:** → Escolher `Anthropic`
3. **API Key:** → Colar a API key da Anthropic
4. **Model:** → Escolher `Claude Sonnet` (bom e barato pra começar)
5. **Instalar como serviço?** → Sim (roda 24/7 automaticamente)

> 💡 **Dica pro curso:** Mostrar onde pegar a API key na Anthropic (console.anthropic.com → API Keys → Create Key). Explicar que precisa ter billing ativo.

---

## ⚠️ Passo 3.5: Configurar Perfil de Ferramentas (NOVO — v2026.3.2)

> 🔴 **CRÍTICO:** Este passo é OBRIGATÓRIO a partir da versão 2026.3.2. Sem ele, seu agente vai responder mensagens mas não vai conseguir fazer NADA útil.

A partir da versão **2026.3.2**, o OpenClaw vem com `tools.profile = messaging` por padrão. Isso significa que o agente só pode responder mensagens, mas **NÃO pode** executar comandos, ler arquivos, usar ferramentas ou fazer qualquer coisa além de conversar.

Para ter um agente verdadeiramente funcional, você PRECISA mudar para o perfil `full`:

```bash
openclaw config set tools.profile full
```

Em seguida, valide que tudo está correto com o novo comando de validação:

```bash
openclaw config validate
```

A saída deve mostrar algo como:

```
✅ tools.profile: full
✅ gateway.mode: local
✅ ai.provider: anthropic
✅ Configuration valid — 0 warnings
```

> 💡 **Por que esse default mudou?** A Anthropic e a comunidade de segurança identificaram que muitas instalações expostas na internet davam acesso completo de ferramentas a qualquer pessoa que encontrasse o bot. O novo default `messaging` é mais seguro para quem não sabe o que está fazendo. Mas **para o curso**, queremos `full` — daí este passo.

> 📺 **Dica pro curso:** Mostrar o "antes e depois" — enviar uma mensagem pro bot sem configurar (`tools.profile = messaging`) e ver ele respondendo mas sem conseguir executar comandos. Depois configurar e mostrar a diferença. Muito didático!

---

## ⚠️ Passo 3.6: Configurar Timezone (NOVO — v2026.3.13)

> 🕐 **IMPORTANTE para quem vai usar crons:** Sem este passo, todos os seus crons vão disparar no horário UTC — 3 horas adiantados em relação ao Brasil. Um cron configurado "todo dia às 9h" vai disparar às 12h.

```bash
sudo systemctl edit openclaw
```

No editor que abrir, adicione dentro de `[Service]`:

```
[Service]
Environment="OPENCLAW_TZ=America/Sao_Paulo"
```

Salve e aplique:

```bash
sudo systemctl daemon-reload
sudo systemctl restart openclaw
```

Verifique que o gateway reiniciou corretamente:

```bash
openclaw gateway status
```

> 📺 **Dica pro curso:** Demonstrar o efeito ao vivo — criar um cron de teste, mostrar ele disparando no horário errado (UTC), depois configurar OPENCLAW_TZ e mostrar o horário correto. Momento muito didático.

---

## Passo 4: Verificar se está rodando (30 seg)

```bash
openclaw gateway status
```

Deve mostrar: `running` ✅

Se quiser ver o painel web:
```bash
openclaw dashboard
```
Acesse: `http://SEU_IP:18789`

> 📡 **Novo na v2026.3.2:** O Telegram streaming agora é ativado por padrão. Quando seu agente estiver "pensando", você vai ver o indicador "digitando..." no Telegram em tempo real. Isso é normal e esperado — o agente está processando sua mensagem ao vivo!

---

## Passo 5: Criar o Bot no Telegram (3 min)

1. Abra o Telegram no celular
2. Busque por `@BotFather`
3. Envie `/newbot`
4. Escolha um nome (ex: "Meu Agente AI")
5. Escolha um username (deve terminar em "bot", ex: "meuagenteai_bot")
6. **Copie o token** que o BotFather der

---

## Passo 6: Conectar Telegram ao OpenClaw (2 min)

De volta no terminal da VPS:

```bash
openclaw provider add telegram
```

Quando pedir, cole o token do bot.

Depois, abra o chat com seu bot no Telegram e envie `/start`.

---

## Passo 7: Segurança IMEDIATA (2 min)

**ANTES de fazer qualquer outra coisa**, blindar o acesso:

```bash
# Ver a config atual
cat ~/.openclaw/openclaw.json
```

Garantir que `dmPolicy` está como `allowlist` e que SÓ o seu Telegram ID está autorizado.

Para descobrir seu Telegram ID:
- Envie qualquer mensagem pro bot
- Cheque os logs: `openclaw gateway logs`
- O ID aparece nas mensagens recebidas

> 🔴 **ALERTA no curso:** Se dmPolicy estiver "open", QUALQUER PESSOA que encontrar seu bot pode comandar seu agente. Isso é um risco de segurança gravíssimo. Mostrar isso no vídeo com ênfase.

---

## Passo 8: Primeiro teste (1 min)

Envie uma mensagem pro bot no Telegram:

> "Oi! Me diz quem você é e o que pode fazer."

Se o agente responder → **SETUP COMPLETO!** 🎉

> 📱 **Novo na v2026.3.2:** Você vai ver "digitando..." aparecer no Telegram enquanto o agente processa. Isso é o streaming ativo — é normal e significa que o agente está funcionando!

---

## Checkpoint do Módulo 1

- [ ] VPS rodando na Hostinger (Ubuntu 24.04)
- [ ] OpenClaw instalado (bare metal, não Docker)
- [ ] Gateway rodando como serviço (24/7)
- [ ] **`tools.profile = full` configurado** ← NOVO (v2026.3.2)
- [ ] `openclaw config validate` sem erros ← NOVO (v2026.3.2)
- [ ] **`OPENCLAW_TZ=America/Sao_Paulo` configurado** ← NOVO (v2026.3.13)
- [ ] Bot do Telegram criado e conectado
- [ ] dmPolicy = allowlist (segurança básica)
- [ ] Primeiro "oi" respondido ✅

---

## Troubleshooting Comum

### "Command not found: openclaw"
```bash
# Recarregar o PATH
source ~/.bashrc
# Ou reinstalar
curl -fsSL https://openclaw.ai/install.sh | bash
```

### "API key inválida"
- Verificar se tem billing ativo na Anthropic
- Copiar a key novamente (sem espaços extras)

### "Bot não responde no Telegram"
```bash
# Ver logs
openclaw gateway logs
# Verificar status
openclaw gateway status
```

### "Agente responde mas não consegue executar comandos" (NOVO — v2026.3.2)
```bash
# Sintoma: bot responde "não consigo fazer isso" para qualquer tarefa
# Causa: tools.profile ainda está como 'messaging'
openclaw config set tools.profile full
openclaw gateway restart
```

### "Gateway não inicia"
```bash
# Checar porta
ss -tlnp | grep 18789
# Reiniciar
openclaw gateway restart
```

---

## Quanto custa?

| Item | Custo mensal |
|------|-------------|
| VPS Hostinger (KVM 1) | ~$5-10/mês |
| API Anthropic (uso moderado) | ~$10-30/mês |
| API Gemini 3.1 Pro (alternativa) | ~$5-15/mês |
| Telegram | Grátis |
| **Total (Anthropic)** | **~$15-40/mês** |
| **Total (Gemini — opção econômica)** | **~$10-25/mês** |

> 💡 **Dica pro curso:** "Menos que um almoço por semana pra ter um assistente AI 24/7"

> 💰 **Opção econômica:** O Gemini 3.1 Pro ($1.25/M tokens input) é uma alternativa viável e mais barata que o Claude Sonnet para quem quer começar com custo menor. Para tarefas simples e heartbeats, funciona muito bem!

---

*Este é o módulo mais técnico. Depois daqui, é só configurar o agente — e isso é a parte divertida.* 🍇
