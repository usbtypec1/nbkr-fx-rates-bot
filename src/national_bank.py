import urllib.request
import urllib.response
from xml.etree import ElementTree

import exceptions
from data_types import CurrencyFXRate


def get_fx_rates() -> str:
    """Get FX rates XML document from National Bank's API.

    Returns:
        FX rates in xml document type.

    Raises:
        `exceptions.NationalBankAPIError` if response status code is not 200.
    """
    url = 'https://www.nbkr.kg/XML/daily.xml'
    with urllib.request.urlopen(url) as response:
        if response.status != 200:
            raise exceptions.NationalBankAPIError
        return response.read().decode('utf-8')


def parse_fx_rates_xml(fx_rates_xml: str) -> list[CurrencyFXRate]:
    """Convert xml document with FX rates to currencies.

    Args:
        fx_rates_xml: xml with FX rates.

    Returns:
        List of `CurrencyFXRate` models.
    """
    root = ElementTree.fromstring(fx_rates_xml)
    result = []
    for currency in root:
        currency_iso_code = currency.get('ISOCode')
        nominal, value = [i.text.replace(',', '.') for i in currency]
        result.append(CurrencyFXRate(currency_iso_code, int(nominal), float(value)))
    return result
