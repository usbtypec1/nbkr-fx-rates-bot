from decimal import Decimal
from xml.etree import ElementTree

from bs4 import BeautifulSoup

from models import CurrencyFXRate

__all__ = ('parse_commercial_bank_fx_rates', 'parse_national_bank_fx_rates')


def parse_commercial_bank_fx_rates(html: str) -> list[CurrencyFXRate]:
    soup = BeautifulSoup(html, 'lxml')
    tbody = soup.find_all('tbody')
    if not tbody:
        return []
    table_rows = tbody[-1].find_all('tr')
    currencies_fx_rates: list[CurrencyFXRate] = []
    for table_row in table_rows:
        tds = [table_data.text for table_data in table_row.find_all('td')]
        (bank_name, usd_buy_value, usd_sell_value, eur_buy_value, eur_sell_value,
         rub_buy_value, rub_sell_value, kzt_buy_value, kzt_sell_value, *_) = tds
        bank_name = bank_name.strip()
        currencies_fx_rates += [
            CurrencyFXRate(
                bank_name=bank_name, iso_code='USD',
                buy_value=Decimal(usd_buy_value), sell_value=Decimal(usd_sell_value)
            ),
            CurrencyFXRate(
                bank_name=bank_name, iso_code='EUR',
                buy_value=Decimal(eur_buy_value), sell_value=Decimal(eur_sell_value)
            ),
            CurrencyFXRate(
                bank_name=bank_name, iso_code='RUB', buy_value=Decimal(rub_buy_value),
                sell_value=Decimal(rub_sell_value)
            ),
            CurrencyFXRate(
                bank_name=bank_name, iso_code='KZT', buy_value=Decimal(kzt_buy_value),
                sell_value=Decimal(kzt_sell_value)
            ),
        ]
    return currencies_fx_rates


def parse_national_bank_fx_rates(xml: str) -> list[CurrencyFXRate]:
    root = ElementTree.fromstring(xml)
    currencies_fx_rates: list[CurrencyFXRate] = []
    for currency in root:
        currency_iso_code = currency.get('ISOCode')
        _, value = [i.text.replace(',', '.') for i in currency]
        currency_fx_rate = CurrencyFXRate(
            bank_name='НБКР',
            iso_code=currency_iso_code,
            buy_value=Decimal(value),
            sell_value=Decimal(value),
        )
        currencies_fx_rates.append(currency_fx_rate)
    return currencies_fx_rates
