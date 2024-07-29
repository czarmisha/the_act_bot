from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    filters,
    CallbackQueryHandler
)

import the_act_bot.src.repos as repos
from the_act_bot.src.handlers.start import start
from the_act_bot.src.utils.cart import get_cart_text
import the_act_bot.src.utils.keyboards as keyboards
from the_act_bot.src.database.session import session_maker
from the_act_bot.src.utils.translation import text


BRAND, CATEGORY, PRODUCT, CART_ADD = range(4)


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
            await update.message.reply_text(text['no_brands'][lang])
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
            return ConversationHandler.END
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
        category = await category_repo.get_by_name_and_brand_id(
            update.message.text,
            context.user_data['selected_brand_id']
        )
        if not category:
            context.bot.send_message(chat_id=update.effective_chat.id, text=text['category_not_found'][lang])
            return BRAND
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
        return await store(update, context)
    elif update.message.text in [text['cart']['ru'], text['cart']['uz'], text['cart']['en']]:
        async with session_maker() as session:
            user_id = context.user_data.get('user_id', None)
            if not user_id:
                user_repo = repos.UserRepo(session)
                user = await user_repo.get_by_telegram_id(update.effective_user.id)
                user_id = user.id
            cart_repo = repos.CartRepo(session)
            cart = await cart_repo.get_by_user_id(user_id)
            cart_info = await cart_repo.get_info(cart.id)
            cart_text = await get_cart_text(cart_info, lang)
            # TODO: inline keyboard for cart to remove and add items
            await update.message.reply_text(cart_text, reply_markup=keyboards.get_main_menu_keyboard(lang))
        return ConversationHandler.END
    async with session_maker() as session:
        if not lang:
            user_repo = repos.UserRepo(session)
            user = await user_repo.get_by_telegram_id(update.effective_user.id)
            lang = user.lang
            context.user_data['lang'] = lang

        product_repo = repos.ProductRepo(session)
        product = await product_repo.get_by_category_id_and_brand_id(
            context.user_data['selected_category_id'],
            context.user_data['selected_brand_id'],
            update.message.text
        )
        if not product:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text['product_not_found'][lang])
            return CATEGORY

        image_repo = repos.ImageRepo(session)
        images = await image_repo.get_by_product_id(int(product.id))

    info_text = f"<b>Имя: {product.name}</b>\n\n{product.description[lang]}\n\nЦена: {product.price}"
    context.user_data['to_add_product_id'] = product.id
    context.user_data['to_add'] = 1
    if not images:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=info_text,
            parse_mode='HTML',
            reply_markup=keyboards.add_product_to_cart(product.id, lang, context.user_data['to_add'])
        )
    else:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=images[0].tg_file_id,
            caption=info_text,
            parse_mode='HTML',
            reply_markup=keyboards.add_product_to_cart(product.id, lang, context.user_data['to_add'])
        )

    return CART_ADD


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
    if query.data == 'add_to_cart_back':
        async with session_maker() as session:
            product_repo = repos.ProductRepo(session)
            products = await product_repo.list_by_brand_and_category(
                category_id=context.user_data['selected_category_id'],
                brand_id=context.user_data['selected_brand_id']
            )
            if not products:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=text['no_product'][lang])
                return ConversationHandler.END

        keyboard = keyboards.get_product_keyboard_markup(products, lang)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text['select_product_continue'][lang],
            reply_markup=keyboard
        )
        return PRODUCT
    elif query.data.startswith('product_minus_'):
        return await product_minus(update, context)
    elif query.data.startswith('product_plus_'):
        return await product_plus(update, context)

    product_id = query.data.split('_')[-2]
    to_add = query.data.split('_')[-1]

    if not cart:
        async with session_maker() as session:
            cart_repo = repos.CartRepo(session)
            cart = await cart_repo.create(user.id)
            cart = await cart_repo.add_item(cart.id, int(product_id), int(to_add))
    else:
        async with session_maker() as session:
            cart_repo = repos.CartRepo(session)
            cart = await cart_repo.add_item(cart.id, int(product_id), int(to_add))

    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text['added_to_cart'][lang],
    )

    async with session_maker() as session:
        product_repo = repos.ProductRepo(session)
        products = await product_repo.list_by_brand_and_category(
            category_id=context.user_data['selected_category_id'],
            brand_id=context.user_data['selected_brand_id']
        )
        if not products:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text['no_product'][lang])
            return ConversationHandler.END

    keyboard = keyboards.get_product_keyboard_markup(products, lang)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text['select_product_continue'][lang],
        reply_markup=keyboard
    )
    return PRODUCT


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

    return CART_ADD


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

    return CART_ADD


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang')  # TODO: add cancel btn
    await update.message.reply_text(
        text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )

    return ConversationHandler.END


async def callback_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data.get('lang')
    query = update.callback_query
    await query.answer()
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_main_menu_keyboard(lang or 'ru')
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
        CART_ADD: [
            CallbackQueryHandler(cart_add, pattern="^add_to_cart_"),
            CallbackQueryHandler(product_minus, pattern="^product_minus_"),
            CallbackQueryHandler(product_plus, pattern="^product_plus_"),
            CallbackQueryHandler(cart_add, pattern="^add_to_cart_back$")
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        CallbackQueryHandler(callback_cancel, pattern="^store_cancel$")
    ],
)
