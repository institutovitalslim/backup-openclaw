# PRD: Como Integrar Suas Ferramentas — Skills & APIs

> Roteiro para gravação da Aula Extra A
> Público: leigo total — nunca mexeu com API ou skill antes

---

## Objetivo da Aula

Ensinar como conectar o agente às ferramentas que o aluno já usa (Notion, Google Calendar, Stripe, etc.) através de:
1. **Skills prontas** do ClawHub
2. **APIs diretas** (quando não tem skill)
3. **Transformar conhecimento em skill customizada**

**Premissa:** O aluno não sabe programar. Tudo tem que ser explicado como se fosse a primeira vez.

---

## Tempo estimado: 20-25 minutos

---

## Estrutura da Aula

### Bloco 1: Por que integrar? (3 min)

**O que mostrar:**
- Agente isolado vs agente conectado
- Exemplo visual: "Sem integração, o agente é cego. Com integração, ele vê tudo."
- Case real: MGM Boss (Stripe + ChartMogul + Notion) e FLG Boss (YouTube + Instagram + Notion)

**Frase-chave:**
> "O agente só é útil se ele tiver acesso aos seus dados. Sem isso, ele é só um chatbot glorificado."

---

### Bloco 2: Skills do ClawHub — O jeito fácil (7 min)

**O que é uma skill:**
"Uma skill é como um app que você instala no seu agente. Alguém já fez o trabalho pesado — você só instala e usa."

**Demonstração ao vivo:**

1. **Buscar skills disponíveis**
   ```bash
   clawhub search notion
   ```
   Explicar: "O ClawHub é tipo uma App Store de skills pra agentes."

2. **Instalar uma skill**
   ```bash
   clawhub install notion
   ```
   Explicar o que acontece:
   - Baixa o código da skill
   - Registra no OpenClaw
   - Agora o agente sabe usar Notion

3. **Ver skills instaladas**
   ```bash
   clawhub list
   ```

4. **Testar a skill** — mandar mensagem pro agente:
   > "Liste as tasks da database [ID da database] que estão com status 'In Progress'"

**Skills recomendadas pra mostrar:**
- `notion` — gestão de projetos
- `1password` — credenciais seguras
- `weather` — exemplo simples pra testar
- `github` — pra quem tem repo

---

### Bloco 2.5: gog CLI — Google Workspace de forma simples (2 min)

**Novo na 3.2 — alternativa recomendada ao fluxo OAuth manual:**

```bash
# Instalar gog CLI
npm install -g gog

# Autenticar (um comando pra tudo: Calendar, Drive, Gmail, Docs)
gog auth login

# Usar
gog calendar list --account=SEU_EMAIL
gog drive ls
gog gmail inbox --limit 10
```

**Por que usar o gog em vez do fluxo OAuth manual?**
- Sem precisar criar projeto no Google Cloud Console
- Sem configurar OAuth credentials manualmente
- Um único `gog auth login` autentica todos os serviços Google
- Skills de Calendar, Drive e Gmail já usam gog por padrão

> 💡 Se você usa Google Calendar, Drive, Gmail ou Docs — instale o gog primeiro. É o caminho mais rápido.

---

### Bloco 3: APIs diretas — Quando não tem skill (8 min)

**Cenário:** "E se não existir uma skill pronta pro Stripe? Ou pro seu CRM interno?"

**Case real: Integrar Stripe no MGM Boss**

**Passo a passo (mostrar o processo, não só o resultado):**

1. **Conseguir a API key**
   - Ir em dashboard.stripe.com → Developers → API Keys
   - Copiar a "Secret key" (começa com `sk_live_` ou `sk_test_`)
   - **NUNCA** colocar direto no código ou config

2. **Guardar no 1Password** (segurança!)
   ```bash
   # Se tiver a CLI do 1Password instalada
   op item create --category=api-credential \
     --title="Stripe MGM" \
     --vault="Amora Vault" \
     secret_key="sk_live_..."
   ```
   Ou manualmente pelo app/web.

3. **Recuperar quando o agente precisar** — mostrar como o agente faz isso:
   > "Agente, pegue a Stripe key do 1Password e me mostre meu MRR atual."

   Por trás dos panos, o agente vai:
   ```bash
   STRIPE_KEY=$(op item get "Stripe MGM" --vault "Amora Vault" --field secret_key --reveal)
   curl https://api.stripe.com/v1/balance \
     -u "$STRIPE_KEY:"
   ```

4. **Registrar no TOOLS.md** — documentar a integração:
   ```markdown
   ### Stripe (Pagamentos MGM)
   - **Item 1PW:** `Stripe MGM`
   - **Vault:** Amora Vault
   - **Acesso:** Read livre, Write = aprovação do Bruno
   ```

**Explicar o fluxo:**
> "1Password → Agente pega credencial → Usa API → Retorna resultado. Sua senha nunca fica exposta."

---

### Bloco 3.5: PDF Tool Nativo — já disponível no seu agente (1 min)

**Sem instalar nada — já funciona:**

> "Desde a versão 3.2, seu agente consegue analisar PDFs diretamente. Nenhuma skill, nenhuma configuração."

**Demonstrar ao vivo:**
- Arrastar um PDF para o chat (ou mencionar o path)
- Pedir: "Analise este contrato e me diga os pontos críticos"
- Mostrar o agente extraindo informações do PDF em tempo real

