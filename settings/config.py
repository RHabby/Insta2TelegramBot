import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

# [Telegram]
TOKEN = os.environ.get("TOKEN")
admins = [
    os.environ.get("admin_01"),
    os.environ.get("admin_02"),
]

# [redis]
REDIS_HOST = os.environ.get("REDIS_HOST") or 'localhost'
REDIS_PORT = 6379

# [Imgur API]
IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID")
IMGUR_CLIENT_SECRET = os.environ.get("IMGUR_CLIENT_SECRET")
IMGUR_ACCESS_TOKEN = os.environ.get("IMGUR_ACCESS_TOKEN")
IMGUR_REFRESH_TOKEN = os.environ.get("IMGUR_REFRESH_TOKEN")

# [Reddit API]
REDDIT_BASE_URL = "https://www.reddit.com"
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.environ.get("REDDIT_USERNAME")
REDDIT_PASSWORD = os.environ.get("REDDIT_PASSWORD")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT")

# [Instagram]
COOKIE = os.environ.get("COOKIE")
INSTAGRAM_BASE = os.environ.get("INSTAGRAM_BASE")

# [subreddits]
SUBREDDIT_LIST = [
    os.environ.get("s_01"),
    os.environ.get("s_02"),
    os.environ.get("s_03"),
    os.environ.get("s_04"),
]
