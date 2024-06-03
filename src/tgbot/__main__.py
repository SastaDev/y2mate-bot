import asyncio
import logging

from pyrogram import idle

from . import bot

logger = logging.getLogger(__name__)

async def main() -> None:
    logger.info("Starting bot...")
    await bot.start()
    logger.info("Bot started!")
    
    await idle()
    
    logger.info("Stopping bot...")
    await bot.stop()
    logger.info("Bot stopped!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
        logger.info("Exiting...")