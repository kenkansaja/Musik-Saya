from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn, CHANNEL, GROUP, ASSISTANT, OWNER, PANDUAN
from helpers.filters import other_filters2, other_filters


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_text(
        f"""hai 👋, saya dapat memutar lagu di voice chat group anda.

➠ Tekan tombol panduan menggunakan bot di bawah jika ingin mengetahui bagaimana cara menggunakan saya.

➠ Tambahkan juga  @{ASSISTANT} ke dalam grup jika anda ingin menambahkan saya ke grup anda.
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 PANDUAN", url = f"{PANDUAN}")
                  ],[
                    InlineKeyboardButton(
                        "💬 Group Support", url=f"https://t.me/{GROUP}"
                    ),
                    InlineKeyboardButton(
                        "🔊 Channel Support", url=f"https://t.me/{CHANNEL}"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "🎁 Kirim Donasi", url=f"https://t.me/{OWNER}"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("start") & other_filters)
async def gstart(_, message: Message):
      await message.reply_text("""**✅ Saya telah online**""",
      reply_markup=InlineKeyboardMarkup(
                  [
                      [
                          InlineKeyboardButton(
                              "💬 GROUP", url=f"https://t.me/{GROUP}"
                          ),
                          InlineKeyboardButton(
                              "OWNER 👮", url=f"https://t.me/{OWNER}"
                          )
                      ]
                  ]
              )
         )

@Client.on_message(filters.command("help") & ~filters.private & ~filters.channel)
async def ghelp(_, message: Message):
    await message.reply_text(
      f"""
**🔰 Perintah**
      
• /play (nama lagu) - Untuk Memutar lagu yang Anda minta melalui youtube
• /song [nama lagu]: Unduh audio lagu dari youtube
• /skip: Melewati trek saat ini
• /pause: Jeda trek
• /resume: Melanjutkan trek yang dijeda
• /end: Menghentikan pemutaran media
      
Semua Perintah Bisa Digunakan Kecuali Perintah /player /skip /pause /resume  /end Hanya Untuk Admin Grup
""",
      reply_markup=InlineKeyboardMarkup(
                  [
                    [InlineKeyboardButton(text = '🔵 ᴏᴡɴᴇʀ', url = f"t.me/{OWNER}")],
                    [InlineKeyboardButton(text = '👥 ɢʀᴏᴜᴘ', url=f"https://t.me/{GROUP}"),
                     InlineKeyboardButton(text = 'ᴄʜᴀɴɴᴇʟ 📣', url=f"https://t.me/{CHANNEL}")]
                ]
        )
    )        
