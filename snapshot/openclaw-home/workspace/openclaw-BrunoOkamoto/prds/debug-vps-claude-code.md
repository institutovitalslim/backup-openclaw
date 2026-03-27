# PRD: Debug na VPS com Claude Code

> Roteiro para gravação da Aula Extra B
> Público: leigo total — pode nunca ter acessado um servidor antes

---

## Objetivo da Aula

Ensinar como acessar a VPS e usar o Claude Code (CLI do OpenClaw) direto no terminal pra:
1. **Debugar problemas** quando o agente travar ou dar erro
2. **Arrumar pastas e arquivos** do workspace
3. **Usar `openclaw doctor`** pra diagnóstico automático
4. **Usar `openclaw doctor fix`** pra correção automática

**Premissa:** O aluno pode não saber usar terminal. Vai aprender fazendo.

---

## Tempo estimado: 18-22 minutos

---

## Estrutura da Aula

### Bloco 1: Por que aprender a debugar? (2 min)

**O que mostrar:**
- Agente travou e não responde? É normal — você vai saber resolver.
- Erro estranho apareceu? Você vai saber onde procurar.
- Autonomia: não depender de suporte pra problema simples.

**Frase-chave:**
> "Você não precisa ser técnico. Mas precisa saber abrir o capô do carro quando a luz vermelha acende."

**Cenários reais que o aluno vai enfrentar:**
- Agente parou de responder no Telegram
- Erro "token limit exceeded"
- **Agente ficou MUITO lento (respostas demoram 30s+)**
- Workspace bagunçado (arquivos demais)
- Gateway não inicia depois de um restart
- Cron não roda no horário

---

### Bloco 2: Como acessar a VPS (4 min)

**Opção 1: Terminal local (Mac/Linux/Windows Terminal)**

1. **Pegar o IP e senha da VPS** (no painel da Hostinger)

2. **Conectar via SSH:**
   ```bash
   ssh root@SEU_IP_AQUI
   ```
   Digite a senha quando pedir.

3. **Você está dentro!** O prompt muda:
   ```
   root@vps-12345:~#
   ```

**Opção 2: Terminal do painel da Hostinger (mais fácil pra iniciante)**

1. Ir em hPanel → VPS → clicar no botão "Terminal" (topo direito)
2. Terminal abre no navegador — sem configurar nada
3. Já está conectado como root

**Mostrar os dois jeitos e deixar o aluno escolher.**

---

### Bloco 3: Comandos básicos de sobrevivência (3 min)

**Antes de debugar, ensinar o mínimo:**

1. **Ver onde você está:**
   ```bash
   pwd
   ```
   Mostra o caminho atual (tipo `/root`)

2. **Listar arquivos:**
   ```bash
   ls -la
   ```
   Mostra tudo, incluindo pastas ocultas (começam com `.`)

3. **Ir pro workspace do agente:**
   ```bash
   cd ~/.openclaw/workspace-NOME-DO-SEU-AGENTE
   ```
   Exemplo:
   ```bash
   cd ~/.openclaw/workspace-amora-cos
   ```

4. **Ver conteúdo de um arquivo:**
   ```bash
   cat AGENTS.md
   ```
   Ou pra arquivos grandes:
   ```bash
   less AGENTS.md
   ```
   (aperta `q` pra sair)

5. **Ver logs do gateway em tempo real:**
   ```bash
   openclaw gateway logs --follow
   ```
   (aperta Ctrl+C pra sair)

**Explicar o conceito de "caminho":**
> "Pensa no servidor como uma árvore de pastas. Você começa na raiz (`/`) e vai descendo. `~` é atalho pra pasta do usuário atual (`/root`)."

---

### Bloco 4: Usar Claude Code no terminal (5 min)

**O que é o Claude Code:**
> "É o Claude rodando DENTRO do terminal da VPS. Você pergunta, ele responde e pode executar comandos pra você."

**Como invocar:**
```bash
claude
```

Abre uma sessão interativa. Agora você pode conversar:

**Exemplo 1 — Diagnosticar problema:**
```
Você: Meu agente parou de responder no Telegram. O que pode ser?

Claude: Vou checar. Primeiro, status do gateway...
[executa: openclaw gateway status]

Claude: Gateway está parado. Vou ver os últimos logs...
[executa: openclaw gateway logs --tail 50]

Claude: Erro de token limit. O problema é excesso de contexto.
Quer que eu limpe os logs antigos e reinicie?
```

