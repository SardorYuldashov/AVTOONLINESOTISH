from aiogram.dispatcher.filters.state import State, StatesGroup

class Auto_Info(StatesGroup):
    title=State()
    year = State()
    color = State()
    price = State()
    probeg = State()
    image = State()
    phone = State()
    confrim=State()