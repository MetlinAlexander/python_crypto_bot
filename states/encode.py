from aiogram.dispatcher.filters.state import StatesGroup, State


class Encode(StatesGroup):
    Q_message = State()
    Q_password = State()
    Q_photo = State()