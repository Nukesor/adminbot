"""Auto-ban logic ."""
from telethon import events

from adminbot.config import config, save_config
from adminbot.telethon import bot


@bot.on(
    events.NewMessage(
        pattern="\\\\ban",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def ban_user(event):
    """Ban a user from the current group."""
    reply_id = event.message.reply_to_msg_id
    if reply_id is None:
        return

    reply_message = await bot.get_messages(event.message.chat_id, ids=reply_id)

    try:
        # Ban this specific user
        await bot.edit_permissions(
            event.message.chat_id,
            reply_message.from_id,
            view_messages=False,
            send_messages=False,
        )
    except Exception as e:
        print(e)

    await event.edit(f"(Bot) Banned user {reply_message.from_id}")


@bot.on(
    events.NewMessage(
        pattern="\\\\unban",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def unban_user(event):
    """Unban a user from the current group."""
    reply_id = event.message.reply_to_msg_id
    if reply_id is None:
        return

    reply_message = await bot.get_messages(event.message.chat_id, ids=reply_id)

    try:
        # Ban this specific user
        await bot.edit_permissions(event.message.chat_id, reply_message.from_id)
    except Exception as e:
        print(e)

    await event.edit(f"(Bot) Unbanned user {reply_message.from_id}")


@bot.on(
    events.NewMessage(
        pattern="\\\\watch",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def watch_chat(event):
    """Watch a specific chat for banned users from my bots."""

    if event.message.chat_id in config["bot"]["watched_chats"]:
        config["bot"]["watched_chats"].remove(event.message.chat_id)
        save_config(config)
        await event.respond(
            f"(Bot) Chat {event.message.chat_id} is no longer being monitored"
        )
        return

    config["bot"]["watched_chats"].append(event.message.chat_id)
    save_config(config)

    await event.respond(f"(Bot) Chat {event.message.chat_id} is now being monitored")
