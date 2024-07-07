from telegram import Update
from telegram.ext import Application

from the_act_bot.src.core.config import settings
from the_act_bot.src.handlers import (
    start_handler,
    brand,
    category,
    product,
    store,
    cart,
)


if __name__ == '__main__':
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()

    #user handlers
    application.add_handler(start_handler)
    application.add_handler(store.store_handler)

    application.add_handler(cart.cart_add_handler)
    application.add_handler(cart.product_minus_handler)
    application.add_handler(cart.product_plus_handler)

    #admin handlers
    application.add_handler(brand.brand_add_handler)
    application.add_handler(brand.brand_list_handler)
    application.add_handler(brand.brand_remove_handler)
    application.add_handler(brand.brand_edit_handler)

    application.add_handler(category.category_list_handler)
    application.add_handler(category.category_add_handler)
    application.add_handler(category.category_edit_handler)
    application.add_handler(category.category_remove_handler)

    application.add_handler(product.product_list_handler)
    application.add_handler(product.product_add_handler)
    application.add_handler(product.product_edit_handler)
    application.add_handler(product.product_remove_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
