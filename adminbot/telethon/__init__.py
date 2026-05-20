"""Telethon bot instance creation."""
from telethon import TelegramClient
import os

from telethon.sessions import SQLiteSession

from adminbot.config import config

path = os.path.expanduser("~/.local/share/adminbot.sql")

bot = TelegramClient(
    SQLiteSession(path),
    config["telegram"]["app_api_id"],
    config["telegram"]["app_api_hash"],
)

# Reexport for easy bot initialization
from .misc import *
from .ban import *
from .speech_to_text import *
