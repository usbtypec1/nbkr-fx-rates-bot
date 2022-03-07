from typing import NamedTuple


class CurrencyFXRate(NamedTuple):
    iso_code: str
    nominal: int
    value: float


class NewAndOldFXRatesPair(NamedTuple):
    old: CurrencyFXRate
    new: CurrencyFXRate


class MatchedCurrencies(NamedTuple):
    new_and_old_fx_rates_pairs: list[NewAndOldFXRatesPair]
    single_old_fx_rates: list[CurrencyFXRate]
    single_new_fx_rates: list[CurrencyFXRate]
