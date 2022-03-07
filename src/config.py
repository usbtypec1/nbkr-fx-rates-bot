import pathlib

from environs import Env

__all__ = (
    'TELEGRAM_BOT_TOKEN',
    'TELEGRAM_CHAT_IDS',
    'DATABASE_PATH',
    'SRC_DIR',
)

env = Env()
env.read_env()

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_IDS = env.list('TELEGRAM_CHAT_IDS', subcast=int)

SRC_DIR = pathlib.Path(__file__).parent

DATABASE_PATH = SRC_DIR / 'database.db'
