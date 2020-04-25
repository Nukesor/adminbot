from telethon import functions, events

from adminbot.db import get_pollbot_session
from adminbot.config import config, config_path, save_config
from adminbot.models.pollbot_user import PollbotUser
from adminbot.telethon import bot
from adminbot.telethon.misc import log, get_peer_information


@bot.on(events.ChatAction)
async def autoban_in_watch_chats(event):
    """Users that are banned in a bot, get auto-banned in watched chats."""
    # Only listen for new users to join
    if not (event.user_joined or event.user_added):
        return

    # Check if they joined a watched chat
    if event.chat_id in config["bot"]["watched_chats"]:
        session = get_pollbot_session()
        try:
            # Check if we know the user
            user = session.query(PollbotUser).get(event.user_id)
            if user is None:
                return

            # If the user is perma-banned in the pollbot, ban them
            if user.banned:
                await bot.edit_permissions(
                    event.chat_id,
                    event.user_id,
                    view_messages=False,
                    send_messages=False,
                )

                await event.respond(f"(Bot) Auto-banned user {user.id}")
        except Exception as e:
            print(e)
        finally:
            session.close()


@bot.on(events.ChatAction())
async def autoblock_private_chats(event):
    """Automatically block banned users that contact me via PM."""
    # A new chat has to be created and it has to be private
    if not (event.created and event.is_private):
        return

    session = get_pollbot_session()
    try:
        # Check if we know the user
        user = session.query(PollbotUser).get(event.user_id)
        if user is None:
            return

        # If the user is perma-banned in the pollbot, block them
        if user.banned:
            message = (
                "Hi! This is an automated message.\n"
                "You have been banned from @ultimate_pollbot\n"
                "Users are automatically banned if they reach the vote limit for 3 days in the last week.\n"
                "The ban is irrevertible and permanent.\n"
                "You have been warned. Think about hosting your own bot."
            )
            await event.respond(message)
            # await bot(functions.contacts.BlockRequest(id=event.user_id))

    except Exception as e:
        print(e)
    finally:
        session.close()
