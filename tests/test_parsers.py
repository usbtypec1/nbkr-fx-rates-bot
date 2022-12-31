import pathlib
from decimal import Decimal

from banks.parsers import parse_commercial_bank_fx_rates, parse_national_bank_fx_rates
from models import CurrencyFXRate
from config import ROOT_PATH


def test_commercial_bank_fx_rates_parser():
    with open(pathlib.Path.joinpath(ROOT_PATH, 'tests', 'commercial_banks.html')) as file:
        html = file.read()
    actual = parse_commercial_bank_fx_rates(html)
    currencies_fx_rates = (
        CurrencyFXRate(bank_name='Бакай Банк', iso_code='USD', buy_value=Decimal('85.73'), sell_value=Decimal('86.73')),
        CurrencyFXRate(bank_name='Бакай Банк', iso_code='EUR', buy_value=Decimal('92.00'), sell_value=Decimal('93.00')),
        CurrencyFXRate(bank_name='Бакай Банк', iso_code='RUB', buy_value=Decimal('1.150'), sell_value=Decimal('1.250')),
        CurrencyFXRate(bank_name='Бакай Банк', iso_code='KZT', buy_value=Decimal('0.120'), sell_value=Decimal('0.195')),
        CurrencyFXRate(bank_name='Демир банк', iso_code='USD', buy_value=Decimal('85.73'), sell_value=Decimal('86.73')),
        CurrencyFXRate(bank_name='Демир банк', iso_code='EUR', buy_value=Decimal('92.00'), sell_value=Decimal('93.00')),
        CurrencyFXRate(bank_name='Демир банк', iso_code='RUB', buy_value=Decimal('1.160'), sell_value=Decimal('1.280')),
        CurrencyFXRate(bank_name='Демир банк', iso_code='KZT', buy_value=Decimal('0.120'), sell_value=Decimal('0.200')),
    )
    for currency_fx_rates in currencies_fx_rates:
        assert currency_fx_rates in actual


def test_national_bank_fx_rates_parser():
    with open(pathlib.Path.joinpath(ROOT_PATH, 'tests', 'national_bank.xml')) as file:
        html = file.read()
    actual = parse_national_bank_fx_rates(html)
    currencies_fx_rates = [
        CurrencyFXRate(bank_name='НБКР', iso_code='USD', buy_value=Decimal('80.9694'), sell_value=Decimal('80.9694')),
        CurrencyFXRate(bank_name='НБКР', iso_code='EUR', buy_value=Decimal('81.2164'), sell_value=Decimal('81.2164')),
        CurrencyFXRate(bank_name='НБКР', iso_code='KZT', buy_value=Decimal('0.1686'), sell_value=Decimal('0.1686')),
        CurrencyFXRate(bank_name='НБКР', iso_code='RUB', buy_value=Decimal('1.3612'), sell_value=Decimal('1.3612')),
    ]
    assert actual == currencies_fx_rates
