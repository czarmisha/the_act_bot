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


def get_add_keyboard(lang: str = 'ru') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text=text['cart'][lang])],
            [KeyboardButton(text=text['back'][lang])]
        ],
        resize_keyboard=True,
    )


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


def add_product_to_cart(product_id: int, lang: str = 'ru', to_add: int = 1) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text='-', callback_data=f"product_minus_{product_id}_{to_add}"),
                InlineKeyboardButton(text=str(to_add), callback_data="ignore"),
                InlineKeyboardButton(text='+', callback_data=f"product_plus_{product_id}_{to_add}")
            ],
            [InlineKeyboardButton(text=text['add_to_cart'][lang], callback_data=f"add_to_cart_{product_id}_{to_add}")]
        ]
    )


def get_brand_keyboard_markup(brands: list) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=i.name)] for i in brands]
    keyboard.append([KeyboardButton(text=text['back']['ru'])])
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )


def get_category_keyboard_markup(categories: list, lang: str = 'ru') -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=i.name[lang])] for i in categories]
    keyboard.append([KeyboardButton(text=text['back']['ru'])])
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )


def get_product_keyboard_markup(products: list, lang: str = 'ru') -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=text['cart'][lang])]]
    keyboard.extend([[KeyboardButton(text=i.name)] for i in products])
    keyboard.append([KeyboardButton(text=text['back'][lang])])
    print('!!!!!!!!!!!', keyboard)
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )


# admin keyboards
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


def get_instance_keyboard(prefix: str, instances: list, lang: str = 'ru') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=i.name[lang], callback_data=f"{prefix}_instance_{i.id}")] for i in instances]
    ) if prefix == 'category' else InlineKeyboardMarkup(
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


def get_category_parents_keyboard(brands: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=i.name, callback_data=f"category_parent_{i.id}")] for i in brands]
    )


def get_product_parents_keyboard(brands: list, prefix: str = 'brand') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=i.name, callback_data=f"product_{prefix}_parent_{i.id}")] for i in brands]
    ) if prefix == 'brand' else InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=i.name['ru'], callback_data=f"product_{prefix}_parent_{i.id}")] for i in brands]
    )


def get_category_add_brand_list(brands: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=i.name, callback_data=f"category_add_brand_{i.id}")] for i in brands]
    )


def get_product_add_brand_list(brands: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=i.name, callback_data=f"product_add_brand_{i.id}")] for i in brands]
    )


def get_product_add_category_list(categories: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=i.name['ru'], callback_data=f"product_add_category_{i.id}")] for i in categories]
    )
