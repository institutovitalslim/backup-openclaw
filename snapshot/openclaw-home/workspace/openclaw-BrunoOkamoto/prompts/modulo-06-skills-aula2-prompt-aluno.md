# Prompt do Aluno — M06 Aula 2: Skills — O sistema de superpoderes

> Use este prompt no seu agente depois de assistir a aula.

---

## 📦 Dica — Instalar o /criar-skill para criar skills mais rápido

Não é obrigatório nesta aula, mas se quiser criar skills com ajuda do agente:

```bash
cd ~/seu-workspace/skills/operations
git clone https://github.com/okjpg/skill-creator criar-skill
```

Ou peça pro agente: *"Instala o /criar-skill do repositório https://github.com/okjpg/skill-creator em skills/operations/criar-skill/"*

---

## 🎯 O que você vai praticar

Criar sua primeira skill do zero, organizar a pasta corretamente e testar se o agente consegue executar o processo de forma consistente.

---

## Prompt para usar no seu agente

```
Quero criar minha primeira skill seguindo a estrutura correta do OpenClaw.

O processo que quero documentar é: [descreva aqui o processo que você repete com frequência — ex: "gerar relatório semanal de métricas", "criar carrossel de LinkedIn", "responder emails de suporte"]

Me ajuda a:
1. Definir o nome correto da skill em kebab-case
2. Escolher a categoria certa (content, analytics, operations, research, ou criar uma nova)
3. Criar o SKILL.md com: name, description (com triggers), metadata e o passo a passo de execução
4. Criar a estrutura de pasta em skills/{categoria}/{nome-da-skill}/

Depois de criar, quero testar se você consegue executar o processo só lendo o SKILL.md — sem eu precisar explicar nada.
```

---

## Variações por nível

**🟢 Iniciante — copiar uma skill existente:**
```
Me mostra o SKILL.md de uma skill simples que você já tem, e me explica cada campo. 
Quero entender a estrutura antes de criar a minha.
```

**🟡 Intermediário — criar skill de analytics:**
```
Cria uma skill chamada "relatorio-semanal" em skills/analytics/.
Ela deve: puxar as métricas mais importantes da semana (você define quais fazem sentido pro meu negócio), 
formatar num texto limpo com os principais números, e me enviar toda segunda-feira de manhã.
Inclui os triggers certos no description pra eu acionar facilmente.
```

**🔴 Avançado — criar skill com script:**
```
Quero uma skill que automatize [processo que usa API ou linha de comando].
Cria o SKILL.md + um script em scripts/ que execute a parte técnica.
A skill deve buscar as credenciais pelo 1Password — nunca hardcodado.
```

---

## Checklist pós-criação

Antes de considerar a skill pronta, confirme:

- [ ] Pasta criada em `skills/{categoria}/{nome}/`
- [ ] SKILL.md tem: name, description com triggers, metadata, e passo a passo claro
- [ ] Testei chamando o agente só com o trigger — sem dar contexto extra
- [ ] O agente executou corretamente lendo só o SKILL.md
- [ ] Skill está no Git (backup feito)

---

## Pergunta de reflexão

> "Qual processo você faz mais de 2 vezes por semana que ainda não virou skill?"

Esse é seu próximo candidato.
