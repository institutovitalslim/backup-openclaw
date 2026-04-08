#!/usr/bin/env python3
import json
import os
import sys
import time
from collections import OrderedDict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, Optional, Tuple
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


BRIDGE_HOST = os.getenv("BRIDGE_HOST", "127.0.0.1")
BRIDGE_PORT = int(os.getenv("BRIDGE_PORT", "8787"))
OPENCLAW_GATEWAY_URL = os.getenv("OPENCLAW_GATEWAY_URL", "http://127.0.0.1:18789/v1/responses")

# QuarckClinic — verificação de pacientes
QUARKCLINIC_AUTH_TOKEN = os.getenv("QUARKCLINIC_AUTH_TOKEN", "")
QUARKCLINIC_BASE_URL = os.getenv("QUARKCLINIC_BASE_URL", "https://api.quark.tec.br/clinic/ext").rstrip("/")
OPENCLAW_GATEWAY_TOKEN = os.getenv("OPENCLAW_GATEWAY_TOKEN", "")
OPENCLAW_AGENT_REF = os.getenv("OPENCLAW_AGENT_REF", "openclaw/main")
OPENCLAW_MODEL_OVERRIDE = os.getenv("OPENCLAW_MODEL_OVERRIDE", "openai/gpt-5.4")
OPENCLAW_SESSION_PREFIX = os.getenv("OPENCLAW_SESSION_PREFIX", "bridge:zapi")
APPS_SCRIPT_FANOUT_URL = os.getenv("APPS_SCRIPT_FANOUT_URL", "")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID", "")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN", "")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN", "")
ZAPI_BASE_URL = os.getenv("ZAPI_BASE_URL", "").strip() or (
    f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}" if ZAPI_INSTANCE_ID and ZAPI_TOKEN else ""
)
ZAPI_SEND_TEXT_PATH = os.getenv("ZAPI_SEND_TEXT_PATH", "/send-text")
CLARA_NOTIFY_PHONE = os.getenv("CLARA_NOTIFY_PHONE", "5571986968887")  # Tiaro
BRIDGE_SHARED_SECRET = os.getenv("BRIDGE_SHARED_SECRET", "")
WEBHOOK_PATH_TOKEN = os.getenv("WEBHOOK_PATH_TOKEN", "")
DEDUP_TTL_SECONDS = int(os.getenv("DEDUP_TTL_SECONDS", "600"))
HTTP_TIMEOUT_SECONDS = int(os.getenv("HTTP_TIMEOUT_SECONDS", "90"))
CLARA_CONTROL_FILE = os.getenv("CLARA_CONTROL_FILE", "/root/.openclaw/workspace/ops/zapi_bridge/clara_control_state.json")
CLARA_SYSTEM_PROMPT_FILE = os.getenv("CLARA_SYSTEM_PROMPT_FILE", "/root/.openclaw/workspace/ops/zapi_bridge/clara_system_prompt.md")

SEEN: "OrderedDict[str, float]" = OrderedDict()


def log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print(f"[{ts}] {msg}", flush=True)


def compact_seen() -> None:
    cutoff = time.time() - DEDUP_TTL_SECONDS
    stale = [k for k, ts in SEEN.items() if ts < cutoff]
    for key in stale:
        SEEN.pop(key, None)
    while len(SEEN) > 5000:
        SEEN.popitem(last=False)


def remember_message(message_id: str) -> bool:
    compact_seen()
    if message_id in SEEN:
        return False
    SEEN[message_id] = time.time()
    return True


def first_nonempty(*values: Any) -> Optional[str]:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def deep_get(data: Any, *path: str) -> Any:
    cur = data
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def extract_text(payload: Dict[str, Any]) -> Optional[str]:
    candidates = [
        deep_get(payload, "text", "message"),
        deep_get(payload, "text"),
        deep_get(payload, "message", "text"),
        deep_get(payload, "message", "body"),
        deep_get(payload, "message", "conversation"),
        deep_get(payload, "message", "extendedTextMessage", "text"),
        deep_get(payload, "body"),
        deep_get(payload, "conversation"),
        deep_get(payload, "msg", "body"),
        deep_get(payload, "data", "text", "message"),
        deep_get(payload, "data", "message", "text"),
    ]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    return None


