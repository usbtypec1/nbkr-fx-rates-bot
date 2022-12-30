import json
import pathlib
from configparser import ConfigParser
from dataclasses import dataclass

__all__ = (
    'DATABASE_PATH',
    'SRC_DIR',
    'ROOT_PATH',
    'load_config',
)

ROOT_PATH = pathlib.Path(__file__).parent.parent

SRC_DIR = ROOT_PATH / 'src'

DATABASE_PATH = SRC_DIR / 'database.db'


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot_token: str
    chat_ids: list[int]


def load_config(config_file_path: str | pathlib.Path) -> Config:
    config_parser = ConfigParser()
    config_parser.read(config_file_path)

    telegram_bot = config_parser['telegram_bot']
    token = telegram_bot['token']
    chat_ids = json.loads(telegram_bot['chat_ids'])

    return Config(telegram_bot_token=token, chat_ids=chat_ids)
