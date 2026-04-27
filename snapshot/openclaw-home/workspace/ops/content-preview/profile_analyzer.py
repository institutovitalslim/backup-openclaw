#!/usr/bin/env python3
"""
profile_analyzer.py — Pipeline autonomo de analise de perfil de Instagram.

Fluxo:
1. Le queue (/root/.openclaw/workspace/ops/content-preview/queue/content-queue.json)
2. Pega o proximo perfil pendente
3. Garante que o fetch dos reels ja foi feito (/tmp/reels/<user>_top.json)
4. Gera MD via Kimi K2.6 (OpenRouter direto)
5. Salva em cerebro/empresa/conteudo/
6. Gera HTML de validacao
7. git commit + push
8. Posta link no topico Marketing do Telegram
9. Marca perfil como 'awaiting_approval' na queue

Uso:
    python3 profile_analyzer.py                 # processa o proximo da fila
    python3 profile_analyzer.py --username X    # forca processar X especifico
    python3 profile_analyzer.py --list          # mostra status da queue
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path


QUEUE_FILE = Path("/root/.openclaw/workspace/ops/content-preview/queue/content-queue.json")
REELS_DIR = Path("/tmp/reels")
CEREBRO_CONTENT_DIR = Path("/root/cerebro-vital-slim/cerebro/empresa/conteudo")
FETCH_SCRIPT = Path("/root/.openclaw/workspace/skills/tweet-carrossel/scripts/fetch_top_reels.py")
MD_TO_HTML = Path("/root/.openclaw/workspace/skills/tweet-carrossel/scripts/md_to_html.py")
MD_TO_PRODUCTION_HTML = Path("/root/.openclaw/workspace/skills/tweet-carrossel/scripts/md_to_production_html.py")

OPENROUTER_KEY_FILE = Path("/root/.openclaw/secure/openrouter.env")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "moonshotai/kimi-k2.6"

TELEGRAM_BOT_TOKEN = "8602727694:AAFr7C50fHVI67sh9IWcyfv8HdwjDxRt9LU"
MARKETING_GROUP_ID = "-1003803476669"
MARKETING_TOPIC_ID = 4
HTML_BASE_URL = "https://conteudo.institutovitalslim.com.br/conteudo"


SYSTEM_PROMPT = """Você é um estrategista de conteúdo médico do Instituto Vital Slim (IVS), clínica de emagrecimento avançado e saúde hormonal da Dra. Daniely Freitas.

Sua tarefa: analisar os top 11 reels mais engajados de um perfil médico/influencer do Instagram, e adaptar 33 scripts (3 por reel) para a voz da Dra. Daniely, mantendo ética médica e alinhamento comercial com a oferta do IVS.

VOZ DA DRA. DANIELY:
- Médica, acolhedora, baseada em evidência
- Nunca promete resultado quantificado
- Traduz jargão para linguagem da paciente (mulher 30-55, profissional, mãe, cansada de tentativas)
- Empática sobre frustração
- Confiante sobre método

REGRAS ÉTICAS INVIOLÁVEIS:
1. NUNCA use crianças como sujeito ou contexto dos scripts
2. NUNCA prometa perda de peso quantificada ("você vai perder 10kg")
3. NUNCA use antes-e-depois sem consentimento clínico
4. NUNCA sugira tratamento específico (canetas, medicamentos) como garantia — só na consulta
5. SEMPRE cite base científica quando mencionar mecanismo (PubMed, NEJM, Lancet, JAMA são referências aceitas)

CTA PADRÃO: redirecionar para "comenta AVALIAÇÃO" (consulta IVS R$ 1.000 com bioimpedância + plano nutricional + cashback condicional)

FORMATO DE SAÍDA OBRIGATÓRIO (markdown):

# Análise @<username> — Fase 2.A (Top 11 Reels + 33 Scripts Adaptados)

