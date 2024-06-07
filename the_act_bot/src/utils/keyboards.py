from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from the_act_bot.src.utils.translation import text


def get_phone_keyboard_markup(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
    [
        [KeyboardButton(text=f"📞 {text['phone'][lang]}", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


def get_lang_keyboard_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text='🇺🇿', callback_data="lang_uz"),
            InlineKeyboardButton(text='🇷🇺', callback_data="lang_ru"),
            InlineKeyboardButton(text='🇺🇸', callback_data="lang_en")
        ]
    ])
