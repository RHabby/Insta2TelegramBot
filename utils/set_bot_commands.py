from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher


async def set_basic_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start the bot"),
            types.BotCommand("help", "Help message"),
        ]
    )