> Engenharia reversa dos 11 reels mais engajados. Scripts adaptados para a voz da Dra. Daniely Freitas, Instituto Vital Slim.

## Perfil do criador (para contexto)
**@<username>** — <breve descrição baseada nas captions>. Estilo: <identificar padrão>. <Por que viraliza no geral>.

## Clusterização em 3 temas
- **T1 — <nome tema>** (reels X, Y, Z)
- **T2 — <nome tema>** (reels X, Y, Z)
- **T3 — <nome tema>** (reels X, Y, Z)

---

## Top 11 Reels — análise + scripts adaptados

### [#N] <shortcode> — "<title curto>" (<eng>k eng)
🔗 https://instagram.com/reel/<shortcode>/

**Por que viralizou:**
- **Hook:** <análise do hook>
- **Estrutura:** <análise da estrutura>
- **Retention driver:** <por que as pessoas assistem até o fim>

**Script adaptado 1 — "<título do script>"**
- HOOK (0-3s): "<texto do hook>"
- CORPO (3-25s): "<texto do corpo>"
- CTA (25-35s): "<texto da CTA>"
- **LEGENDA:** <legenda curta e provocativa> | **Hashtags:** #tag1 #tag2 #tag3 #dradaniely #institutovitalslim

**Script adaptado 2 — "<título>"**
- HOOK: ...
...

**Script adaptado 3 — "<título>"**
- HOOK: ...
...

---

(repetir para os 11 reels)

## Plano de publicação sugerido

### Cadência recomendada
- Reels: 3-4 por semana
- Horários: Quarta 19h, Sexta 12h, Domingo 11h (engagement público IVS)

### Sequenciamento sugerido (primeiras 4 semanas)

| Semana | Scripts publicados | Tema dominante |
|--------|-------------------|----------------|
| 1 | Scripts #N.N, #N.N, #N.N | <Tema do T1> |
| 2 | Scripts #N.N, #N.N, #N.N | <Tema do T2> |
| 3 | Scripts #N.N, #N.N, #N.N | <Tema do T3> |
| 4 | Scripts #N.N, #N.N, #N.N | Mix |

---

Status: Fase 2.A de @<username> entregue. Aguardando aprovação dos scripts.

FIM DO TEMPLATE.

REGRAS DE FORMATAÇÃO:
- Use exatamente a estrutura acima
- Scripts de 30-40 segundos (limite: HOOK 10-15 palavras, CORPO 40-60 palavras, CTA 10-20 palavras)
- Legenda: 100-180 caracteres
- Hashtags: 5-8 tags, sempre incluir #dradaniely #institutovitalslim
- Nunca use emoji dentro do HOOK (só 🚨 como alerta inicial quando fizer sentido)

SAÍDA: apenas o markdown, sem preâmbulo, sem explicação, sem cerca ```markdown```. Comece com o cabeçalho # Análise..."""


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
    print(f"[{ts}] {msg}", flush=True)


def load_queue():
    return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))


def save_queue(queue):
    queue["updated_at"] = datetime.now(timezone.utc).isoformat()
    QUEUE_FILE.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")


def next_pending(queue):
    pending = [p for p in queue["profiles"] if p["status"] == "pending"]
    pending.sort(key=lambda x: x.get("priority", 999))
    return pending[0] if pending else None


