from aiogram import Dispatcher
from settings import config

from utils.misc.loggers import log


async def start_notify(dp: Dispatcher):
    for admin in config.admins:
        try:
            await dp.bot.send_message(
                chat_id=admin,
                text="Бота запустили"
            )
        except Exception as e:
            log.exception(e)


async def shutdown_notify(dp: Dispatcher):
    for admin in config.admins:
        try:
            await dp.bot.send_message(
                chat_id=admin,
                text="Бот упал"
            )
        except Exception as e:
            log.exception(e)
