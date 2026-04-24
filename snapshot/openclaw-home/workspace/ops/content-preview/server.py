#!/usr/bin/env python3
"""Static HTTP server for IVS content delivery validation + feedback endpoint with auto-processing.

Hardened 2026-04-23 via CSO audit (gstack methodology):
  - Secrets via env only (no hardcoded fallbacks)
  - /feedback requires X-IVS-Feedback-Key header (HMAC compare)
  - Origin whitelist on POST
  - Per-IP rate limit (60 req/hour)
  - Doc name regex whitelist
  - Text sanitization (prompt-injection markers stripped)
  - Queue JSON updates with fcntl lock
  - Bind 127.0.0.1 by default (nginx in front)
  - CORS * only on GET/OPTIONS, never POST
  - log() undefined bug fixed -> print()
"""
import fcntl
import hmac
import json
import os
import re
import threading
import time
import urllib.parse
import urllib.request
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/ops/content-preview")
CONTENT_DIR = Path("/root/cerebro-vital-slim/cerebro/empresa/conteudo")
CONTENT_DIR_REAL = CONTENT_DIR.resolve()
FEEDBACK_LOG = BASE_DIR / "feedback.log"
PORT = int(os.getenv("PORT", "8088"))
HOST = os.getenv("HOST", "127.0.0.1")

# --- Secrets (all via env, no fallbacks) -------------------------------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
OPENCLAW_GATEWAY_TOKEN = os.getenv("OPENCLAW_GATEWAY_TOKEN", "")
FEEDBACK_SHARED_SECRET = os.getenv("FEEDBACK_SHARED_SECRET", "")

MARKETING_GROUP_ID = os.getenv("MARKETING_GROUP_ID", "-1003803476669")
MARKETING_TOPIC_ID = int(os.getenv("MARKETING_TOPIC_ID", "4"))
HTML_BASE_URL = os.getenv("HTML_BASE_URL", "https://conteudo.institutovitalslim.com.br/conteudo")

OPENCLAW_GATEWAY_URL = os.getenv("OPENCLAW_GATEWAY_URL", "http://127.0.0.1:18789/v1/responses")

# --- CSRF / origin allowlist -------------------------------------------------
ALLOWED_ORIGINS = {
    "https://conteudo.institutovitalslim.com.br",
}
# If explicitly set, add extra origins (e.g., during testing)
_extra = os.getenv("EXTRA_ALLOWED_ORIGINS", "").strip()
if _extra:
    for o in _extra.split(","):
        if o.strip():
            ALLOWED_ORIGINS.add(o.strip().rstrip("/"))

# --- Input whitelists --------------------------------------------------------
DOC_RX = re.compile(r"^analise-perfil-[a-z0-9._-]{1,80}\.html$", re.IGNORECASE)
ACTION_RX = re.compile(r"^(APROVO|AJUSTAR|REJEITAR)$")

# Prompt-injection markers stripped from user text before sending to agent
PI_MARKERS = re.compile(
    r"(?i)"
    r"(ignore (all|above|previous|the)?.{0,30}instruct|"
    r"system\s*:|"
    r"</?(instructions?|system|assistant)>|"
    r"prompt\s*inject|"
    r"new\s+(system\s+)?prompt|"
    r"disregard\s+(all|above|previous)|"
    r"jailbreak)"
)

# --- Rate limit --------------------------------------------------------------
RATE_WINDOW_S = 3600
RATE_MAX = int(os.getenv("FEEDBACK_RATE_MAX", "60"))
_rate_lock = threading.Lock()
_rate_bucket: dict[str, deque] = {}


def rate_limit_ok(ip: str) -> bool:
    now = time.monotonic()
    with _rate_lock:
        dq = _rate_bucket.setdefault(ip, deque())
        while dq and (now - dq[0]) > RATE_WINDOW_S:
            dq.popleft()
        if len(dq) >= RATE_MAX:
            return False
        dq.append(now)
        return True


# --- Startup sanity ----------------------------------------------------------
def _boot_check():
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not OPENCLAW_GATEWAY_TOKEN:
        missing.append("OPENCLAW_GATEWAY_TOKEN")
    if not FEEDBACK_SHARED_SECRET:
        missing.append("FEEDBACK_SHARED_SECRET")
    if missing:
        print(f"[fatal] missing env: {', '.join(missing)}", flush=True)
        raise SystemExit(2)


