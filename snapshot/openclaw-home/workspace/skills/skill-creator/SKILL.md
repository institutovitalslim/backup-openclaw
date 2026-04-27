# skill-creator

**Descrição:** Criar novas skills para o OpenClaw no formato correto. Gera a estrutura de pastas, SKILL.md, scripts e dependências seguindo as convenções do projeto.

**Dependências:** Nenhuma (Python nativo)

---

## Uso

### Criar nova skill
```bash
python3 ~/.openclaw/workspace/skills/skill-creator/scripts/create_skill.py \
  --name minha-skill \
  --description "Descrição do que a skill faz" \
  --path ~/.openclaw/workspace/skills/
```

### Criar skill com script
```bash
python3 ~/.openclaw/workspace/skills/skill-creator/scripts/create_skill.py \
  --name processar-dados \
  --description "Processar e analisar dados de pacientes" \
  --script python \
  --dependencies "pandas,openpyxl"
```

---

## Estrutura gerada

```
minha-skill/
├── SKILL.md              # Documentação e instruções
├── requirements.txt      # Dependências Python
└── scripts/
    └── main.py           # Script principal
```

---

## Quando usar

- Criar automações repetitivas
- Padronizar tarefas frequentes
- Compartilhar workflows com o time
- Documentar processos operacionais

---

## Convenções

1. Nome em minúsculas com hífen
2. SKILL.md com descrição clara
3. Scripts em Python (preferencial) ou Bash
4. Dependências explícitas em requirements.txt
5. Testar antes de usar em produção
