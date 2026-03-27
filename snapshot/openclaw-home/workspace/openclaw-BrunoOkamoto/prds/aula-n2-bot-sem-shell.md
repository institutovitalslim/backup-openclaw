# PRD — Aula N-2: Bot sem acesso ao shell — identificar e corrigir

**Módulo:** N — Diagnóstico & Troubleshooting  
**Aula:** N-2  
**Duração estimada:** 15 minutos  
**Nível:** Intermediário / Debug  
**Instrutor:** Bruno  
**Formato:** Screencast com narração + slides/terminal ao vivo

---

## Objetivo da Aula

Ao final desta aula, o aluno será capaz de:
1. Identificar quando o agente perdeu acesso ao shell
2. Diagnosticar a causa exata do problema
3. Aplicar a correção correta em cada caso
4. Verificar que o acesso foi restaurado

---

## Roteiro de Gravação

### [00:00 – 01:30] — ABERTURA

> **Bruno (câmera ou voice-over):**

"Fala, pessoal! Bruno aqui. Nessa aula a gente vai resolver um dos problemas mais comuns que vejo acontecer com quem tá começando a usar o OpenClaw: o agente para de executar comandos.

Você pede pra ele instalar uma ferramenta. Ele diz 'não consigo fazer isso'. Você pede pra criar um arquivo. Ele diz 'não tenho permissão'. Parece que o agente virou só um chatbot — responde texto mas não faz nada.

Isso tem causa. E tem solução. Vou te mostrar as 5 causas mais comuns — incluindo a novidade da versão 3.2 que está pegando muita gente. Nos próximos 15 minutos você vai aprender a identificar e corrigir cada uma.

Vamos lá!"

---

### [01:30 – 03:00] — SINTOMAS DO PROBLEMA

> **Bruno (tela do terminal + agente aberto):**

"Primeiro, como saber que você está com esse problema?

Os sintomas clássicos são esses:"

**[Mostrar na tela — lista de sintomas:]**

```
Sintoma 1: Você pede ao agente pra rodar um comando e ele diz:
  → "Não consigo executar comandos no seu sistema"
  → "Não tenho acesso ao shell"
  → "Essa ferramenta não está disponível"

Sintoma 2: O agente responde texto perfeitamente, mas qualquer
  tarefa que envolva o sistema operacional falha.

Sintoma 3: Você recebe mensagens de erro como:
  → "Permission denied"
  → "exec: not in allowlist"
  → "Sandbox restriction"
```

> "Se você tá vendo qualquer um desses, o problema é de permissão de acesso ao shell. Agora vamos entender por quê isso acontece — tem 4 causas principais."

---

### [03:00 – 08:30] — AS 5 CAUSAS

#### ⚠️ Causa 0 (NOVA, MAIS COMUM): `tools.profile = messaging` [03:00 – 03:45]

> **Bruno:**

"Mas antes de qualquer coisa — desde a versão 3.2 do OpenClaw, a causa número um do 'bot não faz nada' mudou. E muita gente está caindo nessa agora.

Quando você configura o agente com `tools.profile = messaging`, o OpenClaw coloca o agente em modo mensageria — otimizado para responder texto no Telegram ou WhatsApp, mas sem acesso ao shell, sem exec, sem nada de sistema.

É exatamente o que acontece quando você copia uma config de exemplo de bot Telegram e não percebe que tem esse parâmetro.

O sintoma é claro: o agente responde fluentemente, parece esperto, mas quando você pede qualquer coisa que envolva o sistema operacional, ele diz 'não consigo'.

A correção é simples: remover o `tools.profile` ou trocá-lo para um perfil que inclua exec, como `full` ou `default`."

**[Mostrar config com o problema:]**
```json
{
  "agents": {
    "main": {
      "tools": {
        "profile": "messaging"
      }
    }
  }
}
```

**[Mostrar a correção:]**
```json
{
  "agents": {
    "main": {
      "tools": {
        "profile": "default"
      }
    }
  }
}
```

> "Ou simplesmente remova a chave `tools.profile` — o padrão já inclui exec."

#### Causa 1: Ferramenta `exec` não está no allowlist [03:45 – 04:45]

> **Bruno:**

"A causa mais comum. O OpenClaw controla quais ferramentas cada agente pode usar. Se a ferramenta `exec` não estiver na lista de ferramentas permitidas, o agente simplesmente não consegue rodar comandos.

Isso acontece quando alguém configura o agente de forma restrita — talvez pra um agente de suporte que não devia ter acesso ao sistema. Faz sentido nesse contexto, mas não faz sentido se você quer um agente que executa tarefas.

A correção vai estar na configuração do allowlist. Vou mostrar como daqui a pouco."

#### Causa 2: Sandbox ativo sem permissão correta [04:00 – 05:00]

> **Bruno:**

"A segunda causa é o sandbox. O OpenClaw tem um sistema de sandbox que isola a execução de comandos. Dependendo de como tá configurado, o agente pode estar rodando num ambiente isolado que não deixa comandos passarem.

