import logging

from .config import Config

from pyrogram import Client
from y2mate import Y2MateClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

bot = Client(
    name=__name__,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins={"root": "tgbot/plugins"}
    )

y2mate_client = Y2MateClient()