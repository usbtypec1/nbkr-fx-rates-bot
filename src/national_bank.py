import urllib.request
import urllib.response
from xml.etree import ElementTree

import exceptions
from data_types import CurrencyFXRate


def get_fx_rates() -> str:
    url = 'https://www.nbkr.kg/XML/daily.xml'
    with urllib.request.urlopen(url) as response:
        if response.status != 200:
            raise exceptions.NationalBankAPIError
        return response.read().decode('utf-8')


def parse_fx_rates_xml(fx_rates_xml: str) -> list[CurrencyFXRate]:
    root = ElementTree.fromstring(fx_rates_xml)
    result = []
    for currency in root:
        currency_iso_code = currency.get('ISOCode')
        nominal, value = [i.text.replace(',', '.') for i in currency]
        result.append(CurrencyFXRate(currency_iso_code, int(nominal), float(value)))
    return result
