import logging

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import ContentType

from keyboards.inline import post_info as p_info

from loader import bot, dp

from settings import config

from states.post_to_reddit import PostToReddit


@dp.message_handler(content_types=ContentType.TEXT, state="*")
@dp.throttled(rate=2)
async def echo_text(message: types.Message):
    logging.info(f'{message.chat.id} | '
                 f'{message.chat.first_name} {message.chat.last_name} | '
                 f'{message.chat.username} | {message.text}')
    await message.answer(message.text)


@dp.message_handler(content_types=ContentType.PHOTO, state="*")
@dp.throttled(rate=2)
async def echo_photo(message: types.Message, state: FSMContext):
    if str(message.chat.id) in config.admins:
        photo = await bot.get_file(message.photo[-1]["file_id"])
        file_url = bot.get_file_url(file_path=photo["file_path"])
        title = message.caption or None

        async with state.proxy() as data:
            data["submit"] = {
                "content": file_url,
                "title": title,
            }

        if not title:
            await message.answer_photo(
                photo=message.photo[-1]["file_id"],
                caption="Now you have to enter the submission title...")
            await PostToReddit.enter_title.set()
        else:
            await message.answer_photo(
                photo=message.photo[-1]["file_id"],
                caption="Now choose the subreddit...",
                reply_markup=p_info.generate_subreddit_kboard(
                    subreddit_list=config.SUBREDDIT_LIST,
                ),
            )
            await PostToReddit.subreddit.set()

    else:
        await message.answer("This is a photo")


@dp.message_handler(content_types=ContentType.VIDEO, state="*")
@dp.throttled(rate=2)
async def echo_video(message: types.Message):
    await message.answer("This is a video...")
