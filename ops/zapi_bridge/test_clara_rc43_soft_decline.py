#!/usr/bin/env python3
import importlib.util

BRIDGE = "/root/.openclaw/workspace/ops/zapi_bridge/zapi_clara_bridge.py"
spec = importlib.util.spec_from_file_location("zapi_bridge_rc43", BRIDGE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

PLAN_ONLY = "Hoje, o atendimento no Instituto Vital Slim é exclusivamente particular. Não atendemos convênios."
REIMBURSEMENT_ONLY = "Hoje, o atendimento no Instituto Vital Slim é exclusivamente particular. Não trabalhamos com reembolso."
BOTH = "Hoje, o atendimento no Instituto Vital Slim é exclusivamente particular. Não atendemos convênios e não trabalhamos com reembolso."


def test_soft_decline_plano():
    inbound = "Saúde metabólica geral\nMas agradeço!"
    bad_reply = "Eu que agradeço seu contato. Se em algum momento quiser uma avaliação particular com a Dra. Daniely.\n\nPara deixar isso bem encaminhado: prefere que eu veja o próximo horário pela manhã ou pela tarde?"
    out = mod.enforce_objection_handling(inbound, bad_reply)
    assert out == BOTH


def test_direct_plan_questions_answer_only_what_was_asked():
    for inbound in (
        "Vocês atendem Unimed?",
        "Aceita Bradesco?",
        "Atende pelo planserv?",
        "Vocês trabalham com algum convênio?",
        "A consulta pode ser pelo meu plano?",
    ):
        out = mod.enforce_plan_question_response(inbound, "Posso te passar os valores?")
        assert out == PLAN_ONLY
        assert "reembolso" not in out.lower()


def test_direct_reimbursement_question_answers_reimbursement_only():
    out = mod.enforce_plan_question_response("Tem reembolso?", "Vou verificar.")
    assert out == REIMBURSEMENT_ONLY


def test_legacy_reimbursement_offer_is_scrubbed_even_without_inbound_context():
    legacy = (
        "Em alguns casos, trabalhamos com possibilidade de reembolso para "
        "Bradesco, SulAmérica e Amil."
    )
    assert mod.enforce_plan_question_response("", legacy) == BOTH


def test_price_question_cannot_be_switched_back_to_plan_or_reimbursement():
    original_ready = mod.consultation_price_context_ready
    original_context = mod.build_declared_lead_context
    try:
        mod.consultation_price_context_ready = lambda phone, inbound="": True
        mod.build_declared_lead_context = lambda phone, inbound="", limit=14: "Lead já relatou dificuldade com peso e disposição."
        wrong = "Perfeito. Você tem Bradesco, SulAmérica ou Amil, ou seria particular mesmo?"
        out = mod.enforce_no_topic_switch_on_price_question("synthetic", "Qual o valor da consulta?", wrong)
        lower = out.lower()
        assert "r$" in lower, out
        for forbidden in ("bradesco", "sulamérica", "amil", "convênio", "reembolso"):
            assert forbidden not in lower, out
    finally:
        mod.consultation_price_context_ready = original_ready
        mod.build_declared_lead_context = original_context


def test_early_price_question_gets_one_useful_spin_not_a_plan_question():
    original_ready = mod.consultation_price_context_ready
    try:
        mod.consultation_price_context_ready = lambda phone, inbound="": False
        wrong = "Você tem algum plano ou seria particular mesmo?"
        out = mod.enforce_no_topic_switch_on_price_question("synthetic", "Qual o valor da consulta?", wrong)
        lower = out.lower()
        assert out.count("?") == 1, out
        assert "o que fez você buscar" in lower, out
        for forbidden in ("plano", "convênio", "reembolso", "bradesco", "amil"):
            assert forbidden not in lower, out
    finally:
        mod.consultation_price_context_ready = original_ready


if __name__ == "__main__":
    test_soft_decline_plano()
    test_direct_plan_questions_answer_only_what_was_asked()
    test_direct_reimbursement_question_answers_reimbursement_only()
    test_legacy_reimbursement_offer_is_scrubbed_even_without_inbound_context()
    test_price_question_cannot_be_switched_back_to_plan_or_reimbursement()
    test_early_price_question_gets_one_useful_spin_not_a_plan_question()
    print("RC-43/sem-reembolso OK")
