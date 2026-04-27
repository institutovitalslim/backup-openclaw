# document-word

**Descrição:** Criar, editar e manipular documentos Microsoft Word (.docx). Gera relatórios, contratos, memorandos e documentos formatados com tabelas, imagens, cabeçalhos e rodapés.

**Dependências:** `python-docx`

---

## Uso

### Criar documento simples
```bash
python3 ~/.openclaw/workspace/skills/document-word/scripts/create_doc.py \
  --output /caminho/documento.docx \
  --title "Título do Documento" \
  --content "Conteúdo do documento..."
```

### Criar documento com tabela
```bash
python3 ~/.openclaw/workspace/skills/document-word/scripts/create_doc.py \
  --output relatorio.docx \
  --title "Relatório Mensal" \
  --content "Resumo das atividades..." \
  --table "Coluna A,Coluna B\nValor 1,Valor 2\nValor 3,Valor 4"
```

### Converter markdown para Word
```bash
python3 ~/.openclaw/workspace/skills/document-word/scripts/md_to_docx.py \
  --input arquivo.md \
  --output documento.docx
```

---

## Quando usar

- Criar relatórios profissionais em Word
- Gerar contratos ou documentos com formatação específica
- Converter conteúdo markdown para .docx
- Editar documentos existentes (adicionar seções, tabelas)
- Criar memorandos ou cartas com cabeçalho/rodapé

---

## Quando NÃO usar

- Para PDFs — usar `nano-pdf` ou `document-pdf`
- Para planilhas — usar `document-excel`
- Para apresentações — usar `document-presentation`
