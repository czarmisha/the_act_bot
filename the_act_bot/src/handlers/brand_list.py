import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
)

import the_act_bot.src.repos as repos
import the_act_bot.src.schemas as schemas
import the_act_bot.src.utils.keyboards as keyboards
from the_act_bot.src.database.session import session_maker
from the_act_bot.src.utils.translation import text


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

ACTION = range(1)


async def brand_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    brands = []
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

        brand_repo = repos.BrandRepo(session)
        brands = await brand_repo.list()
        if not brands:
            await update.message.reply_text(text['no_brands'])
            return ConversationHandler.END

    await update.message.reply_text(text="Для действий, выберите бренд из списка ниже:", reply_markup=keyboards.get_instance_keyboard('brand', brands))
    return ACTION


async def action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    brand_id = query.data.split('_')[-1]

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text['not_admin'])

        brand = await repos.BrandRepo(session).get_by_id(int(brand_id))
        info_text = f"<b>Имя: {brand.name}</b>\nПозиция: {brand.position}"
    
        await query.edit_message_text(text=info_text, parse_mode='HTML', reply_markup=keyboards.get_action_keyboard('brand'))

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang')
    await update.message.reply_text(
        text['canceled'][lang or 'ru']
    )

    return ConversationHandler.END


brand_list_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(fr"^{text['list_brand']['ru']}$"), brand_list)],
        states={
            ACTION: [CallbackQueryHandler(action, pattern="^brand_instance_")],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
