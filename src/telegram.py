import httpx

__all__ = ('TelegramBot',)


class TelegramBot:
    __slots__ = ('_token', 'telegram_api_method')

    def __init__(self, token: str):
        self._token = token

    @property
    def base_url(self) -> str:
        return f'https://api.telegram.org/bot{self._token}'

    def send_message(self, chat_id: int, text: str) -> bool:
        url = f'{self.base_url}/sendMessage'
        response = httpx.post(url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'html'})
        return response.is_success
