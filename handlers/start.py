from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.user import user_main_menu, phone_share, delete_product_table
from keyboards.inline.user import mars_bozor_pagination, not_subs_channels
from states.user import DeleteProductState, ProductAddState, RegisterState
from aiogram.dispatcher import FSMContext

from loader import dp, db_manager
from utils.misc.checker import login_def, next_product, previous_product
from utils.misc.subs_checker import check
from data.config import channels



@dp.callback_query_handler(text="check_sub")
async def check_sub_handler(call: types.CallbackQuery):
        not_subs = []
        for channel in channels:
            check_user = await check(user_id=call.message.chat.id, channel=channel[0])
            if not check_user:
                not_subs.append(channel)
        if len(not_subs) == 0:
            user = db_manager.get_user(chat_id=call.message.chat.id)
            if user:
                text = "Botimizga xush kelibsiz."
                await call.message.answer(text=text, reply_markup=user_main_menu)
            else:
                text = "Iltimos telefon raqamingizni kiriting."
                await call.message.answer(text=text, reply_markup=phone_share)
                await RegisterState.phone_number.set() 
        else:
            text = "Ushbu kanallarga a'zo bo'lishingiz kerak.\n\n"
            for channel in not_subs:
                text += f"<a href='{channel[2]}'>{channel[1]}</a>\n"
            buttons = await not_subs_channels(not_subs)
            await call.message.answer(text=text, reply_markup=buttons)




@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    not_subs = []
    for channel in channels:
        check_user = await check(user_id=message.chat.id, channel=channel[0])
        if not check_user:
            not_subs.append(channel)


    if len(not_subs) == 0:
        user = db_manager.get_user(chat_id=message.chat.id)
        if user:
            text = "Botimizga xush kelibsiz."
            await message.answer(text=text, reply_markup=user_main_menu)
        else:
            text = "Iltimos telefon raqamingizni kiriting."
            await message.answer(text=text, reply_markup=phone_share)
            await RegisterState.phone_number.set() 
    else:
        text = "Ushbu kanallarga a'zo bo'lishingiz kerak.\n\n"
        for channel in not_subs:
            text += f"<a href='{channel[2]}'>{channel[1]}</a>\n"
        buttons = await not_subs_channels(not_subs)
        await message.answer(text=text, reply_markup=buttons)




