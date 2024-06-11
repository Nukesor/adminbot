"""Helper functions for handling telethon stuff."""

from telethon import types


def get_peer_information(peer):
    """Get the id depending on the chat type."""
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
        raise Exception(f"Unknown chat type: {peer} (Type: {type(peer)})")