def normalize_phone(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    digits = "".join(ch for ch in value if ch.isdigit())
    return digits or None


def extract_phone(payload: Dict[str, Any]) -> Optional[str]:
    candidates = [
        payload.get("phone"),
        payload.get("from"),
        payload.get("fromNumber"),
        payload.get("senderPhone"),
        deep_get(payload, "sender", "phone"),
        deep_get(payload, "sender", "id"),
        deep_get(payload, "message", "from"),
        deep_get(payload, "message", "sender", "id"),
        deep_get(payload, "data", "phone"),
        deep_get(payload, "data", "from"),
    ]
    for candidate in candidates:
        phone = normalize_phone(candidate if isinstance(candidate, str) else None)
        if phone:
            return phone
    return None


def extract_message_id(payload: Dict[str, Any]) -> Optional[str]:
    candidates = [
        payload.get("messageId"),
        payload.get("id"),
        payload.get("zaapId"),
        deep_get(payload, "message", "id"),
        deep_get(payload, "messageId", "_serialized"),
        deep_get(payload, "data", "messageId"),
    ]
    return first_nonempty(*candidates)


def is_group_message(payload: Dict[str, Any]) -> bool:
    values = [
        payload.get("isGroup"),
        payload.get("groupMessage"),
        deep_get(payload, "message", "isGroup"),
        deep_get(payload, "data", "isGroup"),
    ]
    return any(value is True for value in values)


def is_from_me(payload: Dict[str, Any]) -> bool:
    values = [
        payload.get("fromMe"),
        deep_get(payload, "message", "fromMe"),
        deep_get(payload, "data", "fromMe"),
    ]
    return any(value is True for value in values)


def is_existing_patient(phone: str) -> bool:
    """Consulta QuarckClinic — retorna True se o telefone pertence a um paciente cadastrado."""
    if not QUARKCLINIC_AUTH_TOKEN:
        return False
    # Normalizar: remover DDI 55 para busca (API aceita só DDD+número)
    digits = "".join(ch for ch in phone if ch.isdigit())
    if digits.startswith("55") and len(digits) > 11:
        digits = digits[2:]  # remove DDI
    try:
        from urllib.request import Request as _Req, urlopen as _urlopen
        url = f"{QUARKCLINIC_BASE_URL}/v1/pacientes?telefone={digits}&limite=1"
        req = _Req(url, headers={"Auth-token": QUARKCLINIC_AUTH_TOKEN})
        with _urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            patients = data.get("response", {}).get("response", []) if isinstance(data.get("response"), dict) else data.get("response", [])
            return bool(patients)
    except Exception as err:
        log(f"quarkclinic check failed (allowing through): {err}")
        return False  # em caso de erro, deixa passar para não bloquear leads


def post_json(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None, timeout: int = HTTP_TIMEOUT_SECONDS) -> Tuple[int, str]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(url, data=body, headers={"Content-Type": "application/json", **(headers or {})}, method="POST")
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except HTTPError as err:
        return err.code, err.read().decode("utf-8", errors="replace")
    except URLError as err:
        raise RuntimeError(f"network error calling {url}: {err}") from err


def default_control_state() -> Dict[str, Any]:
    return {
        "paused": False,
        "manual_overrides": {},
        "updated_at": None,
    }


def load_control_state() -> Dict[str, Any]:
    path = Path(CLARA_CONTROL_FILE)
    if not path.exists():
        return default_control_state()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return default_control_state()
        state = default_control_state()
        state.update(data)
        if not isinstance(state.get("manual_overrides"), dict):
            state["manual_overrides"] = {}
        return state
    except Exception as err:
        log(f"control state read failed: {err}")
        return default_control_state()


def is_manual_override_active(phone: str) -> Tuple[bool, Optional[str]]:
    state = load_control_state()
    overrides = state.get("manual_overrides") or {}
    entry = overrides.get(phone)
    if not isinstance(entry, dict):
        return False, None
    until = entry.get("until")
    note = entry.get("note")
    now = time.time()
    if until is None:
        return True, note or "manual_override"
    try:
        if float(until) > now:
            return True, note or "manual_override_until"
    except Exception:
        return True, note or "manual_override_invalid_until"
    return False, None


def should_pause_clara(phone: str) -> Tuple[bool, Optional[str]]:
    state = load_control_state()
    if state.get("paused") is True:
        return True, "global_pause"
    return is_manual_override_active(phone)


def fanout_to_apps_script(payload: Dict[str, Any]) -> None:
    if not APPS_SCRIPT_FANOUT_URL:
        return
    try:
        status, body = post_json(APPS_SCRIPT_FANOUT_URL, payload, timeout=20)
        log(f"apps-script fanout status={status} body={body[:300]}")
    except Exception as err:
        log(f"apps-script fanout failed: {err}")


def build_session_key(phone: str) -> str:
    return f"{OPENCLAW_SESSION_PREFIX}:{phone}"


def load_clara_prompt() -> str:
    path = Path(CLARA_SYSTEM_PROMPT_FILE)
    try:
        text = path.read_text(encoding="utf-8").strip()
        if text:
            return text
        raise RuntimeError("empty prompt file")
    except Exception as err:
        raise RuntimeError(f"failed to load Clara prompt from {path}: {err}") from err


def call_clara(phone: str, text: str, sender_name: Optional[str] = None) -> str:
    if not OPENCLAW_GATEWAY_TOKEN:
        raise RuntimeError("OPENCLAW_GATEWAY_TOKEN is empty")
    instructions = load_clara_prompt()
    if sender_name:
        instructions += f"\n\nNome do contato nesta conversa: {sender_name}."
    instructions += "\n\nResponda apenas com o texto da mensagem. Se não houver resposta adequada, responda exatamente NO_REPLY."
    payload = {
        "model": OPENCLAW_AGENT_REF,
        "input": text,
        "user": f"zapi:{phone}",
        "instructions": instructions,
    }
    headers = {
        "Authorization": f"Bearer {OPENCLAW_GATEWAY_TOKEN}",
        "x-openclaw-session-key": build_session_key(phone),
        "x-openclaw-message-channel": "whatsapp",
        "x-openclaw-model": OPENCLAW_MODEL_OVERRIDE,
    }
    status, body = post_json(OPENCLAW_GATEWAY_URL, payload, headers=headers)
    if status < 200 or status >= 300:
        raise RuntimeError(f"OpenClaw gateway error status={status} body={body[:600]}")
    data = json.loads(body)
    output = data.get("output") or []
    texts = []
    for item in output:
        if not isinstance(item, dict):
            continue
        for part in item.get("content") or []:
            if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str):
                texts.append(part["text"])
    reply = "\n\n".join(part.strip() for part in texts if part and part.strip()).strip()
    return reply or "NO_REPLY"


