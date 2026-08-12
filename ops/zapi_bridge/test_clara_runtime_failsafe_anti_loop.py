import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("zapi_clara_bridge", ROOT / "zapi_clara_bridge.py")
assert spec is not None and spec.loader is not None
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def setup_history(text: str, last_reply: str = "") -> None:
    setattr(b, "build_recent_conversation_context", lambda phone, limit=16: text)
    setattr(
        b,
        "get_lead_entry",
        lambda phone: {
            "reply_count": 2,
            "inbound_count": 3,
            "last_reply_preview": last_reply,
        },
    )
    setattr(b, "log", lambda message: None)


def test_runtime_failsafe_answers_dra_daniely_specialty_directly():
    setup_history("")
    reply = b.build_text_runtime_failsafe_reply(
        "Qual a especialidade da Dra. Daniely?",
        phone="5571000000000",
    )
    lower = reply.lower()
    assert "endocrinologista" in lower, reply
    assert "o que mais está te incomodando" not in lower, reply
    assert "para eu continuar do ponto certo" not in lower, reply


def test_runtime_failsafe_advances_after_general_health_was_already_declared():
    setup_history(
        "Clara: o que mais está te incomodando hoje — peso, disposição, hormônios ou saúde de forma geral?\n"
        "Lead: Td de uma forma geral\n"
        "Clara: o que mais está te incomodando hoje — peso, disposição, hormônios ou saúde de forma geral?"
    )
    reply = b.build_text_runtime_failsafe_reply(
        "Saúde de forma geral",
        phone="5571000000000",
    )
    lower = reply.lower()
    assert "o que mais está te incomodando" not in lower, reply
    assert "para eu continuar do ponto certo" not in lower, reply
    assert "dra. daniely" in lower or "avaliação" in lower or "avaliacao" in lower, reply


def test_runtime_failsafe_handles_accented_general_health_without_history():
    setup_history("")
    reply = b.build_text_runtime_failsafe_reply(
        "Saúde de forma geral",
        phone="5571000000000",
    )
    lower = reply.lower()
    assert "o que mais está te incomodando" not in lower, reply
    assert "dra. daniely" in lower or "avaliação" in lower or "avaliacao" in lower, reply


def test_runtime_failsafe_never_returns_same_generic_discovery_twice():
    previous = b.build_spin_continuation_reply()
    setup_history(
        "Clara: " + previous + "\nLead: Tudo de forma geral",
        last_reply=previous,
    )
    reply = b.build_text_runtime_failsafe_reply(
        "Tudo de forma geral",
        phone="5571000000000",
    )
    assert reply.strip() != previous.strip(), reply
    assert "o que mais está te incomodando" not in reply.lower(), reply


if __name__ == "__main__":
    test_runtime_failsafe_answers_dra_daniely_specialty_directly()
    test_runtime_failsafe_advances_after_general_health_was_already_declared()
    test_runtime_failsafe_handles_accented_general_health_without_history()
    test_runtime_failsafe_never_returns_same_generic_discovery_twice()
    print("clara_runtime_failsafe_anti_loop_ok")
