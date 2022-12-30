from decimal import Decimal

from banks.parsers import CommercialBankFXRatesParser, NationalBankFXRatesParser
from data_types import CurrencyFXRate, BankFXRates


def test_commercial_bank_fx_rates_parser():
    with open('commercial_banks.html') as file:
        html = file.read()
    actual = CommercialBankFXRatesParser(html).parse()
    banks_fx_rates = (
        BankFXRates(
            name='Бакай Банк',
            currencies=[
                CurrencyFXRate(iso_code='USD', buy_value=Decimal('85.73'), sell_value=Decimal('86.73')),
                CurrencyFXRate(iso_code='EUR', buy_value=Decimal('92.00'), sell_value=Decimal('93.00')),
                CurrencyFXRate(iso_code='RUB', buy_value=Decimal('1.150'), sell_value=Decimal('1.250')),
                CurrencyFXRate(iso_code='KZT', buy_value=Decimal('0.120'), sell_value=Decimal('0.195')),
            ],
        ),
        BankFXRates(
            name='Демир банк',
            currencies=[
                CurrencyFXRate(iso_code='USD', buy_value=Decimal('85.73'), sell_value=Decimal('86.73')),
                CurrencyFXRate(iso_code='EUR', buy_value=Decimal('92.00'), sell_value=Decimal('93.00')),
                CurrencyFXRate(iso_code='RUB', buy_value=Decimal('1.160'), sell_value=Decimal('1.280')),
                CurrencyFXRate(iso_code='KZT', buy_value=Decimal('0.120'), sell_value=Decimal('0.200')),
            ],
        ),
    )
    for bank_fx_rates in banks_fx_rates:
        assert bank_fx_rates in actual


def test_national_bank_fx_rates_parser():
    with open('./national_bank.xml') as file:
        html = file.read()
    actual = NationalBankFXRatesParser(html).parse()
    expected = [
        BankFXRates(
            name='НБКР',
            currencies=[
                CurrencyFXRate(iso_code='USD', buy_value=Decimal('80.9694'), sell_value=Decimal('80.9694')),
                CurrencyFXRate(iso_code='EUR', buy_value=Decimal('81.2164'), sell_value=Decimal('81.2164')),
                CurrencyFXRate(iso_code='KZT', buy_value=Decimal('0.1686'), sell_value=Decimal('0.1686')),
                CurrencyFXRate(iso_code='RUB', buy_value=Decimal('1.3612'), sell_value=Decimal('1.3612')),
            ]
        )
    ]
    assert actual == expected
