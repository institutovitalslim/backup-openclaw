#!/usr/bin/env python3
"""Regressões do incidente real de 2026-08-21 (sem rede e sem PII)."""

import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

import zapi_clara_bridge as b


def test_only_lead_messages_count_as_declared_context():
    b.get_recent_lead_texts = lambda phone, limit=16: ["Tem agenda?"]
    declared = b.build_declared_lead_context("synthetic", "Tem agenda?", limit=16)
    assert "CLARA/CLÍNICA" not in declared
    assert not b.has_substantive_weight_context(declared), declared
    assert not b.has_mature_discovery_context(declared), declared


def test_schedule_question_survives_enforcers_without_invented_symptoms():
    b.get_recent_lead_texts = lambda phone, limit=16: ["Atende pelo plano?", "Tem agenda?"]
    b.get_lead_entry = lambda phone: {"reply_count": 2, "inbound_count": 2}
    b.get_phone_event_entry = lambda phone: {}
    candidate = "Posso verificar a disponibilidade da agenda para você."
    reply = b.enforce_discovery_before_next_step("Tem agenda?", candidate)
    reply = b.enforce_spin_before_agendamento("synthetic", "Tem agenda?", reply)
    reply = b.enforce_no_repetitive_discovery_after_declared_context("synthetic", "Tem agenda?", reply)
    reply = b.enforce_no_reopening_after_context("synthetic", "Tem agenda?", reply)
    reply = b.enforce_direct_objective_question_recovery("synthetic", "Tem agenda?", reply)
    lower = reply.lower()
    assert "agenda" in lower or "disponibilidade" in lower, reply
    for invented in ("ansiedade", "barriga", "dificuldade para perder peso", "metabolismo lento", "desde a infância"):
        assert invented not in lower, reply


def test_thinking_gate_rejects_natural_language_and_returns_valid_local_plan():
    original = b.openclaw_response
    try:
        b.openclaw_response = lambda *args, **kwargs: "Claro. Posso verificar a agenda para você."
        plan = b.call_clara_thinking_gate("synthetic", "Tem agenda?", "instruções")
        parsed = json.loads(plan)
        assert set(parsed) == {
            "intent", "conversation_stage", "known_context", "risk_checks",
            "must_answer", "must_ask", "next_microstep", "forbidden",
        }
        assert parsed["must_answer"]
        assert parsed["must_ask"] == "zero ou uma pergunta útil; nunca perguntar por obrigação"
        assert "não introduzir tema não perguntado" in parsed["forbidden"]
    finally:
        b.openclaw_response = original


def test_takeover_during_chunking_stops_remaining_chunks():
    original_send = b.send_zapi_text
    original_split = b.split_human_conversation_chunks
    original_override = b.is_manual_override_active
    original_recent = b.has_recent_human_activity
    original_chunking = b.CLARA_HUMAN_CHUNKING_ENABLED
    original_delay = b.CLARA_HUMAN_CHUNK_INTER_SEND_SECONDS
    sent = []
    checks = iter([(False, None), (False, None), (True, "from_me_outbound_detected")])
    try:
        b.send_zapi_text = lambda phone, message, **kwargs: (sent.append(message) or (200, "{}"))
        b.split_human_conversation_chunks = lambda message: ["primeiro", "segundo", "terceiro"]
        b.is_manual_override_active = lambda phone: next(checks, (True, "from_me_outbound_detected"))
        b.has_recent_human_activity = lambda phone: (False, None)
        b.CLARA_HUMAN_CHUNKING_ENABLED = True
        b.CLARA_HUMAN_CHUNK_INTER_SEND_SECONDS = 0
        status, body = b.send_zapi_text_human_sequence("synthetic", "mensagem", source="clara_reply", safety_phone="synthetic")
        assert sent == ["primeiro"], sent
        assert status == 409, (status, body)
        assert "human_takeover" in body, body
    finally:
        b.send_zapi_text = original_send
        b.split_human_conversation_chunks = original_split
        b.is_manual_override_active = original_override
        b.has_recent_human_activity = original_recent
        b.CLARA_HUMAN_CHUNKING_ENABLED = original_chunking
        b.CLARA_HUMAN_CHUNK_INTER_SEND_SECONDS = original_delay


def test_automatic_human_takeover_is_bounded():
    assert b.CLARA_HUMAN_TAKEOVER_INDEFINITE is False
    assert b.MANUAL_TAKEOVER_WINDOW_SECONDS == b.HUMAN_RECENT_MESSAGE_WINDOW_SECONDS == 1800


def test_confirmation_failure_stays_out_of_commercial_flow():
    original_state = b.QUARK_CONFIRMATION_STATE_FILE
    original_script = b.QUARK_CONFIRMATION_REPLY_SCRIPT
    original_run = b.subprocess.run
    try:
        with tempfile.TemporaryDirectory() as td:
            state_path = Path(td) / "pending.json"
            state_path.write_text(json.dumps({"items": [{"phone": "557100000001", "status": "sent"}]}))
            b.QUARK_CONFIRMATION_STATE_FILE = str(state_path)
            b.QUARK_CONFIRMATION_REPLY_SCRIPT = __file__
            b.subprocess.run = lambda *args, **kwargs: SimpleNamespace(returncode=1, stdout="", stderr="PATCH failed")
            assert b.process_quarkclinic_confirmation_reply("557100000001", "Confirmo") is True
    finally:
        b.QUARK_CONFIRMATION_STATE_FILE = original_state
        b.QUARK_CONFIRMATION_REPLY_SCRIPT = original_script
        b.subprocess.run = original_run


def test_state_writes_are_atomic_json():
    original_event = b.CLARA_EVENT_STATE_FILE
    original_control = b.CLARA_CONTROL_FILE
    try:
        with tempfile.TemporaryDirectory() as td:
            b.CLARA_EVENT_STATE_FILE = str(Path(td) / "event.json")
            b.CLARA_CONTROL_FILE = str(Path(td) / "control.json")
            for idx in range(25):
                b.update_phone_event_entry("synthetic", {"counter": idx})
                b.set_manual_override("synthetic", True, note="test", until=1)
                json.loads(Path(b.CLARA_EVENT_STATE_FILE).read_text())
                json.loads(Path(b.CLARA_CONTROL_FILE).read_text())
            assert not list(Path(td).glob("*.tmp-*"))
    finally:
        b.CLARA_EVENT_STATE_FILE = original_event
        b.CLARA_CONTROL_FILE = original_control


if __name__ == "__main__":
    test_only_lead_messages_count_as_declared_context()
    test_schedule_question_survives_enforcers_without_invented_symptoms()
    test_thinking_gate_rejects_natural_language_and_returns_valid_local_plan()
    test_takeover_during_chunking_stops_remaining_chunks()
    test_automatic_human_takeover_is_bounded()
    test_confirmation_failure_stays_out_of_commercial_flow()
    test_state_writes_are_atomic_json()
    print("OK incident 2026-08-21 regressions")
