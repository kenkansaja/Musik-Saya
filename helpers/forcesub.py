 # (c) @kenkanasw

import asyncio
from config import GROUP as group
from config import config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def ForceSub(client: Client, event: Message):
    """
    Anda harus bergabung dengan channel atau group kami dulu bos
    :param bot: Pass Client.
    :param event: Pass Message.
    :return: It will return 200 if Successfully Got User in Force Sub Channel and 400 if Found that User Not Participant in Force Sub Channel or User is Kicked from Force Sub Channel it will return 400. Also it returns 200 if Unable to Find Channel.
    """

    try:
        invite_link = await client.create_chat_invite_link(chat_id=(int(config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(client, event)
        return fix_
    except Exception as err:
        print(f"Tidak dapat melakukan Paksa Berlangganan ke {Config.UPDATES_CHANNEL}\n\nKesalahan: {err}\n\nHubungi Grup Dukungan: https://t.me/{group}")
        return 200
    try:
        user = await client.get_chat_member(chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL), user_id=event.from_user.id)
        if user.status == "kicked":
            await client.send_message(
                chat_id=event.from_user.id,
                text=f"Maaf, Anda dilarang menggunakan saya. Hubungi [Grup Dukungan](https://t.me/{group}) saya.",
                parse_mode="markdown",
                disable_web_page_preview=True,
                reply_to_message_id=event.message_id
            )
            return 400
        else:
            return 200
    except UserNotParticipant:
        await client.send_message(
            chat_id=event.from_user.id,
            text="**Silakan Bergabunglah dengan Saluran Pembaruan Saya untuk menggunakan Bot ini!**\n\nKarena Kelebihan Beban, Hanya Pelanggan Saluran yang dapat menggunakan Bot!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ]
                ]
            ),
            parse_mode="markdown",
            reply_to_message_id=event.message_id
        )
        return 400
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(client, event)
        return fix_
    except Exception as err:
        print(f"Ada yang Salah! Tidak dapat melakukan Langganan Paksa.\nKesalahan: {err}\n\nHubungi Grup Dukungan: https://t.me/{group}")
        return 200
