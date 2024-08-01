import os
import sys
import json
import time
import shutil
from asyncio import get_event_loop, new_event_loop, set_event_loop
try :
  import uvloop
except:
   pass
import requests

from pyrogram import Client
from TelegramBot.config import *
from TelegramBot.logging import LOGGER
from apscheduler.schedulers.asyncio import AsyncIOScheduler

try:
  uvloop.install()
except:
  LOGGER(__name__).info("NO uvloop installed")
LOGGER(__name__).info("Starting TelegramBot....")
BotStartTime = time.time()


VERSION_ASCII = """
  =============================================================
  You MUST need to be on python 3.8 or above, shutting down the bot...
  =============================================================
  """

if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    LOGGER(__name__).critical(VERSION_ASCII)
    sys.exit(1)
'''
if not os.path.exists("token.json"):
    LOGGER(__name__).critical("token.json not found. quitting...")
    sys.exit(1)

if not os.path.exists("credentials.json"):
    LOGGER(__name__).info("credentials.json not found. quitting....")
    sys.exit(1)

with open(f"{os.getcwd()}/token.json", "r") as file:
    access_token = file.read()
access_token = json.loads(access_token)

'''

#LOGGER(__name__).info(BANNER)
LOGGER(__name__).info("setting up event loop....")


try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()

# creating download directory
if not os.path.exists("download"):
    os.mkdir("download")


async def clear_download():
    """Clear download directory after every 24 hour."""

    shutil.rmtree("download")
    os.mkdir("download")


scheduler = AsyncIOScheduler()
scheduler.add_job(clear_download, "interval", minutes=1440)
scheduler.start()


LOGGER(__name__).info("initiating the client....")
plugins = dict(root="TelegramBot/plugins")
bot = Client(
    "TelegramBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins,
)
