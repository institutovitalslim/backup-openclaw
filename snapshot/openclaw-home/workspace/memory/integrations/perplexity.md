# perplexity.md - Perplexity API / Skill

## Status
- Validado na VPS em 2026-03-23.
- A skill Perplexity esta funcional no host principal do OpenClaw.
- Nao repetir a afirmacao de indisponibilidade sem retestar antes.

## Credencial
- Chave armazenada no 1Password em `openclaw/Key Perplexity OpenClaw`.
- Referencia usada no ambiente: `PERPLEXITY_API_KEY=op://openclaw/Key Perplexity OpenClaw/password`.

## Validacao Operacional
- Em 2026-03-23, uma consulta real via `skills/perplexity/scripts/search.mjs` retornou resultados com sucesso.
- O runtime do OpenClaw injeta a chave e permite uso da skill no host.

## Referencia Rapida de API
- Search API: `POST https://api.perplexity.ai/search`
- Agent/Responses API: `POST https://api.perplexity.ai/v1/responses`
- Embeddings API: `POST https://api.perplexity.ai/v1/embeddings`

## Regra de Uso
- Se houver duvida sobre disponibilidade, retestar antes de responder ao usuario.
- Se a task for via OpenClaw, priorizar a skill `perplexity`/ferramenta equivalente em vez de chamadas manuais ad hoc.
