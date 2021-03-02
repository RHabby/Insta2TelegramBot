from aiogram import Bot, Dispatcher, types

from settings import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
