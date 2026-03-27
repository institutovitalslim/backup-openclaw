# ❓ Q&A — Contexto & Memória (Token, /compact, /new)

> Linguagem simples. Sem terminal. Cole o prompt no seu bot e ele resolve.

---

## "Meu bot ficou lento e as respostas pioraram muito"

**O que provavelmente aconteceu:** A conversa ficou longa demais. Imagine tentar lembrar de TUDO que você fez nos últimos 6 meses de uma vez só — o cérebro trava. Com o bot é igual.

**O que fazer:**
Cole esse prompt no seu bot:

```
Estou sentindo que você ficou mais lento e as respostas pioraram.
Me diz:
1. Qual é o tamanho atual do contexto? (use /status)
2. Está perto do limite?
3. O que você recomenda: /compact ou /new?
4. Qual a diferença entre os dois pra mim decidir?
```

---

## "Qual a diferença entre /compact e /new? Tenho medo de perder tudo"

**Em linguagem simples:**

| | /compact | /new |
|---|---|---|
| **O que faz** | Resume a conversa atual | Começa uma conversa zerada |
| **Perde memória?** | Não — resume, não apaga | A conversa some, mas arquivos de memória ficam |
| **Quando usar** | Conversa longa mas quer continuar | Quer um começo fresco |
| **Analogia** | Tirar uma foto do que aconteceu | Abrir um caderno novo |

**Resposta curta:** Use `/compact` primeiro. Se ainda estiver lento depois, use `/new`.

**Importante:** Mesmo com `/new`, o bot lembra de você! Ele tem arquivos de memória (MEMORY.md, memory/) que persistem entre conversas.

---

## "O bot 'esqueceu' algo que eu tinha contado"

**O que aconteceu:** Ou a conversa foi compactada e aquela informação não ficou no resumo, ou foi iniciada uma sessão nova.

**O que fazer:**
Cole esse prompt no seu bot:

```
Você parece ter esquecido [DESCREVA O QUE ELE ESQUECEU].
Me ajuda a recuperar isso:
1. Verifica seus arquivos de memória (MEMORY.md, memory/)
2. Essa informação está salva em algum lugar?
3. Se não estiver, vou te recontar agora: [REESCREVA A INFORMAÇÃO]
4. Por favor, salva isso no arquivo de memória adequado pra não esquecer mais.
```

---

## "Apareceu um erro de 'token limit' ou 'context too long'"

**O que aconteceu:** A conversa ultrapassou o limite de memória do modelo. É como tentar colocar 10 litros em um copo de 2 litros.

**O que fazer imediatamente:**
Cole esse prompt no seu bot:

```
Apareceu um erro de limite de contexto/tokens.
Precisa que você:
1. Faça um /compact agora para resumir a conversa
2. Me confirme quando terminar
3. Continue de onde paramos depois do compact
```

**Para evitar que aconteça de novo:**
Cole esse prompt:

```
Quero configurar a compactação automática pra você nunca mais estourar o limite.
Me guia como configurar o "compaction: { mode: default }" no meu openclaw.json.
Explica o que cada opção faz antes de eu aplicar.
```

---

## "O que é memória vetorial? Preciso disso?"

**Em linguagem simples:** É uma forma do bot guardar muita informação e encontrar a parte certa na hora certa — como um índice de livro inteligente.

**Precisa?** Provavelmente não agora. A maioria dos alunos usa muito bem só com os arquivos de memória normais (MEMORY.md). A memória vetorial é para casos avançados com muita informação.

**Se quiser entender mais:**
Cole esse prompt no seu bot:

```
Me explica de forma bem simples:
1. O que são os arquivos MEMORY.md e memory/ que você usa?
2. O que seria "memória vetorial" e quando faz sentido?
3. Para o meu uso atual, o que você recomenda?
```

---

*Última atualização: Fev/2026*
