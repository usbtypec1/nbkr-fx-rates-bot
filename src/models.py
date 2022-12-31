from dataclasses import dataclass
from decimal import Decimal

__all__ = (
    'CurrencyFXRate',
)


@dataclass(frozen=True, slots=True)
class CurrencyFXRate:
    bank_name: str
    iso_code: str
    buy_value: Decimal
    sell_value: Decimal
