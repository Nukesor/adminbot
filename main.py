#!/bin/env python
"""Start the bot."""
import typer
import pprint

from adminbot.telethon import bot
from adminbot.config import config


cli = typer.Typer()


@cli.command()
def print_config():
    """Print the current config."""
    pprint.pprint(config)


@cli.command()
def run():
    """Actually start the bot."""
    print("Starting up adminbot.")
    bot.start(phone=config["telegram"]["phone_number"])
    bot.run_until_disconnected()


if __name__ == "__main__":
    cli()
