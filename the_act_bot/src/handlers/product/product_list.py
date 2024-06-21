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

CATEGORY, INSTANCE, ACTION = range(3)


async def product_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    await update.message.reply_text(text="Продукты какого бренда вы хотите увидеть?", reply_markup=keyboards.get_product_parents_keyboard(brands))
    return CATEGORY


async def category_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
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

    await query.edit_message_text(text="Продукты какой категории показать?", reply_markup=keyboards.get_product_parents_keyboard(categories, 'category'))
    return INSTANCE


async def instance_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category_id = query.data.split('_')[-1]
    effective_user = update.effective_user
    products = []
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await query.edit_message_text(text=text['not_admin'])

        product_repo = repos.ProductRepo(session)
        products = await product_repo.get_by_category_id(int(category_id))
        if not products:
            await query.edit_message_text(text=text['no_products']['ru'])
            return ConversationHandler.END

    await query.edit_message_text(text="Для действий, выберите продукт:", reply_markup=keyboards.get_instance_keyboard('product', products))
    return ACTION


async def action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product_id = query.data.split('_')[-1]

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text['not_admin'])

        product = await repos.ProductRepo(session).get_by_id(int(product_id))
        info_text = f"<b>Название: {product.name}</b>\nНа складе: {product.stock}\nЦена: {product.price}"
    
        await query.edit_message_text(text=info_text, parse_mode='HTML', reply_markup=keyboards.get_action_keyboard('product', int(product_id)))

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang') #TODO: add cancel btn
    await update.message.reply_text(
        text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )

    return ConversationHandler.END


product_list_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(fr"^{text['list_product']['ru']}$"), product_list)],
    states={
        INSTANCE: [CallbackQueryHandler(instance_list, pattern="^product_parent_")],
        ACTION: [CallbackQueryHandler(action, pattern="^product_instance_")],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
