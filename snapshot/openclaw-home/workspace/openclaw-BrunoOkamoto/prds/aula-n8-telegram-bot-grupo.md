# PRD — Aula N-8: Telegram: Bot Não Responde no Grupo

> **Nível:** Intermediário / Troubleshooting  
> **Duração estimada:** 10 minutos  
> **Pré-requisito:** OpenClaw configurado, bot no Telegram funcionando em DM

---

## 🎯 Objetivo da Aula

Ao final desta aula, o aluno será capaz de:

1. Entender por que o bot funciona em DM mas não no grupo
2. Corrigir o privacy mode do BotFather
3. Configurar `groupPolicy` no OpenClaw
4. Descobrir o chat ID de qualquer grupo
5. Entender a diferença entre `dmPolicy` e `groupPolicy`
6. Diagnosticar problemas de grupo sistematicamente

---

## 🎬 ABERTURA (0:00 – 0:45)

**[Bruno na tela, tom direto]**

> "Fala! Aula N-8 — uma das dúvidas mais comuns do curso: 'adicionei meu bot no grupo, mas ele não responde'. Em 10 minutos você vai entender por que isso acontece e como resolver."

> "Spoiler: quase sempre são 3 causas. Vou te mostrar as 3 e o diagnóstico pra saber qual é a sua."

---

## 📚 SEÇÃO 1: Por Que o Bot Não Fala no Grupo (0:45 – 3:00)

**[Tela: slide com 3 causas]**

> "O bot funciona em DM mas não no grupo? Existem 3 causas possíveis, e elas são independentes — qualquer uma delas já basta para o bot ficar mudo:"

**Causa 1: Privacy Mode ATIVADO no BotFather (mais comum)**

> "Por padrão, o Telegram cria bots com 'privacy mode' ATIVADO. Isso significa que o bot NÃO RECEBE mensagens do grupo — ele só recebe mensagens que comecem com `/comando` ou que mencionem diretamente o bot com @username."

> "É uma medida de privacidade do Telegram. Mas pra um agente AI que deve participar das conversas, isso é um problema."

**Causa 2: `groupPolicy` não configurado no OpenClaw**

> "Mesmo que o bot receba as mensagens, o OpenClaw tem uma camada de segurança própria: por padrão, ele não processa mensagens de grupos a menos que você configure explicitamente."

**Causa 3: Chat ID do grupo não está no allowlist**

> "Se você usou `groupPolicy = allowlist`, precisa adicionar o chat ID do grupo específico. Sem o ID correto, o OpenClaw ignora as mensagens mesmo com tudo configurado."

---

## 🔧 FIX 1: BotFather — Desativar Privacy Mode (3:00 – 5:00)

**[Tela: Telegram aberto no BotFather]**

> "Vamos resolver a Causa 1. Abre o Telegram e fala com o **@BotFather**."

```
1. Abra o chat com @BotFather
2. Envie: /setprivacy
3. BotFather vai listar seus bots — selecione o seu
4. Escolha: Disable
5. Confirmação: "Success! Privacy mode is disabled."
```

> "Agora o bot vai receber TODAS as mensagens do grupo, não só comandos. Isso é necessário para o agente participar das conversas normalmente."

> "**Atenção:** Após mudar o privacy mode, você precisa **remover o bot do grupo e adicionar de volta**. O Telegram só aplica a nova configuração quando o bot entra no grupo. Se o bot já estava no grupo, a mudança não vai funcionar até você fazer isso."

---

## 🔧 FIX 2: Configurar groupPolicy no OpenClaw (5:00 – 7:30)

**[Tela: Terminal]**

> "Agora vamos resolver a Causa 2 e 3 juntas. No terminal da VPS:"

```bash
# Configurar política para grupos
# allowlist = só responde em grupos específicos (recomendado)
openclaw config set channels.telegram.groupPolicy allowlist

# Adicionar o chat ID do grupo ao allowlist
# (Veja a seção abaixo para descobrir o chat ID)
openclaw config set channels.telegram.groupAllowlist "[-100XXXXXXXXXX]"
```

> "Se tiver mais de um grupo:"
```bash
openclaw config set channels.telegram.groupAllowlist "[-100111111111, -100222222222]"
```

> "Para permitir qualquer grupo sem allowlist (menos seguro):"
```bash
openclaw config set channels.telegram.groupPolicy open
```

> "Recomendo `allowlist` — você controla exatamente em quais grupos o agente atua."

---

## 🔍 Como Descobrir o Chat ID do Grupo (7:30 – 8:30)

**[Tela: Terminal + Telegram]**

> "Para descobrir o chat ID do seu grupo, siga estes passos:"

```bash
# 1. Adicione o bot ao grupo (se ainda não fez)
# 2. Envie qualquer mensagem no grupo
# 3. Verifique os logs do OpenClaw
openclaw gateway logs | grep "chat_id"
# ou
openclaw gateway logs | tail -50
```

> "Nos logs você vai ver algo como:"
```
Received message from chat_id: -1001234567890, user: João
```

> "O chat ID de grupos começa com `-100` seguido de números. Anote esse ID — é ele que vai no allowlist."

> "Dica alternativa: adicione o bot @userinfobot ao grupo, mande `/start`, ele retorna o ID do grupo também."

---

## 📘 SEÇÃO 5: dmPolicy vs groupPolicy — A Diferença (8:30 – 9:30)

**[Tela: comparativo]**

> "Essa é uma confusão comum. Deixa eu esclarecer de vez:"

