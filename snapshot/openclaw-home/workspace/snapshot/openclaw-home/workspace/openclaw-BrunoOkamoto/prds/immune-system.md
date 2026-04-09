# PRD: Sistema Imunológico

> "Agents are 30% of the work. The other 70% is the immune system." — Eric Siu
> Jogue no agente: "Implementa este sistema imunológico"

## Contexto

Agentes quebram silenciosamente. Crons falham sem avisar. Sub-agents travam no limbo. Sem monitoramento, você descobre problemas dias depois.

## 1. Watchdog de Crons

Criar um cron que monitora os outros crons:

**Lógica:**
1. Listar todos os crons ativos
2. Checar último run de cada um
3. Se algum falhou → retry automático (até 3x)
4. Se falhou 3x → alertar o usuário no Telegram

**Configuração:**
```json
{
  "name": "Watchdog - Monitor de Crons",
  "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "America/Sao_Paulo" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Checar saúde de todos os crons. Listar os que falharam nas últimas 24h. Fazer retry dos que falharam. Se algum falhar 3x, alertar no Telegram."
  },
  "delivery": { "mode": "announce" }
}
```

## 2. Feedback Loops

Sistema de aprendizado contínuo: o agente aprende com suas decisões (approve/reject).

### Setup

Criar `memory/feedback/` com arquivos JSON por domínio:

- `content.json` — feedback sobre conteúdo, drafts, sugestões
- `tasks.json` — feedback sobre entregas de tasks
- `recommendations.json` — feedback sobre sugestões de tools/processos

### Formato

```json
{
  "entries": [
    {
      "date": "2026-02-13",
      "context": "Sugeri thread sobre X para LinkedIn",
      "decision": "approve",
      "reason": "Tom certeiro, dados específicos",
      "tags": ["linkedin", "thread", "tom"]
    }
  ]
}
```

### Regras
- Max 30 entradas por arquivo (FIFO — remove as mais antigas)
- Agente DEVE consultar feedback antes de sugerir → evita repetir erros
- Consolidar padrões em `lessons/` mensalmente
- Ciclo: Feedback (granular, JSON) → Lessons (curado, prose) → Decisions (permanente)

## 3. Monitoramento de Custos

### Split de modelos
| Uso | Modelo | Custo relativo |
|-----|--------|---------------|
| Interação direta | Opus | $$$ |
| Crons e automação | Sonnet | $ |
| Heartbeats | Haiku | ¢ |

### Regra
- TODOS os crons devem rodar em Sonnet (nunca Opus)
- Heartbeats em Haiku
- Só a interação direta usa Opus

## 4. Sub-agents: Nunca "Fire and Forget"

Todo sub-agent spawnado DEVE ter follow-up:

1. **Ao spawnar:** informar o que vai fazer
2. **Follow-up:** checar status em 15-30 min
3. **Sucesso:** resumir resultado em linguagem humana
4. **Falha:** retry imediato → se falhar 2x → avisar o usuário
5. **Nunca** deixar cair no limbo silencioso

## 5. Backup antes de mudanças

Antes de criar agentes, modificar config, ou reorganizar workspace:

```bash
mkdir -p backups/$(date +%Y-%m-%d)
cp /root/.openclaw/openclaw.json backups/$(date +%Y-%m-%d)/
```

## 6. Auditoria de Secrets

### openclaw secrets audit (novo na 3.2)

A versão 3.2 traz um comando dedicado para auditar secrets expostos:

```bash
# Auditar todos os arquivos do workspace por secrets vazados
openclaw secrets audit

# Auditar diretório específico
openclaw secrets audit --path /root/.openclaw/workspace-meu-agente

# Saída com relatório detalhado
openclaw secrets audit --report
```

O comando detecta:
- API keys hardcodadas em arquivos `.json`, `.md`, `.env`
- Tokens no histórico de git
- Credenciais em SOUL.md, AGENTS.md ou TOOLS.md
- Patterns conhecidos (OpenAI, Stripe, Telegram, AWS, etc.)

> ⚠️ Execute `openclaw secrets audit` antes de compartilhar qualquer arquivo do workspace ou fazer backup em cloud.

### openclaw doctor — Melhorado na 3.2

O comando `openclaw doctor` foi expandido na 3.2 e agora verifica:

```bash
openclaw doctor
```

Checks adicionados na 3.2:
- ✅ `tools.profile` compatibility (detecta profile incompatível com tarefas)
- ✅ ACP dispatch status
- ✅ Secrets audit rápido (arquivos mais críticos)
- ✅ Versão do Node.js e dependências
- ✅ Conectividade com canais configurados (Telegram, WhatsApp, Slack)
- ✅ Crons com configuração inválida (`systemEvent` + `main` = problema)

> 💡 Dica: rode `openclaw doctor` após qualquer atualização de versão ou quando algo estiver "estranho". É o ponto de partida do diagnóstico.

## 7. Exec Approvals — Nunca Desabilite

O OpenClaw pode executar comandos no seu servidor. O sistema de approvals é a sua última linha de defesa: quando o agente quer executar algo fora do padrão, ele pausa e pede sua confirmação antes de prosseguir.

**Por que isso existe:** Em março/2026, 7 formas de burlar esse sistema foram encontradas e corrigidas — atacantes tentavam esconder comandos perigosos usando caracteres invisíveis Unicode, quebras de linha com backslash, e wrappers de ferramentas comuns (pnpm, npm, Perl). O sistema existe exatamente para bloquear isso.

**Verificar configuração:**
```bash
openclaw config get exec.approvals
# Deve retornar: ask
```

**Nunca use `allow`** (executa tudo sem confirmação). Mantenha sempre `ask`.

> 📺 **Dica pro curso:** Mostrar ao vivo o sistema pausando e pedindo aprovação. O aluno tende a achar que é burocracia — mostrar o contexto de segurança muda a percepção.

## Checklist

- [ ] Watchdog de crons ativo
- [ ] Feedback loops configurados (pelo menos 1 domínio)
- [ ] Split de modelos aplicado
- [ ] Regra de sub-agents documentada no AGENTS.md
- [ ] Backup automático antes de mudanças
- [ ] `openclaw secrets audit` executado — zero leaks confirmados
- [ ] `openclaw doctor` rodado e sem erros críticos
- [ ] `exec.approvals = ask` (nunca `allow`!) ← v2026.3.13

## Resultado Esperado

Sistema resiliente que se auto-monitora, aprende com decisões e não deixa nada cair no limbo.
