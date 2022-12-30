import pathlib

import db

import national_bank
from config import load_config
import utils
from telegram import TelegramBot


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.ini'
    config = load_config(config_file_path)

    telegram_bot = TelegramBot(config.telegram_bot_token)
    db.init_database()
    new_fx_rates = national_bank.parse_fx_rates_xml(national_bank.get_fx_rates())
    old_fx_rates = db.get_currencies()
    matched_currencies = utils.match_currencies(old_fx_rates, new_fx_rates)

    for new_fx_rate in matched_currencies.single_new_fx_rates:
        db.insert_currency(new_fx_rate)
    for fx_rate_pairs in matched_currencies.new_and_old_fx_rates_pairs:
        if fx_rate_pairs.old.value == fx_rate_pairs.new.value:
            continue
        text = utils.format_changed_fx_rate_text(fx_rate_pairs.old, fx_rate_pairs.new)
        for chat_id in config.chat_ids:
            telegram_bot.send_message(chat_id, text)
        db.update_currency(fx_rate_pairs.new)


if __name__ == '__main__':
    main()
