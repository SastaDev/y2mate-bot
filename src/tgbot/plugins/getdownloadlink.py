from uuid import uuid4

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters

from .. import y2mate_client

CACHE = {}

@Client.on_message(filters.command("getdownloadlink"))
async def on_getdlink(_, message) -> None:
    url = message.command[1] if len(message.command) > 1 else None
    if url is None:
        await message.reply("ℹ️ Please provide a youtube video url after the command.")
        return
    
    status = await message.reply("ℹ️ <i>Extracting information from the url...</i>")
    
    try:
        metadata = await y2mate_client.from_url(url)
    except Exception as exc:
        await message.reply(f"<b>ERROR:</b> {exc}")
        return
    
    caption = (
        f"<b>{metadata.title}</b>\n\n"
        "📥 <b>Select a download option:</b>"
        )
    
    buttons = []
    max_items = 3
    if metadata.video_links:
        buttons.append([InlineKeyboardButton("📹 Video:", callback_data="nocallback_data")])
        
        for i in range(0, len(metadata.video_links), max_items):
            row = []
            for link_info in metadata.video_links[i:i+max_items]:
                uid = str(uuid4())
                CACHE[uid] = {"video_id": metadata.video_id, "key": link_info.key, "size": link_info.size}
                row.append(InlineKeyboardButton(f"📥 {link_info.quality} ({link_info.format.upper()}) [{link_info.size}]", callback_data=f"getdownloadlink {uid}"))
            buttons.append(row)
    if metadata.audio_links:
        buttons.append([InlineKeyboardButton("🎵 Audio:", callback_data="nocallback_data")])
        
        for i in range(0, len(metadata.audio_links), max_items):
            row = []
            for link_info in metadata.audio_links[i:i+max_items]:
                uid = str(uuid4())
                CACHE[uid] = {"video_id": metadata.video_id, "key": link_info.key, "size": link_info.size}
                row.append(InlineKeyboardButton(f"📥 {link_info.quality} ({link_info.format.upper()}) [{link_info.size}]", callback_data=f"getdownloadlink {uid}"))
            buttons.append(row)
    if metadata.other_links:
        buttons.append([InlineKeyboardButton("💿 Other:", callback_data="nocallback_data")])
        
        for i in range(0, len(metadata.other_links), max_items):
            row = []
            for link_info in metadata.other_links[i:i+max_items]:
                uid = str(uuid4())
                CACHE[uid] = {"video_id": metadata.video_id, "key": link_info.key, "size": link_info.size}
                row.append(InlineKeyboardButton(f"📥 {link_info.quality} ({link_info.format.upper()}) [{link_info.size}]", callback_data=f"getdownloadlink {uid}"))
            buttons.append(row)
    
    await message.reply_photo(metadata.get_thumbnail_url(), caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
    await status.delete()

@Client.on_callback_query(filters.regex(r"^getdownloadlink (.+)$"))
async def on_getdownloadlink(_, callback_query) -> None:
    uid = callback_query.matches[0].group(1)
    if uid not in CACHE:
        await callback_query.answer("⚠️ Expired! Please request again.", show_alert=True)
        return
    
    video_id, key, size = CACHE[uid]["video_id"], CACHE[uid]["key"], CACHE[uid]["size"]
    
    try:
        download_info = await y2mate_client.get_download_info(video_id, key)
    except Exception as exc:
        await callback_query.answer("⚠️ Unexpected error!", show_alert=True)
        await callback_query.message.reply(f"ERROR: {exc}")
        return
    
    text = (
        f"📥 <b>Download information:</b>\n\n"
        f"🎬 <b>Title:</b> {download_info.title}\n"
        f"⭐️ <b>Quality:</b> {download_info.quality or 'not found'}\n"
        f"💾 <b>Size:</b> <code>{size or 'not found'}</code>"
        )
    buttons = [
        [InlineKeyboardButton("Download", url=download_info.download_link)]
        ]
    await callback_query.message.reply(text, reply_markup=InlineKeyboardMarkup(buttons))
    await callback_query.answer()