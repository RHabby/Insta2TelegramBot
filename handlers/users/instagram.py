import asyncio
import logging
from utils.misc.loggers import log_event

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import WrongFileIdentifier

from keyboards.inline import post_info as p_info
from keyboards.inline import user_info as u_info

from loader import dp, insta

from settings import config
from settings.text_templates import (no_posts_text, no_stories_text,
                                     not_found_error_text,
                                     not_found_profile_text, post_caption,
                                     private_profile_text, profile_caption)

from states.post_to_reddit import PostToReddit

from utils.InstaCrawler.app.insta_crawler.exceptions import (NotFoundError,
                                                             PrivateProfileError)
from utils.misc import imgur
from utils.sender_helpers import modify_url, regroup_list, send_by_content_len


@dp.message_handler(text_contains=["instagram.com", "/tv/"], state="*")
@dp.message_handler(text_contains=["instagram.com", "/p/"], state="*")
@dp.throttled(rate=2)
async def post(message: types.Message, state: FSMContext):
    url = modify_url(url=message.text)
    try:
        loop = asyncio.get_running_loop()
        post = await loop.run_in_executor(None, insta.get_single_post, url)
        logging.info(f'{message.chat.id} | {message.chat.full_name} | '
                     f'{message.chat.username} | {message.text}')
    except NotFoundError:
        await message.answer(text=not_found_error_text)
        return True

    markup = p_info.generate_post_kboard(
        username=post["owner_username"], user_url=post["owner_link"],
        post_link=post["post_link"], user_id=message.chat.id,
    )
    caption = post_caption.format(
        description=post.get("description")[:800] if post.get(
            "description") else None,
        likes=post.get("likes"), comments=post.get("comments"),
    )
    sent, text_msg = await send_by_content_len(
        msg=message, post=post,
        caption=caption, markup=markup,
    )
    await message.delete()
    if str(message.chat.id) in config.admins:
        async with state.proxy() as data:
            user = await loop.run_in_executor(None, insta.get_user_info, post["owner_link"])

            if isinstance(sent, types.Message):
                data[sent.message_id] = post
                data[sent.message_id]["user"] = {
                    "full_name": user.get("full_name"),
                    "username": user.get("username"),
                }
            else:
                data[text_msg.message_id] = post
                data[text_msg.message_id]["user"] = {
                    "full_name": user.get("full_name"),
                    "username": user.get("username"),
                }
                data[text_msg.message_id]["ids"] = [
                    message.message_id for message in sent
                ]

        await PostToReddit.reddit.set()


@dp.message_handler(regexp=r"^https://(www\.|)instagram\.com/[a-zA-Z0-9\_\.\-]{5,30}/?", state="*")
@dp.throttled(rate=2)
async def profile(message: types.Message):
    url = modify_url(url=message.text)

    try:
        loop = asyncio.get_running_loop()
        user = await loop.run_in_executor(None, insta.get_user_info, url)

        log_event(message.chat.id, message.chat.full_name,
                  message.chat.username, url,
                  level="info")
    except NotFoundError as e:
        await message.delete()
        await message.answer(text=not_found_profile_text.format(url=url, error=e))

        log_event(message.chat.id, message.chat.full_name,
                  message.chat.username, url, repr(e),
                  level="error")

        return True

    caption = profile_caption.format(
        full_name=user.get("full_name"), bio=user.get("bio"),
        is_private=user.get("is_private"), followers=user.get("edge_followed_by"),
        follow=user.get("edge_follow"), category=user.get("category_name"),
        posts=user.get("posts_count"), igtvs=user.get("igtv_count"),
        highlights=user.get("highlight_reel_count"),
    )
    markup = u_info.generate_user_info_kboard(
        username=user.get("username"),
        user_url=user.get("user_url"),
        user_id=message.chat.id,
        external_url=user.get("external_url"),
    )
    try:
        await message.answer_photo(
            photo=rf'{user.get("profile_pic_hd")}',
            caption=caption,
            reply_markup=markup,
        )
    except Exception as e:
        log_event(message.chat.id, message.chat.full_name,
                  message.chat.username, url, user.get("profile_pic_hd"),
                  repr(e), level="error")

        imgur_img = await imgur.upload_to_imgur(url=user.get("profile_pic_hd"))
        await message.answer_photo(
            photo=imgur_img,
            caption=caption,
            reply_markup=markup,
        )
    await message.delete()


@dp.callback_query_handler(lambda call: "posts" in call.data, state="*")
@dp.throttled(rate=2)
async def last_twelve_posts(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    callback_url = call.data.replace("posts", "")
    loop = asyncio.get_running_loop()
    user_info = await loop.run_in_executor(None, insta.get_user_info,
                                           callback_url)
    log_event(call.message.chat.id, call.message.chat.full_name,
              call.message.chat.username, level="info")

    posts = user_info.get("last_twelve_posts")
    if posts:
        for post in posts:
            caption = post_caption.format(
                description=post.get("description")[:800] if post.get(
                    "description") else None,
                likes=post.get("likes"),
                comments=post.get("comments"),
            )
            markup = p_info.generate_post_kboard(
                username=user_info["username"],
                user_url=user_info["user_url"],
                post_link=post["post_link"],
                user_id=call.message.chat.id,
            )
            sent, text_msg = await send_by_content_len(
                msg=call.message, post=post,
                caption=caption, markup=markup,
            )
            if str(call.message.chat.id) in config.admins:
                async with state.proxy() as data:
                    if isinstance(sent, types.Message):
                        data[sent.message_id] = post
                        data[sent.message_id]["user"] = {
                            "full_name": user_info.get("full_name"),
                            "username": user_info.get("username"),
                        }
                    else:
                        data[text_msg.message_id] = post
                        data[text_msg.message_id]["user"] = {
                            "full_name": user_info.get("full_name"),
                            "username": user_info.get("username"),
                        }
                        data[text_msg.message_id]["ids"] = [
                            message.message_id for message in sent
                        ]
                await PostToReddit.reddit.set()
    else:
        if user_info.get("posts_count") > 0 and len(posts) == 0:
            await call.message.answer(text=private_profile_text)

            log_event(call.message.chat.id, call.message.chat.full_name,
                      call.message.chat.username, "private profile", level="info")
        elif user_info.get("posts_count") == 0:
            await call.message.answer(text=no_posts_text)


@dp.callback_query_handler(lambda call: "stories" in call.data, state="*")
@dp.throttled(rate=2)
async def stories(call: types.CallbackQuery):
    await call.answer()

    callback_url = call.data.replace("stories", "")

    try:
        loop = asyncio.get_running_loop()
        stories = await loop.run_in_executor(None, insta.get_stories, callback_url)

        log_event(call.message.chat.id, call.message.chat.full_name,
                  call.message.chat.username, level="info")
    except PrivateProfileError as e:
        await call.message.answer(text=private_profile_text)

        log_event(call.message.chat.id, call.message.chat.full_name,
                  call.message.chat.username, repr(e), level="info")

        return True

    if stories:
        media = [{"media": rf'{item["post_content"][0]}',
                  "parse_mode": "HTML",
                  "type": "video" if ".mp4" in item else "photo"} for item in stories.values()]

        media = sorted(media, key=lambda storie: ".mp4" in storie["media"])

        albums = regroup_list(data=media)
        for album in albums:
            try:
                await types.ChatActions.upload_photo()
                await call.message.answer_media_group(media=album)
            except WrongFileIdentifier:
                (await call.message.answer_video(video=link["media"])
                 if link["type"] == "video" else await call.message.answer_photo(
                    photo=link["media"]) for link in album)
    else:
        await call.message.answer(text=no_stories_text)
