#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

FILES = [
    "bridge.py",
    ".env.example",
    "system_prompt.md",
    "control.py",
    "control_state.json",
    "lead_state.json",
    "deployment_checklist.md",
]


def load_brief(path: str | None) -> dict:
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("Briefing JSON precisa ser um objeto.")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a new Z-API/OpenClaw bridge starter set.")
    parser.add_argument("name", help="Bridge name")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument("--brief", help="Path to JSON briefing file")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent / "references" / "starter-files"
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    brief = load_brief(args.brief)

    replacements = {
        "{{BRIDGE_NAME}}": brief.get("BRIDGE_NAME", args.name),
        "{{AGENT_NAME}}": brief.get("AGENT_NAME", "Clara"),
        "{{AGENT_ROLE}}": brief.get("AGENT_ROLE", "uma concierge comercial"),
        "{{AGENT_GOAL}}": brief.get("AGENT_GOAL", "Responder leads com elegância e conduzir ao próximo passo ideal."),
        "{{SYSTEM_PROMPT_FILE}}": brief.get("SYSTEM_PROMPT_FILE", "./system_prompt.md"),
        "{{CONTROL_FILE}}": brief.get("CONTROL_FILE", "./control_state.json"),
        "{{LEADS_FILE}}": brief.get("LEADS_FILE", "./lead_state.json"),
        "{{ACTIVATION_PHRASE}}": brief.get("ACTIVATION_PHRASE", "Gostaria de saber mais informações"),
        "{{ZAPI_BASE_URL}}": brief.get("ZAPI_BASE_URL", ""),
        "{{ZAPI_INSTANCE_ID}}": brief.get("ZAPI_INSTANCE_ID", ""),
        "{{ZAPI_TOKEN}}": brief.get("ZAPI_TOKEN", ""),
        "{{ZAPI_CLIENT_TOKEN}}": brief.get("ZAPI_CLIENT_TOKEN", ""),
        "{{ZAPI_WEBHOOK_TOKEN}}": brief.get("ZAPI_WEBHOOK_TOKEN", ""),
        "{{OPENCLAW_GATEWAY_URL}}": brief.get("OPENCLAW_GATEWAY_URL", ""),
        "{{OPENCLAW_GATEWAY_TOKEN}}": brief.get("OPENCLAW_GATEWAY_TOKEN", ""),
        "{{OPENCLAW_SESSION_PREFIX}}": brief.get("OPENCLAW_SESSION_PREFIX", "clara"),
        "{{RULE_1}}": brief.get("RULE_1", "Responder com clareza e naturalidade"),
        "{{RULE_2}}": brief.get("RULE_2", "Respeitar os filtros operacionais"),
        "{{RULE_3}}": brief.get("RULE_3", "Conduzir para o próximo passo com elegância"),
    }

    for key, value in brief.items():
        replacements[f"{{{{{key}}}}}"] = str(value)

    for filename in FILES:
        text = (base / filename).read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        target = out / filename
        target.write_text(text, encoding="utf-8")

    print(f"Bridge starter criado em: {out}")
    for filename in FILES:
        print(f"- {filename}")
    print("Revise os placeholders restantes e complete a lógica antes de usar em produção.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