# --- Telegram ----------------------------------------------------------------
def send_telegram(text: str):
    try:
        payload = json.dumps({
            "chat_id": MARKETING_GROUP_ID,
            "message_thread_id": MARKETING_TOPIC_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except Exception as e:
        print(f"[warn] telegram send failed: {e}", flush=True)
        return False


AUTO_PROCESS_INSTRUCTIONS = """Você é o agente de processamento de feedback de conteúdo do Instituto Vital Slim.

Você recebeu um feedback em um documento da pasta `cerebro/empresa/conteudo/`. Sua missão é aplicar o ajuste e fazer commit, tudo autonomamente.

REGRAS DE SANIDADE (obrigatórias ANTES de qualquer edit):

1. **Validar shortcodes Instagram**: um shortcode válido tem 11 caracteres alfanuméricos (ex: DXUNlzhhD8E, DXPEEBNBtZJ). Se o feedback pedir trocar UM shortcode por outro que pareça placeholder (ex: XXXXX, 00000, AAAAAA, DXXXXXX), **NÃO APLIQUE**. Responda: "O shortcode X pareceu placeholder/inválido. Me confirma o shortcode real ou o link do Instagram do reel novo?"

2. **Validar semântica**: se o feedback for ambíguo (ex: "arruma o 5" sem dizer o que arrumar), não chute. Responda pedindo esclarecimento específico.

3. **Reels devem existir no perfil original**: antes de trocar um reel por outro, confirme que o novo shortcode aparece em  ou é verificável via API. Se não existe na lista fetchada, recuse e peça validação.

4. **Mudanças em ética de saúde**: se o feedback pedir algo que conflite com as regras éticas (criança como sujeito, promessa quantificada, antes-depois sem consentimento), recuse e explique.

5. **Mudança massiva** (>30% do doc): sempre responda pedindo confirmação dupla antes de executar.

Se a regra de sanidade disparar: NÃO edite, responda no Telegram pedindo ajuste/confirmação, e deixe o documento intacto.

PROTOCOLO OBRIGATÓRIO:

1. Leia o arquivo .md correspondente (mesmo nome do .html, com extensão .md) em `/root/cerebro-vital-slim/cerebro/empresa/conteudo/`.
2. Identifique EXATAMENTE o que precisa mudar com base no texto do feedback.
3. Edite cirurgicamente usando a ferramenta de edit. Mínimo necessário.
4. Execute o conversor para regenerar o HTML:
   `python3 /root/.openclaw/workspace/skills/tweet-carrossel/scripts/md_to_html.py <md_path> <html_path> "<titulo>"`
5. Faça `git add`, `git commit` com mensagem clara ("Feedback AJUSTAR auto: <resumo>") e `git push origin main` no repo `/root/cerebro-vital-slim/`.
6. Responda com um RESUMO ESTRUTURADO do que foi feito, em PT-BR, máximo 800 caracteres, formato Telegram HTML.

REGRAS ÉTICAS INVIOLÁVEIS (herdadas do cérebro):
- NUNCA use crianças como sujeito/contexto em scripts. IVS atende adultos.
- Sem promessa de resultado quantificado.
- Sem antes-e-depois sem consentimento clínico.
- Voz da Dra. Daniely (acolhedora, evidência, médica).

SE ACTION=APROVO:
    1. NAO edite o arquivo .md.
    2. EXECUTE o gerador de producao: python3 /root/.openclaw/workspace/skills/tweet-carrossel/scripts/md_to_production_html.py <caminho_md> <mesmo_path_trocando_.html_por_-producao.html> "<titulo>"
    3. Faca git add + commit + push no cerebro-vital-slim com mensagem "APROVO: geracao HTML producao".
    4. Responda com resumo confirmando aprovacao E incluindo o link da URL de producao https://conteudo.institutovitalslim.com.br/conteudo/<nome-do-producao-html>
SE ACTION=REJEITAR: não edite. Responda perguntando qual alternativa o Tiaro quer.
SE ACTION=AJUSTAR: execute todo o protocolo acima.

Retorne SOMENTE o resumo final para o Tiaro, sem explicar processo interno."""


# --- Queue file with fcntl lock ---------------------------------------------
def _mark_approved_in_queue(doc: str) -> None:
    from datetime import datetime, timezone
    queue_path = BASE_DIR / "queue" / "content-queue.json"
    if not queue_path.exists():
        return
    try:
        with open(queue_path, "r+", encoding="utf-8") as qf:
            fcntl.flock(qf.fileno(), fcntl.LOCK_EX)
            try:
                qf.seek(0)
                qdata = json.load(qf)
                doc_base = doc.replace(".html", "").replace("-producao", "")
                for prof in qdata.get("profiles", []):
                    if prof.get("doc") == doc_base or (
                        "analise-perfil-" + prof.get("username", "") in doc_base
                    ):
                        prof["status"] = "approved"
                        prof["approved_at"] = datetime.now(timezone.utc).isoformat()
                        break
                qdata["updated_at"] = datetime.now(timezone.utc).isoformat()
                qf.seek(0)
                qf.truncate()
                json.dump(qdata, qf, indent=2, ensure_ascii=False)
            finally:
                fcntl.flock(qf.fileno(), fcntl.LOCK_UN)
        print("[queue] marked as approved (locked update)", flush=True)
    except Exception as e:
        print(f"[queue] mark approved failed: {e}", flush=True)


def process_feedback_async(entry: dict):
    """Dispatch the feedback to the OpenClaw agent for auto-processing."""
    def worker():
        try:
            doc = entry.get("doc", "")
            action = entry.get("action", "")
            text = entry.get("text", "")
            ts = entry.get("ts", "")

            user_msg = (
                f"FEEDBACK AUTOMATICO RECEBIDO\n"
                f"Documento: {doc}\n"
                f"Ação: {action}\n"
                f"Texto do feedback:\n{text}\n\n"
                f"Aplique o protocolo."
            )

            session_key = f"feedback-autoproc-{doc}-{int(time.time())}"

            payload = {
                "model": "openclaw/main",
                "input": user_msg,
                "user": "content-validator",
                "instructions": AUTO_PROCESS_INSTRUCTIONS,
            }
            headers = {
                "Authorization": f"Bearer {OPENCLAW_GATEWAY_TOKEN}",
                "Content-Type": "application/json",
                "x-openclaw-session-key": session_key,
            }
            req = urllib.request.Request(
                OPENCLAW_GATEWAY_URL,
                data=json.dumps(payload).encode(),
                headers=headers,
                method="POST",
            )
            print(f"[autoproc] dispatching feedback: doc={doc} action={action}", flush=True)
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.loads(r.read().decode())

            texts = []
            for item in data.get("output") or []:
                for part in item.get("content") or []:
                    if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str):
                        texts.append(part["text"])
            reply = "\n".join(t.strip() for t in texts if t and t.strip()).strip()

            if action == "APROVO":
                try:
                    _mark_approved_in_queue(doc)
                    import subprocess
                    subprocess.Popen(
                        ["/usr/bin/python3", str(BASE_DIR / "profile_analyzer.py")],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True,
                    )
                    print("[queue] triggered subagent for next profile", flush=True)
                except Exception as e:
                    print(f"[queue] trigger failed: {e}", flush=True)

            if reply:
                send_telegram(f"🤖 <b>Processamento automático concluído</b>\n<b>Doc:</b> {doc}\n\n{reply[:2500]}")
                print(f"[autoproc] done: {reply[:200]}", flush=True)
            else:
                send_telegram(
                    f"⚠️ <b>Processamento automático retornou vazio</b>\n"
                    f"<b>Doc:</b> {doc}\n<b>Ação:</b> {action}\nProvavelmente falha — revise manualmente."
                )
        except Exception as e:
            err = str(e)[:400]
            print(f"[autoproc] error: {err}", flush=True)
            send_telegram(
                f"❌ <b>Falha no processamento automático</b>\n"
                f"<b>Doc:</b> {entry.get('doc','?')}\n<b>Erro:</b> {err}"
            )

    threading.Thread(target=worker, daemon=True).start()


# --- HTTP handler ------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "IVSContent/2.0"
    sys_version = ""

    def _send(self, code, body, content_type="text/html; charset=utf-8", cors_public=False):
        body_bytes = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body_bytes)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        if cors_public:
            self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body_bytes)

    def _file(self, path: Path):
        # Path traversal defense: resolve and check prefix
        try:
            real = path.resolve()
        except Exception:
            self._send(404, "<h1>404</h1>", cors_public=True)
            return
        if not str(real).startswith(str(CONTENT_DIR_REAL) + os.sep) and real != CONTENT_DIR_REAL:
            # For BASE_DIR/index.html, also allow BASE_DIR
            base_real = BASE_DIR.resolve()
            if not (str(real).startswith(str(base_real) + os.sep) or real == base_real):
                self._send(403, "forbidden", cors_public=True)
                return
        if not real.exists() or not real.is_file():
            self._send(404, f"<h1>404</h1><p>{path.name} nao encontrado</p>", cors_public=True)
            return
        data = real.read_bytes()
        # Inject feedback shared secret into validation HTML at serve time
        if real.suffix.lower() == ".html" and FEEDBACK_SHARED_SECRET:
            data = data.replace(b"__IVS_FEEDBACK_KEY__", FEEDBACK_SHARED_SECRET.encode())
        suf = real.suffix.lower()
        ct = (
            "text/html; charset=utf-8" if suf == ".html"
            else "text/markdown; charset=utf-8" if suf == ".md"
            else "application/json; charset=utf-8" if suf == ".json"
            else "text/plain; charset=utf-8"
        )
        self._send(200, data, ct, cors_public=True)

    def do_HEAD(self):
        self.do_GET()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-IVS-Feedback-Key")
        self.send_header("Access-Control-Max-Age", "600")
        self.end_headers()

    def do_GET(self):
        url = urllib.parse.unquote(self.path.split("?")[0])
        if url in ("/", "/index.html"):
            self._file(BASE_DIR / "index.html")
            return
        if url == "/api/list":
            files = []
            for f in sorted(CONTENT_DIR.glob("*.html")):
                st = f.stat()
                files.append({
                    "name": f.name,
                    "size": st.st_size,
                    "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime)),
                })
            self._send(200, json.dumps(files), "application/json; charset=utf-8", cors_public=True)
            return
        if url == "/api/feedbacks":
            feedbacks = []
            if FEEDBACK_LOG.exists():
                for line in FEEDBACK_LOG.read_text(encoding="utf-8").splitlines():
                    try:
                        feedbacks.append(json.loads(line))
                    except Exception:
                        pass
            self._send(200, json.dumps(feedbacks[-50:]), "application/json; charset=utf-8", cors_public=True)
            return
        if url.startswith("/conteudo/"):
            rel = url[len("/conteudo/"):]
            if not rel or ".." in rel or rel.startswith("/") or "\x00" in rel:
                self._send(403, "forbidden", cors_public=True)
                return
            self._file(CONTENT_DIR / rel)
            return
        self._send(404, "<h1>404</h1>", cors_public=True)

    def _client_ip(self) -> str:
        # Trust X-Forwarded-For only from 127.0.0.1 (nginx)
        if self.client_address[0] == "127.0.0.1":
            xff = self.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            if xff:
                return xff
        return self.client_address[0]

    def do_POST(self):
        if self.path != "/feedback":
            self._send(404, "not found")
            return

        ip = self._client_ip()

        # 1. Rate limit
        if not rate_limit_ok(ip):
            self._send(429, json.dumps({"ok": False, "error": "rate_limited"}), "application/json; charset=utf-8")
            return

        # 2. Origin check (CSRF defense)
        origin = (self.headers.get("Origin") or "").rstrip("/")
        if origin and origin not in ALLOWED_ORIGINS:
            print(f"[feedback] rejected origin={origin} ip={ip}", flush=True)
            self._send(403, json.dumps({"ok": False, "error": "origin_not_allowed"}), "application/json; charset=utf-8")
            return

        # 3. Shared-secret auth
        supplied = self.headers.get("X-IVS-Feedback-Key", "")
        if not supplied or not hmac.compare_digest(supplied, FEEDBACK_SHARED_SECRET):
            print(f"[feedback] rejected auth ip={ip}", flush=True)
            self._send(401, json.dumps({"ok": False, "error": "unauthorized"}), "application/json; charset=utf-8")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 10_000:
                self._send(413, json.dumps({"ok": False, "error": "payload_too_large"}), "application/json; charset=utf-8")
                return
            raw = self.rfile.read(length).decode("utf-8")
            data = json.loads(raw) if raw else {}

            # 4. Whitelist doc
            doc = str(data.get("doc", ""))[:200]
            if not DOC_RX.match(doc):
                print(f"[feedback] rejected doc={doc!r} ip={ip}", flush=True)
                self._send(400, json.dumps({"ok": False, "error": "invalid_doc"}), "application/json; charset=utf-8")
                return

            # 5. Whitelist action
            action = str(data.get("action", "")).upper()[:20]
            if not ACTION_RX.match(action):
                self._send(400, json.dumps({"ok": False, "error": "invalid_action"}), "application/json; charset=utf-8")
                return

            # 6. Sanitize text (strip prompt-injection markers, cap 2000)
            text_raw = str(data.get("text", ""))[:2000]
            text = PI_MARKERS.sub("[redacted]", text_raw)

            # 7. Timestamp is server-authoritative
            ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            entry = {"ts": ts, "doc": doc, "action": action, "text": text, "ip": ip}
            with open(FEEDBACK_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

            emoji = {"APROVO": "✅", "AJUSTAR": "🔄", "REJEITAR": "❌"}.get(action, "📋")
            notify_body = (
                f"{emoji} <b>Feedback recebido</b>\n"
                f"<b>Doc:</b> {doc}\n"
                f"<b>Ação:</b> {action}"
            )
            if text:
                notify_body += f"\n\n<b>Nota:</b>\n{text[:1500]}"
            notify_body += "\n\n⏳ Processamento automático iniciado..."
            send_telegram(notify_body)

            process_feedback_async(entry)

            self._send(200, json.dumps({"ok": True, "autoprocess": "started"}), "application/json; charset=utf-8")
        except Exception as e:
            self._send(500, json.dumps({"ok": False, "error": str(e)[:200]}), "application/json; charset=utf-8")

    def log_message(self, fmt, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {self.address_string()} {fmt%args}", flush=True)


if __name__ == "__main__":
    _boot_check()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"content-preview on http://{HOST}:{PORT}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