def update_profile_status(username, status, extra=None):
    queue = load_queue()
    for p in queue["profiles"]:
        if p["username"] == username:
            p["status"] = status
            if extra:
                p.update(extra)
            p["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_queue(queue)


def get_openrouter_key():
    for line in OPENROUTER_KEY_FILE.read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip()
    return os.environ.get("OPENROUTER_API_KEY", "").strip()


def ensure_reels_fetched(username):
    path = REELS_DIR / f"{username}_top.json"
    if path.exists():
        try:
            data = json.loads(path.read_text())
            if data.get("top") and len(data["top"]) >= 10:
                return data
        except Exception:
            pass
    log(f"fetching reels for @{username}...")
    result = subprocess.run(
        ["python3", str(FETCH_SCRIPT), username, "--top", "11", "--max-pages", "10", "--enrich"],
        capture_output=True, text=True, timeout=600,
    )
    if result.returncode != 0:
        raise RuntimeError(f"fetch failed: {result.stderr[:500]}")
    return json.loads(path.read_text())


def build_user_prompt(username, data):
    """Monta o prompt com os 11 reels pro Kimi."""
    top = data.get("top", [])[:11]
    blocks = []
    for i, v in enumerate(top, 1):
        cap = (v.get("caption") or "")[:1800]
        eng = v.get("like_count", 0) + 4 * v.get("comment_count", 0)
        blocks.append(
            f"### Reel {i}\n"
            f"shortcode: {v.get('code')}\n"
            f"url: https://instagram.com/reel/{v.get('code')}/\n"
            f"likes: {v.get('like_count', 0)}\n"
            f"comments: {v.get('comment_count', 0)}\n"
            f"engagement_score: {eng}\n"
            f"caption:\n{cap}\n"
        )
    return (
        f"Perfil: @{username}\n\n"
        f"Você tem acesso aos 11 reels mais engajados desse perfil abaixo. "
        f"Gere a análise COMPLETA conforme o template do system prompt. "
        f"Seja surgical, direto ao ponto, e respeite 100% as regras éticas.\n\n"
        + "\n---\n".join(blocks)
    )


def call_kimi(system, user, timeout=300):
    key = get_openrouter_key()
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.35,
        "max_tokens": 32000,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://institutovitalslim.com.br",
        "X-Title": "IVS Content Analyzer",
    }
    req = urllib.request.Request(OPENROUTER_URL, data=json.dumps(payload).encode(), headers=headers, method="POST")
    log(f"calling Kimi K2.6 (input ~{len(user)//4} tokens)...")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode())
    log(f"Kimi responded in {time.time()-t0:.1f}s")
    choice = data.get("choices", [{}])[0]
    msg = choice.get("message", {})
    content = msg.get("content", "")
    if isinstance(content, list):
        content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
    return content.strip()


def generate_htmls(md_path, base_name, title):
    """Gera HTML de validacao + HTML de producao."""
    html_val_path = md_path.with_suffix(".html")
    html_prod_path = md_path.parent / f"{base_name}-producao.html"

    subprocess.run(
        ["python3", str(MD_TO_HTML), str(md_path), str(html_val_path),
         f"{title} (validação)"],
        check=True, timeout=60,
    )
    subprocess.run(
        ["python3", str(MD_TO_PRODUCTION_HTML), str(md_path), str(html_prod_path),
         f"{title} (produção)"],
        check=True, timeout=60,
    )
    return html_val_path, html_prod_path