**Exemplo 2 — Arrumar workspace:**
```
Você: Meu workspace tá cheio de arquivos de teste. Como limpo?

Claude: Vou listar o que tem aqui...
[executa: ls -lah]

Claude: Tem vários .txt e .json de teste. Posso mover pra uma pasta
/archive. Confirma?

Você: Confirma.

Claude: [cria pasta, move arquivos, mostra resultado]
Pronto. Workspace limpo.
```

**Exemplo 3 — Ver uso de disco:**
```
Você: Quanto espaço tenho na VPS?

Claude: [executa: df -h]
Você tem 50GB total, 12GB usados, 38GB livres.
```

**Sair do Claude Code:**
- Digite `exit` ou aperta Ctrl+D

---

### Bloco 5: openclaw doctor — Diagnóstico automático (3 min)

**O que faz:**
Roda uma bateria de checks e mostra o que tá errado.

**Executar:**
```bash
openclaw doctor
```

**O que ele verifica:**
- ✅ Gateway rodando?
- ✅ Node.js na versão certa?
- ✅ Disco tem espaço?
- ✅ Memória RAM disponível?
- ✅ Config válida? (`openclaw.json`)
- ✅ Provider API key funciona?
- ✅ Canais conectados? (Telegram, etc.)
- ⚠️ Logs muito grandes?
- ⚠️ Workspaces com arquivos demais?

**Saída exemplo:**
```
✅ Gateway: running
✅ Node.js: v22.22.0
✅ Disk: 38GB free (76%)
✅ Memory: 2.1GB free (52%)
✅ Config: valid
✅ Provider: Anthropic API OK
✅ Telegram: connected
⚠️ Logs: 450MB (considere limpar)
⚠️ Workspace "amora-cos": 2.3GB (revisar arquivos grandes)
```

**Explicar cada linha:**
> "Verde = tudo certo. Amarelo = atenção, pode virar problema. Vermelho = precisa corrigir agora."

---

### Bloco 6: openclaw doctor fix — Correção automática (2 min)

**O que faz:**
Tenta corrigir problemas comuns automaticamente.

**Executar:**
```bash
openclaw doctor fix
```

**O que ele pode consertar sozinho:**
- Reiniciar gateway travado
- Limpar logs antigos (mantém últimos 7 dias)
- Corrigir permissões de arquivos
- Recriar pastas ausentes
- Atualizar dependências quebradas

**O que ele NÃO faz (precisa de confirmação):**
- Deletar arquivos do workspace
- Alterar config crítica
- Fazer upgrade de versão major

**Fluxo:**
```bash
openclaw doctor fix
```

Saída:
```
🔍 Scanning for issues...
⚠️ Found 3 fixable issues:

1. Gateway not responding → restart
2. Logs > 500MB → rotate
3. /tmp full → cleanup

Apply fixes? [y/N]
```

Digitar `y` e Enter.

```
✅ Gateway restarted
✅ Logs rotated (freed 380MB)
✅ /tmp cleaned (freed 1.2GB)

All checks passed. System healthy.
```

---

### Bloco 7: Cenários reais + soluções (5 min)

**Mostrar 4 problemas comuns e como resolver:**

#### Cenário 1: "Agente não responde no Telegram"

**Passo a passo:**
1. SSH na VPS
2. `openclaw gateway status` → se "stopped", rodar `openclaw gateway start`
3. Se continua parado, ver logs: `openclaw gateway logs --tail 50`
4. Se erro de API key, reconfigurar: `openclaw provider update anthropic`
5. Se erro de token, rodar `openclaw doctor fix`

#### Cenário 2: "Erro de contexto muito grande"

**Sintoma:** Mensagem de erro "context window exceeded"

**Solução:**
1. SSH na VPS
2. Ir pro workspace: `cd ~/.openclaw/workspace-SEU-AGENTE`
3. Abrir Claude Code: `claude`
4. Perguntar: "Meu contexto tá muito grande. Pode compactar memory/YYYY-MM-DD.md antigos?"
5. Claude vai mover pra arquivo compactado e limpar

