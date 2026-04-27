#!/usr/bin/env python3
import json
import os
import re
import sys
import time
import subprocess
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

# OpenRouter direct path (primary for Kimi K2.6 etc, bypasses OpenClaw catalog)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "").strip()
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions").strip()
OPENROUTER_HISTORY_TURNS = int(os.getenv("OPENROUTER_HISTORY_TURNS", "12"))
OPENROUTER_REFERRER = os.getenv("OPENROUTER_REFERRER", "https://institutovitalslim.com.br")
OPENROUTER_TITLE = os.getenv("OPENROUTER_TITLE", "Clara - Instituto Vital Slim")

OPENROUTER_HISTORY: "OrderedDict[str, list]" = OrderedDict()
OPENROUTER_HISTORY_MAX_PHONES = int(os.getenv("OPENROUTER_HISTORY_MAX_PHONES", "500"))
APPS_SCRIPT_FANOUT_URL = os.getenv("APPS_SCRIPT_FANOUT_URL", "")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID", "")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN", "")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN", "")
ZAPI_BASE_URL = os.getenv("ZAPI_BASE_URL", "").strip() or (
    f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}" if ZAPI_INSTANCE_ID and ZAPI_TOKEN else ""
)
ZAPI_SEND_TEXT_PATH = os.getenv("ZAPI_SEND_TEXT_PATH", "/send-text")
ZAPI_SEND_AUDIO_PATH = os.getenv("ZAPI_SEND_AUDIO_PATH", "/send-audio")
CLARA_NOTIFY_PHONE = os.getenv("CLARA_NOTIFY_PHONE", "5571986968887")  # Tiaro
BRIDGE_SHARED_SECRET = os.getenv("BRIDGE_SHARED_SECRET", "")
WEBHOOK_PATH_TOKEN = os.getenv("WEBHOOK_PATH_TOKEN", "")
DEDUP_TTL_SECONDS = int(os.getenv("DEDUP_TTL_SECONDS", "600"))
HTTP_TIMEOUT_SECONDS = int(os.getenv("HTTP_TIMEOUT_SECONDS", "90"))

# ElevenLabs TTS
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # Default: Rachel
ELEVENLABS_MODEL = os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2")
ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# OpenAI Whisper (for audio transcription)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")
CLARA_CONTROL_FILE = os.getenv("CLARA_CONTROL_FILE", "/root/.openclaw/workspace/ops/zapi_bridge/clara_control_state.json")
CLARA_SYSTEM_PROMPT_FILE = os.getenv("CLARA_SYSTEM_PROMPT_FILE", "/root/.openclaw/workspace/ops/zapi_bridge/clara_system_prompt.md")
CLARA_LEADS_FILE = os.getenv("CLARA_LEADS_FILE", "/root/.openclaw/workspace/ops/zapi_bridge/clara_leads_state.json")
CLARA_MANUAL_INBOX_FILE = os.getenv("CLARA_MANUAL_INBOX_FILE", "/root/.openclaw/workspace/ops/zapi_bridge/clara_manual_inbox.json")
CLARA_EXCLUSIONS_FILE = os.getenv("CLARA_EXCLUSIONS_FILE", "/root/.openclaw/workspace/ops/zapi_bridge/clara_exclusions.json")
ACTIVATION_PHRASE = os.getenv("CLARA_ACTIVATION_PHRASE", "Gostaria de saber mais informações sobre o Instituto Vital Slim")
CONFIRMATION_REPLY_SCRIPT = os.getenv("CONFIRMATION_REPLY_SCRIPT", "/root/cerebro-vital-slim/ops/quarkclinic_confirmations/process_reply.py")

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


