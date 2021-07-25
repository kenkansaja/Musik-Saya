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
    global que
    lel = await message.reply("**🔎 Sedang Mencari Lagu**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id
    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        lmoa = await _.get_chat_member(chid, wew)
    except:
           for administrator in administrators:
                      if administrator == message.from_user.id:  
                          try:
                              invitelink = await _.export_chat_invite_link(chid)
                          except:
                              await lel.edit(
                                  "<b>Tambahkan saya sebagai admin group Anda terlebih dahulu.</b>",
                              )
                              return

                          try:
                              await USER.join_chat(invitelink)
                              await USER.send_message(message.chat.id, "Saya bergabung dengan group ini untuk memainkan musik di VCG.")
                              await lel.edit(
                                  "<b>{user.first_name} berhasil bergabung dengan Group anda</b>",
                              )

                          except UserAlreadyParticipant:
                              pass
                          except Exception as e:
                              await lel.edit(
                                  f"<b>🔴 Flood Wait Error 🔴 \n{user.first_name} tidak dapat bergabung dengan group Anda karena banyaknya permintaan bergabung untuk userbot! Pastikan pengguna tidak dibanned dalam group."
                        f"\n\nAtau tambahkan @{user.username} Bot secara manual ke Group Anda dan coba lagi.</b>",
                              )
                              pass
    try:
        chatdetails = await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<b>{user.first_name} terkena banned dari Group ini, Minta admin untuk unban @{user.username} secara manual, Lalu coba play lagi.</b>"
        )
        return     
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name
    sender_id = message.from_user.id
    user_id = message.from_user.id
    sender_name = message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    await lel.edit(f"**🔄 Sedang Memproses Lagu**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://www.youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
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
        qeue = que.get(message.chat.id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
        photo = "final.png",
        caption = f"🏷 **Judul:** [{title[:60]}]({url})\n⏱ **Durasi:** `{duration}`\n💡 **Status:** `Antrian ke {position}`\n" \
                + f"🎧 **Permintaan** {message.from_user.mention}",
        reply_markup = keyboard
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = message.chat.id
        que[chat_id] = []
        qeue = que.get(message.chat.id)
        s_name = title            
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]      
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo = "final.png",
        caption=f"🏷 **Judul :** [{title[:60]}]({url})\n**⏱ Durasi :** {duration}\n" \
                        + f"🎵 **Antri :** {position}!\n🎧 **Permintaan :** {requested_by}".format(message.from_user.mention()),
        
        reply_markup = keyboard
        )
        os.remove("final.png")
        return await lel.delete()
