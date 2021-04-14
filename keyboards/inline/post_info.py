from typing import List

from aiogram import types

from settings import config


def generate_post_kboard(
        username: str, user_url: str,
        post_link: str, user_id: int) -> types.InlineKeyboardMarkup:
    common_buttons = [
        types.InlineKeyboardButton(text=username, url=user_url),
        types.InlineKeyboardButton(text="post link", url=post_link),
    ]
    admin_buttons = [
        types.InlineKeyboardButton(
            text="reddit", callback_data="reddit"),
        types.InlineKeyboardButton(text="delete", callback_data="delete"),
    ]

    post_kboard = types.InlineKeyboardMarkup(row_width=2)
    post_kboard.add(*common_buttons)

    if str(user_id) in config.admins:
        post_kboard.add(*admin_buttons)

    return post_kboard


def generate_which_one_kboard(post_content_len: int) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(
            text=i, callback_data=f'which_one,{i}') for i in range(1, int(post_content_len) + 1)
    ]

    which_one_kboard = types.InlineKeyboardMarkup(row_width=3)
    which_one_kboard.add(*buttons)

    return which_one_kboard


def generate_subreddit_kboard(subreddit_list: List) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(
            text=subreddit, callback_data=subreddit,
        ) for subreddit in subreddit_list
    ]

    subreddit_kboard = types.InlineKeyboardMarkup(row_width=2)
    subreddit_kboard.add(*buttons)
    subreddit_kboard.add(types.InlineKeyboardButton(
        text="edit title", callback_data="edit_title"))

    return subreddit_kboard


def generate_posted_kboard(permalink: str) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(
            text="Posted on Reddit:", callback_data="bullshit",
        ),
        types.InlineKeyboardButton(
            text="postlink", url=permalink,
        ),
    ]

    posted_kboard = types.InlineKeyboardMarkup(row_width=2)
    posted_kboard.add(*buttons)

    return posted_kboard


def generate_admin_kboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="data info", callback_data="data"),
        types.InlineKeyboardButton(text="redditor info", callback_data="redditor"),
    ]

    admin_kboard = types.InlineKeyboardMarkup(row_width=1)
    admin_kboard.add(*buttons)

    return admin_kboard


def generate_data_info_kboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="clear data", callback_data="clear"),
    ]

    data_kboard = types.InlineKeyboardMarkup(row_width=2)
    data_kboard.add(*buttons)

    return data_kboard


def generate_redditor_info_kboard(submissions) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text=submission["title"], callback_data=f'submission,{submission["id"]}')
        for submission in submissions
    ]

    redditor_kboard = types.InlineKeyboardMarkup(row_width=2)
    redditor_kboard.add(*buttons)

    return redditor_kboard