def phone_variants(value: Optional[str]) -> list[str]:
    digits = normalize_phone(value)
    if not digits:
        return []
    variants = {digits}
    if digits.startswith("55") and len(digits) >= 12:
        ddi = digits[:2]
        ddd = digits[2:4]
        rest = digits[4:]
        if len(rest) == 9 and rest.startswith("9"):
            variants.add(ddi + ddd + rest[1:])
        elif len(rest) == 8:
            variants.add(ddi + ddd + "9" + rest)
    return sorted(variants)


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
    try:
        from urllib.request import Request as _Req, urlopen as _urlopen
        for variant in phone_variants(phone):
            digits = variant
            if digits.startswith("55") and len(digits) > 11:
                digits = digits[2:]
            url = f"{QUARKCLINIC_BASE_URL}/v1/pacientes?telefone={digits}&limite=1"
            req = _Req(url, headers={"Auth-token": QUARKCLINIC_AUTH_TOKEN})
            with _urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode())
                patients = data.get("response", {}).get("response", []) if isinstance(data.get("response"), dict) else data.get("response", [])
                if patients:
                    return True
        return False
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


def load_exclusions_state() -> Dict[str, Any]:
    path = Path(CLARA_EXCLUSIONS_FILE)
    if not path.exists():
        return {"phones": {}, "updated_at": None}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"phones": {}, "updated_at": None}
        phones = data.get("phones")
        if not isinstance(phones, dict):
            data["phones"] = {}
        return data
    except Exception as err:
        log(f"exclusions state read failed: {err}")
        return {"phones": {}, "updated_at": None}


def get_exclusion_reason(phone: str) -> Optional[str]:
    state = load_exclusions_state()
    entry = (state.get("phones") or {}).get(phone)
    if not isinstance(entry, dict):
        return None
    reason = entry.get("reason") or "excluded_phone"
    return str(reason)


def is_bridge_known_patient(phone: str) -> bool:
    state = load_exclusions_state()
    entry = (state.get("phones") or {}).get(phone)
    if not isinstance(entry, dict):
        return False
    reason = str(entry.get("reason") or "")
    source = str(entry.get("source") or "")
    return reason.startswith("patient") or source == "bridge_contexto_paciente"


def run_preflight(mode: str) -> Tuple[bool, str]:
    script = "/root/.openclaw/workspace/ops/preflight/preflight_check.py"
    if not Path(script).exists():
        return False, "missing_preflight_script"
    try:
        proc = subprocess.run([script, mode], capture_output=True, text=True, timeout=20)
        if proc.returncode == 0:
            return True, proc.stdout.strip()[:300]
        return False, (proc.stdout or proc.stderr or "preflight_failed").strip()[:300]
    except Exception as err:
        return False, f"preflight_exception:{err}"


def should_pause_clara(phone: str) -> Tuple[bool, Optional[str]]:
    ok, detail = run_preflight("bridge-followup")
    if not ok:
        return True, f"preflight:{detail}"
    reason = get_exclusion_reason(phone)
    if reason:
        return True, f"exclusion:{reason}"
    state = load_control_state()
    if state.get("paused") is True:
        return True, "global_pause"
    return is_manual_override_active(phone)


def load_manual_inbox() -> Dict[str, Any]:
    path = Path(CLARA_MANUAL_INBOX_FILE)
    if not path.exists():
        return {"messages": [], "updated_at": None}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"messages": [], "updated_at": None}
        messages = data.get("messages")
        if not isinstance(messages, list):
            messages = []
        return {"messages": messages, "updated_at": data.get("updated_at")}
    except Exception as err:
        log(f"manual inbox read failed: {err}")
        return {"messages": [], "updated_at": None}


def save_manual_inbox(state: Dict[str, Any]) -> None:
    state["updated_at"] = int(time.time())
    path = Path(CLARA_MANUAL_INBOX_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def record_manual_inbound(phone: str, text: str, message_id: str, sender_name: Optional[str] = None) -> None:
    state = load_manual_inbox()
    messages = state.setdefault("messages", [])
    messages.append({
        "phone": phone,
        "sender_name": sender_name,
        "text": text,
        "message_id": message_id,
        "received_at": int(time.time()),
    })
    state["messages"] = messages[-500:]
    save_manual_inbox(state)


def load_leads_state() -> Dict[str, Any]:
    path = Path(CLARA_LEADS_FILE)
    if not path.exists():
        return {"leads": {}, "updated_at": None}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"leads": {}, "updated_at": None}
        leads = data.get("leads")
        if not isinstance(leads, dict):
            leads = {}
        return {"leads": leads, "updated_at": data.get("updated_at")}
    except Exception as err:
        log(f"leads state read failed: {err}")
        return {"leads": {}, "updated_at": None}


