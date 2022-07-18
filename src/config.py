import os
import pathlib

import exceptions

__all__ = (
    'TELEGRAM_BOT_TOKEN',
    'TELEGRAM_CHAT_IDS',
    'DATABASE_PATH',
    'SRC_DIR',
    'ROOT_PATH',
)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
_chat_ids = os.getenv('TELEGRAM_CHAT_IDS')

if _chat_ids is None:
    raise exceptions.ConfigError('Environment variable "TELEGRAM_CHAT_IDS" is not set')
if TELEGRAM_BOT_TOKEN is None:
    raise exceptions.ConfigError('Environment variable "TELEGRAM_BOT_TOKEN" is not set')

TELEGRAM_CHAT_IDS = [int(chat_id) for chat_id in _chat_ids.split(',')]

ROOT_PATH = pathlib.Path(__file__).parent.parent

SRC_DIR = ROOT_PATH / 'src'

DATABASE_PATH = SRC_DIR / 'database.db'