O sandbox tem três modos:
- `off` — sem sandbox, acesso total ao sistema
- `non-main` — sandbox ativo só pra sub-agentes
- `all` — sandbox ativo pra todos os agentes, incluindo o principal

Se você colocou `all` sem configurar as permissões de sandbox corretamente, o agente principal também fica preso.

A diferença entre esses modos importa. Vou mostrar na configuração."

#### Causa 3: Security mode "deny" [05:00 – 06:00]

> **Bruno:**

"A terceira causa é o security mode. O OpenClaw tem um parâmetro chamado `security` que controla como o agente lida com execução de comandos. Quando esse parâmetro está configurado como `deny`, o agente bloqueia qualquer tentativa de executar comandos no sistema.

Esse modo existe por uma razão: segurança. Em alguns casos você quer um agente que só lê, não que executa. Mas se você configurou isso por engano no agente errado, ele vai ficar travado.

A solução é simples: mudar o security mode para `allowlist` ou `full`."

#### Causa 4: BotFather privacy mode — bot não responde no grupo [06:00 – 07:00]

> **Bruno:**

"Essa causa é específica pra quem usa o agente em grupos do Telegram. Você adiciona o bot ao grupo, manda mensagem — nada. O bot responde em DM normalmente, mas no grupo, silêncio total.

O culpado é o **Group Privacy Mode** do BotFather. Por padrão, quando você cria um bot no BotFather, ele vem com privacy mode ATIVO. Isso significa que o bot só recebe mensagens que começam com `/comando` — mensagens normais no grupo são invisíveis pra ele.

Como corrigir:"

**[Mostrar passo a passo:]**
```
1. Abra @BotFather no Telegram
2. Envie: /mybots
3. Selecione seu bot
4. Clique em "Bot Settings"
5. Clique em "Group Privacy"
6. Clique em "Turn off"
7. Confirmação: "Privacy mode is disabled"

IMPORTANTE: remova e adicione o bot ao grupo novamente
para as novas permissões valerem.
```

> "Depois de desativar o privacy mode e re-adicionar o bot, ele começa a receber todas as mensagens do grupo. Simples assim."

#### Causa 5: Path do shell não encontrado [07:00 – 08:00]

> **Bruno:**

"A quinta causa é menos comum mas acontece especialmente em VPS — o OpenClaw não consegue encontrar o shell do sistema.

Em ambientes Linux padrão, o shell fica em `/bin/bash` ou `/bin/sh`. Mas em algumas distribuições minimalistas, containers Docker, ou VPS mal configurados, o path pode ser diferente. Ou o usuário que roda o OpenClaw não tem permissão pra usar o shell.

A correção é configurar o path correto do shell na configuração do agente."

---

### [08:00 – 08:30] — FLUXOGRAMA DE DIAGNÓSTICO

> **Bruno:**

"Antes de entrar no diagnóstico passo a passo, deixa eu te mostrar o mapa mental. Quando o bot não faz nada, siga essa ordem:"

**[Mostrar fluxograma na tela:]**

```
Bot não executa comandos?
         │
         ▼
┌─────────────────────────────────┐
│  tools.profile = messaging?    │ ──YES──▶ Remover ou trocar para "default"
└─────────────────────────────────┘
         │ NO
         ▼
┌─────────────────────────────────┐
│  Bot em grupo e não responde?  │ ──YES──▶ BotFather → desativar Group Privacy
└─────────────────────────────────┘
         │ NO
         ▼
┌─────────────────────────────────┐
│  sandbox = "all" ?             │ ──YES──▶ Mudar para "off" ou "non-main"
└─────────────────────────────────┘
         │ NO
         ▼
┌─────────────────────────────────┐
│  security = "deny" ?           │ ──YES──▶ Mudar para "allowlist"
└─────────────────────────────────┘
         │ NO
         ▼
┌─────────────────────────────────┐
│  "exec" no allowlist?          │ ──NO───▶ Adicionar "exec" ao allowlist
└─────────────────────────────────┘
         │ YES
         ▼
    openclaw gateway restart
         │
         ▼
    echo "SHELL_TEST_OK"
         │
    ┌────┴────┐
   OK?      Falhou?
    │           │
  Resolvido   Ver logs
              gateway
```

> "Testa nessa ordem. A causa 0 — o tools.profile — resolve 60% dos casos que aparecem no grupo."

---

### [08:30 – 09:00] — TESTE RÁPIDO

> **Bruno (mostrando terminal):**

"Antes de mergulhar no diagnóstico, tem um teste rápido que você pode fazer. Peça pro seu agente executar isso:"

**[Mostrar no terminal/chat:]**
```
execute: echo test
```

> "Se o agente responder com 'test', ele tem acesso ao shell. Se der erro, você tem um dos problemas que acabamos de ver. Simples assim."

---

### [08:00 – 10:30] — COMO DIAGNOSTICAR

> **Bruno (tela do terminal):**

"Agora vamos ao diagnóstico. Passo a passo:"

#### Passo 1: Verificar os logs do gateway

```bash
openclaw gateway logs --tail 50
```

> "Procure por mensagens como `exec blocked`, `not in allowlist`, `sandbox restriction` ou `permission denied`. O log vai te dizer exatamente o que está bloqueando."

