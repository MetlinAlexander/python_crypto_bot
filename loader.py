from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
"""
proxy_url = 'http://proxy.server:3128'
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, proxy=proxy_url)
"""
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
