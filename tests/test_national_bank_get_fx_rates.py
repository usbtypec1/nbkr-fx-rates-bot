import pytest

from national_bank import get_fx_rates


def test_get_fx_rates():
    xml_response = get_fx_rates()
    assert 'xml' in xml_response
