import asyncio
from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant
from config import SUDO_USERS
from helpers.filters import command
from callsmusic.callsmusic import client as USER


@Client.on_message(command("gcast") & filters.user(SUDO_USERS) & ~filters.edited)
async def gcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("Sedang mengirim pesan global...")
        if not message.reply_to_message:
            await wtf.edit("Balas pesan teks apa pun untuk gcast")
            return
        lmao = message.reply_to_message.text
        async for dialog in USER.iter_dialogs():
            try:
                await USER.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"`Sedang mengirim pesan global` \n\n**Terkirim ke:** `{sent}` chat \n**Gagal terkirim ke:** {failed} chat")
                await asyncio.sleep(0.7)
            except:
                failed=failed+1
                await wtf.edit(f"`Sedang mengirim pesan global` \n\n**Terkirim ke:** `{sent}` Chats \n**Gagal terkirim ke:** {failed} Chats")
                await asyncio.sleep(0.7)

        await message.reply_text(f"`Pesan global selesai` \n\n**Terkirim ke:** `{sent}` Chats \n**Gagal terkirim ke:** {failed} Chats")
                