#### Passo 2: Verificar a configuração do agente

```bash
cat ~/.openclaw/config.json
```

ou, se estiver num workspace específico:

```bash
cat openclaw.json
```

> "Você precisa checar três coisas nesse arquivo: o `allowlist` de tools, o parâmetro `sandbox`, e o `security` mode. Vou mostrar como cada um deve estar configurado."

#### Passo 3: Usar o diagnóstico interativo

> "Você também pode colar o prompt de diagnóstico que disponibilizamos junto com esta aula — ele vai guiar o agente a verificar a própria configuração e identificar o problema automaticamente."

---

### [10:30 – 13:00] — COMO CORRIGIR CADA CAUSA

> **Bruno (editor de código aberto com o config):**

"Agora a parte boa — as correções. Vou mostrar cada uma."

#### Correção 1: Adicionar `exec` ao allowlist

```json
{
  "agents": {
    "main": {
      "tools": {
        "allowlist": ["exec", "read", "write", "edit", "web_search", "web_fetch"]
      }
    }
  }
}
```

> "Simples. Adicione `exec` na lista. Se não existia a chave `tools`, crie ela. Salve o arquivo e reinicie o gateway."

#### Correção 2: Ajustar configuração de sandbox

```json
{
  "agents": {
    "main": {
      "sandbox": "off"
    }
  }
}
```

> "Para o agente principal, use `sandbox: off`. Se quiser sandboxing em sub-agentes mas não no principal, use `non-main`. Só use `all` se você entende bem as implicações e configurou as permissões de sandbox corretamente."

**Tabela explicativa:**

| Valor       | Comportamento |
|-------------|---------------|
| `off`       | Sem sandbox — acesso total ao sistema |
| `non-main`  | Sandbox só em sub-agentes |
| `all`       | Sandbox em todos — **inclui agente principal** |

#### Correção 3: Ajustar security mode

```json
{
  "agents": {
    "main": {
      "security": "allowlist"
    }
  }
}
```

> "Mude de `deny` para `allowlist`. Com `allowlist`, só os comandos e ferramentas na sua lista permitida vão funcionar — é seguro e funcional. `full` desabilita restrições mas só use se souber o que está fazendo."

#### Correção 4: Configurar path do shell

```json
{
  "agents": {
    "main": {
      "shell": "/bin/bash"
    }
  }
}
```

> "Se o shell não está sendo encontrado, especifique o path completo. No Ubuntu/Debian é `/bin/bash`, em alguns Alpine/containers pode ser `/bin/sh`. Rode `which bash` ou `which sh` no terminal pra confirmar o path correto."

---

### [13:00 – 14:30] — CHECKLIST DE VERIFICAÇÃO PÓS-CORREÇÃO

> **Bruno:**

"Depois de aplicar qualquer correção, siga esse checklist:"

**[Mostrar na tela:]**

```
CHECKLIST PÓS-CORREÇÃO

□ 1. Reiniciar o gateway:
     openclaw gateway restart

□ 2. Verificar status do gateway:
     openclaw gateway status

□ 3. Testar acesso básico — pedir pro agente:
     execute: echo "shell funcionando"

□ 4. Testar criação de arquivo:
     execute: touch /tmp/teste-openclaw && echo "OK"

□ 5. Verificar logs por erros residuais:
     openclaw gateway logs --tail 20

□ 6. Testar uma tarefa real simples:
     "liste os arquivos do diretório atual"
```

---

### [14:30 – 15:00] — ENCERRAMENTO

> **Bruno:**

"Pronto! Agora você sabe identificar e corrigir os cinco tipos de problema que tiram o acesso ao shell do seu agente.

Pra recapitular:
- Causa 0 (mais comum!): `tools.profile = messaging` → remova ou troque para `default`
- Causa 1: `exec` não está no allowlist → adicione na lista de tools
- Causa 2: Sandbox mal configurado → ajuste o modo de sandbox
- Causa 3: Security mode `deny` → mude para `allowlist`
- Causa 4: Bot no grupo sem resposta → desativar Group Privacy no BotFather
- Causa 5: Shell não encontrado → configure o path correto

Use o prompt de diagnóstico que deixamos disponível pra você fazer esse processo de forma interativa com o próprio agente.

Qualquer dúvida, joga no grupo. Até a próxima!"

---

## Notas de Produção

- **Mostrar terminal ao vivo** ao explicar logs e config
- **Editor de código** aberto ao mostrar as correções JSON
- **Destacar** as linhas relevantes no config com zoom ou destaque
- **Demonstrar** o teste rápido (`echo test`) ao vivo pra mostrar o agente funcionando depois da correção
- **Adicionar captions/legendas** nas partes técnicas

## Assets Necessários

- [ ] Arquivo `openclaw.json` de exemplo (com erro deliberado)
- [ ] Versão corrigida do `openclaw.json`
- [ ] Screenshot dos logs com mensagem de erro
- [ ] GIF/video do teste `echo test` funcionando

---

*PRD gerado em 2026-03-04 · Curso OpenClaw · Pixel Educação*
