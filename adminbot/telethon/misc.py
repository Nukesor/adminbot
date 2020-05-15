"""Simple handy helper functions."""
from telethon import events

from adminbot.config import config
from adminbot.telethon import bot
from adminbot.telethon.helper import get_peer_information


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


@bot.on(
    events.NewMessage(
        pattern="\\\\default",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def default_feature_request(event):
    """Print the current chat id and type for debugging."""
    chat_id, peer_type = get_peer_information(event.message.to_id)
    message = (
        "This has already been proposed, but it's not implemented yet and I don't know when (if ever) it will be implemented.\n"
        "Frankly, this is no feature that I need myself. Thereby, I'll most likely not build it myself.\n\n"
        "In case somebody comes up with some nice concept and code, feel free to create a pull request. I'll then consider adding it to the pollbot :)"
    )

    await event.edit(message)
