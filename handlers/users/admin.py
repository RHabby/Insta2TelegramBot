import logging

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BadRequest as aiogram_BadRequest

from keyboards.inline import post_info as p_info

from loader import bot, dp

from settings import config, text_templates

from states.post_to_reddit import PostToReddit

from utils.misc import imgur, reddit_utils
from utils.misc.loggers import log_event
from utils.sender_helpers import modify_name


# admin commands entrypoint
@dp.message_handler(commands=["admin"], chat_id=config.admins, state="*")
async def only_admin(message: types.Message):
    await message.answer(text="What do you want?",
                         reply_markup=p_info.generate_admin_kboard())


# storage data funcs
@dp.callback_query_handler(text="data", state="*")
async def storage_data_info(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    async with state.proxy() as data:
        await call.message.answer(text=f'{len(data) = }',
                                  reply_markup=p_info.generate_data_info_kboard())


@dp.callback_query_handler(text="clear", chat_id=config.admins, state="*")
async def clear_data(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text="the data was cleared for your account.")


# redditor funcs
@dp.callback_query_handler(text="redditor", state="*")
async def redditor(call: types.CallbackQuery):
    await call.answer()

    redditor = await reddit_utils.get_redditor_info()
    text = text_templates.redditor_info_text.format(
        name=redditor["name"],
        link_karma=redditor["link_karma"],
        comment_karma=redditor["comment_karma"],
        id=redditor["id"],
    )
    await call.message.answer(
        text=text,
        reply_markup=p_info.generate_redditor_info_kboard(submissions=redditor["submissions"]),
    )


@dp.callback_query_handler(lambda call: "submission" in call.data, state="*")
async def submission_info(call: types.CallbackQuery):
    await call.answer()

    submission_code = call.data.split(",")[1]
    submission = await reddit_utils.get_submission_info(submission_code=submission_code)

    caption = text_templates.submission_info_text.format(
        title=submission.title,
        comments=submission.num_comments,
        score=submission.score,
        subreddit=submission.subreddit.display_name,
        ratio=submission.upvote_ratio,
        id=submission.id,
    )

    await call.message.answer_photo(
        photo=submission.url,
        caption=caption,
        reply_markup=p_info.generate_submission_info_kboard(submission=submission),
    )


# submit insta post to reddit part
@dp.callback_query_handler(text="reddit", state=PostToReddit.reddit)
async def reddit(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    main_key = str(call.message.message_id)
    async with state.proxy() as data:
        post_content_len = len(
            data[str(call.message.message_id)]["post_content"])

        if post_content_len > 1:
            await PostToReddit.which_one.set()
            await call.message.edit_reply_markup(
                reply_markup=p_info.generate_which_one_kboard(
                    post_content_len=post_content_len,
                ),
            )
        else:
            await PostToReddit.subreddit.set()
            await call.message.edit_reply_markup(
                reply_markup=p_info.generate_subreddit_kboard(
                    subreddit_list=config.SUBREDDIT_LIST,
                ),
            )

            full_name = modify_name(name=data[main_key]["user"]["full_name"])
            data["submit"] = {
                "content": data[main_key]["post_content"][0],
                "title": f'{full_name} (@{data[main_key]["user"]["username"]})',
            }


@dp.callback_query_handler(lambda call: "which_one" in call.data, state=PostToReddit.which_one)
async def which_to_post(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    which_one = int(call.data.split(",")[1])
    main_key = str(call.message.message_id)

    async with state.proxy() as data:
        full_name = modify_name(name=data[main_key]["user"]["full_name"])
        data["submit"] = {
            "content": data[main_key]["post_content"][which_one - 1],
            "title": f'{full_name} (@{data[main_key]["user"]["username"]})',
        }

    await call.message.edit_reply_markup(
        reply_markup=p_info.generate_subreddit_kboard(
            subreddit_list=config.SUBREDDIT_LIST,
        ),
    )
    await PostToReddit.subreddit.set()


@dp.callback_query_handler(lambda call: call.data in config.SUBREDDIT_LIST, state=PostToReddit.subreddit)
async def subreddit(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        url = await imgur.upload_to_imgur(data["submit"]["content"])
        reddit_submission = await reddit_utils.submit_post(
            subreddit_name=call.data, title=data["submit"]["title"],
            url=url,
        )
        if reddit_submission:
            await call.answer(text="Done!")
            submission = await reddit_utils.get_submission_info(
                submission_code=reddit_submission,
            )
            await call.message.edit_reply_markup(
                reply_markup=p_info.generate_posted_kboard(
                    permalink=rf'{config.REDDIT_BASE_URL}{submission.permalink}',
                ),
            )
            logging.info(f'{call.message.chat.id} | {call.message.chat.username} | '
                         f'{url} | {data["submit"]["title"]} | '
                         f'{config.REDDIT_BASE_URL}{submission.permalink}')
            del data["submit"]

    await PostToReddit.reddit.set()


@dp.callback_query_handler(text="edit_title", state="*")
async def edit_title_callback(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = (f'Current title: {data["submit"]["title"]}\n'
                f'Enter the new one.')
        try:
            await call.message.edit_caption(
                caption=text,
            )
        except aiogram_BadRequest:
            await call.message.edit_text(
                text=text,
            )
    await PostToReddit.edit_title.set()


@dp.message_handler(state=PostToReddit.edit_title)
async def edit_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["submit"]["title"] = message.text

        await message.answer(
            text=f'New Title: {data["submit"]["title"]}',
            reply_markup=p_info.generate_subreddit_kboard(subreddit_list=config.SUBREDDIT_LIST))
    await PostToReddit.subreddit.set()


@dp.message_handler(state=PostToReddit.enter_title)
async def enter_title(message: types.Message, state: FSMContext):
    title = message.text
    async with state.proxy() as data:
        data["submit"]["title"] = title.strip()

    await message.answer(text="Choose the subreddit now...",
                         reply_markup=p_info.generate_subreddit_kboard(
                             subreddit_list=config.SUBREDDIT_LIST,
                         ))
    await PostToReddit.subreddit.set()


@dp.callback_query_handler(text="delete", state="*")
async def delete_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    async with state.proxy() as data:
        message_data = data.get(str(call.message.message_id))
        if message_data and message_data.get("ids"):
            for msg in message_data["ids"]:
                await bot.delete_message(
                    chat_id=call.message.chat.id,
                    message_id=str(msg),
                )
        if message_data:
            del data[str(call.message.message_id)]
        else:
            data.pop(key="user")

    log_event(str(call.message.chat.id),
              call.message.chat.full_name, call.message.chat.username, level="info")
