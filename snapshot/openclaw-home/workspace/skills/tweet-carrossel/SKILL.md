---
name: tweet-carrossel
description: Gera slides no formato tweet (estilo X/Twitter) para carrosséis do Instagram usando Python + Pillow. Use quando o usuário pedir para criar slides de carrossel com fundo preto, avatar circular, nome + @ do perfil e texto branco centralizado verticalmente — especialmente para a Dra. Daniely Freitas ou qualquer médico/perfil que use esse formato editorial. Também use quando pedir "formato tweet", "carrossel preto com texto branco", "montar slides com foto de perfil" ou variações similares.
---

# Tweet Carrossel

Gera slides 1080x1350 no padrão tweet/X para carrosséis do Instagram.

## Estrutura do carrossel

| Slide | Tipo | Quem monta |
|-------|------|-----------|
| 1 | Capa (foto da médica + headline) | Usuário / externo |
| 2 | Gancho científico (texto + imagem do paper) | Usuário / externo |
| 3+ | Tweet format (este script) | **Clara via script** |

## Especificações técnicas

- **Tamanho:** 1080 × 1350 px (4:5)
- **Fundo:** preto `#000000`
- **Margens laterais:** 64 px
- **Avatar:** 56 px circular, extraído/fornecido pelo usuário
- **Nome:** DejaVu Sans Bold 30 px, branco
- **Handle:** DejaVu Sans Regular 26 px, cinza `#8C9691`
- **Verificado:** círculo azul `#1D9BF0` com checkmark branco
- **Corpo:** DejaVu Sans Regular 34 px, branco, entrelinha 1.45×
- **Sem** contador de página, **sem** ícone de mute

## Regra de posicionamento

- O bloco inteiro (header + texto) é **sempre centralizado verticalmente**
- `y_start = max(40, (H - total_h) // 2)`
- Não usar ancoragem fixa no topo; deixar o espaço vazio distribuído

## Como usar o script

### 1. Preparar o avatar

Extrair do slide 2 existente (coordenadas validadas para Dra. Daniely):

```python
from PIL import Image
slide2 = Image.open("slide_02.png")
avatar = slide2.crop((30, 28, 128, 126))
avatar.save("avatar.png")
```

Ou usar qualquer foto de perfil quadrada/circular fornecida.

### 2. Montar o JSON de slides

```json
[
  {
    "num": 3,
    "total": 6,
    "paragraphs": [
      "Primeira frase de impacto.",
      "",
      "2,4 BILHÕES de pessoas no mundo.",
      "31% da população mundial.",
      "",
      "Mas o que isso causa no seu corpo? →"
    ]
  }
]
```

**Regras do JSON:**
- `""` = linha em branco (respiro visual entre blocos)
- `→` ao final = gancho para próximo slide
- `[TEXTO EM CAIXA ALTA]` = CTA
- Itens de lista começam com `→ ` ou `- `

### 3. Executar

```bash
python3 scripts/make_tweet_slides.py \
  --config slides.json \
  --avatar avatar.png \
  --out ./output \
  --name "Dra Daniely Freitas" \
  --handle "@dradaniely.freitas"
```

### 4. Entregar

```bash
# Upload individual por slide
for f in output/slide_*.png; do
  curl -s -F "reqtype=fileupload" -F "fileToUpload=@$f" https://catbox.moe/user/api.php
done

# Pacote completo
tar -czf carrossel.tar.gz output/*.png
curl -F "reqtype=fileupload" -F "fileToUpload=@carrossel.tar.gz" https://catbox.moe/user/api.php
```

## Fluxo operacional padrão

1. Usuário envia slide 1 (capa) e slide 2 (gancho) prontos
2. Usuário envia texto dos slides 3+ numerados
3. Clara extrai avatar do slide 2, monta o JSON e roda o script
4. Entrega slides individuais via link catbox + pacote `.tar.gz`
5. Ajustes pontuais: roda apenas o slide alterado

## Perfis configurados

### Dra. Daniely Freitas
- Nome: `Dra Daniely Freitas`
- Handle: `@dradaniely.freitas`
- Avatar: extrair de `slide_02.png` crop `(30, 28, 128, 126)`
- Verificado: sim

Para outro perfil, passar `--name` e `--handle` diferentes e fornecer a imagem do avatar.

## Assets incluídos

- `assets/DejaVuSans.ttf` — fonte regular
- `assets/DejaVuSans-Bold.ttf` — fonte bold

O script usa as fontes do diretório `assets/` automaticamente; se não encontrar, faz fallback para as fontes do sistema.
