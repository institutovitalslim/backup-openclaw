#!/usr/bin/env python3
from pathlib import Path
import shutil


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    root = Path("/root/.openclaw/workspace")
    memory = root / "memory"
    backup = memory / "backups" / "pre-reorg-20260323T210000Z"
    backup.mkdir(parents=True, exist_ok=True)

    for rel in ["MEMORY.md", "AGENTS.md", "AGENTS.txt", "MEMORY.txt", "SOUL.md"]:
        src = root / rel
        if src.exists():
            shutil.copy2(src, backup / src.name)

    for name in [
        "decisions.md",
        "lessons.md",
        "people.md",
        "projects.md",
        "pending.md",
        "topic-marketing.md",
        "topic-pacientes.md",
    ]:
        src = memory / name
        if src.exists():
            shutil.copy2(src, backup / src.name)

    for rel in [
        "context",
        "projects",
        "content/voice",
        "content/ideas",
        "content/drafts",
        "content/campaigns",
        "integrations",
        "playbooks",
        "research",
        "sessions",
        "tactical",
    ]:
        (memory / rel).mkdir(parents=True, exist_ok=True)

    moves = {
        "decisions.md": "context/decisions.md",
        "lessons.md": "context/lessons.md",
        "people.md": "context/people.md",
        "pending.md": "context/pending.md",
    }
    for src_name, dest_rel in moves.items():
        src = memory / src_name
        dest = memory / dest_rel
        if src.exists() and not dest.exists():
            shutil.move(str(src), str(dest))

    for path in sorted(memory.glob("*.md")):
        if path.name in {"MEMORY.md", "projects.md"}:
            continue
        if path.name.startswith("topic-"):
            continue
        if path.name in {"decisions.md", "lessons.md", "people.md", "pending.md"}:
            continue
        dest = memory / "sessions" / path.name
        if not dest.exists():
            shutil.move(str(path), str(dest))

    write(
        memory / "context" / "business-context.md",
        """# business-context.md ??? Business Context

- Instituto Vital Slim e uma clinica premium focada em emagrecimento avancado, hormonios, longevidade e performance metabolica.
- O posicionamento do negocio e sofisticado, cientifico, humanizado e orientado a resultados.
- Tiaro prioriza automacao, escala, crescimento estrategico e experiencia premium do paciente.
- A operacao mistura contexto clinico, marketing digital, IA aplicada e integracoes operacionais.
- Canais importantes hoje: Telegram, OpenClaw, Z-API/WhatsApp e rotinas com 1Password.
""",
    )

    project_files = {
        "README.md": """# Projects

- Um arquivo por projeto ativo.
- Atualize status, proximo passo, bloqueios e decisoes importantes em cada arquivo.
""",
        "melinda.md": """# Project: Melinda

## Objetivo
Assistente IA operacional multicanal para atendimento, pre-qualificacao e agendamento.

## Contexto
Projeto ativo ligado ao Instituto Vital Slim e a automacao do atendimento.

## Proximos focos
- integrar contexto de negocio
- melhorar fluxos de atendimento
- consolidar operacao com canais ativos
""",
        "openclaw-memory.md": """# Project: OpenClaw Memory

## Objetivo
Organizar a memoria do OpenClaw com estrutura curada, busca semantica e revisoes periodicas.

## Escopo atual
- contexto
- feedback loops
- revisao quinzenal
- consolidacao mensal
- prune conservador
""",
        "zapi-bridge.md": """# Project: Z-API Bridge

## Objetivo
Receber webhooks da Z-API, armazenar historico por paciente e preparar contexto para o OpenClaw.

## Arquitetura
- ingestao HTTP
- historico por paciente
- contexto em markdown
- integracao com workspace do OpenClaw
""",
    }
    for name, text in project_files.items():
        write(memory / "projects" / name, text)

    content_files = {
        "README.md": """# Content

Memoria para voz, ideias, rascunhos e campanhas.
""",
        "voice/linkedin.md": """# Voice: LinkedIn

- tom profissional, humano e direto
- evitar formalidade corporativa exagerada
- priorizar clareza, autoridade e aplicacao pratica
""",
        "voice/youtube.md": """# Voice: YouTube

- didatico e claro
- abrir loops de curiosidade sem clickbait vazio
- misturar autoridade com explicacao acessivel
""",
        "voice/whatsapp.md": """# Voice: WhatsApp

- respostas curtas e objetivas
- tom natural e util
- evitar blocos longos quando uma resposta curta resolve
""",
        "voice/instagram.md": """# Voice: Instagram

- mensagens mais curtas
- foco em clareza, impacto e conversao
- equilibrar premium com proximidade
""",
        "ideas/README.md": """# Content Ideas

Use esta pasta para bancos de ideias, pautas e ganchos.
""",
        "drafts/README.md": """# Drafts

Use esta pasta para rascunhos de posts, newsletters, scripts e mensagens longas.
""",
        "campaigns/README.md": """# Campaigns

Use esta pasta para memoria de campanhas, funis e lancamentos.
""",
    }
    for rel, text in content_files.items():
        write(memory / "content" / rel, text)

    write(
        memory / "integrations" / "telegram-map.md",
        """# telegram-map.md ??? Telegram Map

## Chats
- Grupo principal AI Vital Slim: `-1003803476669`
- Usuario direto Tiaro: `971050173`

## Topics
- Marketing: chat `-1003803476669`, thread `4`
- Pacientes: chat `-1003803476669`, thread `6`
""",
    )

    write(
        memory / "integrations" / "credentials-map.md",
        """# credentials-map.md ??? Credentials Map

- OpenAI API Key -> 1Password / OpenAI API Key
- Anthropic API Key -> 1Password / Anthropic API Key
- Telegram Bot Token -> 1Password / Telegram Bot Token
- Z-API Instance ID -> 1Password / Z-API Instance ID
- Z-API Token -> 1Password / Z-API Token
- Z-API Client Token -> 1Password / Z-API Client Token
- Perplexity API Key -> 1Password / Key Perplexity OpenClaw
- Gemini API Key -> 1Password / Gemini API Key
""",
    )
    write(
        memory / "integrations" / "zapi.md",
        """# zapi.md ??? Z-API

- Bridge em `workspace/zapi_bridge/`
- Usado para ingestao de historico e contexto de pacientes
""",
    )
    write(
        memory / "integrations" / "onepassword.md",
        """# onepassword.md ??? 1Password

- Segredos devem permanecer no 1Password
- `.env.runtime` e regenerado via service account
- Evitar manter segredos fixos em arquivos locais
""",
    )

    write(
        memory / "playbooks" / "README.md",
        """# Playbooks

Use esta pasta para SOPs, checklists e rotinas operacionais repetiveis.
""",
    )
    write(
        memory / "research" / "README.md",
        """# Research

Use esta pasta para benchmark, estudos, referencias e notas de pesquisa duravel.
""",
    )

    history_parts = ["# telegram-topics-history.md\n"]
    for name in ["topic-marketing.md", "topic-pacientes.md"]:
        src = memory / name
        if src.exists():
            history_parts.append(f"\n## Original: {name}\n\n")
            history_parts.append(src.read_text(encoding="utf-8"))
            src.unlink()
    write(memory / "integrations" / "telegram-topics-history.md", "".join(history_parts))

    legacy_projects = memory / "projects.md"
    if legacy_projects.exists():
        legacy_projects.unlink()

    write(
        memory / "MEMORY.md",
        """# MEMORY.md ??? Memory Index

## Structure
- `context/` ??? memoria relativamente estavel: decisoes, licoes, pessoas, negocio e pendencias.
- `projects/` ??? um arquivo por projeto ativo.
- `content/` ??? voz, ideias, rascunhos e campanhas.
- `integrations/` ??? mapa de canais, credenciais e integracoes.
- `playbooks/` ??? SOPs e checklists operacionais.
- `research/` ??? benchmarks, estudos e referencia duravel.
- `feedback_loops/` ??? aprendizado por feedback granular, lessons e decisions por dominio.
- `sessions/` ??? diario operacional, um arquivo por dia ou tema recente.
- `tactical/` ??? memoria temporaria e explicitamente expiravel.
- `backups/` ??? snapshots de seguranca antes de consolidacoes ou reorganizacoes.

## Core Paths
- `context/decisions.md`
- `context/lessons.md`
- `context/people.md`
- `context/business-context.md`
- `context/pending.md`
- `integrations/telegram-map.md`
- `integrations/credentials-map.md`

## Session Rule
- Inicializacao minima: `SOUL.md`, `USER.md`, `IDENTITY.md` e `memory/sessions/YYYY-MM-DD.md`.
- Em sessao principal, ler tambem `memory/MEMORY.md`.
- Use busca semantica sob demanda para o restante.

## Feedback Loops
- `feedback_loops/decisions/<domain>.md`
- `feedback_loops/lessons/<domain>.md`
- `feedback_loops/feedback/<domain>.jsonl`
- `feedback_loops/indexes/promotion_log.jsonl`
""",
    )

    root_memory = """# MEMORY.md ??? Compatibility Shim

O indice canonico de memoria agora vive em `memory/MEMORY.md`.

Em sessoes principais, leia:
- `memory/MEMORY.md`
- `memory/sessions/YYYY-MM-DD.md`
"""
    write(root / "MEMORY.md", root_memory)
    write(root / "MEMORY.txt", root_memory)

    print("migration-complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

