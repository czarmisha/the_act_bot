import logging, re
from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
)

from the_act_bot.src.database import enums
import the_act_bot.src.repos as repos
import the_act_bot.src.schemas as schemas
import the_act_bot.src.utils.keyboards as keyboards
from the_act_bot.src.database.session import session_maker
from the_act_bot.src.utils.translation import text


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

LANGUAGE, FIO, PHONE = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    is_admin = False
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        user = await user_repo.get_by_telegram_id(effective_user.id)
        if not user:
            logger.info(f'new user {effective_user.id}')
            user = await user_repo.create(
                schemas.UserIn(
                    telegram_id=effective_user.id,
                )
            )
            keyboard = keyboards.get_lang_keyboard_markup()
            await update.message.reply_text(text['start']['ru'], reply_markup=keyboard)
            return LANGUAGE
        else:
            if not user.lang:
                keyboard = keyboards.get_lang_keyboard_markup()
                await update.message.reply_text(text['start']['ru'], reply_markup=keyboard)
                return LANGUAGE
            if not user.name:
                await update.message.reply_text(text['fio'][user.lang])
                return FIO
            if not user.phone:
                keyboard = keyboards.get_phone_keyboard_markup(user.lang)
                await update.message.reply_text(text['phone'][user.lang], reply_markup=keyboard)
                return PHONE
            else:
                is_admin = await user_repo.is_admin(effective_user.id)
                if is_admin:
                    keyboard = keyboards.get_admin_main_menu_keyboard()
                else:
                    keyboard = keyboards.get_main_menu_keyboard()

                await update.message.reply_text(text['start_final'][user.lang], reply_markup=keyboard)
                return ConversationHandler.END


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    answer = query.data.split('_')[1]
    context.chat_data['lang'] = answer

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        await user_repo.update(
            telegram_id=effective_user.id,
            user_in=schemas.UserUpdate(
                lang=answer,
            )
        )

        await query.edit_message_text(text=text['fio'][answer])
        return FIO


async def fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    lang = context.chat_data.get('lang')
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        await user_repo.update(
            telegram_id=effective_user.id,
            user_in=schemas.UserUpdate(
                name=update.message.text,
            )
        )

        if not lang:
            user = await user_repo.get_by_telegram_id(effective_user.id)
            lang = user.lang

    keyboard = keyboards.get_phone_keyboard_markup(lang)
    await update.message.reply_text(text=text['phone'][lang], reply_markup=keyboard)
    return PHONE


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    phone = update.message.contact.phone_number
    lang = context.chat_data.get('lang')
    is_admin = False
    if not lang:
        async with session_maker() as session:
            user_repo = repos.UserRepo(session)
            user = await user_repo.get_by_telegram_id(effective_user.id)
            lang = user.lang

    pattern = r"^(\+998)[ .,-]?[0-9]{2}[ .,-]?[0-9]{3}[ .,-]?[0-9]{2}[ .,-]?[0-9]{2}$"
    if not re.match(pattern, phone):
        await update.message.reply_text(text['phone_format'][lang])
        return PHONE
    
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        await user_repo.update(
            telegram_id=effective_user.id,
            user_in=schemas.UserUpdate(
                phone=phone,
            )
        )
        is_admin = await user_repo.is_admin(effective_user.id)

    if is_admin:
        keyboard = keyboards.get_admin_main_menu_keyboard()
    else:
        keyboard = keyboards.get_main_menu_keyboard()
    await update.message.reply_text(text['start_final'][lang], reply_markup=keyboard)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang')  # TODO: add cancel btn
    await update.message.reply_text(
        text['canceled'][lang or 'ru'],
        reply_markup=keyboards.get_admin_main_menu_keyboard()
    )

    return ConversationHandler.END


start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [
                CallbackQueryHandler(language, pattern='^lang_'),
            ],
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, fio)],
            PHONE: [MessageHandler(filters.CONTACT & ~filters.COMMAND, phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )