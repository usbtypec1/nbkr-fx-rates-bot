import contextlib
import pathlib
import sqlite3
from typing import Union

import config
from data_types import CurrencyFXRate

__all__ = (
    'insert_currency',
    'update_currency',
    'get_currencies',
    'init_database',
)


@contextlib.contextmanager
def auto_closing_database(database_path: Union[pathlib.Path, str]) -> sqlite3.Cursor:
    """Provides cursor of sqlite database and safely closes it.

    Args:
        database_path: Path to database.

    Returns:
        Cursor of database.
    """
    with (contextlib.closing(sqlite3.connect(database_path)) as connection,
          connection,
          contextlib.closing(connection.cursor()) as cursor):
        yield cursor


def insert_currency(fx_rate: CurrencyFXRate):
    query = 'INSERT INTO currency_fx_rates (iso_code, nominal, value) VALUES (?,?,?);'
    with auto_closing_database(config.DATABASE_PATH) as cursor:
        cursor.execute(query, (fx_rate.iso_code, fx_rate.nominal, fx_rate.value))


def update_currency(fx_rate: CurrencyFXRate):
    query = 'UPDATE currency_fx_rates SET nominal=?, value=? WHERE iso_code=?;'
    with auto_closing_database(config.DATABASE_PATH) as cursor:
        cursor.execute(query, (fx_rate.nominal, fx_rate.value, fx_rate.iso_code))


def get_currencies() -> list[CurrencyFXRate]:
    query = 'SELECT iso_code, nominal, value FROM currency_fx_rates;'
    with auto_closing_database(config.DATABASE_PATH) as cursor:
        cursor.execute(query)
        return [CurrencyFXRate(*row) for row in cursor.fetchall()]


def init_database():
    query = '''
    CREATE TABLE IF NOT EXISTS currency_fx_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT
      , iso_code TEXT NOT NULL UNIQUE
      , nominal INTEGER NOT NULL
      , value FLOAT NOT NULL
    );
    '''
    with auto_closing_database(config.DATABASE_PATH) as cursor:
        cursor.execute(query)
