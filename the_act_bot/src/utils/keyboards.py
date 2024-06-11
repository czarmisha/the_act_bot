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


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text=text['shop']['ru'])],
            [KeyboardButton(text=text['cart']['ru'])],
            [KeyboardButton(text=text['order_history']['ru'])],
            [KeyboardButton(text=text['change_lang']['ru'])],
        ],
        resize_keyboard=True,
    )


def get_admin_main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text=text['shop']['ru'])],
            [KeyboardButton(text=text['cart']['ru'])],
            [KeyboardButton(text=text['order_history']['ru'])],
            [KeyboardButton(text=text['change_lang']['ru'])],
            [KeyboardButton(text=text['list_brand']['ru'])],
            [KeyboardButton(text=text['add_brand']['ru'])],
            [KeyboardButton(text=text['list_category']['ru'])],
            [KeyboardButton(text=text['add_category']['ru'])],
            [KeyboardButton(text=text['list_product']['ru'])],
            [KeyboardButton(text=text['add_product']['ru'])],
            [KeyboardButton(text=text['list_admin_user']['ru'])],
            [KeyboardButton(text=text['add_admin_user']['ru'])],
            [KeyboardButton(text=text['cancel']['ru'])],
            [KeyboardButton(text=text['analytics']['ru'])],
        ],
        resize_keyboard=True,
    )

def get_action_keyboard(prefix: str, brand_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text='Редактировать', callback_data=f"{prefix}_edit_{brand_id}"),
            InlineKeyboardButton(text='Удалить', callback_data=f"{prefix}_remove_{brand_id}")
        ]
    ])

def get_instance_keyboard(prefix: str, instances: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=i.name, callback_data=f"{prefix}_instance_{i.id}")] for i in instances]
    )

def get_remove_confirmation_keyboard(prefix: str, id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Да", callback_data=f"{prefix}_remove_confirmation_{id}_yes"),
                InlineKeyboardButton(text="Нет", callback_data=f"{prefix}_remove_confirmation_{id}_no")
            ]
        ]
    )
