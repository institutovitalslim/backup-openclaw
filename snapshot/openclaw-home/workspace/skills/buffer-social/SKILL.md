# Buffer Social Media Posting Skill

Postar diretamente nas redes sociais do Instituto Vital Slim via Buffer GraphQL API.

## Uso

```bash
# Criar um post
python3 ~/.openclaw/workspace/skills/buffer-social/scripts/post_buffer.py \
  --text "Texto do post" \
  --title "Título do post" \
  --org-id "69e90408151436756ee2629a"
```

## Organização

- **ID**: `69e90408151436756ee2629a` (Instituto Vital Slim)

## Variáveis de ambiente

- `BUFFER_API_KEY` → lida de `/root/.openclaw/secure/buffer.env` (token OIDC para GraphQL)

## Regras

- Sempre confirmar com Tiaro antes de postar conteúdo não aprovado.
- Para carrosséis, usar a skill `tweet-carrossel` primeiro para gerar as imagens.
- Nunca postar sem revisão visual quando houver imagem da Dra.
