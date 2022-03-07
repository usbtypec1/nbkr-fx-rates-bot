import config
import db

import national_bank
import utils
from telegram import TelegramBot


def main():
    telegram_bot = TelegramBot(config.TELEGRAM_BOT_TOKEN)
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
        for chat_id in config.TELEGRAM_CHAT_IDS:
            telegram_bot.send_message(chat_id, text)
        db.update_currency(fx_rate_pairs.new)


if __name__ == '__main__':
    main()
