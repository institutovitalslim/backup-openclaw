# document-excel

**Descrição:** Criar, editar e manipular planilhas Microsoft Excel (.xlsx). Gera relatórios financeiros, listas, dashboards e análises de dados com formatação profissional.

**Dependências:** `openpyxl`, `pandas`

---

## Uso

### Criar planilha simples
```bash
python3 ~/.openclaw/workspace/skills/document-excel/scripts/create_xlsx.py \
  --output planilha.xlsx \
  --sheet "Dados" \
  --headers "Nome,Email,Telefone" \
  --rows "João,joao@email.com,71999999999\nMaria,maria@email.com,71888888888"
```

### Criar planilha financeira
```bash
python3 ~/.openclaw/workspace/skills/document-excel/scripts/create_xlsx.py \
  --output financeiro.xlsx \
  --sheet "Fluxo de Caixa" \
  --headers "Data,Descrição,Entrada,Saída,Saldo" \
  --rows "2026-04-01,Consulta Dr. Daniely,1000,0,1000\n2026-04-02,Aluguel,0,3000,-2000" \
  --currency "Entrada,Saída,Saldo"
```

### Converter CSV para Excel
```bash
python3 ~/.openclaw/workspace/skills/document-excel/scripts/csv_to_xlsx.py \
  --input dados.csv \
  --output dados.xlsx
```

---

## Quando usar

- Relatórios financeiros e fluxo de caixa
- Listas de pacientes/contatos
- Dashboards de métricas
- Análise de dados tabulares
- Exportar dados do QuarkClinic/Omie para Excel

---

## Quando NÃO usar

- Para documentos de texto — usar `document-word`
- Para apresentações — usar `document-presentation`
- Para PDFs — usar `nano-pdf`
