import logging
from telegram import Update, ReplyKeyboardRemove, PhotoSize
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

NAME, DESCRIPTION_RU, DESCRIPTION_UZ, DESCRIPTION_EN, STOCK, PRICE, BRAND, CATEGORY, IMAGES = range(9)


async def product_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    await update.message.reply_text(text="Введите имя продукта", reply_markup=ReplyKeyboardRemove())
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
        await update.message.reply_text("Введите имя продукта")
        return NAME
    
    context.chat_data['new_product_name'] = name
    await update.message.reply_text("Введите описание продукта на русском")
    return DESCRIPTION_RU


async def description_ru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    description = update.message.text
    if not description:
        await update.message.reply_text("Введите имя продукта")
        return NAME
    
    context.chat_data['new_product_description_ru'] = description
    await update.message.reply_text("Введите описание продукта на узбекском")
    return DESCRIPTION_UZ


async def description_uz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    description = update.message.text
    if not description:
        await update.message.reply_text("Введите имя продукта")
        return NAME
    
    context.chat_data['new_product_description_uz'] = description
    await update.message.reply_text("Введите описание продукта на английском")
    return DESCRIPTION_EN


async def description_en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    description = update.message.text
    if not description:
        await update.message.reply_text("Введите имя продукта")
        return NAME
    
    context.chat_data['new_product_description_en'] = description
    await update.message.reply_text("Введите количество продукции на складе (число)")
    return STOCK


async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    stock = update.message.text
    if not stock or not stock.isdigit():
        await update.message.reply_text("Введите количество продукции на складе (число)")
        return STOCK
    
    context.chat_data['new_product_stock'] = stock
    await update.message.reply_text("Введите цену продажи в сумах (число)")
    return PRICE


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])

    price = update.message.text
    if not price or not price.isdigit():
        await update.message.reply_text("Введите цену продажи в сумах (число)")
        return PRICE
    
    async with session_maker() as session:
        brand_repo = repos.BrandRepo(session)
        brands = await brand_repo.list()
        if not brands:
            await update.message.reply_text(text['no_brands']['ru'])
            return ConversationHandler.END
        
    context.chat_data['new_product_price'] = price
    
    await update.message.reply_text("К какому бренду добавить продукт?", reply_markup=keyboards.get_product_add_brand_list(brands))
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
    
    async with session_maker() as session:
        category_repo = repos.CategoryRepo(session)
        categories = await category_repo.list_by_brand_id(int(brand_id))
        if not categories:
            await update.message.reply_text(text['no_categories']['ru'])
            return ConversationHandler.END
        
    await query.edit_message_text(text="К какой категории добавить продукт?", reply_markup=keyboards.get_product_add_category_list(categories))
    return CATEGORY


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category_id = query.data.split('_')[-1]

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text['not_admin'])
    
    async with session_maker() as session:
        product_repo = repos.ProductRepo(session)
        product = await product_repo.create(
            product_in=schemas.ProductIn(
                name=context.chat_data['new_product_name'],
                description={
                    'ru': context.chat_data['new_product_description_ru'],
                    'uz': context.chat_data['new_product_description_uz'],
                    'en': context.chat_data['new_product_description_en']
                },
                stock=int(context.chat_data['new_product_stock']),
                price=int(context.chat_data['new_product_price']),
            )
        )
        await product_repo.add_category(
            product_id=product.id,
            category_id=int(category_id)
        )
    
    context.chat_data['new_product_id'] = product.id
    
    await query.edit_message_text(text="Готово, теперь кидай картинки (все разом, не больше 3х)")
    return IMAGES


async def images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await update.message.reply_text(text['not_admin'])
    
    images = update.message.photo
    if not images:
        await update.message.reply_text("Кидай картинки")
        return IMAGES
    
    async with session_maker() as session:
        image_repo = repos.ImageRepo(session)
        for image in images:
            img = await image.get_file()
            await image_repo.create(
                schemas.ImageIn(
                    product_id=int(context.chat_data['new_product_id']),
                    tg_file_path=img.file_path,
                    tg_file_id=img.file_id,
                    tg_file_unique_id=img.file_unique_id,
                )
            )
    
    await update.message.reply_text(
        "Продукт добавлен, картинки сохранены",
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang') #TODO: add cancel btn
    await update.message.reply_text(
        text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )

    return ConversationHandler.END


product_add_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(fr"^{text['add_product']['ru']}$"), product_add)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            DESCRIPTION_RU: [MessageHandler(filters.TEXT & ~filters.COMMAND, description_ru)],
            DESCRIPTION_UZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, description_uz)],
            DESCRIPTION_EN: [MessageHandler(filters.TEXT & ~filters.COMMAND, description_en)],
            STOCK: [MessageHandler(filters.TEXT & ~filters.COMMAND, stock)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price)],
            BRAND: [CallbackQueryHandler(brand, pattern='^product_add_brand_')],
            CATEGORY: [CallbackQueryHandler(category, pattern='^product_add_category_')],
            IMAGES: [MessageHandler(filters.PHOTO, images)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
