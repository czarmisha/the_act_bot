import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
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

CONFIRMATION, ACTION = range(2)

async def product_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product_id = query.data.split('_')[-1]

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await context.bot.send_message(text=text['not_admin'])

        product_repo = repos.ProductRepo(session)
        product = await product_repo.get_by_id(int(product_id))
        if not product:
            await context.bot.send_message(text=text['no_products'])
            return ConversationHandler.END
    info_text = f"<b>Имя: {product.name}</b>\nНа складе: {product.stock}\nЦена: {product.price}"

    await query.edit_message_text(
        text=f"Точно удалить?\n\n{info_text}\n\nВместе будут удалены все связанные объекты",
        reply_markup=keyboards.get_remove_confirmation_keyboard(prefix='product', id=int(product_id)),
        parse_mode='HTML'
    )
    return ACTION


async def action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    confirmation = query.data.split('_')[-1]
    is_confirmed = True if confirmation == 'yes' else False
    if not is_confirmed:
        await query.edit_message_text(text="Отменено")
        return ConversationHandler.END

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await context.bot.send_message(text=text['not_admin'])

        product_repo = repos.ProductRepo(session)
        await product_repo.remove(id=int(query.data.split('_')[-2]))
        

    await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    await context.bot.send_message(chat_id=query.message.chat_id, text="Продукт удален", reply_markup=keyboards.get_admin_main_menu_keyboard())
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang')  # TODO: add cancel btn
    await update.message.reply_text(
        text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )

    return ConversationHandler.END


product_remove_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(product_remove, pattern="^product_remove_\d+$")],
    states={
        ACTION: [CallbackQueryHandler(action, pattern="^product_remove_confirmation_")],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

