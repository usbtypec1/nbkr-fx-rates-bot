import pathlib

import pytest

import config
import national_bank
from data_types import CurrencyFXRate

CURRENCIES_FILE_PATH = pathlib.Path.joinpath(config.ROOT_PATH, 'tests', 'currencies.xml')


def test_parse_currencies():
    with open(CURRENCIES_FILE_PATH, encoding='utf-8') as file:
        currencies = file.read()
    expected = [CurrencyFXRate(iso_code='USD', nominal=1, value=80.9694),
                CurrencyFXRate(iso_code='EUR', nominal=1, value=81.2164),
                CurrencyFXRate(iso_code='KZT', nominal=1, value=0.1686),
                CurrencyFXRate(iso_code='RUB', nominal=1, value=1.3612)]
    assert national_bank.parse_fx_rates_xml(currencies) == expected
