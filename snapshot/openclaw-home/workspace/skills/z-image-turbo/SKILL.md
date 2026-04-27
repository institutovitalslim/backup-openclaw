# Z-Image-Turbo Image Generation

**Repositório:** https://huggingface.co/spaces/mrfakename/Z-Image-Turbo
**Backend:** HuggingFace Spaces (Gradio)
**Modelo:** Fast diffusion (SDXL/Flux acelerado, ~9 steps)
**Custo:** Gratuito (limitado pela fila do HuggingFace)

---

## Quando Usar

| Cenário | Recomendação |
|---------|-------------|
| Rápida prototipagem | ✅ Z-Image-Turbo (veloz, gratuito) |
| Imagens médicas/compliance | ❌ Não usar — sem controle de conteúdo |
| Fotos da Dra. / pacientes | ❌ NÃO USAR — upload para servidor externo |
| Conteúdo Instagram/carrossel | ✅ Pode usar (com revisão humana) |
| Mockups e conceitos | ✅ Ideal |
| Produção final alta qualidade | ⚠️ Preferir OpenAI/Google (mais controle) |

---

## Uso

### Via Script

```bash
python3 scripts/generate_image.py \
  --prompt "Descrição da imagem" \
  --output /caminho/para/salvar.png \
  --width 1024 \
  --height 1024 \
  --steps 9
```

### Parâmetros

| Parâmetro | Padrão | Range | Descrição |
|-----------|--------|-------|-----------|
| `--prompt` | obrigatório | - | Texto descrição |
| `--output` | None | - | Caminho de saída |
| `--width` | 1024 | 256-2048 | Largura |
| `--height` | 1024 | 256-2048 | Altura |
| `--steps` | 9 | 1-50 | Inference steps (menos = mais rápido) |
| `--seed` | None | int | Seed para reprodutibilidade |

---

## Limitações

⚠️ **Fila do HuggingFace** — em horários de pico, pode demorar 30-60s
⚠️ **Rate limiting** — ~5-10 requisições/minuto (espaço gratuito)
⚠️ **Sem filtros NSFW** — revisar imagens antes de usar publicamente
⚠️ **Downtime** — HuggingFace Spaces podem hibernar após inatividade

---

## Comparação com Stack Atual

| Provider | Velocidade | Custo | Qualidade | Uso Recomendado |
|----------|-----------|-------|-----------|-----------------|
| **Z-Image-Turbo** | ⚡⚡⚡ Rápido | Grátis | Média/Alta | Prototipagem, conceitos |
| OpenAI (DALL-E) | ⚡⚡ Rápido | Pago | Alta | Produção, compliance |
| Google (NanoBanana) | ⚡⚡ Rápido | Pago | Muito Alta | Fotos reais, capas |
| Wan 2.2 | ⚡ Médio | Pago | Alta | Vídeo |

---

## Segurança

✅ **Não envia dados sensíveis** — prompt é texto, não envia imagens
✅ **Sem API key** — acesso direto ao HuggingFace Spaces
⚠️ **Servidor externo** — prompts vão para HuggingFace (não ideal para dados médicos)

---

## Instalação

```bash
pip3 install gradio_client
```

Ou via requisitos:
```bash
pip3 install -r requirements.txt
```

---

## Manutenção

**Status:** Operacional (testado em 2026-04-26)
**Último teste:** Imagem gerada com sucesso (507KB PNG, 1024x1024)
**Responsável:** Clara (VPS)
