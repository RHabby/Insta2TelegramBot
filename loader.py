from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from settings import config

from utils.InstaCrawler import app


bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host=config.REDIS_HOST)
dp = Dispatcher(bot, storage=storage)

insta = app.insta_crawler.InstaCrawler(cookie=config.COOKIE)
