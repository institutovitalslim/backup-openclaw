#!/usr/bin/env python3
"""Omie ERP API client for OpenClaw."""
import json
import os
import sys
import time
import subprocess
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = os.getenv("OMIE_BASE_URL", "https://app.omie.com.br/api/").rstrip("/")
APP_KEY = os.getenv("OMIE_APP_KEY", "")
APP_SECRET = os.getenv("OMIE_APP_SECRET", "")
ENV_FILE = os.getenv("OMIE_ENV_FILE", "/root/.openclaw/secure/omie_api.env")
OP_ITEM = "Acesso API OMIE"
OP_VAULT = "openclaw"
RATE_LIMIT_DELAY = 0.35  # ~3 req/s max

last_call = 0.0


def load_env_file():
    global APP_KEY, APP_SECRET
    if APP_KEY and APP_SECRET:
        return
    if os.path.isfile(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
        APP_KEY = os.getenv("OMIE_APP_KEY", APP_KEY)
        APP_SECRET = os.getenv("OMIE_APP_SECRET", APP_SECRET)


def load_from_1password():
    global APP_KEY, APP_SECRET
    if APP_KEY and APP_SECRET:
        return
    try:
        sa_env = "/root/.openclaw/.op.service-account.env"
        if os.path.isfile(sa_env):
            with open(sa_env) as f:
                for line in f:
                    if line.startswith("OP_SERVICE_ACCOUNT_TOKEN="):
                        os.environ["OP_SERVICE_ACCOUNT_TOKEN"] = line.split("=", 1)[1].strip()
        result = subprocess.run(
            ["op", "item", "get", OP_ITEM, "--vault", OP_VAULT, "--reveal", "--format", "json"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            item = json.loads(result.stdout)
            notes = ""
            for f in item.get("fields", []):
                if f.get("label") == "notesPlain":
                    notes = f.get("value", "")
            # Parse APP_KEY and APP_SECRET from notes
            for line in notes.split("\n"):
                line = line.strip()
                if line.startswith("APP_KEY"):
                    APP_KEY = line.split("\n")[-1].strip() if "\n" in line else ""
                elif line.startswith("APP_SECRET"):
                    APP_SECRET = line.split("\n")[-1].strip() if "\n" in line else ""
                elif line and not APP_KEY:
                    APP_KEY = line
                elif line and APP_KEY and not APP_SECRET:
                    APP_SECRET = line
    except Exception as e:
        print(f"[warn] 1Password lookup failed: {e}", file=sys.stderr)


def resolve_credentials():
    load_env_file()
    load_from_1password()
    if not APP_KEY or not APP_SECRET:
        print("ERROR: OMIE_APP_KEY and OMIE_APP_SECRET not found.", file=sys.stderr)
        print("Set them via environment, env file, or 1Password.", file=sys.stderr)
        sys.exit(1)


def throttle():
    global last_call
    elapsed = time.time() - last_call
    if elapsed < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - elapsed)
    last_call = time.time()


def api_call(endpoint: str, method: str, params: dict) -> dict:
    throttle()
    url = f"{BASE_URL}/v1/{endpoint}/"
    payload = {
        "call": method,
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [params]
    }
    data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"error": True, "status": e.code, "message": error_body}
    except URLError as e:
        return {"error": True, "message": str(e.reason)}


def check_connection():
    resolve_credentials()
    result = api_call("geral/empresas", "ListarEmpresas", {"pagina": 1, "registros_por_pagina": 1})
    if "error" in result:
        print(f"FAIL: {result}")
        return False
    empresas = result.get("empresas_cadastro", [])
    if empresas:
        emp = empresas[0]
        print(f"OK: Connected to Omie")
        print(f"  Empresa: {emp.get('razao_social', 'N/A')}")
        print(f"  CNPJ: {emp.get('cnpj', 'N/A')}")
        print(f"  Codigo: {emp.get('codigo_empresa', 'N/A')}")
        return True
    print("WARN: Connected but no empresa found")
    return True


def main():
    args = sys.argv[1:]

    if not args or args[0] == "--help":
        print("Usage:")
        print("  omie_api.py --check                              Check connection")
        print("  omie_api.py call <endpoint> <method> <params>    API call")
        print("  omie_api.py call <endpoint> <method> @file.json  API call from file")
        print("")
        print("Options:")
        print("  --write-ok    Allow write operations (Incluir/Alterar/Excluir)")
        print("")
        print("Examples:")
        print("  omie_api.py --check")
        print("  omie_api.py call financas/contapagar ListarContasPagar '{\"pagina\":1,\"registros_por_pagina\":20}'")
        print("  omie_api.py call geral/clientes ListarClientes '{\"pagina\":1,\"registros_por_pagina\":20}'")
        return

    if args[0] == "--check":
        resolve_credentials()
        ok = check_connection()
        sys.exit(0 if ok else 1)

    if args[0] == "call":
        if len(args) < 4:
            print("ERROR: call requires <endpoint> <method> <params>", file=sys.stderr)
            sys.exit(1)

        endpoint = args[1]
        method = args[2]
        params_raw = args[3]
        write_ok = "--write-ok" in args

        # Check if write operation
        write_prefixes = ("Incluir", "Alterar", "Excluir", "Upsert", "Faturar", "Gerar", "Cancelar", "Prorrogar")
        if method.startswith(write_prefixes) and not write_ok:
            print(f"ERROR: '{method}' is a write operation. Pass --write-ok to confirm.", file=sys.stderr)
            sys.exit(1)

        # Load params
        if params_raw.startswith("@"):
            filepath = params_raw[1:]
            with open(filepath) as f:
                params = json.load(f)
        else:
            params = json.loads(params_raw)

        resolve_credentials()
        result = api_call(endpoint, method, params)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Unknown command: {args[0]}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
