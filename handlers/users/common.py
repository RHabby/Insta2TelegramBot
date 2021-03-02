from utils.misc.loggers import log

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from loader import dp


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    log.info(
        f"{message.chat.id} | {message.chat.first_name} {message.chat.last_name} | {message.chat.username} | {message.text}")
    await message.answer("Hello, you started me.")


@dp.message_handler(CommandHelp())
async def help(message: types.Message):
    text = [
        "List of Commands:",
        "/start — Start the bot;",
        "/help — This help message;",
        "",
        "If you want to work with me, you have to follow for some rules:",
        "1. Make sure that the link you send me belongs to an open profile;",
        "2. may be something else..."
    ]
    await message.answer("\n".join(text))
