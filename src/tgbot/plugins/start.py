from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def on_start(_, message) -> None:
    text = (
        "👋 Hello! I'm a bot to give you <b>direct download links</b> for the Youtube Videos using <a href='https://y2mate.com'>Y2Mate</a>'s API.\n\n"
        "🏷 Send me /getdownloadlink <video-url> to get download options."
        )
    buttons = [
        [InlineKeyboardButton("📝 Source code", url="https://github.com/SastaDev/y2mate-bot")],
        [InlineKeyboardButton("🆘 Help group", url="https://t.me/KangersChat")]
        ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons), disable_webpage_preview=True)