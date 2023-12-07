"""Simple helper functions."""
import os
import sys
import subprocess
import uuid

from telethon import events, types, Message

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

    # Ignore non-private and non-audio messages.
    if not message.is_private or not is_audio_message(message):
        return

    print(f"Got audio message from private chat")

    # Try to detect text
    # Return early if something went wrong.
    output = detect_text(message)
    if output is None:
        return

    print(f"Detection finished, detected the following text:\n{output}")
    response = f"Speech-to-text detection:\n\n{output}"

    await event.reply(response)


async def detect_text(message: Message) -> str | None:
    """Run speech-to-text detection.

    1. Download the audio from the message
    2. Transfrom to 16khz WAV
    3. Feed file into speech detector
    """
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

    # Return output
    return detection_output.stdout.decode("utf-8").strip()


def is_audio_message(message: Message) -> bool:
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
