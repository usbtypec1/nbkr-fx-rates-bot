import json
import urllib.request

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

    def send_message(self, chat_id: int, text: str) -> bool:
        request = urllib.request.Request(self.telegram_api_method.send_message, method='POST')
        request.add_header('Content-Type', 'application/json')
        data = json.dumps({'chat_id': chat_id, 'text': text, 'parse_mode': 'html'}).encode('utf-8')
        with urllib.request.urlopen(request, data) as response:
            return response.status == 200
