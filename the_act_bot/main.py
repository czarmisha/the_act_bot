from telegram import Update
from telegram.ext import Application

from the_act_bot.src.core.config import settings
from the_act_bot.src.handlers import (
    start_handler,
    brand,
    category,
)


if __name__ == '__main__':
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    application.add_handler(start_handler)
    application.add_handler(brand.brand_add_handler)
    application.add_handler(brand.brand_list_handler)
    application.add_handler(brand.brand_remove_handler)
    application.add_handler(brand.brand_edit_handler)
    application.add_handler(category.category_list_handler)
    application.add_handler(category.category_add_handler)
    application.add_handler(category.category_edit_handler)
    application.add_handler(category.category_remove_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
