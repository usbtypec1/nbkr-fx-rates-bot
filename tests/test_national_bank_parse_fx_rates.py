import pytest

from data_types import CurrencyFXRate
from national_bank import parse_fx_rates_xml


@pytest.fixture(scope='module')
def xml_response() -> str:
    return '''<?xml version="1.0" encoding="windows-1251" ?>
    <CurrencyRates Name="Daily Exchange Rates" Date="08.03.2022">
    <Currency ISOCode="USD">
    <Nominal>1</Nominal>
    <Value>97,6945</Value>
    </Currency>
    <Currency ISOCode="EUR">
    <Nominal>1</Nominal>
    <Value>106,1255</Value>
    </Currency>
    <Currency ISOCode="KZT">
    <Nominal>1</Nominal>
    <Value>0,1939</Value>
    </Currency>
    <Currency ISOCode="RUB">
    <Nominal>1</Nominal>
    <Value>0,9233</Value>
    </Currency>
    </CurrencyRates>
    '''


@pytest.fixture(scope='module')
def expected_currency_fx_rates():
    return [CurrencyFXRate(iso_code, nominal, value) for iso_code, nominal, value in
            (('USD', 1, 97.6945), ('EUR', 1, 106.1255), ('KZT', 1, 0.1939), ('RUB', 1, 0.9233))]


def test_parse_fx_rates(xml_response, expected_currency_fx_rates):
    assert parse_fx_rates_xml(xml_response) == expected_currency_fx_rates
