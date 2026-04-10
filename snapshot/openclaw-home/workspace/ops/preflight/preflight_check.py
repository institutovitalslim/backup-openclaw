#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

CANON = Path('/root/cerebro-vital-slim/CONTEXT_CANON.md')
OPERATING = Path('/root/cerebro-vital-slim/OPERATING_RULES.md')
EXEC = Path('/root/cerebro-vital-slim/EXECUTION_CHECKLIST.md')
PREFLIGHT = Path('/root/cerebro-vital-slim/PREFLIGHT.md')
BRIDGE_CHECK = Path('/root/.openclaw/workspace/ops/zapi_bridge/FOLLOWUP_CHECKLIST.md')
LLM_REPORT = Path('/root/.openclaw/workspace/ops/llm-audit/latest_report_v3.json')
EXCLUSIONS = Path('/root/.openclaw/workspace/ops/zapi_bridge/clara_exclusions.json')

mode = sys.argv[1] if len(sys.argv) > 1 else 'generic'
report = {
    'mode': mode,
    'ok': True,
    'checks': []
}

def add(name, ok, detail):
    report['checks'].append({'name': name, 'ok': ok, 'detail': detail})
    if not ok:
        report['ok'] = False

for p in [CANON, OPERATING, EXEC, PREFLIGHT]:
    add(f'exists:{p.name}', p.exists(), str(p))

if mode == 'bridge-followup':
    add('exists:FOLLOWUP_CHECKLIST', BRIDGE_CHECK.exists(), str(BRIDGE_CHECK))
    add('exists:clara_exclusions', EXCLUSIONS.exists(), str(EXCLUSIONS))

if LLM_REPORT.exists():
    try:
        obj = json.loads(LLM_REPORT.read_text())
        forbidden = obj.get('summary', {}).get('forbidden', 0)
        add('llm_audit_forbidden_zero', forbidden == 0, f'forbidden={forbidden}')
    except Exception as e:
        add('llm_audit_parse', False, repr(e))
else:
    add('exists:latest_report_v3.json', False, str(LLM_REPORT))

print(json.dumps(report, ensure_ascii=False, indent=2))
if not report['ok']:
    sys.exit(2)
