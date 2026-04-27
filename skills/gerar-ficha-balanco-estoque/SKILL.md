# gerar-ficha-balanco-estoque

**Descrição:** Gerar ficha de balanço de estoque de injetáveis em PDF com logomarca da clínica. Lê o arquivo de estoque atual e gera uma ficha pronta para contagem física, com itens críticos destacados e seção especial para Tirzepatida.

**Dependências:** weasyprint

---

## Uso

### Gerar ficha com estoque atual
```bash
python3 ~/.openclaw/workspace/skills/gerar-ficha-balanco-estoque/scripts/main.py \
  --estoque ~/.openclaw/workspace/memory/tactical/estoque-injetaveis-clinica-2026-04-02.md \
  --logo ~/.openclaw/workspace/memory/tactical/logo-vital-slim.png \
  --output ~/ficha-balanco-estoque.pdf
```

### Gerar ficha com caminhos padrão
```bash
python3 ~/.openclaw/workspace/skills/gerar-ficha-balanco-estoque/scripts/main.py
```

---

## Quando usar

- Antes de realizar contagem física de estoque na clínica
- Quando houver divergência entre estoque sistêmico e físico
- Mensalmente ou no período definido para inventário
- Antes de fazer pedidos de reposição

## Quando NÃO usar

- Se o arquivo de estoque estiver desatualizado (atualizar primeiro)
- Se a logomarca não estiver disponível (será gerado sem logo)
- Para fins que não sejam contagem física de injetáveis

---

## Estrutura da ficha gerada

1. **Cabeçalho** com logomarca e campos de data/responsáveis
2. **Instruções** de preenchimento
3. **Tabela principal** com 56 medicamentos (ordem alfabética)
4. **Itens críticos destacados** em vermelho (≤ 5 unidades)
5. **Seção Tirzepatida** com controle de ampolas
6. **Tabela de divergências** para anotações
7. **Assinaturas** (contagem 1, contagem 2, conferência, aprovação)

---

## Arquivos relacionados

- Estoque sistêmico: `memory/tactical/estoque-injetaveis-clinica-2026-04-02.md`
- Logo da clínica: `memory/tactical/logo-vital-slim.png` (convertido do PDF em `assets/brand/`)
- Saída padrão: `memory/tactical/balanco-estoque-fisico-YYYY-MM-DD.pdf`
