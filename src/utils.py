import http.client
import json
import urllib.request

from data_types import CurrencyFXRate, NewAndOldFXRatesPair, MatchedCurrencies


def match_currencies(old_fx_rates: list[CurrencyFXRate],
                     new_fx_rates: list[CurrencyFXRate]) -> MatchedCurrencies:
    iso_code_to_old_fx_rates = {fx_rate.iso_code: fx_rate for fx_rate in old_fx_rates}
    pairs = []
    single_new_fx_rates = []
    for new_fx_rate in new_fx_rates:
        try:
            old_fx_rate = iso_code_to_old_fx_rates.pop(new_fx_rate.iso_code)
        except KeyError:
            single_new_fx_rates.append(new_fx_rate)
        else:
            pairs.append(NewAndOldFXRatesPair(old_fx_rate, new_fx_rate))
    single_old_fx_rates = list(iso_code_to_old_fx_rates.values())
    return MatchedCurrencies(pairs, single_old_fx_rates, single_new_fx_rates)


def format_changed_fx_rate_text(old_fx_rate: CurrencyFXRate, new_fx_rate: CurrencyFXRate) -> str:
    if old_fx_rate.value == new_fx_rate.value:
        return 'Currency has not been changed'
    emoji = '📈' if new_fx_rate.value > old_fx_rate.value else '📉'
    diff = round(new_fx_rate.value * 100 / old_fx_rate.value - 100, 2)
    diff = f'+{diff}%' if diff > 0 else f'{diff}%'
    return (f'{emoji} {new_fx_rate.iso_code}: <b>{old_fx_rate.value}'
            f' ➞ {new_fx_rate.value}</b> ({diff})')
