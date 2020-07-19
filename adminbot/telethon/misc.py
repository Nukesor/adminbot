"""Simple helper functions."""
from telethon import events

from adminbot.config import config
from adminbot.db import get_pollbot_session
from adminbot.models import PollbotUser
from adminbot.sentry import handle_exceptions
from adminbot.telethon import bot
from adminbot.telethon.helper import get_peer_information


@bot.on(
    events.NewMessage(
        pattern="\\\\id", forwards=False, from_users=config["bot"]["admin"],
    )
)
@handle_exceptions
async def print_id(event):
    """Print the current chat id and type for debugging."""
    message = event.message
    reply_id = message.reply_to_msg_id

    # If the command is a reply to a message, get information about the sender of the message.
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
        pattern="\\\\default", forwards=False, from_users=config["bot"]["admin"],
    )
)
@handle_exceptions
async def default_feature_request(event):
    """Print the current chat id and type for debugging."""
    chat_id, peer_type = get_peer_information(event.message.to_id)
    message = (
        "This has already been proposed, but it's not implemented yet and I don't know when (if ever) it will be implemented.\n"
        "Frankly, this is no feature that I need myself. Thereby, I'll most likely not build it myself.\n\n"
        "In case somebody comes up with some nice concept and code, feel free to create a pull request. I'll then consider adding it to the pollbot :)"
    )

    await event.edit(message)


@bot.on(
    events.NewMessage(
        pattern="\\\\check", forwards=False, from_users=config["bot"]["admin"],
    )
)
@handle_exceptions
async def check_watched_chats(event):
    """Go trough all chats and remove banned/deleted users."""
    session = get_pollbot_session()

    try:
        for chat_id in config["bot"]["watched_chats"]:
            participants = await bot.get_participants(chat_id, limit=200)

            for user in participants:
                pollbot_user = session.query(PollbotUser).get(user.id)
                if pollbot_user is None:
                    continue

                # Kick them
                # if pollbot_user.deleted or pollbot_user.banned:
                #    await bot.edit_permissions(
                #        chat_id, user_id, view_messages=False, send_messages=False,
                #    )
    finally:
        session.close()
