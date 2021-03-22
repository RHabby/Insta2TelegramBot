import logging

from aiogram import Dispatcher

from settings import config


async def start_notify(dp: Dispatcher):
    for admin in config.admins:
        try:
            await dp.bot.send_message(
                chat_id=admin,
                text="Бота запустили",
                disable_notification=True,
            )
        except Exception as e:
            logging.exception(e)


async def shutdown_notify(dp: Dispatcher):
    for admin in config.admins:
        try:
            await dp.bot.send_message(
                chat_id=admin,
                text="Бот упал",
                disable_notification=True,
            )
        except Exception as e:
            logging.exception(e)
