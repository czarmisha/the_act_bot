import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
)

import the_act_bot.src.repos as repos
import the_act_bot.src.utils.keyboards as keyboards
from the_act_bot.src.database.session import session_maker
from the_act_bot.src.utils.translation import text


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def cart_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang')
    user = None
    cart = None
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        user = await user_repo.get_by_telegram_id(update.effective_user.id)
        cart = await user_repo.get_cart(user.id)
        if not lang:
            lang = user.lang
            context.user_data['lang'] = lang

    query = update.callback_query
    await query.answer()
    product_id = query.data.split('_')[-2]
    to_add = query.data.split('_')[-1]

    async with session_maker() as session:
        cart_repo = repos.CartRepo(session)
        if not cart:
            cart = await cart_repo.create(user.id)
            cart = await cart_repo.add_item(cart.id, int(product_id), int(to_add))
        else:
            cart = await cart_repo.add_item(cart.id, int(product_id), int(to_add))

    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text['added_to_cart'][lang], 
        reply_markup=keyboards.get_main_menu_keyboard(lang)
    )


async def product_minus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang')
    if not lang:
        async with session_maker() as session:
            user_repo = repos.UserRepo(session)
            user = await user_repo.get_by_telegram_id(update.effective_user.id)
            lang = user.lang
            context.user_data['lang'] = lang

    query = update.callback_query
    await query.answer()
    product_id = query.data.split('_')[-2]
    to_add = query.data.split('_')[-1]
    if int(context.user_data.get('to_add', 1)) == 1:
        return
    to_add = int(to_add) - 1
    context.user_data['to_add'] = to_add
    await query.edit_message_reply_markup(reply_markup=keyboards.add_product_to_cart(int(product_id), lang, to_add))


async def product_plus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang')
    if not lang:
        async with session_maker() as session:
            user_repo = repos.UserRepo(session)
            user = await user_repo.get_by_telegram_id(update.effective_user.id)
            lang = user.lang
            context.user_data['lang'] = lang

    query = update.callback_query
    await query.answer()
    product_id = query.data.split('_')[-2]
    if int(context.user_data.get('to_add')) == 10:
        return
    to_add = query.data.split('_')[-1]
    to_add = int(to_add) + 1
    context.user_data['to_add'] = to_add
    await query.edit_message_reply_markup(reply_markup=keyboards.add_product_to_cart(int(product_id), lang, to_add))


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang')  # TODO: add cancel btn
    await update.message.reply_text(
        text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )

    return ConversationHandler.END


cart_add_handler = CallbackQueryHandler(cart_add, pattern="^add_to_cart_")
product_minus_handler = CallbackQueryHandler(product_minus, pattern="^product_minus_")
product_plus_handler = CallbackQueryHandler(product_plus, pattern="^product_plus_")
