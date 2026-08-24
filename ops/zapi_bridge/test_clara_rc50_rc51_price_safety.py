#!/usr/bin/env python3
import importlib.util
from pathlib import Path

BRIDGE = Path('/root/.openclaw/workspace/ops/zapi_bridge/zapi_clara_bridge.py')
spec = importlib.util.spec_from_file_location('bridge', BRIDGE)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


def assert_no_money(text: str):
    lower = text.lower()
    assert 'r$' not in lower and '1.000' not in lower and '1000' not in lower and '900' not in lower, text


def test_rc50_bare_category_does_not_release_price():
    phone = '5599988877766'
    bridge.update_phone_event_entry(phone, {'price_context_ready': False, 'price_questions': 1})
    unsafe = 'Perfeito. Para emagrecimento, a consulta inicial é completa. O valor é R$ 1.000 ou R$ 900 fechando hoje.'
    out = bridge.enforce_price_timing(phone, 'Emagrecimento', unsafe)
    assert_no_money(out)
    assert 'Dentro do emagrecimento' in out


def test_rc51_admin_send_price_safety_without_context():
    phone = '5599977766655'
    bridge.update_phone_event_entry(phone, {'price_context_ready': False})
    unsafe = 'A consulta inicial é R$ 1.000. Fechando hoje, fica R$ 900.'
    out = bridge.enforce_outbound_price_safety(phone, unsafe, 'Emagrecimento')
    assert_no_money(out)
    assert 'Dentro do emagrecimento' in out


if __name__ == '__main__':
    test_rc50_bare_category_does_not_release_price()
    test_rc51_admin_send_price_safety_without_context()
    print('ok')

def test_detects_written_price_and_discount_language():
    assert bridge.contains_money_value('A consulta é mil reais')
    assert bridge.contains_money_value('Consigo aplicar um desconto hoje')
    assert bridge.contains_money_value('Fica por novecentos fechando hoje')

# Re-run extra tests when executed directly after original block
if __name__ == '__main__':
    test_detects_written_price_and_discount_language()
