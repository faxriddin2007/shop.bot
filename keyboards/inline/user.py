from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def mars_bozor_pagination(total_products, index):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️", callback_data="previous_product"),
                InlineKeyboardButton(text=f"{index + 1}/{total_products}", callback_data="show"),
                InlineKeyboardButton(text="➡️", callback_data="next_product"),
            ]
        ]
    )
    return markup

async def not_subs_channels(channels):
    markup = InlineKeyboardMarkup()
    for channel in channels:
        button = InlineKeyboardButton(text=channel[1], url=channel[2])
        markup.row(button)
    check = InlineKeyboardButton(text="Tekshirish", callback_data="check_sub")    
    markup.row(check)
    return markup