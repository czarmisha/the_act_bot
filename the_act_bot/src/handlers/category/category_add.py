import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
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

NAME, POSITION, BRAND = range(3)


async def category_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    await update.message.reply_text(text="Введите имя категории на 3 языках(ru, uz, en). Каждый с новой строки.\nПример:\n\nЯблоко\nOlma\nApple", reply_markup=ReplyKeyboardRemove())
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    name = update.message.text.split('\n')
    if not name or not len(name) == 3:
        await update.message.reply_text("Введите имя категории на 3 языках(ru, uz, en). Каждый с новой строки.\nПример:\n\nЯблоко\nOlma\nApple")
        return NAME
    
    context.chat_data['new_category_name'] = {
        'ru': name[0],
        'uz': name[1],
        'en': name[2]
    }
    await update.message.reply_text("Введите позицию в списке категорий (число)")
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
        await update.message.reply_text("Введите позицию в списке категорий (число)")
        return POSITION
    
    context.chat_data['new_category_position'] = position
    async with session_maker() as session:
        brand_repo = repos.BrandRepo(session)
        brands = await brand_repo.list()
        if not brands:
            await update.message.reply_text(text['no_brands']['ru'])
            return ConversationHandler.END
    
    await update.message.reply_text("К какому бренду добавить категорию?", reply_markup=keyboards.get_category_add_brand_list(brands))
    return BRAND


async def brand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    brand_id = query.data.split('_')[-1]

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text['not_admin'])

    category_position = context.chat_data.get('new_category_position')
    if not category_position or not category_position.isdigit():
        await query.edit_message_text(text="Введите позицию в списке категорий (число)")
        return POSITION
    
    category_name = context.chat_data.get('new_category_name')
    if not category_name:
        await query.edit_message_text(text="Введите имя категории на 3 языках(ru, uz, en). Каждый с новой строки.\nПример:\n\nЯблоко\nOlma\nApple")
        return NAME
    
    async with session_maker() as session:
        category_repo = repos.CategoryRepo(session)
        await category_repo.create(
            category_in=schemas.CategoryIn(
                name=category_name,
                position=category_position,
                brand_id=brand_id
            )
        )
    
    await query.edit_message_text(text="Готово, категория добавлена", reply_markup=keyboards.get_admin_main_menu_keyboard())
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang') #TODO: add cancel btn
    await update.message.reply_text(
        text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )

    return ConversationHandler.END


category_add_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(fr"^{text['add_category']['ru']}$"), category_add)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, position)],
            BRAND: [CallbackQueryHandler(brand, pattern="^category_add_brand_")],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
