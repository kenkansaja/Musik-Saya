from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn, CHANNEL, GROUP, ASSISTANT, OWNER, PANDUAN, BOT_NAME, START_IMAGE
from helpers.filters import other_filters2, other_filters


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_sticker("CAACAgUAAxkBAAFF-KFg-jaEvlhu_kNknYQjxsuyDvp--AACjAMAAtpWSVeocCICILIfRSAE")
    await message.reply_photo(
       photo = f"{START_IMAGE}",
       caption = f"""Hai 👋, Saya adalah {BOT_NAME} saya dapat memutar lagu di voice chat group anda.
➜ Tekan tombol panduan menggunakan bot di bawah jika ingin mengetahui bagaimana cara menggunakan saya.
➜ Tambahkan juga  @{ASSISTANT} ke dalam grup jika anda ingin menambahkan saya ke grup anda.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📑 ᴘᴀɴᴅᴜᴀɴ", url = f"{PANDUAN}")
                  ],[
                    InlineKeyboardButton("💬 ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP}"),
                    InlineKeyboardButton("🔊 ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL}")
                ],[ 
                    InlineKeyboardButton("📱 ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER}")]
            ]
        )
    )

@Client.on_message(filters.command(["start", "reload", "admincache"]) & other_filters)
async def gstart(_, message: Message):
    await message.reply_photo(
      photo = f"{START_IMAGE}",
      caption = "**✅ Saya telah online**",
      reply_markup=InlineKeyboardMarkup(
                  [
                      [
                          InlineKeyboardButton("💬 ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP}"),
                          InlineKeyboardButton("ᴏᴡɴᴇʀ 👮", url=f"https://t.me/{OWNER}")
                      ]
                  ]
              )
         )

@Client.on_message(filters.command("hp") & ~filters.private & ~filters.channel)
async def ghelp(_, message: Message):
    await message.reply_text(
      f"""
**🔰 Perintah**
      
• /p (nama lagu) : Untuk Memutar lagu yang Anda minta melalui youtube
• /so [nama lagu] : Unduh audio lagu dari youtube
• /sk : Melewati trek saat ini
• /ps : Jeda trek
• /rs : Melanjutkan trek yang dijeda
• /e : Menghentikan pemutaran media
• /sc : Mencari judul lagu
      
Semua Perintah Bisa Digunakan Kecuali Perintah /ps /rs  /e Hanya Untuk Admin Grup
""",
      reply_markup=InlineKeyboardMarkup(
                  [
                    [InlineKeyboardButton(text = '🔵 ᴏᴡɴᴇʀ', url = f"t.me/{OWNER}")],
                    [InlineKeyboardButton(text = '👥 ɢʀᴏᴜᴘ', url=f"https://t.me/{GROUP}"),
                     InlineKeyboardButton(text = 'ᴄʜᴀɴɴᴇʟ 📣', url=f"https://t.me/{CHANNEL}")]
                ]
        )
    )        
