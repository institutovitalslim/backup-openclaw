#!/usr/bin/env python3
import argparse
import importlib.util
import json
from datetime import datetime
from pathlib import Path
import unicodedata


SCRIPT_DIR = Path(__file__).resolve().parent
CLIENT_PATH = SCRIPT_DIR / "quarkclinic_api.py"


def load_client():
    spec = importlib.util.spec_from_file_location("quarkclinic_api", CLIENT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


client = load_client()


def parse_time(value: str):
    return datetime.strptime(value, "%H:%M")


def to_query_date(date_br: str) -> str:
    return datetime.strptime(date_br, "%d/%m/%Y").strftime("%d-%m-%Y")


def parse_interval_start(interval_text: str) -> str:
    return interval_text.split(" - ", 1)[0].strip()


def parse_interval_end(interval_text: str) -> str:
    return interval_text.split(" - ", 1)[1].strip()


def normalize_name(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_value.lower().split())


def split_name_tokens(value: str) -> list[str]:
    return [token for token in normalize_name(value).split(" ") if token]


def fetch_patient_candidates(name_query: str, max_pages: int = 3):
    tokens = split_name_tokens(name_query)
    if not tokens:
        return []

    seen_ids = set()
    matches = []
    for page in range(1, max_pages + 1):
        status, _content_type, raw, _source, _url = client.request_api(
            "GET",
            "/v1/pacientes",
            [("nome", name_query), ("page", str(page))],
            None,
            60,
        )
        if status >= 400:
            break
        payload = client.redact_sensitive(json.loads(raw) if raw else None)
        items = (payload or {}).get("response") or []
        if not items:
            break
        for item in items:
            patient_id = item.get("id")
            if patient_id in seen_ids:
                continue
            patient_name = item.get("nome", "")
            patient_tokens = split_name_tokens(patient_name)
            if all(token in patient_tokens for token in tokens):
                seen_ids.add(patient_id)
                matches.append(item)
        if len(items) < 100:
            break
    return matches


def summarize_patient(item: dict) -> dict:
    return {
        "id": item.get("id"),
        "nome": item.get("nome"),
        "cpf": item.get("cpf"),
        "dataNascimento": item.get("dataNascimento"),
        "email": item.get("email"),
        "clinicaOrigemId": item.get("clinicaOrigemId"),
    }


def fetch_free_slots(agenda_id: int, date_br: str):
    query_date = to_query_date(date_br)
    status, _content_type, raw, source, url = client.request_api(
        "GET",
        f"/v1/agendas/{agenda_id}/horarios-livres",
        [("data", query_date)],
        None,
        60,
    )
    payload = client.redact_sensitive(json.loads(raw) if raw else None)
    if status >= 400:
        return {
            "ok": False,
            "status_code": status,
            "source": source,
            "url": url,
            "response": payload,
            "slots": [],
        }

    slots = []
    for date_item in payload or []:
        for slot in date_item.get("horarios", []):
            if slot.get("status") != "LIVRE":
                continue
            interval = slot.get("intervalo")
            if not interval or " - " not in interval:
                continue
            slots.append(
                {
                    "intervalo": interval,
                    "inicio": parse_interval_start(interval),
                    "fim": parse_interval_end(interval),
                }
            )
    return {
        "ok": True,
        "status_code": status,
        "source": source,
        "url": url,
        "response": payload,
        "slots": slots,
    }


def suggest_slots(slots: list[dict], preferred_time: str, limit: int):
    preferred_dt = parse_time(preferred_time)
    ranked = []
    for slot in slots:
        start_dt = parse_time(slot["inicio"])
        end_dt = parse_time(slot["fim"])
        contains_preferred = start_dt <= preferred_dt < end_dt
        exact_match = slot["inicio"] == preferred_time
        delta_minutes = abs(int((start_dt - preferred_dt).total_seconds() // 60))
        ranked.append(
            {
                **slot,
                "exact_match": exact_match,
                "contains_preferred": contains_preferred,
                "delta_minutes": delta_minutes,
            }
        )
    ranked.sort(
        key=lambda item: (
            0 if item["exact_match"] else 1,
            0 if item["contains_preferred"] else 1,
            item["delta_minutes"],
            item["inicio"],
        )
    )
    return ranked[:limit]


def build_payload(args, slot_start: str):
    return {
        "unidadeId": args.unidade_id,
        "agendaId": args.agenda_id,
        "pacienteId": args.paciente_id,
        "convenioId": args.convenio_id,
        "especialidadeId": args.especialidade_id,
        "procedimentosIds": [args.procedimento_id],
        "data": args.data,
        "hora": slot_start,
        "telefonePaciente": args.telefone,
        "telemedicina": args.telemedicina,
    }


def post_booking(payload: dict):
    status, _content_type, raw, source, url = client.request_api(
        "POST",
        "/v1/agendamentos",
        [],
        payload,
        60,
    )
    try:
        response = client.redact_sensitive(json.loads(raw) if raw else None)
    except json.JSONDecodeError:
        response = raw
    return {
        "status_code": status,
        "source": source,
        "url": url,
        "response": response,
    }


def is_slot_conflict(result: dict) -> bool:
    if result["status_code"] < 400:
        return False
    response = result.get("response")
    if isinstance(response, dict):
        detail = str(response.get("errorDetail", "")).lower()
        return "hor" in detail and "dispon" in detail
    return False


def main():
    parser = argparse.ArgumentParser(description="Quarkclinic assisted booking helper")
    parser.add_argument("--agenda-id", type=int, required=True)
    parser.add_argument("--unidade-id", type=int, required=True)
    parser.add_argument("--paciente-id", type=int, required=True)
    parser.add_argument("--convenio-id", type=int, required=True)
    parser.add_argument("--especialidade-id", type=int, required=True)
    parser.add_argument("--procedimento-id", type=int, required=True)
    parser.add_argument("--telefone", required=True)
    parser.add_argument("--data", required=True, help="dd/MM/yyyy")
    parser.add_argument("--hora-preferida", required=True, help="HH:mm")
    parser.add_argument("--telemedicina", action="store_true")
    parser.add_argument("--suggestions", type=int, default=5)
    parser.add_argument("--book", action="store_true", help="Attempt booking after checking availability")
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--paciente-nome", help="Nome completo para conferência de homônimos antes do agendamento")
    parser.add_argument("--confirm-paciente-id", type=int, help="ID confirmado quando houver mais de um paciente compatível")
    args = parser.parse_args()

    if args.paciente_nome:
        candidates = fetch_patient_candidates(args.paciente_nome)
        summarized = [summarize_patient(item) for item in candidates]
        if not candidates:
            print(
                json.dumps(
                    {
                        "patient_lookup": {
                            "query": args.paciente_nome,
                            "match_count": 0,
                            "matches": [],
                            "confirmed": False,
                        }
                    },
                    indent=2,
                    ensure_ascii=False,
                )
            )
            raise SystemExit(1)
        if len(candidates) > 1 and args.confirm_paciente_id is None:
            print(
                json.dumps(
                    {
                        "patient_lookup": {
                            "query": args.paciente_nome,
                            "match_count": len(candidates),
                            "matches": summarized,
                            "confirmed": False,
                            "message": "Mais de um paciente compatível encontrado. Confirme pelo sobrenome e informe --confirm-paciente-id.",
                        }
                    },
                    indent=2,
                    ensure_ascii=False,
                )
            )
            raise SystemExit(2)
        if args.confirm_paciente_id is not None:
            if not any(item.get("id") == args.confirm_paciente_id for item in candidates):
                print(
                    json.dumps(
                        {
                            "patient_lookup": {
                                "query": args.paciente_nome,
                                "match_count": len(candidates),
                                "matches": summarized,
                                "confirmed": False,
                                "message": "O paciente confirmado não está entre os compatíveis encontrados para esse nome.",
                            }
                        },
                        indent=2,
                        ensure_ascii=False,
                    )
                )
                raise SystemExit(1)
            args.paciente_id = args.confirm_paciente_id

    availability = fetch_free_slots(args.agenda_id, args.data)
    if not availability["ok"]:
        print(json.dumps(availability, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    suggestions = suggest_slots(availability["slots"], args.hora_preferida, args.suggestions)
    envelope = {
        "availability_source": availability["source"],
        "agenda_id": args.agenda_id,
        "data": args.data,
        "hora_preferida": args.hora_preferida,
        "suggestions": suggestions,
    }
    if args.paciente_nome:
        envelope["patient_lookup"] = {
            "query": args.paciente_nome,
            "confirmed_patient_id": args.paciente_id,
        }

    if not args.book:
        print(json.dumps(envelope, indent=2, ensure_ascii=False))
        return

    attempts = []
    for slot in suggestions[: args.max_attempts]:
        payload = build_payload(args, slot["inicio"])
        result = post_booking(payload)
        attempts.append(
            {
                "hora_tentada": slot["inicio"],
                "intervalo": slot["intervalo"],
                "status_code": result["status_code"],
                "response": result["response"],
            }
        )
        if result["status_code"] < 400:
            envelope["booked"] = {
                "hora_escolhida": slot["inicio"],
                "intervalo": slot["intervalo"],
                "api_result": result["response"],
            }
            envelope["attempts"] = attempts
            print(json.dumps(envelope, indent=2, ensure_ascii=False))
            return
        if not is_slot_conflict(result):
            envelope["attempts"] = attempts
            envelope["error"] = result
            print(json.dumps(envelope, indent=2, ensure_ascii=False))
            raise SystemExit(1)

    envelope["attempts"] = attempts
    envelope["error"] = "No slot could be booked from the suggested candidates."
    print(json.dumps(envelope, indent=2, ensure_ascii=False))
    raise SystemExit(1)


if __name__ == "__main__":
    main()
