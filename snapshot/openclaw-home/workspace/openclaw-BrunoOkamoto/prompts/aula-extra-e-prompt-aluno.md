# Prompt do Aluno: Aula Extra E — Gerenciamento de Contexto & Memória

> **Cole este prompt no chat com seu agente OpenClaw para praticar os conceitos da aula.**

---

Olá! Vou praticar gerenciamento de contexto e memória com você.

**Objetivo:** Aprender a usar `/status`, `/compact`, `/new`, entender compactação automática e como a memória funciona entre sessões.

Por favor, me guie através dos seguintes exercícios:

---

## Exercício 1: Entendendo o `/status`

1. Me mostre como usar o comando `/status`
2. Me explique o que cada informação significa:
   - Modelo atual
   - Uso de contexto (tokens e %)
   - Custo (se disponível)
   - Tempo de sessão
3. Me diga: em qual % de contexto eu deveria começar a me preocupar?

---

## Exercício 2: Simulando Crescimento de Contexto

Vamos fazer uma conversa longa para encher o contexto (não precisa ser útil, só pra praticar):

1. Me conte uma história sobre como você foi criado (use bastante texto)
2. Depois, me explique como funciona um LLM em detalhes técnicos (de novo, bastante texto)
3. Depois disso, rode `/status` de novo e me mostre quanto o contexto cresceu

**Pergunta reflexiva:** Por que conversas longas aumentam tanto o contexto?

---

## Exercício 3: Compactação Manual

1. Me mostre como usar o comando `/compact`
2. Rode `/status` antes e depois para eu ver a diferença
3. Me explique:
   - O que foi preservado?
   - O que foi resumido?
   - Você ainda lembra da nossa conversa anterior?

---

## Exercício 4: Diferença entre `/compact` e `/new`

1. Me explique a diferença entre:
   - Compactar a sessão (`/compact`)
   - Iniciar sessão nova (`/new`)

2. Me dê exemplos de quando usar cada um:
   - 3 situações para `/compact`
   - 3 situações para `/new`

---

## Exercício 5: Testando `/new`

**Antes de fazer `/new`:**
1. Me ajude a criar um arquivo `memory/teste-aula-e.md` com:
   - Resumo do que praticamos até agora
   - Uma decisão fictícia importante: "Projeto X deve usar Python 3.11"
   - Data e hora atual

**Agora faça `/new`**

**Depois do `/new`:**
1. Você ainda lembra de mim?
2. Você lembra do que conversamos antes?
3. Você consegue acessar o arquivo `memory/teste-aula-e.md`?
4. Me explique o que aconteceu: o que você perdeu e o que você manteve?

---

## Exercício 6: Compactação Automática

Me explique como configurar compactação automática no OpenClaw:

1. Qual arquivo eu preciso editar?
2. Quais parâmetros eu devo configurar?
3. Qual threshold você recomenda? (70%, 75%, 80%?)
4. Quais são as vantagens e desvantagens de ativar?

---

## Exercício 7: Hierarquia de Memória

Me desenhe (em texto/ASCII) a hierarquia de memória do OpenClaw:

1. Contexto da sessão (temporário)
2. Memória recente (memory/*.md)
3. Memória de longo prazo (MEMORY.md)

E me explique:
- O que acontece com cada nível quando uso `/compact`?
- O que acontece com cada nível quando uso `/new`?
- Como você decide o que salvar em cada nível?

---

## Exercício 8: Troubleshooting

Me ajude a resolver estes problemas fictícios:

**Problema 1:** "Fiz `/new` e o agente não lembra do projeto que começamos ontem"
- O que pode ter acontecido?
- Como eu resolvo?

**Problema 2:** "Meu contexto tá em 95% e `/compact` só liberou 10%"
- O que devo fazer?
- Como prevenir isso no futuro?

**Problema 3:** "Após compactar, o agente esqueceu uma decisão importante"
- Por que isso acontece?
- Como eu garanto que decisões importantes não se percam?

---

## Exercício 9: Estratégia Pessoal

Com base no meu uso (você pode me perguntar como eu pretendo usar o OpenClaw), me recomende:

1. Devo ativar auto-compact? Com qual threshold?
2. Com que frequência devo usar `/new`?
3. Devo monitorar contexto ativamente ou deixar no automático?
4. Dicas específicas para economizar custo de API

---

## Exercício 10: Checklist Final

Me crie um checklist personalizado de boas práticas de gestão de contexto que eu possa imprimir e deixar do lado do computador. Algo tipo:

**Antes de começar:**
- [ ] ...

**Durante o trabalho:**
- [ ] ...

**Ao terminar:**
- [ ] ...

---

## Reflexão Final

Depois de fazer todos esses exercícios, me responda:

1. Qual é a diferença prática entre `/compact` e `/new`?
2. Por que compactação automática é importante?
3. Como memória funciona entre sessões?
4. Qual é a maior lição que você aprendeu sobre gestão de contexto?

---

**Obrigado por me guiar! 🚀**

Agora eu sei:
✅ Usar `/status`, `/compact`, `/new` com confiança  
✅ Configurar compactação automática  
✅ Entender a hierarquia de memória  
✅ Gerenciar contexto de forma proativa  
✅ Economizar custo de API  

---

*Se tiver dúvidas adicionais durante os exercícios, sinta-se livre para perguntar!*
