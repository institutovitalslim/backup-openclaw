#!/usr/bin/env python3
"""Regressão do anúncio WhatsApp que pulou conexão e SPIN em 2026-08-23."""

import zapi_clara_bridge as b


CAMPAIGN_TEXT = (
    "Olá! Vi o anúncio do Instituto Vital Slim e quero entender como "
    "funciona o acompanhamento. [an. g904915]"
)


def test_prefilled_ad_message_gets_connection_and_open_spin_before_program_explanation():
    payload = {
        "adContext": {
            "entryPointConversionSource": "click_to_chat_link",
            "title": "Teste Metabólico",
        }
    }
    bad_candidate = (
        "Depois da consulta inicial, se fizer sentido para o seu caso, a Dra. Daniely "
        "pode indicar um Programa de Acompanhamento individual."
    )

    reply = b.enforce_campaign_prefilled_connection(
        CAMPAIGN_TEXT,
        bad_candidate,
        payload=payload,
    )

    lower = reply.lower()
    assert "sou a clara" in lower, reply
    assert "que bom te receber" not in lower, reply
    assert "me conta" in lower, reply
    assert "o que fez você buscar um acompanhamento agora" in lower, reply
    assert "como posso te chamar" not in lower, reply
    assert reply.count("?") == 1, reply
    assert "programa" not in lower, reply
    assert "consulta inicial" not in lower, reply
    assert "valor" not in lower, reply
    assert "agenda" not in lower, reply
    assert "\n\n" in reply, reply


def test_prefilled_ad_tracking_marker_with_g_is_detected_without_adcontext():
    assert b.is_campaign_prefilled_message(CAMPAIGN_TEXT, payload={}) is True


def test_all_generic_opening_failsafes_use_human_connection_without_banned_template():
    replies = [
        b.build_spin_opening_reply(),
        b.enforce_discovery_before_next_step("Quero", "Posso verificar a agenda para você?"),
    ]
    for reply in replies:
        lower = reply.lower()
        assert "que bom te receber" not in lower, reply
        assert "me conta um pouquinho" not in lower, reply
        assert reply.count("?") == 1, reply
        assert "o que fez você buscar ajuda agora" in lower, reply


def test_ordinary_program_question_is_not_rewritten_as_campaign_opening():
    original = "Claro. Vou entender primeiro o que você busca."
    reply = b.enforce_campaign_prefilled_connection(
        "Como funciona o programa?",
        original,
        payload={},
    )
    assert reply == original


if __name__ == "__main__":
    test_prefilled_ad_message_gets_connection_and_open_spin_before_program_explanation()
    test_prefilled_ad_tracking_marker_with_g_is_detected_without_adcontext()
    test_all_generic_opening_failsafes_use_human_connection_without_banned_template()
    test_ordinary_program_question_is_not_rewritten_as_campaign_opening()
    print("OK: 4 regressões de anúncio/SPIN")
