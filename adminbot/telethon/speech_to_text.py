"""Simple helper functions."""
import os
import sys
import subprocess
import uuid

from telethon import events, types

from adminbot.config import config
from adminbot.sentry import handle_exceptions
from adminbot.telethon import bot

temp_dir = "/tmp/telegram-text-to-speech"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@bot.on(events.NewMessage())
@handle_exceptions
async def speech_to_text(event):
    """Print the current chat id and type for debugging."""
    message = event.message

    # Don't read messages in non private chats
    if not message.is_private:
        return

    # We're only interested in audio messages
    if message.document is None:
        return

    # Check if there an audio document in here.
    if not any(
        type(attribute) is types.DocumentAttributeAudio
        for attribute in message.document.attributes
    ):
        return

    print(f"Got audio message from chat {message.from_id}")

    # Create the temp dir that's used for downloading and transcoding audio files.
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    filename = str(uuid.uuid4())
    ogg_path = f"{temp_dir}/{filename}.ogg"
    wav_path = f"{temp_dir}/{filename}.wav"

    # Download the message
    await message.download_media(file=ogg_path)

    # Transcode the telegram ogg file to a 16khz wav file for network consumption.
    print("Transcoding")
    transcode_output = subprocess.run(
        ["ffmpeg", "-i", ogg_path, "-ar", "16000", wav_path], capture_output=True
    )
    if transcode_output.returncode != 0:
        eprint("Detection failed!")
        eprint("Stdout: {}".format(transcode_output.stdout.decode("utf-8")))
        eprint("Stderr: {}".format(transcode_output.stderr.decode("utf-8")))
        return

    # Transcoding is done, we can clean up the ogg file.
    os.remove(ogg_path)

    # Run speech to text detection on wav file.
    print("Running detection")
    detection_output = subprocess.run(
        [
            config["speech_to_text"]["path_to_binary"],
            "--no-timestamps",
            "--language",
            "auto",
            "--model",
            config["speech_to_text"]["path_to_model"],
            "--file",
            wav_path,
        ],
        capture_output=True,
    )
    if detection_output.returncode != 0:
        eprint("Detection failed!")
        eprint("Stdout: {}".format(detection_output.stdout.decode("utf-8")))
        eprint("Stderr: {}".format(detection_output.stderr.decode("utf-8")))
        return
    # Detection is done, we can clean up the wav file.
    os.remove(wav_path)

    # Parse output and build response
    output = detection_output.stdout.decode("utf-8").strip()
    print(f"Detection is finished, detected the following text:\n{output}")
    response = f"Sprach zu Text detection:\n\n{output}"

    await event.reply(response)
