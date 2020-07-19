"""Helper functions for handling telethon stuff."""
from telethon import types

from adminbot.config import config
from adminbot.telethon import bot


def log(message):
    """Log message if logging is enabled."""
    if config["logging"]["debug"]:
        print(message)


def get_peer_information(peer):
    """Get the id depending on the chat type."""
    print(peer)
    if isinstance(peer, types.PeerUser) or isinstance(peer, types.InputPeerUser):
        return peer.user_id, "user"
    elif isinstance(peer, types.PeerChat) or isinstance(peer, types.InputPeerChat):
        return peer.chat_id, "peer"
    elif isinstance(peer, types.PeerChannel) or isinstance(
        peer, types.InputPeerChannel
    ):
        return peer.channel_id, "channel"
    elif isinstance(peer, types.InputPeerSelf):
        return "myself", "user"
    else:
        raise Exception("Unknown chat type")
