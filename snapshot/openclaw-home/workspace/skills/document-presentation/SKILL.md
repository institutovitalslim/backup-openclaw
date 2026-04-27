# document-presentation

**Descrição:** Criar apresentações Microsoft PowerPoint (.pptx). Gera slides profissionais com layouts, imagens, tabelas e gráficos para apresentações de resultados, pitches e treinamentos.

**Dependências:** `python-pptx`

---

## Uso

### Criar apresentação simples
```bash
python3 ~/.openclaw/workspace/skills/document-presentation/scripts/create_pptx.py \
  --output apresentacao.pptx \
  --title "Resultados do Trimestre" \
  --subtitle "Instituto Vital Slim" \
  --slides "Slide 1 conteúdo\n---\nSlide 2 conteúdo"
```

### Criar apresentação com imagem
```bash
python3 ~/.openclaw/workspace/skills/document-presentation/scripts/create_pptx.py \
  --output pitch.pptx \
  --title "Pitch HomeMatch Club" \
  --slides "Problema: Falta de concierge imobiliário\n---\nSolução: HomeMatch Club" \
  --image /caminho/logo.png
```

---

## Quando usar

- Apresentações de resultados para a Dra. Daniely
- Pitch para investidores ou parceiros
- Treinamentos internos
- Propostas comerciais
- Relatórios visuais

---

## Quando NÃO usar

- Para documentos de texto — usar `document-word`
- Para planilhas — usar `document-excel`
- Para carrosséis Instagram — usar `tweet-carrossel`
