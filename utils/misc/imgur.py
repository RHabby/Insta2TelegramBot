import asyncio
from functools import partial

from imgurpython import ImgurClient

from settings import config

imgur = ImgurClient(
    client_id=config.IMGUR_CLIENT_ID,
    client_secret=config.IMGUR_CLIENT_SECRET,
    access_token=config.IMGUR_ACCESS_TOKEN,
    refresh_token=config.IMGUR_REFRESH_TOKEN,
)


async def upload_to_imgur(url: str) -> str:
    upload_to_imgur = partial(imgur.upload_from_url, url, anon=False)

    loop = asyncio.get_running_loop()
    imgur_image = await loop.run_in_executor(None, upload_to_imgur)

    imgur_image = imgur_image["link"]

    return imgur_image
