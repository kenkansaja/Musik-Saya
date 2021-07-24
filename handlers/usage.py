import codecs
import heroku3
import aiohttp
import math
import os
import requests
import asyncio
from helpers.decorators import errors, authorized_users_only

from config import (
    HEROKU_APP_NAME,
    HEROKU_API_KEY, SUDO_USERS, BOT_USERNAME)
from pyrogram import Client, filters, emoji

heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

@Client.on_message(command("dn") & filters.user(SUDO_USERS) & ~filters.edited)
async def dyno_usage(dyno):
    """
        Get your account Dyno Usage
    """
    await dyno.edit("`Mendapatkan Informasi Dyno Heroku Anda ヅ`")
    useragent = (
        'Mozilla/5.0 (Linux; Android 10; SM-G975F) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/81.0.4044.117 Mobile Safari/537.36'
    )
    user_id = Heroku.account().id
    headers = {
        'User-Agent': useragent,
        'Authorization': f'Bearer {HEROKU_API_KEY}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    async with aiohttp.ClientSession() as session:
        async with session.get(heroku_api + path, headers=headers) as r:
            if r.status != 200:
                await dyno.client.send_message(
                    dyno.chat_id,
                    f"`{r.reason}`",
                    reply_to=dyno.id
                )
                await dyno.edit("`Tidak Bisa Mendapatkan Informasi Dyno ヅ`")
                return False
            result = await r.json()
            quota = result['account_quota']
            quota_used = result['quota_used']

            """ - User Quota Limit and Used - """
            remaining_quota = quota - quota_used
            percentage = math.floor(remaining_quota / quota * 100)
            minutes_remaining = remaining_quota / 60
            hours = math.floor(minutes_remaining / 60)
            minutes = math.floor(minutes_remaining % 60)

            """ - User App Used Quota - """
            Apps = result['apps']
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
            await asyncio.sleep(20)
            await event.delete()
            return True

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
