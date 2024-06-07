import logging, datetime, re
from telegram import Update, InlineKeyboardMarkup
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

LANGUAGE, FIO, PHONE = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
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
            await update.message.reply_text(text['start']['ru'])
            keyboard = keyboards.language #TODO:
            return LANGUAGE
        else:
            if not user.lang:
                await update.message.reply_text(text['start']['ru'])
                keyboard = keyboards.language#TODO:
                return LANGUAGE
            if not user.name:
                await update.message.reply_text(text['fio'][user.lang])
                return FIO
            else:
                await update.message.reply_text(text['start_final'][user.lang])
                return ConversationHandler.END


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    answer = query.data.split('_')[1]
    context.chat_data['lang'] = answer

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        await user_repo.update(
            telegram_id=effective_user.id,
            user_id=schemas.UserUpdate(
                language=answer,
            )
        )

        await query.edit_message_text(text=text['fio'][answer])
        return FIO


async def fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        await user_repo.update(
            telegram_id=effective_user.id,
            user_id=schemas.UserUpdate(
                name=update.message.text,
            )
        )
        keyboard = keyboards.PHONE #TODO: кнопка отправить контакт
        await update.message.reply_text(text=text['fio'][answer])
        return PHONE


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user = update.effective_user
    phone = update.message.text or update.message.contact.phone_number

    pattern = r"^(\+998)[ .,-]?[0-9]{2}[ .,-]?[0-9]{3}[ .,-]?[0-9]{2}[ .,-]?[0-9]{2}$"
    if not re.match(pattern, phone):
        await update.message.reply_text(text['phone_format'][lang])
        return PHONE
    
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        await user_repo.update(
            telegram_id=effective_user.id,
            user_id=schemas.UserUpdate(
                phone=phone,
            )
        )
        keyboard = keyboards.SHOP #TODO:
        await update.message.reply_text(text=text['fio'][answer])
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang')
    await update.message.reply_text(
        text['canceled'][lang or 'ru']
    )

    return ConversationHandler.END


start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [
                CallbackQueryHandler(language, pattern='^lang_'),
            ],
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, fio)],
            PHONE: [MessageHandler(filters.TEXT & filters.CONTACT & ~filters.COMMAND, phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )