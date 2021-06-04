from aiogram.dispatcher.filters.state import StatesGroup, State
# машина состояний для расшифровки

class Decode(StatesGroup):
    Q_password = State()
    Q_photo = State()