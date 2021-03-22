from aiogram import types

from settings import config


def generate_user_info_kboard(
        username: str, user_url: str,
        user_id: str, external_url: str = None) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(
            text="12 Posts", callback_data=f"posts{user_url}"),
        types.InlineKeyboardButton(
            text="Stories", callback_data=f"stories{user_url}"),
        types.InlineKeyboardButton(
            text=f"{username}`s Profile", url=f"{user_url}"),
    ]
    admin_buttons = [
        types.InlineKeyboardButton(text="delete", callback_data="delete"),
    ]

    user_info_kboard = types.InlineKeyboardMarkup(row_width=2)
    user_info_kboard.add(*buttons)

    if external_url:
        user_info_kboard.add(
            types.InlineKeyboardButton(
                text=f"{username}`s External Link", url=f"{external_url}"),
        )

    if str(user_id) in config.admins:
        user_info_kboard.add(*admin_buttons)

    return user_info_kboard
