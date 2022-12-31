import httpx
import pytest

from telegram import TelegramBot


@pytest.fixture
def telegram_bot():
    return TelegramBot(token='hellokitty')


def test_base_url(telegram_bot):
    assert telegram_bot.base_url == 'https://api.telegram.org/bothellokitty'


def test_send_message(telegram_bot, monkeypatch):
    class FakeResponse:
        @property
        def is_success(self) -> int:
            return 200

    def fake_post(*args, **kwargs) -> FakeResponse:
        return FakeResponse()

    monkeypatch.setattr(httpx, 'post', fake_post)
    assert telegram_bot.send_message(chat_id=2020202002, text='hello') == 200