**Casos de uso práticos:**
- Analisar boletos e notas fiscais
- Resumir relatórios longos
- Extrair dados de planilhas em PDF
- Revisar contratos (com alerta: agente não é advogado!)

**Detalhes técnicos (breve):**
- Suporte nativo: Claude (Anthropic) e Gemini (Google)
- Outros modelos: extração automática de texto/imagens como fallback
- Limite: até 10 PDFs por mensagem

---

### Bloco 4: Transformar conhecimento em skill (5 min)

**Cenário:** "E se você usar uma ferramenta nichada que ninguém mais usa? Tipo um CRM interno da sua empresa?"

**Mostrar o conceito (não precisa implementar ao vivo):**

Uma skill é só uma pasta com:
- `SKILL.md` — instruções pro agente
- Scripts auxiliares (se necessário)

**Exemplo simples — Skill "CRM da Empresa X":**

Criar pasta:
```bash
mkdir -p ~/.openclaw/skills/crm-empresa-x
```

Criar `SKILL.md`:
```markdown
# Skill: CRM da Empresa X

Acesso à API interna do CRM.

## Credenciais
- API Key: 1Password → "CRM Empresa X API Key"
- Base URL: https://crm.empresax.com.br/api/v1

## Endpoints principais

### Listar leads
GET /leads?status=active
Header: Authorization: Bearer {API_KEY}

### Criar lead
POST /leads
Body: {"name": "...", "email": "...", "phone": "..."}

## Como usar
O agente deve:
1. Pegar a API key do 1Password
2. Fazer chamadas via curl ou fetch
3. Parsear a resposta JSON
```

**Registrar a skill:**
```bash
openclaw skills register ~/.openclaw/skills/crm-empresa-x
```

**Testar:**
> "Agente, me liste os leads ativos no CRM."

**Explicar:**
> "Você não precisa saber programar. Só precisa saber onde está a documentação da API e copiar pra dentro do SKILL.md. O agente faz o resto."

---

### Bloco 5: Cases reais — FLG e MGM (3 min)

**Mostrar os dois workspaces lado a lado:**

**MGM Boss (`workspace-mgm-boss`):**
- **TOOLS.md aberto** — mostrar as integrações documentadas:
  - Supabase (banco de dados)
  - Stripe (pagamentos)
  - ChartMogul (métricas SaaS)
  - PostHog (analytics)
  - Notion (sprint board)
  - Google Analytics + Search Console (SEO)

**FLG Boss (`workspace-flg-boss`):**
- **TOOLS.md aberto** — mostrar:
  - YouTube Data API + Analytics API
  - Instagram via RapidAPI
  - LinkedIn via RapidAPI
  - Twitter/X Bearer Token
  - Tella.tv (gravações)
  - Figma (design)
  - Notion (calendário editorial)

**Frase-chave:**
> "Esses dois agentes veem TUDO que acontece nos meus negócios. E eu não preciso abrir 15 abas todo dia."

---

### Bloco 6: Checklist prático pra integrar qualquer ferramenta (2 min)

**Roteiro que o aluno pode seguir:**

1. ✅ A ferramenta tem API? (procurar "API documentation" no Google)
2. ✅ Existe skill pronta no ClawHub? (`clawhub search nome-da-ferramenta`)
3. ✅ Se sim → instalar e testar
4. ✅ Se não → seguir o fluxo:
   - Pegar API key na ferramenta
   - Guardar no 1Password
   - Documentar no TOOLS.md
   - Testar com o agente
5. ✅ Se for recorrente → criar uma skill customizada

---

## Alertas de Segurança (enfatizar)

🔴 **NUNCA** colocar API keys direto no código ou config
🔴 **NUNCA** commitar credenciais no Git
🔴 **SEMPRE** usar 1Password (ou similar)
🔴 **SEMPRE** definir permissões (read-only quando possível)

**Exemplo real do MGM:**
> "No MGM Boss, o agente pode LER dados do Stripe à vontade. Mas pra fazer um refund ou cancelar uma subscription, ele PRECISA pedir aprovação minha. Isso está documentado no TOOLS.md e ele respeita."

---

## Checkpoint da Aula

Ao final, o aluno deve saber:
- [ ] O que é uma skill e onde encontrar
- [ ] Como instalar uma skill do ClawHub
- [ ] Como integrar uma API direto (sem skill pronta)
- [ ] Onde guardar credenciais (1Password)
- [ ] Como documentar integrações no TOOLS.md
- [ ] Como criar uma skill customizada (conceito)

---

## Prompt que vai no PDF

Vai estar no arquivo `prompts/modulo-extra-a-integracoes.md`.

---

## Troubleshooting Comum

### "clawhub: command not found"
```bash
npm install -g clawhub
```

### "Skill instalou mas agente não sabe usar"
```bash
# Verificar se registrou
openclaw skills list
# Se não aparece, registrar manualmente
openclaw skills register ~/.openclaw/skills/nome-da-skill
# Reiniciar gateway
openclaw gateway restart
```

### "API retorna 401 Unauthorized"
- Verificar se a API key está certa
- Verificar se expirou
- Verificar se tem permissões suficientes

---

*Esta aula é o divisor de águas: antes dela, o aluno tem um agente isolado. Depois, tem um agente que vê tudo.*
