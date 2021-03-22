from aiogram.dispatcher.filters.state import StatesGroup, State


class PostToReddit(StatesGroup):
    reddit = State()
    which_one = State()
    subreddit = State()
    enter_title = State()
    edit_title = State()
