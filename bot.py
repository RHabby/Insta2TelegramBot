from aiogram import executor

from handlers import dp

from utils.notify_admins import start_notify
from utils.set_bot_commands import set_basic_commands


async def on_startup(dp):
    await start_notify(dp)
    await set_basic_commands(dp)


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True)
