import unicodedata
from typing import Dict, List, Tuple

from aiogram import types
import aiogram

import demoji

import iuliia

from settings import config
from settings.text_templates import error_post_caption


async def send_by_content_len(
        msg: types.Message, post: Dict,
        caption: str, markup: types.InlineKeyboardMarkup) -> Tuple:

    if len(post["post_content"]) == 1:
        return await configure_simple_post(post=post["post_content"],
                                           msg=msg, caption=caption,
                                           markup=markup)
    elif len(post["post_content"]) > 1:
        try:
            return await configure_media_group(post=post["post_content"],
                                               msg=msg, caption=caption,
                                               markup=markup)
        except aiogram.utils.exceptions.WrongFileIdentifier:
            return [await configure_simple_post(post=[post], msg=msg,
                                                caption=caption, markup=markup)
                    for post in post["post_content"]][0]


async def configure_simple_post(post: List, **kwargs):
    msg = kwargs.get("msg")
    caption = kwargs.get("caption")
    markup = kwargs.get("markup")

    try:
        if ".mp4" in post[0]:
            sent = await msg.answer_video(video=rf'{post[0]}',
                                          caption=caption,
                                          reply_markup=markup)
        else:
            sent = await msg.answer_photo(photo=rf'{post[0]}',
                                          caption=caption,
                                          reply_markup=markup)
    except Exception:
        sent = await msg.answer(
            text=error_post_caption.format(
                post_content=post[0],
                caption=caption,
            ),
            disable_web_page_preview=False,
            reply_markup=markup,
        )
    return sent, None


async def configure_media_group(post: List, **kwargs):
    msg = kwargs.get("msg")
    media = types.MediaGroup()
    for item in post:
        if ".mp4" in item:
            media.attach_video(video=rf"{item}")
        else:
            media.attach_photo(photo=rf"{item}")

    sent = await msg.answer_media_group(media=media)
    text_msg = await msg.answer(text=kwargs.get("caption"),
                                reply_markup=kwargs.get("markup"))
    return sent, text_msg


def regroup_list(data: List, max_inner_list_len: int = 3):
    res = []
    tmp = []
    for item in data:
        tmp.append(item)
        if len(tmp) == max_inner_list_len:
            res.append(tmp)
            tmp = []
    if tmp:
        res.append(tmp)

    return res


def modify_name(name: str) -> str:
    if not demoji.last_downloaded_timestamp():
        demoji.download_codes()

    name = demoji.replace(string=name, repl="")
    name = unicodedata.normalize("NFKC", name)
    name = iuliia.translate(source=name, schema=iuliia.WIKIPEDIA)
    return name.title()


def modify_url(url: str) -> str:
    url = url.split("?")[0].split(".com/")[1]
    url = f'{config.INSTAGRAM_BASE}{url}{"/" if not url.endswith("/") else ""}'
    return url
