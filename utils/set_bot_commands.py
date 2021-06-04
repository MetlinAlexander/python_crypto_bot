from aiogram import types
# добавляем команды для доступа через /
async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("menu", "Открыть меню"),
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("instruction", "получение подробной инструкции"),
            types.BotCommand("cancel", "Отмена"),
        ]
    )