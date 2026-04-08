#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TEMPLATES = [
    "concierge_system_prompt.md",
    "concierge_brain.md",
    "concierge_learning_log.md",
    "WhatsApp.md",
    "concierge_qa_scenarios.md",
    "concierge_qa_report.md",
    "concierge_preproduction_plan.md",
]


def load_brief(path: str | None) -> dict:
    if not path:
        return {}
    brief_path = Path(path).resolve()
    data = json.loads(brief_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("Briefing JSON precisa ser um objeto.")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new concierge starter set from the concierge-creator skill templates.")
    parser.add_argument("name", help="Concierge name")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument("--role", default="concierge comercial", help="Role description")
    parser.add_argument("--goal", default="converter leads qualificados no próximo passo ideal", help="Primary goal")
    parser.add_argument("--target-action", default="agendamento", help="Target action")
    parser.add_argument("--brief", help="Path to a JSON briefing file with placeholder values")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    template_dir = script_dir.parent / "references" / "starter-files"
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    brief = load_brief(args.brief)

    replacements = {
        "{{CONCIERGE_NAME}}": brief.get("CONCIERGE_NAME", args.name),
        "{{ROLE_DESCRIPTION}}": brief.get("ROLE_DESCRIPTION", args.role),
        "{{PRIMARY_GOAL}}": brief.get("PRIMARY_GOAL", args.goal),
        "{{TARGET_ACTION}}": brief.get("TARGET_ACTION", args.target_action),
    }

    for key, value in brief.items():
        replacements[f"{{{{{key}}}}}"] = str(value)

    for filename in TEMPLATES:
        src = template_dir / filename
        dst = out_dir / filename
        text = src.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        dst.write_text(text, encoding="utf-8")

    print(f"Starter criado em: {out_dir}")
    for filename in TEMPLATES:
        print(f"- {filename}")
    print("Preencha os placeholders restantes antes de usar em produção.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
