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
            return LANGUAGE
        else:
            if not user.lang:
                await update.message.reply_text(text['start']['ru'])
                return LANGUAGE
            if not user.name:
                await update.message.reply_text(text['fio'][user.lang])
                return FIO
            else:
                await update.message.reply_text(text['start_final'][user.lang])
                return ConversationHandler.END
    
#     if not candidate:
#         candidate = Candidate(
#             tg_id =user.id, chat_id=update.effective_chat.id,
#             created=datetime.datetime.now(), last_activity=datetime.datetime.now()
#         )
#         session.add(candidate)
#         session.commit()
#         context.chat_data['user_id'] = candidate.id
#         lang = 'ru'
#         keyboard = lang_keyboard()
#         await update.message.reply_text(text['select_lang'][lang], reply_markup=InlineKeyboardMarkup(keyboard))
#         return LANGUAGE
#     else:
#         candidate.last_activity = datetime.datetime.now()
#         session.add(candidate)
#         session.commit()
#         lang = candidate.language
#         context.chat_data['lang'] = lang
#         context.chat_data['user_id'] = candidate.id
#         stmt = select(Application).where(Application.candidate_id==candidate.id)
#         application = session.execute(stmt).scalars().first()
#         if application and application.completed:
#             await update.message.reply_text(text['application_already_completed'][lang])
#             return ConversationHandler.END  # TODO: если заявку уже подали но с ним не связались?? 

#         await update.message.reply_text(company_description[lang])
#         keyboard = final_keyboard(lang)
#         await update.message.reply_text(text['what_d_u_think'][lang], reply_markup=InlineKeyboardMarkup(keyboard))

#         return ABOUT


# async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     query.answer()
#     answer = query.data.split('_')[1]
#     user = update.effective_user
#     stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
#     candidate = session.execute(stmt).scalars().first()
#     if not candidate:
#         await update.message.reply_text(text=text['error'][answer])
#         return ConversationHandler.END
    
#     candidate.language = answer
#     context.chat_data['user_id'] = candidate.id

#     session.add(candidate)
#     session.commit()

#     stmt = select(Application).where(Application.candidate_id==candidate.id)
#     application = session.execute(stmt).scalars().first()
#     if application and application.completed:
#         await update.message.reply_text(text['application_already_completed'][answer])
#         return ConversationHandler.END  # TODO: если заявку уже подали но с ним не связались?? 

#     await query.edit_message_text(text=company_description[answer])
#     keyboard = final_keyboard(answer)
#     await query.edit_message_text(text=text['what_d_u_think'][answer], reply_markup=InlineKeyboardMarkup(keyboard))

#     return ABOUT


# async def fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     lang = context.chat_data.get('lang')
#     stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
#     candidate = session.execute(stmt).scalars().first()
#     if not candidate:
#         await update.message.reply_text(text=text['error'][lang or 'ru'])
#         return ConversationHandler.END

#     lang = candidate.language
#     context.chat_data['lang'] = lang
    
#     full_name = update.message.text
#     candidate.full_name = full_name
#     session.add(candidate)
#     session.commit()

#     await update.message.reply_text(text['phone'][lang])
#     return PHONE


# async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     lang = context.chat_data.get('lang')
#     stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
#     candidate = session.execute(stmt).scalars().first()
#     if not candidate:
#         await update.message.reply_text(text=text['error'][lang or 'ru'])
#         return ConversationHandler.END

#     lang = candidate.language
#     context.chat_data['lang'] = lang
    
#     phone_num = update.message.text
#     pattern = r"^(\+998)[ .,-]?[0-9]{2}[ .,-]?[0-9]{3}[ .,-]?[0-9]{2}[ .,-]?[0-9]{2}$"
#     if not re.match(pattern, phone_num):
#         await update.message.reply_text(text['phone_format'][lang])
#         return PHONE

#     candidate.phone = phone_num
#     session.add(candidate)
#     session.commit()

#     await update.message.reply_text(text['birth'][lang])
#     return BIRTH


# async def query_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     query = update.callback_query
#     query.answer()
#     lang = context.chat_data.get('lang')
#     await query.edit_message_text(
#         text=text['canceled'][lang or 'ru']
#     )

#     return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # lang = context.chat_data.get('lang')
    # await update.message.reply_text(
    #     text['canceled'][lang or 'ru']
    # )

    return ConversationHandler.END


# async def timeout(update, context):
#     lang = context.chat_data.get('lang')
#     msg_text = text['timeout'][lang or 'ru']
#     if update.message:
#         await update.message.reply_text(msg_text)
#     else:
#         await context.bot.send_message(chat_id=update.effective_user.id, text=msg_text)

#     return ConversationHandler.END


start_handler = CommandHandler('start', start)
# start_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],
#         states={
#             AGREEMENT: [
#                 CallbackQueryHandler(agreement, pattern='^agreement_'),
#                 CallbackQueryHandler(query_cancel, pattern='^cancel$'),
#             ],
#             FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, fio)],
#             PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
#             BIRTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, birth)],
#             EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, education)],
#             ENGLISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, english)],
#             FAMILY: [MessageHandler(filters.TEXT & ~filters.COMMAND, family)],
#             RESUME: [MessageHandler(
#                 filters.Document.APPLICATION
#                 | filters.Document.TEXT
#                 # filters.Document.FileExtension("xls")
#                 # | filters.Document.FileExtension("xlsx")
#                 # | filters.Document.FileExtension("txt")
#                 # | filters.Document.FileExtension("doc")
#                 # | filters.Document.FileExtension("docx")
#                 # | filters.Document.FileExtension("pdf")
#                 # | filters.Document.FileExtension("ppt")
#                 # | filters.Document.FileExtension("pptx")
#                 | filters.TEXT
#                 & ~filters.COMMAND, resume)
#             ],
#             SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, source)],
#             FINAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, final)],
#             ABOUT: [
#                 CallbackQueryHandler(about, pattern='^final_'),
#                 CallbackQueryHandler(query_cancel, pattern='^cancel$'),
#             ],
#             LANGUAGE: [
#                 CallbackQueryHandler(language, pattern='^lang_'),
#             ],
#             REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, reason)],
#             ConversationHandler.TIMEOUT: [
#                 MessageHandler(filters.ALL, timeout),
#                 CallbackQueryHandler(timeout, pattern='.*'),
#             ],
#         },
#         fallbacks=[CommandHandler("cancel", cancel)]
#     )