def send_zapi_text(phone: str, message: str) -> Tuple[int, str]:
    if not ZAPI_BASE_URL:
        raise RuntimeError("ZAPI_BASE_URL is empty")
    if not ZAPI_CLIENT_TOKEN:
        raise RuntimeError("ZAPI_CLIENT_TOKEN is empty")
    payload = {"phone": phone, "message": message}
    headers = {"Client-Token": ZAPI_CLIENT_TOKEN}
    url = ZAPI_BASE_URL.rstrip("/") + ZAPI_SEND_TEXT_PATH
    return post_json(url, payload, headers=headers, timeout=30)


def allowed_webhook_paths() -> set[str]:
    base_paths = {"/webhook", "/zapi/webhook"}
    if WEBHOOK_PATH_TOKEN:
        return {f"/webhook/{WEBHOOK_PATH_TOKEN}", f"/zapi/webhook/{WEBHOOK_PATH_TOKEN}"}
    return base_paths


def extract_sender_name(payload: Dict[str, Any]) -> Optional[str]:
    return first_nonempty(
        deep_get(payload, "sender", "name"),
        deep_get(payload, "sender", "pushName"),
        deep_get(payload, "message", "senderName"),
        payload.get("senderName"),
        payload.get("pushName"),
    )


class Handler(BaseHTTPRequestHandler):
    server_version = "ZapiClaraBridge/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        log(format % args)

    def _send_json(self, code: int, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path in ("/healthz", "/health"):
            self._send_json(200, {"ok": True, "service": "zapi-clara-bridge"})
            return
        self._send_json(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        if path not in allowed_webhook_paths():
            self._send_json(404, {"ok": False, "error": "not found"})
            return
        if BRIDGE_SHARED_SECRET:
            supplied = self.headers.get("X-Bridge-Secret", "")
            if supplied != BRIDGE_SHARED_SECRET:
                self._send_json(403, {"ok": False, "error": "forbidden"})
                return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length or 0)
        try:
            payload = json.loads(raw.decode("utf-8")) if raw else {}
        except json.JSONDecodeError:
            self._send_json(400, {"ok": False, "error": "invalid json"})
            return

        fanout_to_apps_script(payload)

        if is_from_me(payload):
            self._send_json(200, {"ok": True, "ignored": "from_me"})
            return
        if is_group_message(payload):
            self._send_json(200, {"ok": True, "ignored": "group_message"})
            return

        phone = extract_phone(payload)
        text = extract_text(payload)
        sender_name = extract_sender_name(payload)
        message_id = extract_message_id(payload) or f"anon:{phone}:{hash(raw)}"

        if not phone:
            self._send_json(200, {"ok": True, "ignored": "missing_phone"})
            return
        if not text:
            self._send_json(200, {"ok": True, "ignored": "non_text_or_empty"})
            return
        if not remember_message(message_id):
            self._send_json(200, {"ok": True, "ignored": "duplicate", "messageId": message_id})
            return

        # Respond immediately to avoid webhook timeout, then process async
        self._send_json(200, {"ok": True, "queued": True, "phone": phone})

        import threading
        def process_async():
            log(f"processing phone={phone} message_id={message_id} text={text[:180]!r}")
            try:
                paused, reason = should_pause_clara(phone)
                if paused:
                    log(f"blocked phone={phone} reason={reason}")
                    return
                if is_existing_patient(phone):
                    log(f"blocked phone={phone} reason=existing_patient")
                    return
                reply = call_clara(phone, text, sender_name=sender_name)
                if reply.strip() == "NO_REPLY":
                    log(f"reply=NO_REPLY phone={phone}")
                    return
                status, body = send_zapi_text(phone, reply)
                log(f"sent phone={phone} zapiStatus={status} replyPreview={reply[:120]!r} zapiBody={body[:200]}")
            except Exception as err:
                log(f"bridge error phone={phone}: {err}")

        threading.Thread(target=process_async, daemon=True).start()


def main() -> int:
    missing = []
    if not OPENCLAW_GATEWAY_TOKEN:
        missing.append("OPENCLAW_GATEWAY_TOKEN")
    if not ZAPI_CLIENT_TOKEN:
        missing.append("ZAPI_CLIENT_TOKEN")
    if not ZAPI_BASE_URL:
        missing.append("ZAPI_BASE_URL or ZAPI_INSTANCE_ID+ZAPI_TOKEN")
    if missing:
        log("warning: missing required env vars: " + ", ".join(missing))
    server = ThreadingHTTPServer((BRIDGE_HOST, BRIDGE_PORT), Handler)
    webhook_suffix = f"/webhook/{WEBHOOK_PATH_TOKEN}" if WEBHOOK_PATH_TOKEN else "/webhook"
    log(f"listening on http://{BRIDGE_HOST}:{BRIDGE_PORT} webhook={webhook_suffix} health=/healthz")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("shutting down")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
