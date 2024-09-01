"""Simple helper functions."""

import getpass
import os
import sys

import requests
from telethon import events, types

from adminbot.sentry import handle_exceptions
from adminbot.telethon import bot
from adminbot.telethon.helper import get_peer_information


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@bot.on(events.NewMessage())
@handle_exceptions
async def speech_to_text(event):
    """Print the current chat id and type for debugging."""
    message = event.message

    # Ignore non-private and non-audio messages.
    if not message.is_private or not is_audio_message(message):
        return

    print("Got audio message from private chat")

    # Try to detect text
    # Return early if something went wrong.
    output = await detect_text(message)
    if output is None:
        return

    print(f"Detection finished, detected the following text:\n{output}")
    response = f"Speech-to-text detection:\n\n{output}"

    # Send speech-to-text message in the same chat for my own messages.
    # However, send speech-to-text message for other people to my own saved messages
    # folder. I don't want to scare them off.
    me = await bot.get_me()

    # Not sure why, but the `from_id` can sometimes be None.
    # Just send the message to me in that case.
    if message.from_id is None:
        await event.client.send_message("me", response)
        return

    peer_id, _ = get_peer_information(message.from_id)
    if peer_id == me.id or peer_id == "myself":
        await event.reply(response)
    else:
        await event.client.send_message("me", response)


async def detect_text(message) -> str | None:
    """Run speech-to-text detection.

    1. Download the audio from the message
    2. Send request to speech-to-text server
    """
    # Use a user-based temporary text-to-speech directory
    username = getpass.getuser()
    temp_dir = f"/tmp/telegram-text-to-speech-{username}"

    # Create the temp dir that's used for downloading and transcoding audio files.
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    print("Downloading media")
    # Download the message
    blob = await message.download_media(bytes)

    print("Running detection")
    url = "http://localhost:9000/asr"
    files = {"audio_file": blob}
    response = requests.post(url, files=files)

    return response.text


def is_audio_message(message) -> bool:
    """Make sure we got an audio message."""
    # Audio messages are documents
    if message.document is None:
        return False

    # Messages might have multiple document attributes.
    # Look for the audio one.
    if not any(
        type(attribute) is types.DocumentAttributeAudio
        for attribute in message.document.attributes
    ):
        return False

    return True
