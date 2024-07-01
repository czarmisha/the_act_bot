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
from the_act_bot.src.handlers.start import start
import the_act_bot.src.schemas as schemas
import the_act_bot.src.utils.keyboards as keyboards
from the_act_bot.src.database.session import session_maker
from the_act_bot.src.utils.translation import text


BRAND, CATEGORY, PRODUCT = range(3)


async def store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang')
    async with session_maker() as session:
        if not lang:
            user_repo = repos.UserRepo(session)
            user = await user_repo.get_by_telegram_id(update.effective_user.id)
            lang = user.lang
            context.user_data['lang'] = lang

        brand_repo = repos.BrandRepo(session)
        brands = await brand_repo.list()
        if not brands:
            await update.message.reply_text(text['no_brand'][lang])
            return ConversationHandler.END
    
    keyboard = keyboards.get_brand_keyboard_markup(brands)
    await update.message.reply_text(text['select_brand'][lang], reply_markup=keyboard)
    return BRAND


async def brand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang')
    if update.message.text in [text['back']['ru'], text['back']['uz'], text['back']['en']]:
        return await start(update, context)
    async with session_maker() as session:
        if not lang:
            user_repo = repos.UserRepo(session)
            user = await user_repo.get_by_telegram_id(update.effective_user.id)
            lang = user.lang
            context.user_data['lang'] = lang
        
        brand_repo = repos.BrandRepo(session)
        brand = await brand_repo.get_by_name(update.message.text)
        if not brand:
            await update.message.reply_text(text['brand_not_found'][lang])
            return BRAND
        context.user_data['selected_brand_id'] = brand.id

        category_repo = repos.CategoryRepo(session)
        categories = await category_repo.list_by_brand_id(brand_id=brand.id)
        if not categories:
            await update.message.reply_text(text['no_category'][lang])
            return ConversationHandler.END

    keyboard = keyboards.get_category_keyboard_markup(categories, lang)
    await update.message.reply_text(text['select_category'][lang], reply_markup=keyboard)
    return CATEGORY


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang')
    if update.message.text in [text['back']['ru'], text['back']['uz'], text['back']['en']]:
        return await store(update, context)
    async with session_maker() as session:
        category_repo = repos.CategoryRepo(session)
        category = await category_repo.get_by_name_and_brand_id(update.message.text, context.user_data['selected_brand_id'])
        if not category:
            await update.message.reply_text(text['category_not_found'][lang])
            return CATEGORY
        context.user_data['selected_category_id'] = category.id

        product_repo = repos.ProductRepo(session)
        products = await product_repo.list_by_brand_and_category(
            category_id=context.user_data['selected_category_id'],
            brand_id=context.user_data['selected_brand_id']
        )
        if not products:
            await update.message.reply_text(text['no_product'][lang])
            return ConversationHandler.END

    keyboard = keyboards.get_product_keyboard_markup(products, lang)
    await update.message.reply_text(text['select_product'][lang], reply_markup=keyboard)
    return PRODUCT


async def product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang')
    if update.message.text in [text['back']['ru'], text['back']['uz'], text['back']['en']]:
        return await brand(update, context)
    async with session_maker() as session:
        product_repo = repos.ProductRepo(session)
        product = await product_repo.get(update.message.text)
        if not product:
            await update.message.reply_text(text['product_not_found'][lang])
            return PRODUCT

    await update.message.reply_text(
        text['product_info'][lang].format(
            name=product.name[lang],
            price=product.price,
            description=product.description[lang],
        )
    )
    return ConversationHandler.END


store_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex(text['shop']['ru']), store
        ),
        MessageHandler(
            filters.Regex(text['shop']['uz']), store
        ),
        MessageHandler(
            filters.Regex(text['shop']['en']), store
        ),
    ],
    states={
        BRAND: [MessageHandler(filters.TEXT, brand)],
        CATEGORY: [MessageHandler(filters.TEXT, category)],
        PRODUCT: [MessageHandler(filters.TEXT, product)],
    },
    fallbacks=[CommandHandler('cancel', lambda update, context: ConversationHandler.END)],
)