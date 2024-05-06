"""Manual ban logic."""

from telethon import events

from adminbot.config import config
from adminbot.sentry import handle_exceptions
from adminbot.telethon import bot


@bot.on(
    events.NewMessage(
        pattern="\\\\ban",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
@handle_exceptions
async def ban_user(event):
    """Ban a user from the current group."""
    reply_id = event.message.reply_to_msg_id
    if reply_id is None:
        return

    reply_message = await bot.get_messages(event.message.chat_id, ids=reply_id)

    # Ban this specific user
    await bot.edit_permissions(
        event.message.chat_id,
        reply_message.from_id,
        view_messages=False,
        send_messages=False,
    )

    await event.edit(f"(Bot) Banned user {reply_message.from_id}")


@bot.on(
    events.NewMessage(
        pattern="\\\\unban",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
@handle_exceptions
async def unban_user(event):
    """Unban a user from the current group."""
    reply_id = event.message.reply_to_msg_id
    if reply_id is None:
        return

    reply_message = await bot.get_messages(event.message.chat_id, ids=reply_id)

    # Ban this specific user
    await bot.edit_permissions(event.message.chat_id, reply_message.from_id)

    await event.edit(f"(Bot) Unbanned user {reply_message.from_id}")
