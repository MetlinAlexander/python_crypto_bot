from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import menu
from loader import dp

# хендлер реагирующий на команду /menu
@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите действие из меню ниже", reply_markup=menu)