def save_leads_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = int(time.time())
    path = Path(CLARA_LEADS_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def has_activation_phrase(text: str) -> bool:
    return ACTIVATION_PHRASE.strip().lower() in text.strip().lower()


def is_known_lead(phone: str) -> bool:
    state = load_leads_state()
    return phone in (state.get("leads") or {})


def mark_lead_active(phone: str, source: str) -> None:
    state = load_leads_state()
    leads = state.setdefault("leads", {})
    entry = leads.get(phone) if isinstance(leads.get(phone), dict) else {}
    entry.update({"active": True, "source": source, "updated_at": int(time.time())})
    leads[phone] = entry
    save_leads_state(state)


def should_respond_to_lead(phone: str, text: str) -> Tuple[bool, str]:
    if has_activation_phrase(text):
        mark_lead_active(phone, "activation_phrase")
        return True, "activation_phrase"
    if is_known_lead(phone):
        mark_lead_active(phone, "existing_lead")
        return True, "existing_lead"
    mark_lead_active(phone, "new_contact")
    return True, "new_contact"


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


# Regex triggers for loading deep knowledge module.
# If the current user message OR any past message in the phone's history matches,
# append clara_knowledge_deep.md to the system prompt.
DEEP_TRIGGERS_RX = re.compile(
    r"\b("
    r"valor|pre[cç]o|custa|investimento|quanto|orçamento|orcamento|parcel|cart[aã]o|cashback|desconto"
    r"|caro|salgado|cabe no bolso"
    r"|vou pensar|vou conversar|te aviso|depois eu|depois te|por enquanto|agora n[aã]o|mais pra frente|pensando"
    r"|conv[eê]nio|plano|reembolso|bradesco|amil|sulam[eé]rica|unimed|notredame|hapvida"
    r"|j[aá] tentei|j[aá] fiz|outro m[eé]dico|outra cl[ií]nica|nutricionista|academia|dieta"
    r"|compuls[aã]o|ansiedade|sanfona|efeito sanfona"
    r"|menopausa|libido|queda de cabelo|tpm|insônia|insonia|hormonal"
    r"|minha filha|meu filho|minha m[aã]e|meu marido|minha esposa|meu pai"
    r"|mounjaro|ozempic|tirzepatida|semaglutida"
    r"|agendar|marcar|hor[aá]rio|disponibilidade"
    r")\b",
    re.I,
)


def _context_needs_deep(phone: Optional[str], current_text: str) -> bool:
    """Decide if the conversation context warrants loading the deep-knowledge module."""
    # Rule 1: if the current message hits any trigger, load deep
    if DEEP_TRIGGERS_RX.search(current_text or ""):
        return True
    # Rule 2: if the phone has 3+ inbound messages in its history, load deep (high engagement)
    if phone and phone in OPENROUTER_HISTORY:
        history = OPENROUTER_HISTORY[phone]
        inbound_count = sum(1 for msg in history if msg.get("role") == "user")
        if inbound_count >= 3:
            return True
    return False


def load_clara_prompt(phone: Optional[str] = None, current_text: str = "") -> str:
    """Load the Clara system prompt with modular deep-knowledge loading.

    - Always loads the base prompt (CLARA_SYSTEM_PROMPT_FILE)
    - Always appends the rolling learnings buffer (if present)
    - Conditionally appends clara_knowledge_deep.md if the context triggers it
    """
    path = Path(CLARA_SYSTEM_PROMPT_FILE)
    try:
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            raise RuntimeError("empty prompt file")
    except Exception as err:
        raise RuntimeError(f"failed to load Clara prompt from {path}: {err}") from err

    # Conditionally append deep-knowledge module
    if _context_needs_deep(phone, current_text):
        deep_path = Path("/root/.openclaw/workspace/ops/zapi_bridge/clara_knowledge_deep.md")
        try:
            if deep_path.exists():
                deep = deep_path.read_text(encoding="utf-8").strip()
                if deep:
                    text = text + "\n\n---\n\n" + deep
                    log(f"deep knowledge loaded for phone={phone}")
        except Exception as err:
            log(f"deep knowledge load failed (non-fatal): {err}")

    # Always append rolling learnings
    rolling_path = Path("/root/.openclaw/workspace/ops/zapi_bridge/clara_learnings_rolling.md")
    try:
        if rolling_path.exists():
            rolling = rolling_path.read_text(encoding="utf-8").strip()
            if rolling:
                text = text + "\n\n---\n\n" + rolling
    except Exception as err:
        log(f"rolling learnings load failed (non-fatal): {err}")
    return text


def _openrouter_history_get(phone: str) -> list:
    h = OPENROUTER_HISTORY.get(phone)
    return list(h) if h else []


def _openrouter_history_push(phone: str, user_text: str, assistant_text: str) -> None:
    h = OPENROUTER_HISTORY.get(phone) or []
    h.append({"role": "user", "content": user_text})
    h.append({"role": "assistant", "content": assistant_text})
    max_msgs = OPENROUTER_HISTORY_TURNS * 2
    if len(h) > max_msgs:
        h = h[-max_msgs:]
    OPENROUTER_HISTORY[phone] = h
    OPENROUTER_HISTORY.move_to_end(phone)
    while len(OPENROUTER_HISTORY) > OPENROUTER_HISTORY_MAX_PHONES:
        OPENROUTER_HISTORY.popitem(last=False)


def call_openrouter(phone: str, text: str, instructions: str) -> str:
    """Call OpenRouter chat completions directly. Primary path.
    OpenRouter is stateless, so we maintain per-phone history here."""
    if not OPENROUTER_API_KEY or not OPENROUTER_MODEL:
        raise RuntimeError("openrouter not configured")
    messages = [{"role": "system", "content": instructions}]
    messages.extend(_openrouter_history_get(phone))
    messages.append({"role": "user", "content": text})
    payload = {"model": OPENROUTER_MODEL, "messages": messages}
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": OPENROUTER_REFERRER,
        "X-Title": OPENROUTER_TITLE,
    }
    status, body = post_json(OPENROUTER_URL, payload, headers=headers)
    if status < 200 or status >= 300:
        raise RuntimeError(f"openrouter error status={status} body={body[:400]}")
    data = json.loads(body)
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError(f"openrouter empty choices body={body[:400]}")
    msg = choices[0].get("message") or {}
    content = msg.get("content")
    if isinstance(content, list):
        content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("openrouter empty content")
    reply = content.strip()
    _openrouter_history_push(phone, text, reply)
    return reply


