from telethon import events

from adminbot.db import get_pollbot_session
from adminbot.config import config, config_path, save_config
from adminbot.models.pollbot_user import PollbotUser
from adminbot.telethon import bot
from adminbot.telethon.misc import log, get_peer_information

@bot.on(events.ChatAction)
async def autoban_in_watch_chats(event):
    """Users that are banned in a bot, get auto-banned in watched chats."""
    # Check all users that join a group
    if event.user_joined or event.user_added:
        # Check if they joined a watched chat
        if event.chat_id in config['bot']['watched_chats']:
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

                    await event.respond(f'Banned user {user.id}')
            except Exception as e:
                print(e)
            finally:
                session.close()
