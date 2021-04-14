from typing import Dict, List

import asyncpraw
from asyncpraw import models

from settings import config


reddit = asyncpraw.Reddit(
    client_id=config.REDDIT_CLIENT_ID,
    client_secret=config.REDDIT_CLIENT_SECRET,
    user_agent=config.REDDIT_USER_AGENT,
    username=config.REDDIT_USERNAME,
    password=config.REDDIT_PASSWORD,
)


async def submit_post(subreddit_name: str, title: str, url: str):
    sub = await reddit.subreddit(subreddit_name)

    return await sub.submit(title=title, url=url)


async def get_submission_info(submission_code: str):
    submission = await reddit.submission(id=submission_code)
    return submission


async def get_me_as_redditor() -> models.reddit.redditor.Redditor:
    """
    the user (Redditor) according to the
    credentials specified in the .env file
    """
    return await reddit.user.me()
