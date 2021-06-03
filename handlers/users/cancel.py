from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from loader import dp

@dp.message_handler(commands="cancel", state="*")
async def answer_q1(message: types.Message, state: FSMContext):
    # Меняем состояние
    await state.finish()
    await message.answer("Действие отменено.")
