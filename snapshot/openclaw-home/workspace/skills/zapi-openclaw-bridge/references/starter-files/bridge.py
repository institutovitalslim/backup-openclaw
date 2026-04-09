#!/usr/bin/env python3
"""{{BRIDGE_NAME}} starter bridge."""

from pathlib import Path

SYSTEM_PROMPT_FILE = "{{SYSTEM_PROMPT_FILE}}"
CONTROL_FILE = "{{CONTROL_FILE}}"
LEADS_FILE = "{{LEADS_FILE}}"
ACTIVATION_PHRASE = "{{ACTIVATION_PHRASE}}"


def main() -> int:
    print("Starter bridge gerado. Complete a lógica de transporte, filtros e envio.")
    print(f"Prompt: {SYSTEM_PROMPT_FILE}")
    print(f"Control: {CONTROL_FILE}")
    print(f"Leads: {LEADS_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
