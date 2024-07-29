import logging
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
)

from the_act_bot.src import schemas
import the_act_bot.src.repos as repos
import the_act_bot.src.utils.keyboards as keyboards
from the_act_bot.src.database.session import session_maker
from the_act_bot.src.utils.translation import text


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

NAME, POSITION, ACTIVE = range(3)

async def category_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category_id = query.data.split('_')[-1]

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await context.bot.send_message(text=text['not_admin'])

    context.chat_data['category_id'] = int(category_id)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    await context.bot.send_message(chat_id=query.message.chat_id, text="Введите имя категории на 3 языках(ru, uz, en). Каждый с новой строки.\nПример:\n\nЯблоко\nOlma\nApple\n\nЕсли оно не меняется, отправьте '-'", reply_markup=ReplyKeyboardRemove())
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
        await update.message.reply_text("Введите имя категории на 3 языках(ru, uz, en). Каждый с новой строки.\nПример:\n\nЯблоко\nOlma\nApple\n\nЕсли оно не меняется, отправьте '-'")
        return NAME
    
    if name == '-':
        context.chat_data['new_category_name'] = None
    else:
        name = update.message.text.split('\n')
        context.chat_data['new_category_name'] = {
            'ru': name[0],
            'uz': name[1],
            'en': name[2]
        }
    await update.message.reply_text("Введите позицию в списке категорий (число)\n\nЕсли она не меняется, отправьте '-'")
    return POSITION


async def position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    position = update.message.text
    if not position:
        await update.message.reply_text("Введите позицию в списке категорий (число)\n\nЕсли она не меняется, отправьте '-'")
        return POSITION
    
    context.chat_data['new_category_position'] = position if position != '-' else None
    
    await update.message.reply_text("Категория активна или нет?\nВведите число 1(активна) или 0(отключена)\n\nЕсли оно не меняется, отправьте '-'")
    return ACTIVE


async def active(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    active = update.message.text
    if not active:
        await update.message.reply_text("Категория активна или нет?\nВведите число 1(активна) или 0(отключена)\n\nЕсли оно не меняется, отправьте '-'")
        return ACTIVE
    
    name = context.chat_data['new_category_name']
    position = context.chat_data['new_category_position']
    if active == '-':
        active = None
    else:
        active = bool(int(active))

    async with session_maker() as session:
        category_repo = repos.CategoryRepo(session)
        category = schemas.Category(
            name=name,
            position=position,
            active=active,
        )
        await category_repo.update(context.chat_data['category_id'], category)
    
    await update.message.reply_text("Категория изменена", reply_markup=keyboards.get_admin_main_menu_keyboard())
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang')  # TODO: add cancel btn
    await update.message.reply_text(
        text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )

    return ConversationHandler.END


category_edit_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(category_edit, pattern="^category_edit_\d+$")],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
        POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, position)],
        ACTIVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, active)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
