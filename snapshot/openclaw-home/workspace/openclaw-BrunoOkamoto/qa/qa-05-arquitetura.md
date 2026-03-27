# ❓ Q&A — Arquitetura OpenClaw (Cérebro, Braços, Subagentes)

> Linguagem simples. Sem terminal. Cole o prompt no seu bot e ele resolve.

---

## "Qual a diferença entre o cérebro e os braços do agente?"

**Em linguagem simples:**

Pensa assim: você é o **chefe**. O OpenClaw é sua **empresa**.

- **Cérebro (Gateway)** = O escritório central. Recebe seus pedidos, toma decisões, coordena tudo.
- **Braços (Tools/Skills)** = Os funcionários especializados. Um faz busca na web, outro acessa o calendário, outro manda mensagem.
- **Subagentes** = Freelancers contratados pra tarefas específicas. Trabalham em paralelo e entregam resultado.

**Analogia completa:**
> Você manda: "Pesquisa os melhores restaurantes perto de mim pra hoje à noite e coloca no meu calendário."
> - O **cérebro** entende o pedido
> - O **braço de busca** procura os restaurantes
> - O **braço de calendário** cria o evento
> - Tudo acontece de forma coordenada

---

## "O que é um subagente e quando usar?"

**Em linguagem simples:** Um subagente é como contratar um assistente temporário pra fazer uma tarefa específica enquanto você continua fazendo outra coisa.

**Quando usar:**
- Tarefas que demoram muito (pesquisa longa, análise de muitos dados)
- Tarefas paralelas (enquanto um pesquisa, outro escreve)
- Tarefas de risco (melhor deixar um "assistente" testar antes do "chefe" executar)

**O que fazer:**
Cole esse prompt no seu bot:

```
Quero entender quando vale usar subagentes no meu caso.
Me explica:
1. O que diferencia um subagente de uma tarefa normal?
2. Para o que eu uso o bot hoje, faz sentido usar subagentes?
3. Se sim, me dá um exemplo prático de como ficaria?
```

---

## "Devo usar o OpenClaw ou o n8n para automatizar?"

**Diferença simples:**

| | OpenClaw | n8n |
|---|---|---|
| **Melhor pra** | Tarefas que precisam de raciocínio e linguagem natural | Fluxos fixos e previsíveis (se X então Y) |
| **Exemplo** | "Resumir emails importantes e me avisar os urgentes" | "Quando receber email com assunto X, salvar no sheet" |
| **Precisa de** | VPS + API de IA | Servidor ou conta cloud |
| **Curva de aprendizado** | Média (tem IA te ajudando) | Média (interface visual) |

**Resposta curta:** Use OpenClaw quando precisar de julgamento humano. Use n8n quando o fluxo for sempre igual.

**Eles podem trabalhar juntos:** n8n dispara um webhook → OpenClaw recebe e decide o que fazer.

---

## "Como sei se meu agente está funcionando corretamente?"

**O que fazer:**
Cole esse prompt no seu bot:

```
Faz um diagnóstico completo de saúde do meu agente:
1. O gateway está rodando corretamente?
2. Todas as ferramentas (tools) estão funcionando?
3. A memória está sendo salva corretamente?
4. Tem algum cron ou automação com problema?
5. O que você recomenda verificar regularmente?
Me dá um resumo do status geral.
```

---

## "Posso ter mais de um agente? Como funciona?"

**Em linguagem simples:** Sim! É como ter uma equipe de assistentes especializados.

**Exemplos:**
- **Agente Principal:** Faz tudo, é o seu assistente pessoal
- **Agente de Trabalho:** Só cuida de emails e tarefas profissionais
- **Agente de Conteúdo:** Especializado em criar posts e textos

**O que fazer:**
Cole esse prompt no seu bot:

```
Quero entender como ter múltiplos agentes funciona.
Me explica:
1. Como cada agente é configurado?
2. Eles compartilham memória ou são separados?
3. Quanto isso aumenta o custo?
4. Faz sentido pro meu uso atual ter mais de um?
```

---

*Última atualização: Fev/2026*
