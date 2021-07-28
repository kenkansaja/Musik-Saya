# the logging things
import logging

from pyrogram.types import Message
from search_engine_parser import GoogleSearch
from youtube_search import YoutubeSearch

from pyrogram import Client as app, filters

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

import pyrogram

logging.getLogger("pyrogram").setLevel(logging.WARNING)

@app.on_message(pyrogram.filters.command(["sc"]))
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("/search (judul lagu)!")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("Searching....")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"──────── ⋆⋅☆⋅⋆ ────────\nᴊᴜᴅᴜʟ - {results[i]['title']}\n"
            text += f"──────── ⋆⋅☆⋅⋆ ────────\nᴅᴜʀᴀꜱɪ - {results[i]['duration']}\n"
            text += f"──────── ⋆⋅☆⋅⋆ ────────\nᴘᴇɴᴏɴᴛᴏɴ - {results[i]['views']}\n"
            text += f"──────── ⋆⋅☆⋅⋆ ────────\nᴄʜᴀɴɴᴇʟ - {results[i]['channel']}\n\n"
            text += f"──────── ⋆⋅☆⋅⋆ ────────\n`https://youtube.com{results[i]['url_suffix']}`\n"
            text += f"════════════════════\n\n"
            i += 1      
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))
