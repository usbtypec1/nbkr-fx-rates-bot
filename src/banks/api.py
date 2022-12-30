import httpx

import exceptions

__all__ = ('get_national_bank_fx_rates', 'get_commercial_bank_fx_rates')


def get_national_bank_fx_rates() -> str:
    url = 'https://www.nbkr.kg/XML/daily.xml'
    response = httpx.get(url)
    if response.status_code != 200:
        raise exceptions.NationalBankAPIError
    return response.text


def get_commercial_bank_fx_rates() -> str:
    url = 'https://banks.kg/rates'
    response = httpx.get(url)
    if response.status_code != 200:
        raise exceptions.CommercialBankAPIError
    return response.text
