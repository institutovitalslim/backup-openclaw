# security-compliance

**Descrição:** Auditoria de segurança e compliance para projetos e ambientes. Verifica vulnerabilidades em dependências, variáveis de ambiente, credenciais expostas e conformidade com LGPD/GDPR.

**Dependências:** `pip-audit`, `bandit`, `safety` (opcional)

---

## Uso

### Auditoria de dependências Python
```bash
python3 ~/.openclaw/workspace/skills/security-compliance/scripts/audit_deps.py \
  --path /caminho/do/projeto \
  --output relatorio_audit.md
```

### Scan de variáveis de ambiente
```bash
python3 ~/.openclaw/workspace/skills/security-compliance/scripts/audit_env.py \
  --path /caminho/do/projeto
```

### Verificação completa de compliance
```bash
python3 ~/.openclaw/workspace/skills/security-compliance/scripts/compliance_check.py \
  --path /caminho/do/projeto \
  --standard lgpd
```

---

## Quando usar

- Antes de deploy em produção
- Auditoria trimestral de segurança
- Verificação de credenciais expostas
- Compliance LGPD para dados de pacientes
- Análise de vulnerabilidades em dependências

---

## Padrões suportados

- **LGPD** — Lei Geral de Proteção de Dados (Brasil)
- **GDPR** — General Data Protection Regulation (UE)
- **HIPAA** — Health Insurance Portability and Accountability Act (US)
- **OWASP Top 10** — Vulnerabilidades web
