import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
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

NAME, POSITION = range(2)


async def brand_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    await update.message.reply_text(text="Введите имя бренда", reply_markup=ReplyKeyboardRemove())
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    name = update.message.text
    if not name:
        await update.message.reply_text("Введите имя бренда")
        return NAME
    
    context.chat_data['new_brand_name'] = name
    await update.message.reply_text("Введите позицию в списке брендов (число)")
    return POSITION


async def position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    position = update.message.text
    if not position or not position.isdigit():
        await update.message.reply_text("Введите позицию в списке брендов (число)")
        return POSITION
    
    brand_name = context.chat_data.get('new_brand_name')
    if not brand_name:
        await update.message.reply_text("Введите имя бренда")
        return NAME
    
    async with session_maker() as session:
        brand_repo = repos.BrandRepo(session)
        await brand_repo.create(
            brand_in=schemas.BrandIn(
                name=brand_name,
                position=int(position),
            )
        )
    
    await update.message.reply_text("Готово, бренд добавлен", reply_markup=keyboards.get_admin_main_menu_keyboard())
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang') #TODO: add cancel btn
    await update.message.reply_text(
        text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )

    return ConversationHandler.END


brand_add_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(fr"^{text['add_brand']['ru']}$"), brand_add)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, position)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
