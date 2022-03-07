import pytest

from utils import match_currencies
from data_types import CurrencyFXRate


@pytest.mark.parametrize(
    'old_fx_rates,new_fx_rates',
    [
        ([CurrencyFXRate('USD', 1, 60)], [CurrencyFXRate('USD', 1, 60)]),
        ([CurrencyFXRate('KGS', 1, 30), CurrencyFXRate('TRY', 1, 1)],
         [CurrencyFXRate('KGS', 1, 60), CurrencyFXRate('TRY', 1, 1)]),
    ]
)
def test_all_fx_rates_have_pairs(old_fx_rates, new_fx_rates):
    matched = match_currencies(old_fx_rates, new_fx_rates)
    assert not matched.single_new_fx_rates
    assert not matched.single_old_fx_rates


@pytest.mark.parametrize(
    'old_fx_rates,new_fx_rates,single_fx_rates',
    [
        ([CurrencyFXRate('USD', 1, 60), CurrencyFXRate('KGS', 1, 30)], [CurrencyFXRate('USD', 1, 60)], [CurrencyFXRate('KGS', 1, 30)]),
        ([CurrencyFXRate('USD', 1, 60)], [CurrencyFXRate('USD', 1, 60), CurrencyFXRate('KGS', 1, 30)], [CurrencyFXRate('KGS', 1, 30)]),
    ]
)
def test_with_single_fx_rates(old_fx_rates, new_fx_rates, single_fx_rates):
    matched = match_currencies(old_fx_rates, new_fx_rates)
    assert (matched.single_old_fx_rates or matched.single_new_fx_rates) == single_fx_rates


def test_no_passed_currencies():
    matched = match_currencies([], [])
    assert not matched.single_new_fx_rates
    assert not matched.single_old_fx_rates
    assert not matched.new_and_old_fx_rates_pairs
