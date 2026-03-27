#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib import parse, request, error


DEFAULT_BASE_URL = "https://api.quark.tec.br/clinic/ext"
DEFAULT_OP_ITEM = "Dados Acesso API Quarckclinic"
DEFAULT_ENV_FILES = (
    Path("/root/.openclaw/quarkclinic.env"),
    Path.home() / ".openclaw" / "quarkclinic.env",
)
DEFAULT_OP_SERVICE_ACCOUNT_FILES = (
    Path("/root/.openclaw/.op.service-account.env"),
    Path.home() / ".openclaw" / ".op.service-account.env",
)
WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
SENSITIVE_KEYS = {
    "token",
    "auth-token",
    "auth_token",
    "x-chave-key",
    "x_chave_key",
    "x-secret-key",
    "x_secret_key",
    "hashkey",
    "hash_key",
}


def load_env_file(path: Path) -> dict:
    data = {}
    if not path.exists():
        return data
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def normalize_label(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def classify_secret(label: str, field_id: str, purpose: str) -> str | None:
    probe = " ".join(part for part in [label or "", field_id or "", purpose or ""] if part).lower()
    compact = normalize_label(probe)
    if "xsecretkey" in compact or ("secret" in compact and "key" in compact):
        return "QUARKCLINIC_X_SECRET_KEY"
    if "xchavekey" in compact or ("chave" in compact and "key" in compact):
        return "QUARKCLINIC_X_CHAVE_KEY"
    if "authtoken" in compact or ("token" in compact and "secret" not in compact and "chave" not in compact):
        return "QUARKCLINIC_AUTH_TOKEN"
    if "baseurl" in compact or compact.endswith("url") or "endpoint" in compact:
        return "QUARKCLINIC_BASE_URL"
    if "organizacaoid" in compact:
        return "QUARKCLINIC_ORGANIZACAO_ID"
    if "clinicas" in compact or "clinica" in compact:
        return "QUARKCLINIC_CLINICAS"
    return None


def parse_secure_note_blob(blob: str) -> dict:
    if not blob:
        return {}
    labels = [
        ("X-Chave-Key", "QUARKCLINIC_X_CHAVE_KEY"),
        ("X-Secret-Key", "QUARKCLINIC_X_SECRET_KEY"),
        ("Auth-token", "QUARKCLINIC_AUTH_TOKEN"),
        ("ORGANIZACAO_ID", "QUARKCLINIC_ORGANIZACAO_ID"),
        ("CLINICAS", "QUARKCLINIC_CLINICAS"),
        ("BASE_URL", "QUARKCLINIC_BASE_URL"),
    ]
    matches = []
    for raw_label, env_key in labels:
        for match in re.finditer(re.escape(raw_label), blob, flags=re.IGNORECASE):
            matches.append((match.start(), match.end(), raw_label, env_key))
    matches.sort(key=lambda item: item[0])
    parsed = {}
    for index, (_, label_end, _raw_label, env_key) in enumerate(matches):
        next_start = matches[index + 1][0] if index + 1 < len(matches) else len(blob)
        value = blob[label_end:next_start].strip(" |\t\r\n:")
        if value:
            parsed[env_key] = value
    return parsed


def load_from_op() -> tuple[dict, str | None]:
    if not os.environ.get("OP_SERVICE_ACCOUNT_TOKEN"):
        for candidate in DEFAULT_OP_SERVICE_ACCOUNT_FILES:
            token_env = load_env_file(candidate)
            if token_env.get("OP_SERVICE_ACCOUNT_TOKEN"):
                os.environ["OP_SERVICE_ACCOUNT_TOKEN"] = token_env["OP_SERVICE_ACCOUNT_TOKEN"]
                break
    item_name = os.environ.get("QUARKCLINIC_OP_ITEM", DEFAULT_OP_ITEM)
    vault = os.environ.get("QUARKCLINIC_OP_VAULT")
    cmd = ["op", "item", "get", item_name, "--format", "json"]
    if vault:
        cmd.extend(["--vault", vault])
    try:
        raw = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return {}, None
    payload = json.loads(raw)
    creds = {}
    for field in payload.get("fields", []):
        key = classify_secret(field.get("label", ""), field.get("id", ""), field.get("purpose", ""))
        value = field.get("value")
        if key and value:
            creds[key] = value
        if field.get("purpose") == "NOTES" and value:
            creds.update(parse_secure_note_blob(value))
    if payload.get("additional_information"):
        creds.update(parse_secure_note_blob(payload["additional_information"]))
    for url in payload.get("urls", []):
        if url.get("primary") and url.get("href"):
            creds.setdefault("QUARKCLINIC_BASE_URL", url["href"])
            break
    return creds, item_name


def resolve_credentials() -> tuple[dict, str]:
    creds = {}
    source = "defaults"
    file_creds = {}

    for key in (
        "QUARKCLINIC_AUTH_TOKEN",
        "QUARKCLINIC_X_CHAVE_KEY",
        "QUARKCLINIC_X_SECRET_KEY",
        "QUARKCLINIC_BASE_URL",
        "QUARKCLINIC_OP_ITEM",
        "QUARKCLINIC_OP_VAULT",
    ):
        if os.environ.get(key):
            creds[key] = os.environ[key]
            source = "environment"

    env_file = os.environ.get("QUARKCLINIC_ENV_FILE")
    search_files = [Path(env_file)] if env_file else list(DEFAULT_ENV_FILES)
    for candidate in search_files:
        file_creds = load_env_file(candidate)
        if file_creds:
            creds.setdefault("QUARKCLINIC_BASE_URL", file_creds.get("QUARKCLINIC_BASE_URL", DEFAULT_BASE_URL))
            creds.setdefault("QUARKCLINIC_OP_ITEM", file_creds.get("QUARKCLINIC_OP_ITEM", DEFAULT_OP_ITEM))
            creds.setdefault("QUARKCLINIC_OP_VAULT", file_creds.get("QUARKCLINIC_OP_VAULT", ""))
            break

    if creds.get("QUARKCLINIC_OP_ITEM"):
        os.environ.setdefault("QUARKCLINIC_OP_ITEM", creds["QUARKCLINIC_OP_ITEM"])
    if creds.get("QUARKCLINIC_OP_VAULT"):
        os.environ.setdefault("QUARKCLINIC_OP_VAULT", creds["QUARKCLINIC_OP_VAULT"])

    if not creds.get("QUARKCLINIC_AUTH_TOKEN"):
        op_creds, item_name = load_from_op()
        if op_creds:
            creds.update(op_creds)
            source = "1password:" + (item_name or DEFAULT_OP_ITEM)

    if not creds.get("QUARKCLINIC_AUTH_TOKEN"):
        for candidate in search_files:
            if file_creds:
                creds.update(file_creds)
                source = str(candidate)
                break

    creds.setdefault("QUARKCLINIC_BASE_URL", DEFAULT_BASE_URL)
    return creds, source


def build_headers(method: str, creds: dict) -> dict:
    headers = {
        "Accept": "application/json",
        "Auth-token": creds["QUARKCLINIC_AUTH_TOKEN"],
    }
    if method in WRITE_METHODS:
        headers["Content-Type"] = "application/json"
        headers["X-Chave-Key"] = creds["QUARKCLINIC_X_CHAVE_KEY"]
        headers["X-Secret-Key"] = creds["QUARKCLINIC_X_SECRET_KEY"]
    return headers


def parse_query(entries: list[str]) -> list[tuple[str, str]]:
    parsed = []
    for entry in entries:
        if "=" not in entry:
            raise SystemExit(f"Invalid query entry: {entry!r}. Expected key=value.")
        key, value = entry.split("=", 1)
        parsed.append((key, value))
    return parsed


def load_body(body_arg: str | None):
    if not body_arg:
        return None
    if body_arg.startswith("@"):
        return json.loads(Path(body_arg[1:]).read_text(encoding="utf-8"))
    return json.loads(body_arg)


def ensure_credentials(method: str, creds: dict):
    if not creds.get("QUARKCLINIC_AUTH_TOKEN"):
        raise SystemExit("Missing QUARKCLINIC_AUTH_TOKEN. Configure /root/.openclaw/quarkclinic.env or 1Password access first.")
    if method in WRITE_METHODS:
        if not creds.get("QUARKCLINIC_X_CHAVE_KEY"):
            raise SystemExit("Missing QUARKCLINIC_X_CHAVE_KEY for write operation.")
        if not creds.get("QUARKCLINIC_X_SECRET_KEY"):
            raise SystemExit("Missing QUARKCLINIC_X_SECRET_KEY for write operation.")


def request_api(method: str, path: str, query: list[tuple[str, str]], body, timeout: int):
    creds, source = resolve_credentials()
    ensure_credentials(method, creds)

    base_url = creds["QUARKCLINIC_BASE_URL"].rstrip("/")
    full_url = base_url + "/" + path.lstrip("/")
    if query:
        full_url += "?" + parse.urlencode(query, doseq=True)

    payload = None
    if body is not None:
        payload = json.dumps(body).encode("utf-8")

    req = request.Request(full_url, method=method, headers=build_headers(method, creds), data=payload)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            raw = response.read().decode("utf-8", errors="replace")
            return response.status, content_type, raw, source, full_url
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        return exc.code, exc.headers.get("Content-Type", ""), raw, source, full_url


def redact_sensitive(value):
    if isinstance(value, dict):
        sanitized = {}
        for key, inner in value.items():
            normalized = normalize_label(str(key))
            if normalized in SENSITIVE_KEYS:
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = redact_sensitive(inner)
        return sanitized
    if isinstance(value, list):
        return [redact_sensitive(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser(description="Safe Quarkclinic API client")
    parser.add_argument("method", nargs="?", help="HTTP method, ex: GET or POST")
    parser.add_argument("path", nargs="?", help="API path, ex: /v1/pacientes")
    parser.add_argument("--query", action="append", default=[], help="Query parameter in key=value format")
    parser.add_argument("--body", help="Inline JSON string or @path/to/file.json")
    parser.add_argument("--timeout", type=int, default=60, help="Request timeout in seconds")
    parser.add_argument("--check", action="store_true", help="Show credential readiness without printing secrets")
    parser.add_argument("--write-ok", action="store_true", help="Allow write methods like POST or PATCH")
    args = parser.parse_args()

    creds, source = resolve_credentials()
    if args.check:
        status = {
            "source": source,
            "has_auth_token": bool(creds.get("QUARKCLINIC_AUTH_TOKEN")),
            "has_x_chave_key": bool(creds.get("QUARKCLINIC_X_CHAVE_KEY")),
            "has_x_secret_key": bool(creds.get("QUARKCLINIC_X_SECRET_KEY")),
            "base_url": creds.get("QUARKCLINIC_BASE_URL", DEFAULT_BASE_URL),
            "op_item": os.environ.get("QUARKCLINIC_OP_ITEM", DEFAULT_OP_ITEM),
            "op_vault": os.environ.get("QUARKCLINIC_OP_VAULT"),
        }
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return

    if not args.method or not args.path:
        parser.error("method and path are required unless --check is used")

    method = args.method.upper()
    if method in WRITE_METHODS and not args.write_ok:
        raise SystemExit(f"{method} is blocked by default. Re-run with --write-ok after confirming the mutation.")

    query = parse_query(args.query)
    body = load_body(args.body)
    status, content_type, raw, source, full_url = request_api(method, args.path, query, body, args.timeout)

    envelope = {
        "status_code": status,
        "source": source,
        "url": full_url,
    }
    try:
        envelope["response"] = redact_sensitive(json.loads(raw) if raw else None)
    except json.JSONDecodeError:
        envelope["response"] = raw
    print(json.dumps(envelope, indent=2, ensure_ascii=False))
    if status >= 400:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
