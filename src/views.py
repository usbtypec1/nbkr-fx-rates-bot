import collections

from models import CurrencyFXRate


def group_fx_rates_by_bank_name(
        currencies_fx_rates: list[tuple[CurrencyFXRate, CurrencyFXRate]],
) -> dict[str, list[tuple[CurrencyFXRate, CurrencyFXRate]]]:
    bank_name_to_currencies_fx_rates = collections.defaultdict(list)
    for (currency_fx_rates) in currencies_fx_rates:
        currency_old_fx_rates, _ = currency_fx_rates
        bank_name_to_currencies_fx_rates[currency_old_fx_rates.bank_name].append(currency_fx_rates)
    return bank_name_to_currencies_fx_rates


def render_fx_rates_delta_view(
        currencies_fx_rates_by_bank_name: dict[str, list[tuple[CurrencyFXRate, CurrencyFXRate]]],
) -> str:
    lines = []
    for bank_name, currencies_fx_rates in currencies_fx_rates_by_bank_name.items():
        lines.append(f'<b>{bank_name}:</b>')
        lines.append('<b>Buy:</b>')
        for currency_fx_rates in currencies_fx_rates:
            currency_old_fx_rates, currency_new_fx_rates = currency_fx_rates
            emoji = '📈' if currency_old_fx_rates.buy_value < currency_new_fx_rates.buy_value else '📉'
            diff = round(100 - (currency_old_fx_rates.buy_value * 100 / currency_new_fx_rates.buy_value), 2)
            diff = f'{diff:+}%'
            lines.append(f'{emoji} {currency_old_fx_rates.iso_code}: <b>{currency_old_fx_rates.buy_value}'
                         f' ➞ {currency_new_fx_rates.buy_value}</b> ({diff})')

        lines.append('<b>Sell:</b>')
        for currency_fx_rates in currencies_fx_rates:
            currency_old_fx_rates, currency_new_fx_rates = currency_fx_rates
            emoji = '📈' if currency_old_fx_rates.sell_value < currency_new_fx_rates.sell_value else '📉'
            diff = round(100 - (currency_old_fx_rates.sell_value * 100 / currency_new_fx_rates.sell_value), 2)
            diff = f'{diff:+}%'
            lines.append(f'{emoji} {currency_old_fx_rates.iso_code}: <b>{currency_old_fx_rates.sell_value}'
                         f' ➞ {currency_new_fx_rates.sell_value}</b> ({diff})')
        lines.append('\n')
    return '\n'.join(lines).rstrip('\n')
