"""Simple handy helper functions."""
import toml
from telethon import events

from adminbot.config import config, config_path
from adminbot.telethon import bot
from adminbot.telethon.helper import log, get_peer_information


@bot.on(
    events.NewMessage(
        pattern="\\\\id",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def print_id(event):
    """Print the current chat id and type for debugging."""
    chat_id, peer_type = get_peer_information(event.message.to_id)
    message = f"(Bot) Chat type: {peer_type}, chat id: {chat_id}"

    await event.respond(message)
