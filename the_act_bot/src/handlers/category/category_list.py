import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
)

import the_act_bot.src.repos as repos
import the_act_bot.src.utils.keyboards as keyboards
from the_act_bot.src.database.session import session_maker
from the_act_bot.src.utils.translation import text


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

INSTANCE, ACTION = range(2)


async def category_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            await update.message.reply_text(text['brands'])
            return ConversationHandler.END

    await update.message.reply_text(text="Категории какого бренда вы хотите увидеть?", reply_markup=keyboards.get_category_parents_keyboard(brands))
    return INSTANCE


async def instance_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    brand_id = query.data.split('_')[-1]
    effective_user = update.effective_user
    categories = []
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await query.edit_message_text(text=text['not_admin'])

        category_repo = repos.CategoryRepo(session)
        categories = await category_repo.list_by_brand_id(int(brand_id))
        if not categories:
            await query.edit_message_text(text=text['no_categories']['ru'])
            return ConversationHandler.END

    await query.edit_message_text(text="Для действий, выберите категорию:", reply_markup=keyboards.get_instance_keyboard('category', categories))
    return ACTION


async def action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category_id = query.data.split('_')[-1]

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text['not_admin'])

        category = await repos.CategoryRepo(session).get_by_id(int(category_id))
        info_text = f"<b>Имя: {category.name}</b>\nПозиция: {category.position}\nАктивна: {'Да' if category.active else 'Нет'}"
    
        await query.edit_message_text(text=info_text, parse_mode='HTML', reply_markup=keyboards.get_action_keyboard('category', int(category_id)))

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang')  # TODO: add cancel btn
    await update.message.reply_text(
        text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )

    return ConversationHandler.END


category_list_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(fr"^{text['list_category']['ru']}$"), category_list)],
    states={
        INSTANCE: [CallbackQueryHandler(instance_list, pattern="^category_parent_")],
        ACTION: [CallbackQueryHandler(action, pattern="^category_instance_")],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
