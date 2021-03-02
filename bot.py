from aiogram import executor

from handlers import dp
from utils.misc.loggers import log
from utils.notify_admins import shutdown_notify, start_notify


async def on_startup(dp):
    await start_notify(dp)


async def on_shutdown(dp):
    await shutdown_notify(dp)


if __name__ == "__main__":
    log.warning("Starting the bot")
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
