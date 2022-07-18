from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CurrencyFXRate:
    iso_code: str
    nominal: int
    value: float


@dataclass(frozen=True, slots=True)
class NewAndOldFXRatesPair:
    old: CurrencyFXRate
    new: CurrencyFXRate


@dataclass(frozen=True, slots=True)
class MatchedCurrencies:
    new_and_old_fx_rates_pairs: list[NewAndOldFXRatesPair]
    single_old_fx_rates: list[CurrencyFXRate]
    single_new_fx_rates: list[CurrencyFXRate]
