#!/usr/bin/env python3
import json, re
from pathlib import Path

ROOTS = [Path('/root/.openclaw/workspace'), Path('/root/.config/systemd/user')]
IGNORE_PARTS = {
    'site-packages','node_modules','.git','venv','.venv','__pycache__','snapshot','memory','docs','dist','build'
}
ALLOWED_EXTS = {'.env','.service','.timer','.py','.json','.yaml','.yml','.sh','.conf'}
OPERATIONAL_HINTS = ('service','bridge','cron','timer','env','agent-config','workflow','skill','scripts')
PATS = [
    re.compile(r'OPENCLAW_MODEL_OVERRIDE\s*=\s*(.+)'),
    re.compile(r'x-openclaw-model[^\n]*?[:=]\s*["\']?([^"\'\n]+)'),
    re.compile(r'\bmodel_override\b[^\n]{0,80}?[:=]\s*["\']?([A-Za-z0-9_./:-]+)'),
    re.compile(r'\bmodel\b[^\n]{0,40}?[:=]\s*["\']?(anthropic/[^"\'\s]+|openai/[^"\'\s]+|openai-codex/[^"\'\s]+|google/[^"\'\s]+)')
]
PREFERRED = {'openai/gpt-5.4','openai-codex/gpt-5.4'}
WARN = {'anthropic/claude-sonnet-4-6'}

def skip(p: Path):
    return any(part in IGNORE_PARTS for part in p.parts)

findings=[]
for root in ROOTS:
    if not root.exists(): continue
    for p in root.rglob('*'):
        if not p.is_file() or skip(p):
            continue
        if p.suffix and p.suffix not in ALLOWED_EXTS:
            continue
        if not any(h in str(p).lower() for h in OPERATIONAL_HINTS):
            continue
        try:
            lines=p.read_text(encoding='utf-8', errors='ignore').splitlines()
        except Exception:
            continue
        for i,line in enumerate(lines,1):
            for pat in PATS:
                m=pat.search(line)
                if not m: continue
                model=m.groups()[-1].strip()
                sev='review'
                if model in PREFERRED: sev='ok'
                if model in WARN: sev='warn'
                findings.append({'path':str(p),'line':i,'model':model,'severity':sev,'text':line.strip()})
                break

report={
  'summary': {
    'total': len(findings),
    'warn': sum(1 for x in findings if x['severity']=='warn'),
    'review': sum(1 for x in findings if x['severity']=='review'),
    'ok': sum(1 for x in findings if x['severity']=='ok'),
  },
  'preferred_models': sorted(PREFERRED),
  'warn_models': sorted(WARN),
  'findings': findings,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
