# Prompt do Aluno — M06 Aula 3: Crie suas skills com o /criar-skill

> Use este prompt no seu agente depois de assistir a aula bônus.

---

## 📦 Passo 1 — Instalar o /criar-skill

A skill está disponível no GitHub. Instale antes de usar:

```bash
# No terminal do seu workspace
cd ~/seu-workspace/skills/operations

# Clone a skill
git clone https://github.com/okjpg/skill-creator criar-skill

# Pronto. O agente já consegue usar.
```

Ou peça pro agente instalar:
```
Instala a skill do /criar-skill no meu workspace. 
Repositório: https://github.com/okjpg/skill-creator
Coloca em skills/operations/criar-skill/
```

---

## 🎯 O que você vai praticar

Usar o `/criar-skill` nos dois modos: capturar um processo que já resolveram juntos, e criar uma skill nova a partir de uma ideia que você ainda não sabe estruturar.

---

## Caminho A — Você acabou de resolver algo. Não deixa sumir.

Use logo depois de uma conversa onde vocês resolveram um problema juntos:

```
/criar-skill
```

Só isso. O agente lê o histórico, extrai o processo e propõe a skill completa.

**Quando usar:** Sempre que uma conversa levou mais de 10 minutos pra resolver algo. Se foi trabalhoso uma vez, vai ser de novo — a menos que vire skill.

---

## Caminho B — Você tem uma ideia. Quer estruturar.

```
/criar-skill quero [descreva sua ideia em 1 frase]
```

**Exemplos reais para testar:**

```
/criar-skill quero gerar um resumo semanal das minhas métricas mais importantes
```

```
/criar-skill quero criar briefings de reunião antes de cada call importante
```

```
/criar-skill quero responder comentários do Instagram mantendo meu tom de voz
```

```
/criar-skill quero analisar concorrentes e me dar os 3 pontos principais
```

O agente vai fazer perguntas pra entender o processo — responda naturalmente. No final, ele propõe a skill completa e você aprova o deploy.

---

## Desafio da aula

Crie **pelo menos 2 skills** esta semana:

1. **Uma do Caminho A** — Pense num problema que você já resolveu com o agente recentemente. Recrie a conversa e use `/criar-skill` no final.

2. **Uma do Caminho B** — Pense num processo que você faz manualmente hoje e gostaria que o agente assumisse. Use `/criar-skill quero [sua ideia]`.

---

## Pergunta para cada skill que você criar

Antes de aprovar o deploy, responda:

- O trigger faz sentido? (Consigo acionar naturalmente?)
- O output é o que eu esperava?
- Tem algum detalhe importante que ficou faltando?

Se sim para os três — aprova. Se não, pede pro agente ajustar antes de salvar.

---

## Lembre-se

> "Qualquer processo que você repete mais de 2 vezes é candidato a skill."

Toda vez que você se pegar explicando algo pro agente de novo — é sinal de que falta uma skill.
