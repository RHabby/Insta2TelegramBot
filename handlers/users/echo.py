import logging

from aiogram import types
from loader import dp


@dp.message_handler()
async def echo(message: types.Message):
    logging.info(
        f"{message.chat.id} | {message.chat.first_name} {message.chat.last_name} | {message.chat.username} | {message.date} | {message.text}")
    await message.answer(message.text)
