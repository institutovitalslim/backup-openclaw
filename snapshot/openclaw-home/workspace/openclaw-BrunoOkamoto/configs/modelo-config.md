# Configurações Recomendadas do OpenClaw

> Referência para configurar seu openclaw.json

## Modelo por Uso

| Uso | Modelo Recomendado | Por quê |
|-----|-------------------|---------|
| Interação direta | Claude Opus | Melhor raciocínio, mais criativo |
| Crons / automação | Claude Sonnet | 90% mais barato, suficiente pra tasks |
| Heartbeats | Claude Haiku | Mínimo custo, só checa e reporta |
| Imagens | Gemini Flash | Bom e barato |
| Análise avançada / multimodal | Gemini 2.5 Pro | Contexto enorme (1M tokens), multimodal nativo |
| Alternativa Google | Gemini 3.1 Pro (`google/gemini-3.1-pro-preview`) | Reasoning avançado, boa opção de fallback |
| Volume alto / custo mínimo | MiniMax (`minimax/minimax-01`) | Contexto de 1M tokens a custo extremamente baixo |

### IDs dos Modelos (para openclaw.json)

```json
"anthropic/claude-opus-4-5"       // Claude Opus — interação principal
"anthropic/claude-sonnet-4-5"     // Claude Sonnet — crons e automação
"anthropic/claude-haiku-4-5"      // Claude Haiku — heartbeats
"google/gemini-2.5-pro-preview"   // Gemini 2.5 Pro — análise avançada
"google/gemini-3.1-pro-preview"   // Gemini 3.1 Pro — reasoning / fallback
"google/gemini-flash-2.0"         // Gemini Flash — imagens e volume
"minimax/minimax-01"              // MiniMax — custo mínimo, contexto longo
```

## Config de Compaction (IMPORTANTE)

Se não configurar, sua sessão vai estourar tokens e o agente trava.

```json
{
  "compaction": {
    "mode": "default"
  },
  "contextTokens": 160000,
  "reserveTokensFloor": 30000
}
```

## Thinking Mode

| Nível | Quando usar | Custo |
|-------|------------|-------|
| off | Tasks simples, respostas rápidas | $ |
| low | Dia a dia, maioria das interações | $$ |
| medium | Análise, planejamento, conteúdo | $$$ |
| high | Coding, problemas complexos, estratégia | $$$$ |

## Crons: Regra de Ouro

**SEMPRE:**
```json
{
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Sua tarefa aqui"
  },
  "delivery": { "mode": "announce" }
}
```

**NUNCA** usar `sessionTarget: "main"` + `payload.kind: "systemEvent"` — dispara mas não executa.

## Dicas de Economia

1. Heartbeats com Haiku: ~$0.005 cada (vs ~$0.10 com Opus)
2. Crons com Sonnet: economia de ~90% vs Opus
3. Espaçar crons: não colocar múltiplos no mesmo minuto (rate limit)
4. config.patch reinicia gateway — fazer em horários sem crons
