from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues


from os import path
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch


import converter
from downloaders import youtube

from config import BOT_NAME as bn
from config import DURATION_LIMIT
from config import GROUP as group
from config import CHANNEL as channel
from config import OWNER as kenkan
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import os
import aiohttp
import aiofiles
import ffmpeg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")




@Client.on_message(command("p") & other_filters)
async def play(_, message: Message):
    lel = await message.reply("🔄 **Memproses lagu...**")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("📣 ᴄʜᴀɴɴᴇʟ", url=f"t.me/{channel}"),
                                InlineKeyboardButton("ɢʀᴏᴜᴘ 👥", url=f"t.me/{group}")
                            ],[
                                InlineKeyboardButton("🌟 ᴏᴡɴᴇʀ 🌟", url=f"t.me/{kenkan}")                                
                            ]
                        ]
                    )
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            await lel.edit(f"❌ Video dengan durasi lebih dari {DURATION_LIMIT} minute(s) tidak dapat dimainkan!")
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/c9c7e24b03919fa5f8022.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "locally added"
        keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("📣 ᴄʜᴀɴɴᴇʟ", url=f"t.me/{channel}"),
                                InlineKeyboardButton("ɢʀᴏᴜᴘ 👥", url=f"t.me/{group}")
                            ],[
                                InlineKeyboardButton("🌟 ᴏᴡɴᴇʀ 🌟", url=f"t.me/{kenkan}")                                
                            ]
                        ]
                    )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            #url = f"https://youtube.com{results[0]['url_suffix']}"
            #print(results)
            title = results[0]["title"][:40]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("📣 ᴄʜᴀɴɴᴇʟ", url=f"t.me/{channel}"),
                                InlineKeyboardButton("ɢʀᴏᴜᴘ 👥", url=f"t.me/{group}")
                            ],[
                                InlineKeyboardButton("🌟 ᴏᴡɴᴇʀ 🌟", url=f"t.me/{kenkan}")                                
                            ]
                        ]
                    )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/c9c7e24b03919fa5f8022.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("📣 ᴄʜᴀɴɴᴇʟ", url=f"t.me/{channel}"),
                                InlineKeyboardButton("ɢʀᴏᴜᴘ 👥", url=f"t.me/{group}")
                            ],[
                                InlineKeyboardButton("🌟 ᴏᴡɴᴇʀ 🌟", url=f"t.me/{kenkan}")                                
                            ]
                        ]
                    )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        await lel.edit("🔎 **Menemukan lagu...**")
        sender_id = message.from_user.id
        user_id = message.from_user.id
        sender_name = message.from_user.first_name
        user_name = message.from_user.first_name
        rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

        query = ''
        for i in message.command[1:]:
            query += ' ' + str(i)
        print(query)
        await lel.edit("🎵 **Persiapan memutar lagu...**")
        ydl_opts = {"format": "141/bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            #print(results)
            title = results[0]["title"][:40]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]

            except Exception as e:
        await lel.edit("**Lagu tidak ditemukan.** Coba cari dengan judul lagu yang lebih jelas")
        print(str(e))
        return
    try:    
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❌ **Lagu dengan durasi lebih dari `{DURATION_LIMIT}` menit tidak dapat diputar!**")
             return
    except:
        pass
    durl = url
    durl = durl.replace("youtube","youtubepp")
    keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("📣 ᴄʜᴀɴɴᴇʟ", url=f"t.me/{channel}"),
                                InlineKeyboardButton("ɢʀᴏᴜᴘ 👥", url=f"t.me/{group}")
                            ],[
                                InlineKeyboardButton("🌟 ᴏᴡɴᴇʀ 🌟", url=f"t.me/{kenkan}")                                
                            ]
                        ]
                    )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="final.png", 
        caption=f"🏷 **Judul :** [{title[:60]}]({url})\n**⏱ Durasi :** {duration}\n" \
                + f"🎵 **Antri :** {position}!\n🎧 **Permintaan :** {requested_by}".format(message.from_user.mention()),
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption=f"🏷 **Judul :** [{title[:60]}]({url})\n**⏱ Durasi :** {duration}\n" \
                + f"💡 **Status :** Playing\n🎧 **Permintaan :** {requested_by}".format(
        message.from_user.mention()
        ),
    )
        os.remove("final.png")
        return await lel.delete()
