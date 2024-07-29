# from the_act_bot.src import schemas


# async def calculate_cart_total(cart: schemas.Cart):
#     total = 0
#     for item in cart.items:
#         total += item.product.price * item.quantity
#     return total


async def get_cart_text(cart_info, lang: str) -> str:
    text = ''
    for item in cart_info:
        text += f"{item.product.name} - {item.quantity} шт.\n"  # TODO: localize
    return text
