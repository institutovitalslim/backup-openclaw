#!/usr/bin/env python3
"""Regressões RC-78/RC-79: responder pergunta objetiva e não repetir jornada.

Casos reais Tiaro 2026-07-03:
- Lead pergunta se atende sábado/amanhã; Clara não pode repetir SPIN genérico.
- Lead pergunta sobre tireoide; Clara não pode ignorar e voltar para descoberta.
- Jornada/bioimpedância já enviada; nova resposta não pode reenviar o mesmo pitch.
"""

import zapi_clara_bridge as b


def setup_context():
    b.build_recent_conversation_context = lambda phone, limit=14: (
        "CONTEXTO RECENTE REAL DO WHATSAPP:\n"
        "- LEAD: Faz acompanhamento da tireóide ou só tratamento pra emagrecimento\n"
        "- CLARA/CLÍNICA: Pelo que você trouxe — queda de energia, objetivo de eliminar peso — faz sentido explicar a jornada antes de falar de valor.\n"
        "- CLARA/CLÍNICA: O tratamento no Instituto Vital Slim é médico e olha o sobrepeso, obesidade, saúde hormonal e metabolismo de forma multifatorial.\n"
        "- CLARA/CLÍNICA: Seu atendimento começa com uma consulta médica profunda com a Dra. Daniely, em torno de 60 a 90 minutos.\n"
        "- CLARA/CLÍNICA: Você também passa por uma avaliação de enfermagem completa e por uma bioimpedância de última geração, para entendermos composição corporal.\n"
        "- CLARA/CLÍNICA: Com tudo isso, a Dra. Daniely define se faz sentido um Programa de Acompanhamento personalizado."
    )


def test_schedule_question_is_answered_not_spin():
    setup_context()
    generic = "Claro, eu te explico direitinho.\n\nAntes, para eu não te passar uma informação solta: o que mais está te incomodando hoje e fez você buscar ajuda agora?"
    fixed = b.enforce_direct_objective_question_recovery("5571996570462", "Certo atende dia de sábado", generic)
    lower = fixed.lower()
    assert "sábado" in lower or "sabado" in lower, fixed
    assert "atendemos" in lower or "disponibilidade" in lower, fixed
    assert "o que mais está te incomodando" not in lower, fixed
    assert "o que fez você buscar" not in lower, fixed


def test_thyroid_scope_question_is_answered_not_spin():
    setup_context()
    generic = "Entendi. Para eu continuar do ponto certo e sem pular etapas: o que mais está te incomodando hoje — peso, disposição, hormônios ou saúde de forma geral?"
    fixed = b.enforce_direct_objective_question_recovery("5571996570462", "Faz acompanhamento da tireóide ou só tratamento pra emagrecimento", generic)
    lower = fixed.lower()
    assert "tireoide" in lower or "tireóide" in lower, fixed
    assert "metabólica" in lower or "metabolica" in lower or "hormonal" in lower, fixed
    assert "o que mais está te incomodando" not in lower, fixed


def test_patient_journey_not_repeated_after_it_was_already_sent():
    setup_context()
    repeated_journey = b.build_journey_fit_check_reply("queda de energia, objetivo de eliminar peso, mudança no corpo")
    fixed = b.enforce_no_repeat_patient_journey("5571996570462", "Incomodação da tireóide inchado indisposição, dificuldade de emagrecer", repeated_journey)
    lower = fixed.lower()
    assert "já te expliquei a jornada" in lower or "ja te expliquei a jornada" in lower, fixed
    assert "bioimpedância de última geração" not in lower, fixed
    assert "o tratamento no instituto vital slim" not in lower, fixed
    assert "tireoide" in lower, fixed


def test_context_summary_preserves_thyroid_and_swelling():
    summary = b.summarize_declared_context("Incomodação da tireóide inchado indisposição, entre outros dificuldade de emagrecer")
    lower = summary.lower()
    assert "tireoide" in lower, summary
    assert "inchaço" in lower or "inchaco" in lower, summary


if __name__ == "__main__":
    test_schedule_question_is_answered_not_spin()
    test_thyroid_scope_question_is_answered_not_spin()
    test_patient_journey_not_repeated_after_it_was_already_sent()
    test_context_summary_preserves_thyroid_and_swelling()
    print("OK RC-78/RC-79 direct objective + no repeat journey")
