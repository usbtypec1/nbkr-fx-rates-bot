import logging
import pathlib
import traceback
from typing import TypedDict, Callable, TypeVar

from data_types import CurrencyFXRate
from db import SqliteDatabase, upsert_currency_fx_rates, init_database, get_currency_fx_rates
import exceptions

from config import load_config
from banks.parsers import parse_commercial_bank_fx_rates, parse_national_bank_fx_rates
from banks.api import get_national_bank_fx_rates, get_commercial_bank_fx_rates
from views import group_fx_rates_by_bank_name, render_fx_rates_delta_view
from telegram import TelegramBot

T = TypeVar('T')


class Strategy(TypedDict):
    api_callback: Callable[[], T]
    parser_callback: Callable[[T], list[CurrencyFXRate]]


strategies: tuple[Strategy, ...] = (
    {
        'api_callback': get_commercial_bank_fx_rates,
        'parser_callback': parse_commercial_bank_fx_rates,
    },
    {
        'api_callback': get_national_bank_fx_rates,
        'parser_callback': parse_national_bank_fx_rates,
    },
)


def main():
    database_file_path = pathlib.Path(__file__).parent.parent / 'database.db'
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.ini'
    config = load_config(config_file_path)

    telegram_bot = TelegramBot(config.telegram_bot_token)
    database = SqliteDatabase(database_file_path)
    currencies_fx_rates: list[CurrencyFXRate] = []

    for strategy in strategies:
        api_callback = strategy['api_callback']
        parser_callback = strategy['parser_callback']

        try:
            raw_fx_rates = api_callback()
        except exceptions.BankAPIError:
            logging.error('Could not load data from banks API')
            continue

        try:
            currencies_fx_rates += parser_callback(raw_fx_rates)
        except Exception:
            # log all available exceptions to catch only them in the future
            logging.error(traceback.format_exc())
            continue

    changed_currency_fx_rates = []
    with database.closing_connection() as connection:
        init_database(connection)
        for new_currency_fx_rates in currencies_fx_rates:
            try:
                old_currency_fx_rates = get_currency_fx_rates(
                    connection=connection,
                    bank_name=new_currency_fx_rates.bank_name,
                    iso_code=new_currency_fx_rates.iso_code,
                )
            except exceptions.FXRateNotFoundError:
                logging.warning('FX rates not found in database')
            else:
                if new_currency_fx_rates == old_currency_fx_rates:
                    continue
                changed_currency_fx_rates.append((old_currency_fx_rates, new_currency_fx_rates))
            finally:
                upsert_currency_fx_rates(connection, currency_fx_rates=new_currency_fx_rates)

    if not changed_currency_fx_rates:
        return
    grouped_currency_fx_rates = group_fx_rates_by_bank_name(changed_currency_fx_rates)
    rendered_view = render_fx_rates_delta_view(grouped_currency_fx_rates)

    for chat_id in config.chat_ids:
        telegram_bot.send_message(chat_id, rendered_view)


if __name__ == '__main__':
    main()
