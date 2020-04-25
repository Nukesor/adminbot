#!/bin/python3
"""Entry script."""

from adminbot.telethon import bot
from adminbot.config import config

print("Starting up")
bot.start(phone=config["telegram"]["phone_number"])
bot.run_until_disconnected()