def _call_openclaw_gateway(phone: str, text: str, instructions: str) -> str:
    """Original OpenClaw gateway path. Fallback."""
    if not OPENCLAW_GATEWAY_TOKEN:
        raise RuntimeError("OPENCLAW_GATEWAY_TOKEN is empty")
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


def call_clara(phone: str, text: str, sender_name: Optional[str] = None) -> str:
    instructions = load_clara_prompt(phone=phone, current_text=text)
    if sender_name:
        instructions += f"\n\nNome do contato nesta conversa: {sender_name}."
    instructions += "\n\nResponda apenas com o texto da mensagem. Se nao houver resposta adequada, responda exatamente NO_REPLY."

    # Primary: OpenRouter direct (Kimi K2.6). Fallback: OpenClaw gateway.
    if OPENROUTER_API_KEY and OPENROUTER_MODEL:
        try:
            reply = call_openrouter(phone, text, instructions)
            log(f"reply_via=openrouter model={OPENROUTER_MODEL} phone={phone}")
            return reply or "NO_REPLY"
        except Exception as err:
            log(f"openrouter failed, falling back to openclaw: {err}")

    reply = _call_openclaw_gateway(phone, text, instructions)
    log(f"reply_via=openclaw model={OPENCLAW_MODEL_OVERRIDE} phone={phone}")
    return reply