@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentTypes.CONTACT)
async def get_phone_number_handler(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    text = "Iltimos, Modme id kiriting."
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterState.login.set()


@dp.message_handler(state=RegisterState.login)
async def get_login_handler(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    text = "Iltimos, Modme parol kiriting."
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterState.password.set()




@dp.message_handler(state=RegisterState.password)
async def get_password_handler(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text, chat_id=message.chat.id)
    data = await state.get_data()
    login = data.get('login')
    password = data.get('password')
    student = login_def(login, password)
    if student:
        await state.update_data(full_name=student)

        data = await state.get_data()
        if db_manager.insert_user(data):
            text = f"Ro'yxatdan o'tdingiz. ✅ {student}"
            await message.answer(text=text, reply_markup=user_main_menu)
        else:
            text = "Botda xatolik bor."
            await message.answer(text=text)
    else:
        text = "Login yoki parolda xatolik mavjud. Qayta urunish uchun /start bosing."
        await message.answer(text=text)
    await state.finish()
    


# delete product
@dp.message_handler(text="🗑 Mahsulot o'chirish")
async def delete_product_handler(message: types.Message):
    text = "O'chirmoqchi bo'lgan mahsulot ID-sini kiriting."
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await DeleteProductState.id.set()
    


@dp.message_handler(state=DeleteProductState.id)
async def delete_product(message: types.Message, state: FSMContext):
    if db_manager.delete_products(int(message.text)):
        text = "Mahsulot muvaffaqiyatli o'chirildi."
    else:
       text = "Noto'gri ID kiritdingiz!"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()



# back
@dp.message_handler(text="🔙 Orqaga")
async def back_handler(message: types.Message):
    text = "Asosiy menyuga qaytdingiz."
    await message.answer(text=text, reply_markup=user_main_menu)




@dp.callback_query_handler(text="next_product", state='my-products-state')
async def next_product_handler(call: types.CallbackQuery, state:FSMContext):
    products = db_manager.get_user_all_products(chat_id=call.message.chat.id)
    data = await state.get_data()
    index = data.get('index')

    product = await next_product(products, index)
    if product:
        user = db_manager.get_user(chat_id=call.message.chat.id)
        await call.message.delete()
        index = index + 1
        photo = product[3]
        caption = f"🆔 {product[0]}\n{product[1]} - {product[4]}\n\n{product[2]}\n\n👤 {user[4]}\n☎️ {user[1]}" # 3 parol, 1 raqam, 2 id,
        await call.message.answer_photo(photo=photo, caption=caption,
                                   reply_markup=await mars_bozor_pagination(len(products), index))
        await state.update_data(index=index)
    else:
        text = "Bundan keyin mahsulot mavjud emas !"
        await call.answer(text=text, show_alert=True)


@dp.callback_query_handler(text="previous_product", state='my-products-state')
async def previous_product_handler(call: types.CallbackQuery, state: FSMContext):
    products = db_manager.get_user_all_products(chat_id=call.message.chat.id)
    data = await state.get_data()
    index = data.get('index')

    product = await previous_product(products, index)
    if product:
        user = db_manager.get_user(chat_id=call.message.chat.id)
        await call.message.delete()
        index = index - 1
        photo = product[3]
        caption = f"🆔 {product[0]}\n🔴 Nomi: {product[1]} - {product[4]} so'm\n\nℹ️ : {product[2]}\n\n👤 : {user[4]}\n☎️: {user[1]}"
        await call.message.answer_photo(photo=photo, caption=caption,
                                        reply_markup=await mars_bozor_pagination(len(products), index))
        await state.update_data(index=index)
    else:
        text = "Bundan oldin mahsulot mavjud emas !"
        await call.answer(text=text, show_alert=True)



# my products

@dp.message_handler(text="🖱 Mahsulotlarim", state="*")
async def mars_bozor_handler(message: types.Message, state:FSMContext):
    await state.set_state('my-products-state')
    products = db_manager.get_user_all_products(chat_id=message.chat.id)
    if products:
        user = db_manager.get_user(chat_id=message.chat.id)
        await state.update_data(index=0)
        product = products[0]
        photo = product[3]
        caption = f"🆔 {product[0]}\n🔴 Nomi: {product[1]} - {product[4]} so'm\n\nℹ️ Ma'lumot: {product[2]}\n\n👤 Sotuvchi: {user[4]}\n☎️ Aloqa uchun: {user[1]}"
        await message.answer_photo(photo=photo, caption=caption, reply_markup=await mars_bozor_pagination(len(products), 0))
    else:
        text = "Aktiv mahsulotlar mavjud emas"
        await message.answer(text=text, reply_markup=user_main_menu)


# Profile

@dp.message_handler(text="👤 Profil", state="*") 
async def profile_handler(message: types.Message):
    user =db_manager.get_user(chat_id=message.chat.id)
    if user:
        text = f"""
👤: {user[1]}
☎️: {user[2]}
🔄: {user[3]}
🔑: {user[4]}
"""
        await message.answer(text=text)
    else:
        text = "Iltimos telefon raqamingizni kiriting."
        await message.answer(text=text, reply_markup=phone_share)
        await RegisterState.phone_numnber.set()



#mars bozor
        
@dp.message_handler(text="🚀 Mars Bozor", state="*")
async def mars_bozor_handler(message: types.Message, state: FSMContext):
    await state.set_state('mars-bozor-state')
    products = db_manager.get_all_products()
    if products:
        await state.update_data(index=0)
        product = products[0]
        user =db_manager.get_user(chat_id=product[6])
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}\n\n👤 {user[4]}\n☎️ {user[1]}"
        await message.answer_photo(photo=photo, caption=caption, reply_markup=await mars_bozor_pagination(len(products), 0))
    else:
        text = "Aktiv mahsulotlar mavjud emas"
        await message.answer(text=text, reply_markup=user_main_menu)


@dp.callback_query_handler(text="next_product", state='mars-bozor-state')
async def next_product_handler(call: types.CallbackQuery, state:FSMContext):
    products = db_manager.get_user_all_products(chat_id=call.message.chat.id)
    data = await state.get_data()
    index = data.get('index')

    product = await next_product(products, index)
    if product:
        user = db_manager.get_user(chat_id=call.message.chat.id)
        await call.message.delete()
        index = index + 1
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}\n\n👤 {user[4]}\n☎️ {user[1]}" # 3 parol, 1 raqam, 2 id,
        await call.message.answer_photo(photo=photo, caption=caption,
                                   reply_markup=await mars_bozor_pagination(len(products), index))
        await state.update_data(index=index)
    else:
        text = "Bundan keyin mahsulot mavjud emas !"
        await call.answer(text=text, show_alert=True)



