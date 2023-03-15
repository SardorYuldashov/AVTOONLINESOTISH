import logging
from aiogram import Bot, Dispatcher, executor, types
from confrig import API_TOKEN, ADMIN
from keyboard import main_markup, colors, contact_types, confrim_markub
from  aiogram.contrib.fsm_storage.memory import MemoryStorage
from state import Auto_Info
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
@dp.message_handler(commands=['start', 'help'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    full_name = message.from_user.full_name
    try:
        await message.reply(f"Salom!{id} {full_name}\nMen sizlarga 🚘 moshingaizni online sotishda yordam beraman!\nQuydagi ⭕️ tugmani bosing va ma'lumot kiriting")
    except Exception as error:
        logging.error(error)
@dp.message_handler(text="🚘 Moshinani haqida ma'lumot kiritish tugmasi")
async def sotish(message: types.Message):
    await message.answer("🚘 Mashinangizni nomini kiriting", reply_markup=ReplyKeyboardRemove)
    await Auto_Info.title.set()
@dp.message_handler(state=Auto_Info.title)
async  def get_auto_title(message: types.Message, state: FSMContext):
    title = message.text
    await state.update_data({"title": title})
    await message.answer("🚘 Moshinangizni ishlab chiqarilgan yilini kiriting!\n(Masalan 2020)")
    await Auto_Info.next()
@dp.message_handler(lambda message: message.text.isdigit(), state = Auto_Info.year)
async def get_auto_year(message: types.Message, state: FSMContext):
    year = message.text
    await state.update_data({"year": year})
    await message.answer("🌈 Mashinagizni rangini tanlang!", reply_markup=colors)
    await Auto_Info.next()

@dp.callback_query_handler(state=Auto_Info.color)
async def get_auto_color(call: types.CallbackQuery, state: FSMContext):
    color = call.data
    await state.update_data({"color": color})
    await call.answer(text=f"{color.title()} rangini tanladingiz")
    await call.message.delete()
    await call.message.answer("🏄‍♀️ Moshinangizni bosib o'tgan masofasini kiriting! (km)")
    await Auto_Info.probeg.set()

@dp.message_handler(lambda message: message.text.isdigit(), state=Auto_Info.probeg)
async def get_auto_probeg(message: types.Message, state: FSMContext):
    probeg=message.text
    await state.update_data({"probeg": probeg})
    await message.answer("🎆 Mashinagizni rasmini yuboring!", reply_markup=colors)
    await Auto_Info.image.set()

@dp.message_handler(content_types=["photo"], state=Auto_Info.image)
async def get_auto_image(message: types.Message, state: FSMContext):
    photo_id=message.photo[-1].file_id
    await state.update_data({"photo": photo_id})
    await message.answer("Bog'lanish uchun raqamingizni jo'nating", reply_markup = contact_types)
    await Auto_Info.next()

@dp.message_handler(state=Auto_Info.phone)
@dp.message_handler(contact_types=["contact"], state=Auto_Info.phone)
async def get_auto_phone(message: types.Message, state: FSMContext):
    if message.text:
        phone = message.text
    else:
        phone = message.contact.phone_number
    await state.update_data({"phone": phone})
    await message.answer(" 💰 Mashinangizni narxini kiriting! ($)", reply_markup=ReplyKeyboardRemove())
    await Auto_Info.price.set()

@dp.message_handler(lambda message: types.Message, state=Auto_Info.price)
async  def get_auto_price(message: types.Message, state: FSMContext):
    price=message.text
    await state.update_data({"price": price})
    data=await  state.get_data()
    msg=f"<b>🚘 Mashina ma'lumotlari\n\n{data.get('title')}\n⚙️ Yili: {data.get('year')}yil\n🌈 Rangi: {data.get('color')}\n🛞 Probeg: {data.get('probeg')}km\n📞Telefon raqami: {data.get('phone')},📲Telegram: @{message.from_user.username}\n\n💰Mashina narxi: {data.get('price')}$</b>"
    await message.answer(photo=data.get('photo'), caption=msg, parse_mode="html", reply_markup=confrim_markub)
    await Auto_Info.confrim.set()

@dp.callback_query_handler(state=Auto_Info.confrim, text="no")
async  def delete_data(call:types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Menyulardan birini tanlang", reply_markup=main_markup)
    await state.finish()
@dp.callback_query_handler(state=Auto_Info.confrim, text="yes")
async  def send_to_admin(call:types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer("Adminga jo'natildi!", show_alert=True)
    await call.message.send_copy(chat_id=ADMIN[0])
    await call.message.answer("Menyulardan birini tanlang", reply_markup=main_markup)
    await call.message.answer("Menyulardan birini tanlang", reply_markup=main_markup)
    await state.finish()







if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
