#!/usr/bin/env python3
"""
gerar-ficha-balanco-estoque
Gerar ficha de balanço de estoque de injetáveis em PDF com logomarca da clínica.
Lê o arquivo de estoque atual e gera uma ficha pronta para contagem física.
"""

import argparse
import os
import re
import sys
from datetime import datetime

from weasyprint import HTML, CSS


def parse_estoque(filepath):
    """Parse the stock file and extract items with quantities."""
    items = []
    critical_items = []
    tirzepatida_info = ""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract stock items from "## Estoque Atual" section
    estoque_match = re.search(r'## Estoque Atual\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if estoque_match:
        estoque_text = estoque_match.group(1)
        for line in estoque_text.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Parse lines like "- Item Name — 10 (Supplier)" or "- Item — 0 ⚠️ ESGOTADO"
            match = re.match(r'-\s+(.+?)\s+[—-]\s+(\d+)(?:\s+UI)?(?:\s+\(.*?\))?(?:\s+⚠️\s+.*)?', line)
            if match:
                name = match.group(1).strip()
                qty_str = match.group(2)
                
                # Check if it's tirzepatida (special handling)
                if 'tirzepatida' in name.lower():
                    tirzepatida_info = line
                    continue
                
                try:
                    qty = int(qty_str)
                    items.append({'name': name, 'qty': qty, 'critical': qty <= 5})
                    if qty <= 5:
                        critical_items.append({'name': name, 'qty': qty})
                except ValueError:
                    continue
    
    # Sort items alphabetically
    items.sort(key=lambda x: x['name'].lower())
    
    return items, critical_items, tirzepatida_info


def generate_html(items, logo_path, date_str):
    """Generate HTML for the stock balance sheet."""
    
    # Build stock rows
    stock_rows = []
    for i, item in enumerate(items, 1):
        critical_class = 'critical' if item['critical'] else ''
        stock_rows.append(
            f'<tr class="{critical_class}">'
            f'<td>{i}</td>'
            f'<td>{item["name"]}</td>'
            f'<td>{item["qty"]}</td>'
            f'<td></td><td></td><td></td><td></td>'
            f'</tr>'
        )
    
    stock_rows_html = '\n'.join(stock_rows)
    
    # Logo handling
    logo_html = ''
    if logo_path and os.path.exists(logo_path):
        logo_html = f'<img src="file://{logo_path}" alt="Logo Vital Slim">'
    
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Ficha de Balanço de Estoque — Injetáveis Clínica</title>
<style>
@page {{ size: A4 landscape; margin: 1.2cm; }}
body {{ font-family: Arial, sans-serif; font-size: 9pt; line-height: 1.3; }}
.header {{ display: flex; align-items: center; margin-bottom: 10px; }}
.header img {{ height: 250px; margin-right: 25px; }}
.header-text {{ flex: 1; }}
h1 {{ text-align: center; font-size: 16pt; margin-bottom: 8px; margin-top: 0; }}
h2 {{ font-size: 11pt; margin-top: 12px; margin-bottom: 5px; border-bottom: 1px solid #333; padding-bottom: 3px; }}
.info {{ margin-bottom: 10px; font-size: 9pt; }}
.info table {{ width: 100%; border-collapse: collapse; }}
.info td {{ padding: 3px 6px; border: 1px solid #999; }}
table.stock {{ width: 100%; border-collapse: collapse; margin-top: 5px; font-size: 8pt; }}
table.stock th {{ background: #2c3e50; color: white; padding: 4px; text-align: left; border: 1px solid #333; }}
table.stock td {{ padding: 3px 5px; border: 1px solid #999; }}
table.stock tr:nth-child(even) {{ background: #f5f5f5; }}
.critical {{ background: #ffcccc !important; font-weight: bold; color: #900; }}
.critical td {{ background: #ffcccc !important; }}
.footer {{ margin-top: 12px; font-size: 8pt; text-align: center; }}
.sig-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
.sig-table td, .sig-table th {{ border: 1px solid #999; padding: 5px; text-align: center; font-size: 9pt; }}
</style>
</head>
<body>
<div class="header">
{logo_html}
<div class="header-text">
<h1>FICHA DE BALANÇO DE ESTOQUE — INJETÁVEIS CLÍNICA</h1>
</div>
</div>

<div class="info">
<table>
<tr><td width="20%"><b>Data:</b></td><td width="20%">___________</td><td width="20%"><b>Responsável 1:</b></td><td width="20%">___________</td><td width="20%"><b>Responsável 2:</b></td></tr>
<tr><td><b>Conferência:</b></td><td>___________</td><td><b>Aprovação:</b></td><td>___________</td><td></td></tr>
</table>
</div>

<h2>INSTRUÇÕES</h2>
<ol style="font-size:9pt;margin:5px 0;">
<li>Preencher "CONTAGEM FÍSICA 1" com a quantidade real encontrada</li>
<li>Preencher "CONTAGEM FÍSICA 2" com a segunda conferência</li>
<li>Itens em <b style="color:#900;">VERMELHO</b> são críticos (≤ 5 unidades ou esgotados)</li>
</ol>

<h2>ESTOQUE DE INJETÁVEIS</h2>
<table class="stock">
<tr><th>#</th><th>MEDICAMENTO</th><th>SALDO SIST.</th><th>CONT. 1</th><th>CONT. 2</th><th>DIF.</th><th>OBSERVAÇÕES</th></tr>
{stock_rows_html}
</table>

<h2>TIRZEPATIDA — CONTROLE ESPECIAL</h2>
<table class="stock">
<tr><th>#</th><th>ITEM</th><th>REGISTRO SIST.</th><th>CONT. FÍSICA</th><th>OBSERVAÇÕES</th></tr>
<tr><td>1</td><td>Ampola #1 (09-14/04)</td><td>360 UI usadas</td><td></td><td>Esgotada</td></tr>
<tr><td>2</td><td>Ampola #2 (14-15/04)</td><td>360 UI usadas</td><td></td><td>Esgotada</td></tr>
<tr><td>3</td><td>Ampola #3 (15-20/04)</td><td>360 UI usadas</td><td></td><td>Esgotada</td></tr>
<tr><td>4</td><td>Ampola #4 (20-23/04)</td><td>360 UI usadas</td><td></td><td>Esgotada</td></tr>
<tr><td>5</td><td>Ampola #5 (aberta 23/04)</td><td>145 UI restantes</td><td></td><td></td></tr>
<tr><td>6</td><td>Ampola #6 (fechada)</td><td>—</td><td></td><td>Confirmar existência</td></tr>
<tr><td>7</td><td>Ampola #7 (fechada)</td><td>—</td><td></td><td>Confirmar existência</td></tr>
<tr><td>8</td><td>Ampola #8 (fechada)</td><td>—</td><td></td><td>Confirmar existência</td></tr>
<tr style="font-weight:bold;background:#e8f4f8;"><td></td><td>TOTAL EM ESTOQUE</td><td>145 UI + ampolas</td><td></td><td></td></tr>
</table>

<h2>RESUMO DE DIVERGÊNCIAS</h2>
<table class="stock">
<tr><th>MEDICAMENTO</th><th>SALDO SIST.</th><th>CONTAGEM FÍS.</th><th>DIFERENÇA</th><th>JUSTIFICATIVA</th></tr>
<tr><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td></tr>
</table>

<h2>ASSINATURAS</h2>
<table class="sig-table">
<tr><th>FUNÇÃO</th><th>NOME</th><th>ASSINATURA</th><th>DATA</th></tr>
<tr><td>Contagem 1</td><td></td><td></td><td></td></tr>
<tr><td>Contagem 2</td><td></td><td></td><td></td></tr>
<tr><td>Conferência</td><td></td><td></td><td></td></tr>
<tr><td>Aprovação (Tiaro)</td><td></td><td></td><td></td></tr>
</table>

<div class="footer">
<i>Ficha gerada em {date_str} — Sistema Clara / Instituto Vital Slim</i>
</div>
</body>
</html>'''
    
    return html


def main():
    parser = argparse.ArgumentParser(
        description='Gerar ficha de balanço de estoque de injetáveis em PDF com logomarca da clínica'
    )
    parser.add_argument(
        '--estoque',
        default=os.path.expanduser('~/.openclaw/workspace/memory/tactical/estoque-injetaveis-clinica-2026-04-02.md'),
        help='Caminho do arquivo de estoque (padrão: estoque-injetaveis-clinica-2026-04-02.md)'
    )
    parser.add_argument(
        '--logo',
        default=os.path.expanduser('~/.openclaw/workspace/memory/tactical/logo-vital-slim.png'),
        help='Caminho da logomarca (padrão: logo-vital-slim.png)'
    )
    parser.add_argument(
        '--output',
        default=None,
        help='Caminho de saída do PDF (padrão: balanco-estoque-fisico-YYYY-MM-DD.pdf)'
    )
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.estoque):
        print(f"❌ Erro: Arquivo de estoque não encontrado: {args.estoque}", file=sys.stderr)
        sys.exit(1)
    
    # Generate default output path if not specified
    if not args.output:
        date_str = datetime.now().strftime('%Y-%m-%d')
        args.output = os.path.expanduser(
            f'~/.openclaw/workspace/memory/tactical/balanco-estoque-fisico-{date_str}.pdf'
        )
    
    # Parse stock file
    print(f"📖 Lendo estoque: {args.estoque}")
    items, critical_items, tirzepatida_info = parse_estoque(args.estoque)
    print(f"📦 {len(items)} itens encontrados")
    print(f"⚠️  {len(critical_items)} itens críticos")
    
    # Generate HTML
    date_str = datetime.now().strftime('%d/%m/%Y')
    html_content = generate_html(items, args.logo, date_str)
    
    # Save HTML temporarily
    html_path = args.output.replace('.pdf', '.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Generate PDF
    print(f"📄 Gerando PDF: {args.output}")
    HTML(string=html_content).write_pdf(args.output)
    
    # Clean up temp HTML
    os.remove(html_path)
    
    print(f"✅ Ficha gerada com sucesso!")
    print(f"   📁 {args.output}")
    
    return args.output


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)
