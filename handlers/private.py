from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn, CHANNEL, GROUP, ASSISTANT, OWNER
from helpers.filters import other_filters2, other_filters


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_sticker("CAACAgUAAxkBAAEKORJguwR4VsN1PCqbNh82LgABstqGU2EAAjMCAAK8hthX2HwTiIOxnxofBA")
    await message.reply_text(
        f"""hai 👋, saya dapat memutar lagu di voice chat group anda.

➠ Tekan tombol panduan menggunakan bot di bawah jika ingin mengetahui bagaimana cara menggunakan saya.

➠ Tambahkan juga  @{ASSISTANT} ke dalam grup jika anda ingin menambahkan saya ke grup anda.
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 PANDUAN", callback_data="help")
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
      await message.reply_text("""**✅ ava music player is online**""",
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
         
@Client.on_message(filters.command("help") & other_filters)
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
                    [InlineKeyboardButton(text = '👥 ɢʀᴏᴜᴘ', url=f"https://t.me/{SUPPORT_GROUP}"),
                     InlineKeyboardButton(text = 'ᴄʜᴀɴɴᴇʟ 📣', url=f"https://t.me/{UPDATES_CHANNEL}")]
                ]
        )
    )        
@Client.on_message(filters.private & filters.incoming & filters.command(['help']))
def _help(client, message):
    client.send_message(chat_id = message.chat.id,
        text = tr.HELP_MSG,
        parse_mode="markdown",
        disable_web_page_preview=True,
        disable_notification=True,
        reply_markup = InlineKeyboardMarkup(map(1)),
        reply_to_message_id = message.message_id
    )

help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))
