from api import telegram_bot as tg_bot
from pathlib import Path


token = Path("Telegram Bot/Token.txt").read_text()

language_path = "Telegram Bot/languages.csv"
rate_path = None


print("\n◢ Telegram_bot was started ◣\n")

tg_bot.TelegramBot(token, language_path, rate_path).run()

print("\n◥ Telegram_bot was stopped ◤\n")
