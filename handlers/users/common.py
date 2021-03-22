import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart

from loader import dp

from settings.text_templates import hello_msg, help_text


@dp.message_handler(CommandStart(), state="*")
@dp.throttled(rate=2)
async def start_cmd(message: types.Message):
    logging.info(f'{message.chat.id} | {message.chat.full_name} | '
                 f'{message.chat.username} | {message.text}')
    await message.answer(text=hello_msg.format(user_name=message.chat.full_name))


@dp.message_handler(CommandHelp(), state="*")
@dp.throttled(rate=2)
async def help_cmd(message: types.Message):
    logging.info(f'{message.chat.id} | {message.chat.full_name} | '
                 f'{message.chat.username} | {message.text}')
    await message.answer(text=help_text)