def git_commit_push(file_paths, commit_msg):
    cwd = "/root/cerebro-vital-slim"
    try:
        subprocess.run(["git", "-C", cwd, "add"] + [str(p) for p in file_paths],
                       check=True, capture_output=True, text=True, timeout=30)
        r = subprocess.run(["git", "-C", cwd, "commit", "-m", commit_msg],
                           capture_output=True, text=True, timeout=30)
        if r.returncode != 0 and "nothing to commit" in (r.stdout + r.stderr).lower():
            log("nothing to commit")
            return None
        subprocess.run(["git", "-C", cwd, "push", "origin", "main"],
                       check=True, capture_output=True, text=True, timeout=60)
        # Get commit hash
        h = subprocess.run(["git", "-C", cwd, "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=10)
        return h.stdout.strip()
    except Exception as e:
        log(f"git failed: {e}")
        return None


def send_telegram(text):
    payload = json.dumps({
        "chat_id": MARKETING_GROUP_ID,
        "message_thread_id": MARKETING_TOPIC_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200
    except Exception as e:
        log(f"telegram failed: {e}")
        return False


def process_profile(username):
    log(f"=== processing @{username} ===")
    update_profile_status(username, "processing", {"started_at": datetime.now(timezone.utc).isoformat()})

    try:
        # 1. Ensure reels fetched
        reels_data = ensure_reels_fetched(username)
        log(f"reels loaded: {len(reels_data.get('top', []))}")

        # 2. Generate MD via Kimi
        user_prompt = build_user_prompt(username, reels_data)
        md_content = call_kimi(SYSTEM_PROMPT, user_prompt)
        if not md_content or len(md_content) < 2000:
            raise RuntimeError(f"Kimi returned suspiciously short content: {len(md_content)} chars")

        # 3. Save MD
        today = date.today().strftime("%Y-%m-%d")
        base_name = f"analise-perfil-{username}-{today}"
        md_path = CEREBRO_CONTENT_DIR / f"{base_name}.md"
        md_path.write_text(md_content, encoding="utf-8")
        log(f"MD saved: {md_path} ({len(md_content)} chars)")

        # 4. Generate HTMLs
        title = f"@{username} — 33 scripts adaptados"
        html_val, html_prod = generate_htmls(md_path, base_name, title)
        log(f"HTMLs generated: {html_val.name} + {html_prod.name}")

        # 5. Git commit + push
        commit_hash = git_commit_push(
            [md_path, html_val, html_prod],
            f"Fase 2.A auto: analise @{username} (subagente profile_analyzer)",
        )
        log(f"commit: {commit_hash}")

        # 6. Send Telegram
        url_val = f"{HTML_BASE_URL}/{html_val.name}"
        url_prod = f"{HTML_BASE_URL}/{html_prod.name}"
        msg = (
            f"🎯 <b>Nova análise pronta</b>\n"
            f"Perfil: <b>@{username}</b>\n"
            f"Gerado pelo subagente (Kimi K2.6).\n\n"
            f"📋 <b>Validação (revisar e aprovar):</b>\n{url_val}\n\n"
            f"🎬 <b>Produção (disponível após APROVO):</b>\n{url_prod}\n\n"
            f"Aguardando seu APROVO / AJUSTAR / REJEITAR na validação para seguir para o próximo perfil da fila."
        )
        send_telegram(msg)

        # 7. Mark awaiting approval
        update_profile_status(username, "awaiting_approval", {
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "doc": base_name,
            "commit": commit_hash,
        })
        log(f"=== done @{username} ===")
        return True

    except Exception as e:
        log(f"ERROR processing @{username}: {e}")
        update_profile_status(username, "error", {
            "error": str(e)[:500],
            "error_at": datetime.now(timezone.utc).isoformat(),
        })
        send_telegram(
            f"❌ <b>Erro ao processar @{username}</b>\n"
            f"<code>{str(e)[:400]}</code>\n\n"
            f"Revisar logs ou forçar reprocessamento."
        )
        return False


def show_queue():
    queue = load_queue()
    print(f"\n=== Queue ({len(queue['profiles'])} profiles) ===\n")
    for p in sorted(queue["profiles"], key=lambda x: x.get("priority", 999)):
        status_emoji = {
            "approved": "✅", "awaiting_approval": "⏳", "pending": "⏸️",
            "processing": "🔄", "error": "❌",
        }.get(p["status"], "?")
        print(f"{status_emoji} {p['priority']:2d}. @{p['username']:<30} [{p['status']}]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--username", help="Force processing specific username")
    ap.add_argument("--list", action="store_true", help="Show queue state")
    args = ap.parse_args()

    if args.list:
        show_queue()
        return

    if args.username:
        process_profile(args.username)
        return

    # Pick next pending
    queue = load_queue()
    nxt = next_pending(queue)
    if not nxt:
        log("no pending profile, queue done or all approved/awaiting")
        return
    process_profile(nxt["username"])


if __name__ == "__main__":
    main()
