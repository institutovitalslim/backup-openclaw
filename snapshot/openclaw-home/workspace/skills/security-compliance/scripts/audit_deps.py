#!/usr/bin/env python3
"""
Security Compliance - Dependency Auditor
Audita dependências Python em busca de vulnerabilidades conhecidas.
"""

import argparse
import sys
import os
import subprocess
import json
from datetime import datetime

def audit_dependencies(project_path, output_path=None):
    """Audita dependências do projeto usando pip-audit."""
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'project_path': project_path,
        'vulnerabilities': [],
        'warnings': [],
        'status': 'ok'
    }
    
    # Verificar se pip-audit está instalado
    try:
        subprocess.run(['pip-audit', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        results['warnings'].append("pip-audit não instalado. Instale com: pip install pip-audit")
        results['status'] = 'incomplete'
        return results
    
    # Encontrar requirements.txt
    req_file = os.path.join(project_path, 'requirements.txt')
    if not os.path.exists(req_file):
        results['warnings'].append(f"requirements.txt não encontrado em {project_path}")
        results['status'] = 'incomplete'
        return results
    
    # Rodar pip-audit
    try:
        cmd = ['pip-audit', '-r', req_file, '--format=json']
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_path)
        
        if result.returncode == 0:
            audit_data = json.loads(result.stdout)
            results['vulnerabilities'] = audit_data.get('dependencies', [])
            if results['vulnerabilities']:
                results['status'] = 'vulnerabilities_found'
        else:
            results['warnings'].append(f"pip-audit erro: {result.stderr}")
            
    except Exception as e:
        results['warnings'].append(f"Erro ao rodar audit: {e}")
    
    # Gerar relatório
    report = generate_report(results)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"✅ Relatório salvo: {output_path}")
    
    print(report)
    return results

def generate_report(results):
    """Gera relatório em Markdown."""
    
    report = f"""# Relatório de Auditoria de Dependências

**Data:** {results['timestamp']}
**Projeto:** {results['project_path']}
**Status:** {results['status']}

---

"""
    
    if results['vulnerabilities']:
        report += "## ⚠️ Vulnerabilidades Encontradas\n\n"
        for dep in results['vulnerabilities']:
            vulns = dep.get('vulns', [])
            if vulns:
                report += f"### {dep.get('name')} {dep.get('version')}\n"
                for vuln in vulns:
                    report += f"- **{vuln.get('id')}**: {vuln.get('description', 'N/A')}\n"
                report += "\n"
    else:
        report += "## ✅ Nenhuma vulnerabilidade encontrada\n\n"
    
    if results['warnings']:
        report += "## ⚡ Avisos\n\n"
        for warning in results['warnings']:
            report += f"- {warning}\n"
        report += "\n"
    
    report += """---

## Recomendações

1. Atualize pacotes vulneráveis: `pip install --upgrade <pacote>`
2. Use ambiente virtual isolado
3. Execute auditoria regularmente
4. Considere usar `pip-audit` no CI/CD

---

*Relatório gerado automaticamente por security-compliance*
"""
    
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auditar dependências Python')
    parser.add_argument('--path', '-p', default='.', help='Caminho do projeto')
    parser.add_argument('--output', '-o', help='Caminho do relatório .md')
    
    args = parser.parse_args()
    
    try:
        audit_dependencies(args.path, args.output)
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)
