#!/usr/bin/env python3
"""
Buffer Social Media Poster - GraphQL API

Posta conteúdo nas redes sociais do Instituto Vital Slim via Buffer GraphQL API.
"""

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import List, Optional
from urllib.error import HTTPError


BUFFER_GRAPHQL_URL = "https://api.buffer.com/"


def load_api_key() -> str:
    """Carrega a API key do arquivo seguro."""
    env_file = Path("/root/.openclaw/secure/buffer.env")
    if env_file.exists():
        for line in env_file.read_text().strip().split("\n"):
            if line.startswith("BUFFER_API_KEY="):
                return line.split("=", 1)[1].strip()
    key = os.getenv("BUFFER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("BUFFER_API_KEY não configurada. Verifique /root/.openclaw/secure/buffer.env")
    return key


def graphql_request(query: str, variables: Optional[dict] = None) -> dict:
    """Faz uma requisição GraphQL à API do Buffer."""
    api_key = load_api_key()
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Buffer-Social-Poster/1.0 (Instituto Vital Slim)",
        "Accept": "application/json",
    }
    
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BUFFER_GRAPHQL_URL, data=body, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"Buffer GraphQL error {e.code}: {error_body[:500]}") from e


def get_profiles() -> List[dict]:
    """Lista todos os perfis sociais conectados ao Buffer."""
    query = """
    query {
        profiles {
            id
            service
            username
            formatted_username
        }
    }
    """
    result = graphql_request(query)
    data = result.get("data", {})
    return data.get("profiles", [])


def find_profile_ids(services: List[str]) -> List[str]:
    """Encontra os IDs dos perfis pelos nomes de serviço."""
    profiles = get_profiles()
    service_set = {s.lower().strip() for s in services}
    ids = []
    for profile in profiles:
        service = profile.get("service", "").lower()
        formatted_service = profile.get("formatted_service", "").lower()
        if service in service_set or formatted_service in service_set:
            ids.append(profile["id"])
    return ids


def create_idea(
    organization_id: str,
    title: str,
    text: str,
    profile_ids: Optional[List[str]] = None,
) -> dict:
    """Cria uma nova ideia/post no Buffer."""
    query = """
    mutation CreateIdea($input: CreateIdeaInput!) {
        createIdea(input: $input) {
            ... on Idea {
                id
                content {
                    title
                    text
                }
            }
        }
    }
    """
    
    variables = {
        "input": {
            "organizationId": organization_id,
            "content": {
                "title": title,
                "text": text,
            }
        }
    }
    
    if profile_ids:
        variables["input"]["profileIds"] = profile_ids
    
    return graphql_request(query, variables)


def get_organizations() -> List[dict]:
    """Lista as organizações disponíveis."""
    # A API requer IDs específicos e o token pode não ter permissão
    # Retornamos o ID conhecido da organização do Instituto Vital Slim
    return [{"id": "69e90408151436756ee2629a", "name": "Instituto Vital Slim"}]


def main() -> int:
    parser = argparse.ArgumentParser(description="Postar nas redes sociais via Buffer GraphQL")
    parser.add_argument("--text", help="Texto do post")
    parser.add_argument("--title", default="Post do Instituto Vital Slim", help="Título do post")
    parser.add_argument("--profiles", help="Perfis separados por vírgula (instagram,facebook,linkedin,twitter)")
    parser.add_argument("--org-id", help="ID da organização no Buffer")
    parser.add_argument("--list-profiles", action="store_true", help="Listar perfis disponíveis")
    parser.add_argument("--list-orgs", action="store_true", help="Listar organizações disponíveis")
    
    args = parser.parse_args()
    
    if args.list_orgs:
        orgs = get_organizations()
        print(json.dumps(orgs, indent=2, ensure_ascii=False))
        return 0
    
    if args.list_profiles:
        profiles = get_profiles()
        print(json.dumps(profiles, indent=2, ensure_ascii=False))
        return 0
    
    if not args.text:
        parser.error("--text é obrigatório (exceto com --list-profiles ou --list-orgs)")
    
    # Se não tiver org-id, tentar descobrir
    organization_id = args.org_id
    if not organization_id:
        orgs = get_organizations()
        if orgs:
            organization_id = orgs[0]["id"]
            print(f"Usando organização: {orgs[0].get('name')} ({organization_id})")
        else:
            print("Erro: Nenhuma organização encontrada. Forneça --org-id.", file=sys.stderr)
            return 1
    
    # Encontrar IDs dos perfis se fornecidos
    profile_ids = None
    if args.profiles:
        services = [s.strip() for s in args.profiles.split(",")]
        profile_ids = find_profile_ids(services)
        if not profile_ids:
            print(f"Aviso: Nenhum perfil encontrado para: {services}", file=sys.stderr)
            print("Perfis disponíveis:", file=sys.stderr)
            profiles = get_profiles()
            for p in profiles:
                print(f"  - {p.get('service')} ({p.get('formatted_username')}): {p['id']}", file=sys.stderr)
    
    # Criar o post
    print(f"Criando post na organização {organization_id}...")
    result = create_idea(
        organization_id=organization_id,
        title=args.title,
        text=args.text,
        profile_ids=profile_ids,
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
