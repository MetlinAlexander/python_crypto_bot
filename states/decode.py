from aiogram.dispatcher.filters.state import StatesGroup, State


class Decode(StatesGroup):
    Q_password = State()
    Q_photo = State()