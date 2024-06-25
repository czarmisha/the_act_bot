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


async def tmp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    effective_user = update.effective_user
    async with session_maker() as session:
        user_repo = repos.UserRepo(session)
        is_admin = await user_repo.is_admin(effective_user.id)
        if not is_admin:
            await context.bot.send_message(text=text['not_admin'])

    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    await context.bot.send_message(chat_id=query.message.chat_id, text="Долго делать, пока не работает короче эта функция.\nВозьми удали просто этот продукт и добавь заного уже измененный))", reply_markup=keyboards.get_admin_main_menu_keyboard())


product_edit_handler = CallbackQueryHandler(tmp, pattern="^product_edit_\d+$")

# NAME, POSITION = range(2)

# async def brand_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     brand_id = query.data.split('_')[-1]

#     effective_user = update.effective_user
#     async with session_maker() as session:
#         user_repo = repos.UserRepo(session)
#         is_admin = await user_repo.is_admin(effective_user.id)
#         if not is_admin:
#             await context.bot.send_message(text=text['not_admin'])

#     context.chat_data['brand_id'] = int(brand_id)
#     context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
#     await context.bot.send_message(chat_id=query.message.chat_id, text="Введите имя бренда. \nЕсли оно не меняется, отправьте '-'", reply_markup=ReplyKeyboardRemove())
#     return NAME


# async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     effective_user = update.effective_user
#     async with session_maker() as session:
#         user_repo = repos.UserRepo(session)
#         is_admin = await user_repo.is_admin(effective_user.id)
#         if not is_admin:
#             await update.message.reply_text(text['not_admin'])

#     name = update.message.text
#     if not name:
#         await update.message.reply_text("Введите имя бренда. \nЕсли оно не меняется, отправьте '-'")
#         return NAME
    
#     context.chat_data['new_brand_name'] = name
#     await update.message.reply_text("Введите позицию в списке брендов (число). \nЕсли она не меняется, отправьте '-'")
#     return POSITION


# async def position(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     effective_user = update.effective_user
#     async with session_maker() as session:
#         user_repo = repos.UserRepo(session)
#         is_admin = await user_repo.is_admin(effective_user.id)
#         if not is_admin:
#             await update.message.reply_text(text['not_admin'])

#     position = update.message.text
#     if not position or (not position.isdigit() and position != '-'):
#         await update.message.reply_text("Введите позицию в списке брендов (число). \nЕсли она не меняется, отправьте '-'")
#         return POSITION
    
#     brand_name = context.chat_data.get('new_brand_name')
#     if not brand_name:
#         await update.message.reply_text("Введите имя бренда. \nЕсли оно не меняется, отправьте '-'")
#         return NAME
    
#     async with session_maker() as session:
#         brand_repo = repos.BrandRepo(session)
#         await brand_repo.update(
#             id=context.chat_data['brand_id'],
#             brand_in=schemas.BrandIn(
#                 name=brand_name if brand_name != '-' else None,
#                 position=int(position) if position != '-' else None,
#             )
#         )
    
#     await update.message.reply_text("Готово, бренд изменен", reply_markup=keyboards.get_admin_main_menu_keyboard())
#     return ConversationHandler.END


# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     lang = context.chat_data.get('lang') #TODO: add cancel btn
#     await update.message.reply_text(
#         text['canceled'][lang or 'ru'],
#         reply_markup=keyboards.get_admin_main_menu_keyboard()
#     )

#     return ConversationHandler.END


# brand_edit_handler = ConversationHandler(
#     entry_points=[CallbackQueryHandler(brand_remove, pattern="^brand_edit_\d+$")],
#     states={
#         NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
#         POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, position)],
#     },
#     fallbacks=[CommandHandler("cancel", cancel)]
# )
