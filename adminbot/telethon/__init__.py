"""Telethon bot instance creation."""
from telethon import TelegramClient

from adminbot.config import config


bot = TelegramClient(
    "reddit_media_bot",
    config["telegram"]["app_api_id"],
    config["telegram"]["app_api_hash"],
)


# Reexport for easy bot initialization
from .misc import *
from .ban import *
from .watcher import *
