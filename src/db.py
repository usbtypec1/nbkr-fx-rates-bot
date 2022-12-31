import contextlib
import pathlib
import sqlite3
from decimal import Decimal

import exceptions
from models import CurrencyFXRate

__all__ = (
    'SqliteDatabase',
    'get_currency_fx_rates',
    'init_database',
    'upsert_currency_fx_rates',
)


class SqliteDatabase:

    def __init__(self, database_file_path: str | pathlib.Path):
        self.__database_file_path = database_file_path

    @contextlib.contextmanager
    def closing_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.__database_file_path)
        with contextlib.closing(connection):
            yield connection


def init_database(connection: sqlite3.Connection) -> None:
    query = '''
    CREATE TABLE IF NOT EXISTS fx_rates (
        bank_name TEXT NOT NULL,
        iso_code TEXT NOT NULL,
        buy_value TEXT NOT NULL,
        sell_value TEXT NOT NULL,
        UNIQUE (bank_name, iso_code) ON CONFLICT IGNORE
    );
    '''
    connection.execute(query)
    connection.commit()


def upsert_currency_fx_rates(connection: sqlite3.Connection, currency_fx_rates: CurrencyFXRate) -> None:
    query = '''
    INSERT INTO fx_rates (bank_name, iso_code, buy_value, sell_value) 
        VALUES (?,?,?,?)
    ON CONFLICT(bank_name, iso_code) DO 
        UPDATE SET buy_value = ?, sell_value = ?
        WHERE bank_name = ? AND iso_code = ?;
    '''
    params = (
        currency_fx_rates.bank_name,
        currency_fx_rates.iso_code,
        str(currency_fx_rates.buy_value),
        str(currency_fx_rates.sell_value),
        str(currency_fx_rates.buy_value),
        str(currency_fx_rates.sell_value),
        currency_fx_rates.bank_name,
        currency_fx_rates.iso_code,
    )
    cursor = connection.cursor()
    with contextlib.closing(cursor):
        cursor.execute(query, params)
        connection.commit()


def get_currency_fx_rates(connection: sqlite3.Connection, bank_name: str, iso_code: str) -> CurrencyFXRate:
    query = 'SELECT bank_name, iso_code, buy_value, sell_value FROM fx_rates WHERE bank_name = ? AND iso_code = ?;'
    params = (bank_name, iso_code)
    cursor = connection.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    if not row:
        raise exceptions.FXRateNotFoundError
    bank_name, iso_code, buy_value, sell_value = row
    return CurrencyFXRate(
        bank_name=bank_name,
        iso_code=iso_code,
        buy_value=Decimal(buy_value),
        sell_value=Decimal(sell_value),
    )
