import pytest

from data_types import CurrencyFXRate
from utils import format_changed_fx_rate_text


@pytest.mark.parametrize(
    'old_fx_rate,new_fx_rate',
    [
        (CurrencyFXRate('USD', 1, 1), CurrencyFXRate('USD', 1, 1)),
        (CurrencyFXRate('USD', 1, 4), CurrencyFXRate('USD', 1, 4)),
    ]
)
def test_old_value_and_new_value_are_same(old_fx_rate, new_fx_rate):
    assert format_changed_fx_rate_text(old_fx_rate, new_fx_rate) == 'Currency has not been changed'


@pytest.mark.parametrize(
    'old_fx_rate,new_fx_rate,expected',
    [
        (CurrencyFXRate('USD', 1, 1), CurrencyFXRate('USD', 1, 2), '📈 USD: <b>1 ➞ 2</b> (+100.0%)'),
        (CurrencyFXRate('USD', 1, 5), CurrencyFXRate('USD', 1, 3), '📉 USD: <b>5 ➞ 3</b> (-40.0%)'),
    ]
)
def test_fx_rates_changed(old_fx_rate, new_fx_rate, expected):
    assert format_changed_fx_rate_text(old_fx_rate, new_fx_rate) == expected
