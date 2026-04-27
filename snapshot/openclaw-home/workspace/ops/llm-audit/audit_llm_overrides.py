#!/usr/bin/env python3
import os, re, json
from pathlib import Path

ROOTS = [
    Path('/root/.openclaw/workspace'),
    Path('/root/.config/systemd/user'),
    Path('/root/cerebro-vital-slim'),
]
IGNORE_PARTS = {'site-packages', 'node_modules', '.git', 'venv', '.venv', '__pycache__'}
TEXT_EXTS = {'.env', '.service', '.timer', '.py', '.md', '.json', '.yaml', '.yml', '.sh', '.conf', '.txt'}
PATTERNS = [
    re.compile(r'OPENCLAW_MODEL_OVERRIDE\s*=\s*(.+)'),
    re.compile(r'x-openclaw-model[^\n]*?[:=]\s*["\']?([^"\'\n]+)'),
    re.compile(r'\b(model|model_override)\b[^\n]{0,80}?[:=]\s*["\']?([A-Za-z0-9_./:-]+)'),
]
BAD_HINTS = ['anthropic/claude-sonnet-4-6']
PREFERRED = 'openai/gpt-5.4'

def should_skip(path: Path) -> bool:
    return any(part in IGNORE_PARTS for part in path.parts)

rows=[]
for root in ROOTS:
    if not root.exists():
        continue
    for p in root.rglob('*'):
        if not p.is_file() or should_skip(p):
            continue
        if p.suffix and p.suffix not in TEXT_EXTS:
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for pat in PATTERNS:
                m = pat.search(line)
                if m:
                    model = (m.group(1) if pat.pattern.startswith('OPENCLAW') else m.groups()[-1]).strip()
                    severity = 'ok'
                    if any(h in model for h in BAD_HINTS):
                        severity = 'warn'
                    elif 'openai/gpt-5.4' in model or 'openai-codex/gpt-5.4' in model:
                        severity = 'ok'
                    elif any(x in model for x in ['anthropic/', 'google/', 'openai/','openai-codex/']):
                        severity = 'review'
                    rows.append({'path': str(p), 'line': i, 'model': model, 'severity': severity, 'text': line.strip()})

report = {
    'preferred_model': PREFERRED,
    'bad_hints': BAD_HINTS,
    'findings': rows,
    'summary': {
        'total': len(rows),
        'warn': sum(1 for r in rows if r['severity']=='warn'),
        'review': sum(1 for r in rows if r['severity']=='review'),
        'ok': sum(1 for r in rows if r['severity']=='ok'),
    }
}
print(json.dumps(report, ensure_ascii=False, indent=2))