@dp.callback_query_handler(text="previous_product", state='mars-bozor-state')
async def previous_product_handler(call: types.CallbackQuery, state: FSMContext):
    products = db_manager.get_user_all_products(chat_id=call.message.chat.id)
    data = await state.get_data()
    index = data.get('index')

    product = await previous_product(products, index)
    if product:
        user = db_manager.get_user(chat_id=call.message.chat.id)
        await call.message.delete()
        index = index - 1
        photo = product[3]
        caption = f"\n🔴 Nomi: {product[1]} - {product[4]} so'm\n\nℹ️ : {product[2]}\n\n👤 : {user[4]}\n☎️: {user[1]}"
        await call.message.answer_photo(photo=photo, caption=caption,
                                        reply_markup=await mars_bozor_pagination(len(products), index))
        await state.update_data(index=index)
    else:
        text = "Bundan oldin mahsulot mavjud emas !"
        await call.answer(text=text, show_alert=True)

# add product
        
@dp.message_handler(text="➕ Mahsulot qo'shish", state="*")
async def add_product_handler(message: types.Message):
    user_products = db_manager.get_user_all_products(chat_id=message.chat.id)
    if len(user_products) < 3:
        text = "Iltimos rasmini kiriting"
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
        await ProductAddState.photo.set()
    else:
        text = "Siz maksimal 3 ta mahsulotni sota olasiz. Avval active mahsulotlardan birini o'chiring."
        await message.answer(text=text, reply_markup=delete_product_table)


@dp.message_handler(state=ProductAddState.photo, content_types=types.ContentTypes.PHOTO)
async def get_photo_handler(message: types, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    text = "Iltimos mahsulot nomini kiriting"
    await message.answer(text=text)
    await ProductAddState.name.set()


@dp.message_handler(state=ProductAddState.name)
async def get_name_handler(message: types, state: FSMContext):
    await state.update_data(name=message.text)
    text = "Iltimos mahsulot haqida ma'lumot kiriting"
    await message.answer(text=text)
    await ProductAddState.info.set()


@dp.message_handler(state=ProductAddState.info)
async def get_info_handler(message: types, state: FSMContext):
    await state.update_data(info=message.text)
    text = "Iltimos mahsulot narxini kiriting"
    await message.answer(text=text)
    await ProductAddState.price.set()


@dp.message_handler(state=ProductAddState.price)
async def get_price_handler(message: types, state: FSMContext):
    await state.update_data(price=message.text, status="active", chat_id=message.chat.id)
    data = await state.get_data()
    product =db_manager.insert_product(data)
    if product:
        text = "Mahsulot bozorga qo'shildi ✅"
    else:
        text = "Botda xatolik bor ❌"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()

# # back
    
@dp.message_handler(text="🔙 Orqaga")
async def back_handler(message: types.Message):
    text = "Asosiy menyuga qaytdingiz."
    await message.answer(text=text, reply_markup=user_main_menu)