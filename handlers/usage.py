import codecs
import heroku3
import aiohttp
import math
import os
import requests
import asyncio
from helpers.decorators import errors, authorized_users_only
from time import time
from datetime import datetime
from helpers.filters import command
from pyrogram import Client, filters, emoji
from pyrogram.types import Message
from config import HEROKU_API, HEROKU_APP_NAME, SUDO_USERS

try:
    if Var.HEROKU_API and Var.HEROKU_APP_NAME:
        HEROKU_API = Var.HEROKU_API
        HEROKU_APP_NAME = Var.HEROKU_APP_NAME
        Heroku = heroku3.from_key(Var.HEROKU_API)
        app = Heroku.app(Var.HEROKU_APP_NAME)
except BaseException:
    HEROKU_API = None
    HEROKU_APP_NAME = None

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)
async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command("dn") & filters.user(SUDO_USERS) & ~filters.edited)
async def dyno_usage(dyno):
    await dyno.edit("`Mendapatkan Informasi Dyno Heroku`")
    for apps in Apps:
        if apps.get('app_uuid') == app.id:
            AppQuotaUsed = apps.get('quota_used') / 60
            AppPercentage = math.floor(
                apps.get('quota_used') * 100 / quota)
            break
        else:
            AppQuotaUsed = 0
            AppPercentage = 0

            AppHours = math.floor(AppQuotaUsed / 60)
            AppMinutes = math.floor(AppQuotaUsed % 60)

            await dyno.edit(
                "┏━━━━━━༻❁༺━━━━━━┓\nＩＮＦＯＲＭＡＳＩ　ＤＹＮＯ\n┗━━━━━━༻❁༺━━━━━━┛\n\n╭━┯━━━━━━━━━━━━━━┯━╮\n"
                f"✸ **Penggunaan Dyno {app.name} :**\n"
                f"❉ **{AppHours} Jam - "
                f"{AppMinutes} Menit  -  {AppPercentage}%**\n"
                "✲━─━─━─━─━─━─━─━─━✲\n"
                "✸ **Sisa Dyno Bulan Ini :**\n"
                f"❉ **{hours} Jam - {minutes} Menit  "
                f"-  {percentage}%**\n"
                "╰━┷━━━━━━━━━━━━━━┷━╯"
            )
              

@Client.on_message(command("pn") & ~filters.edited)
@authorized_users_only
async def ping_pong(client: Client, m: Message):
    start = time()
    m_reply = await m.reply_text("Pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        f"{emoji.PING_PONG} **PONG!!**\n"
        f"`{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command("up") & ~filters.edited)
@authorized_users_only
async def get_uptime(client: Client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        f"{emoji.ROBOT}\n"
        f"• **Uptime:** `{uptime}`\n"
        f"• **Start Time:** `{START_TIME_ISO}`"
    )
