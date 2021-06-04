from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from loader import dp
# хендлер для отмены состояний
comands = ["cancel", "start", "menu", "help", "instruction"]
@dp.message_handler(commands=comands, state="*")
async def answer_q1(message: types.Message, state: FSMContext):
    # Меняем состояние
    await state.finish()
    await message.answer("Действие отменено.")
