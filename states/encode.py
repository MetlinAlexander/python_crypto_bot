from aiogram.dispatcher.filters.state import StatesGroup, State

# машина состояний для шифровки
class Encode(StatesGroup):
    Q_message = State()
    Q_password = State()
    Q_photo = State()