from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.row("🚘 Moshinani haqida ma'lumot kiritish tugmasi")

colors=InlineKeyboardMarkup(row_width=1)
colors_lst=[( "🔴 Qizil","Qizil"), ("🔵 Kok", "Ko'k"),("⚪️Oq", "Oq"), ("🟡 Sariq", "Sariq"), ("🟤 Shokolod ", "Shokolod"),("⚫️ Qora", "Qora") ]
for color in colors:
    colors.insert(InlineKeyboardButton(text=color[0], callback_data=color[1]))

contact_types = ReplyKeyboardMarkup(resize_keyboard=True)
contact_types.add(KeyboardButton(text="☎️ Raqamni jo'natish",request_contact=True))

confrim_markub = InlineKeyboardMarkup(row_width=True)
confrim_markub.row(InlineKeyboardButton(text="✅ Ha", callback_data="yes"),InlineKeyboardButton(text="❌ yo'q", callback_data="no"))