import requests
from pyrogram import Client as Bot

from config import API_HASH, API_ID, BOT_TOKEN, BG_IMAGE
from callsmusic import run

response = requests.get(BG_IMAGE)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers"),
)

bot.start()
run()
