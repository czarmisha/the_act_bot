from telegram import Update
from telegram.ext import Application

from the_act_bot.src.core.config import settings
from the_act_bot.src.handlers import start_handler


if __name__ == '__main__':
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    application.add_handler(start_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