ZAPI_MAX_CHUNK = int(os.getenv("ZAPI_MAX_CHUNK", "3500"))


def _split_message_for_zapi(message: str, max_len: int = None) -> list:
    """Quebra mensagens longas em chunks preservando limites naturais
    (paragrafos > frases > palavras), evitando truncamento/falhas na Z-API."""
    if max_len is None:
        max_len = ZAPI_MAX_CHUNK
    if not message:
        return [""]
    if len(message) <= max_len:
        return [message]

    chunks = []
    remaining = message
    while len(remaining) > max_len:
        window = remaining[:max_len]
        cut = -1
        for sep in ["\n\n", "\n", ". ", "! ", "? ", " "]:
            idx = window.rfind(sep)
            if idx > max_len * 0.5:
                cut = idx + len(sep)
                break
        if cut < 0:
            cut = max_len
        chunks.append(remaining[:cut].rstrip())
        remaining = remaining[cut:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


def extract_audio_url(payload: Dict[str, Any]) -> Optional[str]:
    """Extract audio URL from Z-API webhook payload."""
    candidates = [
        deep_get(payload, "audio", "audioUrl"),
        deep_get(payload, "audio", "url"),
        deep_get(payload, "message", "audioMessage", "url"),
        deep_get(payload, "message", "audio", "url"),
        deep_get(payload, "message", "mediaUrl"),
        deep_get(payload, "mediaUrl"),
        deep_get(payload, "audioUrl"),
        deep_get(payload, "url"),
    ]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    return None


def is_audio_message(payload: Dict[str, Any]) -> bool:
    """Check if payload is an audio message."""
    if extract_audio_url(payload):
        return True
    types = [
        payload.get("type"),
        deep_get(payload, "message", "type"),
        deep_get(payload, "messageType"),
    ]
    return any(str(t).lower() in ("audio", "ptt", "voice") for t in types if t)


def download_audio(url: str, timeout: int = 30) -> bytes:
    """Download audio file from URL."""
    req = Request(url, method="GET")
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def transcribe_audio(audio_bytes: bytes, filename: str = "audio.ogg") -> str:
    """Transcribe audio using OpenAI Whisper."""
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured for Whisper")
    import ssl
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: audio/ogg\r\n\r\n"
    ).encode("utf-8") + audio_bytes + f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\n{WHISPER_MODEL}\r\n--{boundary}--\r\n".encode("utf-8")
    req = Request(
        "https://api.openai.com/v1/audio/transcriptions",
        data=body,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
            return data.get("text", "").strip()
    except HTTPError as err:
        error_body = err.read().decode()
        raise RuntimeError(f"Whisper error {err.code}: {error_body[:400]}") from err


def generate_elevenlabs_tts(text: str) -> bytes:
    """Generate audio from text using ElevenLabs TTS."""
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY not configured")
    url = f"{ELEVENLABS_URL}/{ELEVENLABS_VOICE_ID}"
    payload = {
        "text": text,
        "model_id": ELEVENLABS_MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    req = Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urlopen(req, timeout=60) as resp:
            return resp.read()
    except HTTPError as err:
        error_body = err.read().decode()
        raise RuntimeError(f"ElevenLabs error {err.code}: {error_body[:400]}") from err


def send_zapi_audio(phone: str, audio_bytes: bytes) -> Tuple[int, str]:
    """Send audio message via Z-API."""
    if not ZAPI_BASE_URL:
        raise RuntimeError("ZAPI_BASE_URL is empty")
    if not ZAPI_CLIENT_TOKEN:
        raise RuntimeError("ZAPI_CLIENT_TOKEN is empty")
    headers = {"Client-Token": ZAPI_CLIENT_TOKEN}
    url = ZAPI_BASE_URL.rstrip("/") + ZAPI_SEND_AUDIO_PATH
    import base64
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    payload = {"phone": phone, "audioBase64": audio_b64}
    status, body = post_json(url, payload, headers=headers, timeout=60)
    return status, body


def send_zapi_text(phone: str, message: str) -> Tuple[int, str]:
    if not ZAPI_BASE_URL:
        raise RuntimeError("ZAPI_BASE_URL is empty")
    if not ZAPI_CLIENT_TOKEN:
        raise RuntimeError("ZAPI_CLIENT_TOKEN is empty")
    headers = {"Client-Token": ZAPI_CLIENT_TOKEN}
    url = ZAPI_BASE_URL.rstrip("/") + ZAPI_SEND_TEXT_PATH

    chunks = _split_message_for_zapi(message)
    last_status, last_body = 0, ""
    for i, chunk in enumerate(chunks):
        payload = {"phone": phone, "message": chunk}
        status, body = post_json(url, payload, headers=headers, timeout=30)
        last_status, last_body = status, body
        if status < 200 or status >= 300:
            return status, f"chunk_{i+1}_of_{len(chunks)}_failed: {body[:200]}"
        if i < len(chunks) - 1:
            time.sleep(1.2)
    return last_status, last_body


def save_control_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = int(time.time())
    path = Path(CLARA_CONTROL_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def manual_assume(phone: str, note: str = "telegram_manual") -> Dict[str, Any]:
    state = load_control_state()
    overrides = state.setdefault("manual_overrides", {})
    overrides[phone] = {"note": note, "updated_at": int(time.time())}
    save_control_state(state)
    return state


def manual_release(phone: str) -> Dict[str, Any]:
    state = load_control_state()
    overrides = state.setdefault("manual_overrides", {})
    overrides.pop(phone, None)
    save_control_state(state)
    return state


def try_process_confirmation_reply(phone: str, text: str) -> tuple[bool, str]:
    script = Path(CONFIRMATION_REPLY_SCRIPT)
    if not script.exists():
        return False, "script_missing"
    try:
        raw = subprocess.check_output(
            ["python3", str(script), phone, text],
            text=True,
            timeout=60,
        ).strip()
        if not raw:
            return False, "empty_output"
        data = json.loads(raw)
        if not data.get("matched"):
            return False, str(data.get("reason") or "not_matched")
        return True, str(data.get("decision") or "matched")
    except Exception as err:
        log(f"confirmation_reply_error phone={phone}: {err}")
        return False, f"error:{err}"


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
        audio_url = extract_audio_url(payload)
        is_audio = is_audio_message(payload)

        if not phone:
            self._send_json(200, {"ok": True, "ignored": "missing_phone"})
            return
        if not text and not is_audio:
            self._send_json(200, {"ok": True, "ignored": "non_text_or_empty"})
            return
        if not remember_message(message_id):
            self._send_json(200, {"ok": True, "ignored": "duplicate", "messageId": message_id})
            return

        # Respond immediately to avoid webhook timeout, then process async
        self._send_json(200, {"ok": True, "queued": True, "phone": phone})

        import threading
        def process_async():
            processed_text = text or ""
            # If audio message, transcribe it first
            if is_audio and audio_url:
                try:
                    log(f"transcribing audio phone={phone} url={audio_url[:100]!r}")
                    audio_bytes = download_audio(audio_url)
                    processed_text = transcribe_audio(audio_bytes)
                    log(f"transcribed phone={phone} text={processed_text[:180]!r}")
                except Exception as err:
                    log(f"transcription failed phone={phone}: {err}")
                    # Fallback: notify that we received audio but couldn't transcribe
                    try:
                        send_zapi_text(phone, "Oi! Recebi seu áudio, mas não consegui entender o conteúdo. Pode enviar por texto? Fica mais fácil para te ajudar com precisão. 😊")
                    except Exception as e:
                        log(f"failed to send fallback text phone={phone}: {e}")
                    return
            elif is_audio and not audio_url:
                log(f"audio message without url phone={phone}")
                try:
                    send_zapi_text(phone, "Oi! Recebi seu áudio, mas não consegui processá-lo. Pode enviar por texto? Fica mais fácil para te ajudar com precisão. 😊")
                except Exception as e:
                    log(f"failed to send fallback text phone={phone}: {e}")
                return

            log(f"processing phone={phone} message_id={message_id} text={processed_text[:180]!r}")
            try:
                handled_confirmation, confirmation_reason = try_process_confirmation_reply(phone, processed_text)
                if handled_confirmation:
                    log(f"confirmation_handled phone={phone} decision={confirmation_reason}")
                    return
                paused, reason = should_pause_clara(phone)
                if paused:
                    if reason and str(reason).startswith("manual_override"):
                        record_manual_inbound(phone, processed_text, message_id, sender_name=sender_name)
                        log(f"manual_inbound phone={phone} reason={reason} text={processed_text[:180]!r}")
                    else:
                        log(f"blocked phone={phone} reason={reason}")
                    return
                if is_existing_patient(phone):
                    log(f"blocked phone={phone} reason=existing_patient")
                    return
                should_reply, reason = should_respond_to_lead(phone, processed_text)
                if not should_reply:
                    log(f"blocked phone={phone} reason={reason}")
                    return
                log(f"lead_allowed phone={phone} reason={reason}")
                reply = call_clara(phone, processed_text, sender_name=sender_name)
                if reply.strip() == "NO_REPLY":
                    log(f"reply=NO_REPLY phone={phone}")
                    return
                # TOXIC MESSAGE FILTER - block responses that indicate lost context
                toxic_patterns = [
                    "não consegui recuperar",
                    "nao consegui recuperar",
                    "me reenvia",
                    "me reenviar",
                    "reenvia a última",
                    "reenvia a ultima",
                    "trecho anterior",
                    "ponto exato",
                    "execução anterior",
                    "execucao anterior",
                    "tentativa anterior",
                    "o que ficou pendente",
                    "já te enviei",
                    "já enviei",
                    "continuar dali",
                    "continuo daqui",
                    "continuo imediatamente",
                    "de forma confiável",
                ]
                reply_lower = reply.lower()
                has_toxic = any(p in reply_lower for p in toxic_patterns)
                if has_toxic:
                    log(f"BLOCKED TOXIC reply phone={phone} preview={reply[:120]!r}")
                    # Notify Tiaro on Telegram instead of sending toxic reply to lead
                    try:
                        notification = f"⚠️ Mensagem tóxica bloqueada para {phone}. Lead disse: {processed_text[:200]!r}. Clara tentou responder: {reply[:200]!r}. Por favor, atenda manualmente."
                        send_zapi_text("5571986968887", notification)
                    except Exception as e:
                        log(f"failed to notify Tiaro: {e}")
                    return

                # If original message was audio, reply with audio via ElevenLabs TTS
                if is_audio and ELEVENLABS_API_KEY:
                    try:
                        log(f"generating TTS phone={phone} reply={reply[:120]!r}")
                        audio_reply = generate_elevenlabs_tts(reply)
                        status, body = send_zapi_audio(phone, audio_reply)
                        log(f"sent audio phone={phone} zapiStatus={status} audioSize={len(audio_reply)} zapiBody={body[:200]}")
                    except Exception as err:
                        log(f"TTS failed phone={phone}: {err}, falling back to text")
                        status, body = send_zapi_text(phone, reply)
                        log(f"sent text fallback phone={phone} zapiStatus={status} replyPreview={reply[:120]!r}")
                else:
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
