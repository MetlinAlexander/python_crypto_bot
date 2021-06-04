from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

# хендлер реагирующий на команду /help
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = """Список команд: 
/start - Начать диалог
/cancel - Отмена действия
/help - Получить справку
/menu - Открыть меню
/instruction - Получение подробной инструкции
"""
    await message.answer(text)