| | dmPolicy | groupPolicy |
|---|---|---|
| **Controla** | Mensagens diretas (DM/privadas) | Mensagens em grupos |
| **Default** | allowlist | não configurado |
| **Escopo** | 1-para-1 com você | Muitos usuários no mesmo chat |
| **Risco** | Alguém comandar seu agente | Agente ativo em grupos não autorizados |

> "São dois guardiões independentes. O `dmPolicy` cuida da sua conversa privada com o bot. O `groupPolicy` cuida de quando o bot está em grupos."

> "Você pode ter: DM aberta (só você) + grupos no allowlist. Ou DM só para você + nenhum grupo ativo. A combinação depende do seu caso de uso."

---

## 🗺️ SEÇÃO 6: Diagnóstico Passo a Passo (Fluxograma)

```
Bot adicionado ao grupo mas não responde
│
├── [1] Privacy mode está ATIVO?
│   → Teste: envie /start ou /help no grupo
│   → Se o bot RESPONDE a comandos mas ignora mensagens normais → Privacy mode ATIVO
│   → FIX: BotFather → /setprivacy → Disable → Remover e re-adicionar bot ao grupo
│
├── [2] groupPolicy configurado?
│   → Teste: openclaw config get channels.telegram.groupPolicy
│   → Se retornar vazio ou "none" → não configurado
│   → FIX: openclaw config set channels.telegram.groupPolicy allowlist
│
├── [3] Chat ID no allowlist?
│   → Teste: openclaw config get channels.telegram.groupAllowlist
│   → Verifique se o ID do grupo está na lista
│   → FIX: openclaw config set channels.telegram.groupAllowlist "[-100XXXXXXX]"
│
└── [4] Ainda não funciona?
    → openclaw gateway logs | tail -100
    → Procure mensagens de erro relacionadas ao chat
    → openclaw gateway restart
```

---

## 💡 SEÇÃO 7: Tópicos (Forum Mode) — Referência

> "Se o seu grupo usa **tópicos** (grupos com forum mode ativado), há uma configuração adicional. O bot precisa ser admin do grupo para ter acesso a todos os tópicos, e você pode precisar configurar quais tópicos o agente monitora."

> "Para configuração detalhada de tópicos, consulte a **Aula Extra C** — ela cobre o forum mode completo com exemplos práticos."

---

## 📋 Configuração Completa (Referência Rápida)

```bash
# 1. BotFather: /setprivacy → Disable (no Telegram)
# 2. Remover e re-adicionar o bot ao grupo

# 3. Configurar groupPolicy
openclaw config set channels.telegram.groupPolicy allowlist

# 4. Adicionar chat ID do grupo
openclaw config set channels.telegram.groupAllowlist "[-100XXXXXXXXXX]"

# 5. Verificar configuração
openclaw config get channels.telegram.groupPolicy
openclaw config get channels.telegram.groupAllowlist

# 6. Reiniciar gateway
openclaw gateway restart

# 7. Checar logs
openclaw gateway logs | tail -30
```

---

## ✅ Checklist Final do Aluno

- [ ] Privacy mode desativado no BotFather (`/setprivacy → Disable`)
- [ ] Bot removido e re-adicionado ao grupo após mudança de privacy mode
- [ ] Chat ID do grupo descoberto (começa com `-100...`)
- [ ] `groupPolicy = allowlist` configurado
- [ ] Chat ID adicionado ao `groupAllowlist`
- [ ] Gateway reiniciado
- [ ] Teste: mensagem enviada no grupo → bot respondeu ✅

---

## 🚨 Erros Comuns

| Sintoma | Causa | Solução |
|---------|-------|---------|
| Bot responde `/start` mas ignora mensagens | Privacy mode ATIVADO | BotFather → /setprivacy → Disable |
| Bot não responde nada no grupo | groupPolicy não configurado | `openclaw config set channels.telegram.groupPolicy allowlist` |
| groupPolicy configurado mas não responde | Chat ID não está no allowlist | Adicione o ID correto ao groupAllowlist |
| Bot funciona em DM, mudo no grupo | Qualquer das 3 causas | Seguir fluxograma de diagnóstico |
| Após mudança de privacy mode, ainda mudo | Bot ainda no grupo com config antiga | Remover bot do grupo e adicionar de volta |
| Chat ID inválido | Copiou ID errado | Ver logs: `openclaw gateway logs | grep chat_id` |

---

## ❓ Dúvidas Frequentes

**1. Preciso remover o bot e adicionar de volta sempre que mudar o privacy mode?**

> Sim. O Telegram processa a configuração de privacy mode no momento em que o bot entra no grupo. Mudanças retroativas não se aplicam — precisa sair e entrar de novo.

**2. Posso ter groupPolicy = open?**

> Sim, mas não recomendo para uso geral. Com `open`, o agente responde em qualquer grupo onde estiver adicionado — qualquer pessoa que adicione o bot a um grupo pode usá-lo. Prefira `allowlist`.

**3. O bot pode ser admin do grupo?**

> Sim, e é necessário para alguns recursos (deletar mensagens, acessar todos os tópicos em forum mode). Para uso básico de resposta, ser membro comum é suficiente.

**4. Funciona com grupos grandes (centenas de pessoas)?**

> Tecnicamente sim. Mas pense no custo: cada mensagem no grupo vai para o agente. Com 200 pessoas no grupo e muitas mensagens por dia, o custo de tokens pode ser alto. Configure bem o `groupPolicy` e considere usar `groupMentionOnly` (o bot só responde quando @mencionado) para grupos grandes.

**5. Tópicos (forum mode) exigem configuração extra?**

> Sim. Consulte a Aula Extra C para configuração completa de forum mode com tópicos.
