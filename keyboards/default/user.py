from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚀 Mars Bozor"),
            KeyboardButton(text="🖱 Mahsulotlarim"),
        ],
        [
            KeyboardButton(text="👤 Profil"),
            KeyboardButton(text="➕ Mahsulot qo'shish"),
        ]
    ],
    resize_keyboard=True
)


phone_share = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton("📞 Raqamni yuborish", request_contact=True)
        ]
    ], resize_keyboard=True
)


delete_product_table = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗑 Mahsulot o'chirish"),
            KeyboardButton(text="🔙 Orqaga")
        ]
    ],
    resize_keyboard=True
)