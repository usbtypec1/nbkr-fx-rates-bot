from xml.etree import ElementTree

import httpx

from data_types import CurrencyFXRate


def get_fx_rates() -> str:
    url = 'https://www.nbkr.kg/XML/daily.xml'
    return httpx.get(url).text


def parse_fx_rates_xml(fx_rates_xml: str) -> list[CurrencyFXRate]:
    root = ElementTree.fromstring(fx_rates_xml)
    result = []
    for currency in root:
        currency_iso_code = currency.get('ISOCode')
        nominal, value = [i.text.replace(',', '.') for i in currency]
        result.append(CurrencyFXRate(currency_iso_code, int(nominal), float(value)))
    return result
