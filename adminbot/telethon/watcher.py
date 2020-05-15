from telethon import events
from datetime import date

from adminbot.db import get_pollbot_session
from adminbot.config import config
from adminbot.models import PollbotUser, PollbotUserStat
from adminbot.telethon import bot


@bot.on(events.ChatAction)
async def autoban_in_watch_chats(event):
    """Users that are banned in a bot, get auto-banned in watched chats."""
    # Only listen for new users to join
    if not (event.user_joined or event.user_added):
        return

    # Check if they joined a watched chat
    if event.chat_id in config["bot"]["watched_chats"]:
        print("Got new user in watched chat:")
        print(event)

        session = get_pollbot_session()
        try:
            # Check if we know the user
            user = session.query(PollbotUser).get(event.user_id)
            if user is None:
                return

            # If the user is perma-banned or deleted in the pollbot, ban them
            if user.banned or user.deleted:
                await bot.edit_permissions(
                    event.chat_id,
                    event.user_id,
                    view_messages=False,
                    send_messages=False,
                )

                await event.respond(f"(Bot) Removed banned user {user.id} (UPB user)")
        except Exception as e:
            print(e)
        finally:
            session.close()


@bot.on(events.ChatAction())
async def autoblock_in_private_chats(event):
    """Automatically block banned users that contact me via PM."""
    # A new chat has to be created and it has to be private
    if not (event.created and event.is_private):
        return

    print("Got new private chat:")
    print(event)
    session = get_pollbot_session()
    try:
        # Check if we know the user
        user = session.query(PollbotUser).get(event.user_id)
        if user is None:
            print("User isn't a pollbot user: {}", event.user_id)
            return

        if user.deleted:
            print("User is deleted")
            message = (
                "Hi! This is an automated message.\n"
                "Your @ultimate_pollbot account has been permanently deleted.\n"
                "This action is irrevertible to protect against vote manipulation.\n"
                "Think about hosting your own bot.\n"
                "I won't see any messages you're writing, this is a completely automated account."
            )
            await event.respond(message)
            # await bot(functions.contacts.BlockRequest(id=event.user_id))

        # If the user is perma-banned in the pollbot, block them
        if user.banned:
            print("User is banned")
            message = (
                "Hi! This is an automated message.\n"
                "You have been banned from @ultimate_pollbot\n"
                "Users are automatically banned if they reach the vote limit for 3 days in the last week.\n"
                "The ban is irrevertible and permanent.\n"
                "You have been warned. Think about hosting your own bot."
            )
            await event.respond(message)
            # await bot(functions.contacts.BlockRequest(id=event.user_id))

        stat = session.query(PollbotUserStat).get((date.today(), user))
        if stat.votes >= 250:
            print("User is temp banned")
            message = (
                "Hi! This is an automated message.\n"
                "You have been temporarily banned from @ultimate_pollbot\n"
                "Users are automatically banned if they spam and reach the vote limit.\n"
                "Continue spamming and you'll be banned permanently.\n"
                "If you think this is a bug, please don't PM me, but rather read my bio and go to my support channel.\n"
            )
            await event.respond(message)

    except Exception as e:
        print(e)
    finally:
        session.close()
