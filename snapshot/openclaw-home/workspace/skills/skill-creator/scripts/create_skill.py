#!/usr/bin/env python3
"""
Skill Creator
Cria novas skills para OpenClaw com estrutura padronizada.
"""

import argparse
import sys
import os

SKILL_TEMPLATE = """# {name}

**Descrição:** {description}

**Dependências:** {dependencies}

---

## Uso

### Comando principal
```bash
python3 ~/.openclaw/workspace/skills/{name}/scripts/main.py
```

---

## Quando usar

- Descreva quando usar esta skill

---

## Quando NÃO usar

- Descreva quando NÃO usar esta skill
"""

SCRIPT_TEMPLATE = """#!/usr/bin/env python3
\"\"\"
{name}
{description}
\"\"\"

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='{description}')
    # Adicione seus argumentos aqui
    args = parser.parse_args()
    
    # Sua lógica aqui
    print("Skill {name} executada com sucesso!")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Erro: {{e}}", file=sys.stderr)
        sys.exit(1)
"""

def create_skill(name, description, base_path, dependencies=None, script_type='python'):
    """Cria estrutura de nova skill."""
    
    # Validar nome
    if not name or ' ' in name:
        raise ValueError("Nome da skill deve ser em minúsculas sem espaços (use hífen)")
    
    # Criar pastas
    skill_path = os.path.join(base_path, name)
    scripts_path = os.path.join(skill_path, 'scripts')
    
    os.makedirs(scripts_path, exist_ok=True)
    
    # Criar SKILL.md
    deps_str = dependencies if dependencies else "Nenhuma"
    skill_md = SKILL_TEMPLATE.format(
        name=name,
        description=description,
        dependencies=deps_str
    )
    
    with open(os.path.join(skill_path, 'SKILL.md'), 'w') as f:
        f.write(skill_md)
    
    # Criar requirements.txt
    if dependencies:
        with open(os.path.join(skill_path, 'requirements.txt'), 'w') as f:
            for dep in dependencies.split(','):
                f.write(dep.strip() + '\n')
    
    # Criar script principal
    if script_type == 'python':
        script_content = SCRIPT_TEMPLATE.format(
            name=name,
            description=description
        )
        script_path = os.path.join(scripts_path, 'main.py')
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
    
    print(f"✅ Skill criada: {skill_path}")
    print(f"   SKILL.md: {skill_path}/SKILL.md")
    print(f"   Script: {scripts_path}/main.py")
    if dependencies:
        print(f"   Dependências: {skill_path}/requirements.txt")
    
    return skill_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Criar nova skill OpenClaw')
    parser.add_argument('--name', '-n', required=True, help='Nome da skill (minúsculas, hífen)')
    parser.add_argument('--description', '-d', required=True, help='Descrição da skill')
    parser.add_argument('--path', '-p', default='~/.openclaw/workspace/skills/', help='Caminho base')
    parser.add_argument('--dependencies', '-deps', help='Dependências (separadas por vírgula)')
    parser.add_argument('--script', '-s', default='python', choices=['python', 'bash'], help='Tipo de script')
    
    args = parser.parse_args()
    
    try:
        base_path = os.path.expanduser(args.path)
        create_skill(args.name, args.description, base_path, args.dependencies, args.script)
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)
