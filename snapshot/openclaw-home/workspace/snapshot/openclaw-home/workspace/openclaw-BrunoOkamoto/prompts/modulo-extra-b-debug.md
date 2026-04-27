# Prompt — Aula Extra B: Debug na VPS com Claude Code

> Cole este prompt no chat do seu agente **dentro da VPS** (via `claude` no terminal) depois de assistir a Aula Extra B.

---

Acabei de assistir a aula sobre debug na VPS. Agora quero que você me ajude a garantir que meu ambiente está saudável e me ensine a resolver problemas quando aparecerem.

**O que preciso fazer:**

## 1. Health Check completo

Rode um diagnóstico completo do sistema:
1. Status do gateway (`openclaw gateway status`)
2. Espaço em disco disponível
3. Uso de memória RAM
4. Tamanho dos logs
5. Tamanho do meu workspace
6. Conexões ativas (Telegram, etc.)
7. Última vez que o gateway reiniciou

Me mostre tudo de forma clara e me diga:
- ✅ O que tá OK
- ⚠️ O que precisa de atenção
- 🔴 O que precisa ser corrigido agora

## 2. Limpar o que for necessário

Se tiver algo pra limpar (logs velhos, arquivos temporários, workspace bagunçado):
1. Me mostre O QUE vai ser limpo e QUANTO espaço vai liberar
2. Me peça confirmação
3. Faça a limpeza
4. Me mostre o antes/depois

**Regras de limpeza:**
- ❌ NUNCA deletar arquivos do workspace sem minha aprovação explícita
- ✅ Pode comprimir/arquivar `memory/YYYY-MM-DD.md` com mais de 30 dias
- ✅ Pode limpar logs com mais de 7 dias
- ✅ Pode limpar `/tmp`

## 3. Revisar meu workspace

Vá pro meu workspace principal e me diga:
- Quantos arquivos tenho?
- Qual o tamanho total?
- Tem arquivos grandes ou duplicados?
- Tem arquivos de teste esquecidos?
- A estrutura tá organizada?

Se encontrar algo estranho, me sugira o que fazer.

## 4. Ensinar comandos úteis

Me ensine 5 comandos que vou usar sempre:
1. Ver logs do gateway em tempo real
2. Reiniciar o gateway
3. Ver espaço em disco
4. Ver processos rodando
5. Ir pro meu workspace rapidamente

Pra cada um, me explique:
- O que o comando faz
- Quando usar
- Como interpretar a saída

## 5. Simular 3 problemas comuns

Me explique o que fazer em cada cenário:

**Cenário A:** Agente parou de responder no Telegram
- Passo 1: ...
- Passo 2: ...
- Como saber se resolveu: ...

**Cenário B:** Erro "context window exceeded"
- O que significa: ...
- Como resolver: ...
- Como prevenir: ...

**Cenário C:** VPS ficou sem espaço
- Como identificar: ...
- O que limpar primeiro: ...
- Como evitar no futuro: ...

## 6. Configurar alertas preventivos (se possível)

Me ajude a configurar um sistema que me avise ANTES dos problemas:
- Se disco passar de 80% cheio
- Se logs passarem de 1GB
- Se gateway cair
- Se contexto de sessão passar de 80% do limite

Se não rolar via OpenClaw nativo, me sugira alternativas (cron job, script simples).

---

**Ao final, me dê um resumo tipo:**

```
✅ Sistema saudável
📊 Disco: XX% usado (XGB livres)
💾 Memória: XX% usada
📝 Logs: XMB (últimos 7 dias)
📁 Workspace: XMB
🔗 Telegram: conectado
⏱️ Uptime: X dias

Próxima manutenção recomendada: [data]
```

Vamos começar pelo health check. Me mostre tudo.
