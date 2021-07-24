from os import getenv

from dotenv import load_dotenv

load_dotenv()
SESSION_NAME = getenv("SESSION_NAME", "session")

BOT_TOKEN = getenv("BOT_TOKEN")

BOT_NAME = getenv("BOT_NAME")

API_ID = int(getenv("API_ID"))

API_HASH = getenv("API_HASH")

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "7"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))

ASSISTANT = getenv("ASSISTANT")

OWNER = getenv("OWNER")

GROUP = getenv("GROUP", "musikkugroup")

CHANNEL = getenv("CHANNEL", "musikkuchannel")

OWNER = getenv("OWNER", "kenkanasw")

PANDUAN = getenv("PANDUAN", "https://telegra.ph/Panduan-07-20")

BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/7dfd80f33fca97cc14b75.png")
