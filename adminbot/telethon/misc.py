"""Simple helper functions."""

from telethon import events

from adminbot.config import config
from adminbot.sentry import handle_exceptions
from adminbot.telethon import bot
from adminbot.telethon.helper import get_peer_information


@bot.on(
    events.NewMessage(
        pattern="\\\\id",
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
@handle_exceptions
async def print_chat_id(event):
    """Print the current chat id and type for debugging."""
    message = event.message
    reply_id = message.reply_to_msg_id

    # If the command is a reply to a message, get information
    # about the sender of the message.
    if reply_id is not None:
        message = await bot.get_messages(event.message.chat_id, ids=reply_id)
        sender = await bot.get_input_entity(message.from_id)
        peer_id, peer_type = get_peer_information(sender)
    else:
        peer_id, peer_type = get_peer_information(message.to_id)

    response = (
        "(Bot) Meta information of this peer:\n"
        f"Peer type: {peer_type}\n"
        f"Peer id: {peer_id}\n"
        f"Chat id: {event.chat_id}"
    )

    await event.edit(response)


@bot.on(
    events.NewMessage(
        pattern="\\\\message_id",
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
@handle_exceptions
async def print_message_id(event):
    """Print the current chat id and type for debugging."""
    message = event.message
    reply_id = message.reply_to_msg_id

    if reply_id is None:
        response = "You have to reply to a message"
    else:
        referenced_message = await bot.get_messages(event.message.chat_id, ids=reply_id)
        response = f"Message id is: {referenced_message.id}"

    await event.edit(response)
