import httpx

__all__ = (
    'TelegramAPIMethod',
    'TelegramBot',
)


class TelegramAPIMethod:

    def __init__(self, token: str):
        self._token = token
        self._base_url = f'https://api.telegram.org/bot{self._token}'

    @property
    def send_message(self) -> str:
        return self._base_url + '/sendMessage'


class TelegramBot:
    __slots__ = ('_token', 'telegram_api_method')

    def __init__(self, token: str):
        self._token = token
        self.telegram_api_method = TelegramAPIMethod(self._token)

    def send_message(self, chat_id: int, text: str) -> httpx.Response:
        return httpx.post(
            url=self.telegram_api_method.send_message,
            json={'chat_id': chat_id, 'text': text, 'parse_mode': 'html'},
        )