#### Cenário 3: "Agente ficou MUITO lento (respostas demoram 30s+)"

**Sintoma:** Agente demora pra responder, às vezes timeout

**Causas comuns:**

1. **Contexto de sessão passou de 100k tokens**
   - Usuário nunca deu `/new` ou `/compact`
   - Sessão acumula meses de histórico
   
   **Solução:**
   ```bash
   # Ver tamanho das sessões
   cd ~/.openclaw
   du -sh sessions/*.json | sort -h | tail -10
   ```
   Se tiver session.json com mais de 5MB:
   - Pedir pro usuário rodar `/compact` ou `/new`
   - Ou mover pra backup: `mv sessions/SESSAO.json sessions/backup/`

2. **session.json corrompido ou gigante**
   - Arquivo pode chegar a 50MB+ se nunca compactou
   
   **Solução:**
   ```bash
   # Ver o maior session.json
   ls -lh ~/.openclaw/sessions/ | sort -k5 -h | tail -5
   ```
   Se achar arquivo > 10MB, pode arquivar:
   ```bash
   mkdir -p ~/.openclaw/sessions/backup
   mv ~/.openclaw/sessions/ARQUIVO-GIGANTE.json ~/.openclaw/sessions/backup/
   ```

3. **Muitos agentes rodando em paralelo**
   - Cada agente consome memória e CPU
   - VPS pequena não aguenta 5+ agentes simultâneos
   
   **Solução:**
   ```bash
   # Ver quantos processos do OpenClaw estão rodando
   ps aux | grep openclaw | wc -l
   ```
   Se tiver mais de 3-4 em VPS pequena (4GB RAM), considerar:
   - Parar agentes não-usados
   - Upgrade de VPS
   - Usar `sessionTarget: isolated` com `cleanup: delete` nos crons

**Explicar no vídeo:**
> "O contexto é como a memória de curto prazo do agente. Se você nunca limpar, é como tentar lembrar de TUDO que aconteceu nos últimos 6 meses — o cérebro trava. Use `/compact` toda semana ou `/new` quando precisar recomeçar."

#### Cenário 4: "VPS sem espaço"

**Sintoma:** "No space left on device"

**Solução:**
1. Rodar `openclaw doctor` → vai mostrar o problema
2. Rodar `openclaw doctor fix` → limpa logs e /tmp
3. Se continua cheio, usar Claude Code:
   ```
   Você: Preciso liberar espaço. O que tá ocupando mais?
   Claude: [executa: du -sh ~/.openclaw/* | sort -h]
   Mostra os workspaces maiores...
   ```
4. Decidir o que arquivar ou deletar

---

## Checkpoint da Aula

Ao final, o aluno deve saber:
- [ ] Como conectar na VPS via SSH (terminal local ou painel Hostinger)
- [ ] Comandos básicos de navegação (pwd, ls, cd, cat)
- [ ] Como invocar Claude Code no terminal (`claude`)
- [ ] Como usar `openclaw doctor` pra diagnóstico
- [ ] Como usar `openclaw doctor fix` pra correção automática
- [ ] Resolver 4 problemas comuns sozinho (não responde, contexto, lentidão, sem espaço)

---

## Alertas de Segurança

🔴 **NUNCA** deletar arquivos sem saber o que são
🔴 **SEMPRE** fazer backup antes de mudanças grandes
🔴 **CUIDADO** com `rm -rf` — pode apagar tudo

**Regra de ouro:**
> "Se não sabe o que o comando faz, pergunte pro Claude Code antes de rodar."

---

## Prompt que vai no PDF

Vai estar no arquivo `prompts/modulo-extra-b-debug.md`.

---

## Troubleshooting Comum

### "Permission denied" ao tentar algo
Provavelmente precisa de `sudo`. Mas como root, não deveria acontecer.

### "Command not found: claude"
```bash
# Reinstalar OpenClaw CLI
npm install -g @anthropic-ai/claude-code
```

### "SSH connection refused"
- Verificar se o IP tá certo
- Verificar se a VPS tá ligada (painel Hostinger)
- Verificar se a porta 22 tá aberta (firewall)

---

*Esta aula dá autonomia. Antes dela, o aluno depende de suporte. Depois, resolve 80% dos problemas sozinho.*
