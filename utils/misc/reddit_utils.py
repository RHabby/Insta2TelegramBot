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


async def crosspost_submission(submission_code: str, subreddit_name: str) -> models.reddit.submission.Submission:
    submission = await reddit.submission(id=submission_code)

    return await submission.crosspost(subreddit=subreddit_name)


async def delete_submission(submission_code: str):
    submission = await reddit.submission(id=submission_code)

    return await submission.delete()


async def get_submission_info(submission_code: str) -> models.reddit.submission.Submission:
    submission = await reddit.submission(id=submission_code)
    return submission


async def get_me_as_redditor() -> models.reddit.redditor.Redditor:
    """
    the user (Redditor) according to the
    credentials specified in the .env file
    """
    return await reddit.user.me()


async def get_redditors_submissions(redditor: models.reddit.redditor.Redditor) -> List:
    """
    info about the last 10 redditor submissions
    """
    redditor_submissions = []

    async for submission in redditor.submissions.new(limit=10):
        redditor_submissions.append(
            {
                "id": submission.id,
                "title": submission.title,
            },
        )

    return redditor_submissions


async def get_redditor_info() -> Dict:
    """
    additional info about the redditor
    """
    owner_redditor = await get_me_as_redditor()
    redditor_submissions = await get_redditors_submissions(redditor=owner_redditor)

    redditor_info = {
        "name": owner_redditor.name,
        "id": owner_redditor.id,
        "comment_karma": owner_redditor.comment_karma,
        "link_karma": owner_redditor.link_karma,
        "submissions": redditor_submissions,
    }

    return redditor_info
