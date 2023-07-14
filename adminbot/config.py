"""Config values for pollbot."""
import os
import sys

import toml

default_config = {
    "telegram": {
        "phone_number": "your_phone_number",
        "app_api_id": 0,
        "app_api_hash": "apihash",
    },
    "bot": {
        "admin": "27755184",
    },
    "database": {
        "pollbot_sql_uri": "",
        "pollbot_connection_count": 5,
        "pollbot_overflow_count": 5,
    },
    "logging": {
        "sentry_enabled": False,
        "sentry_token": "",
        "debug": False,
    },
}

config_path = os.path.expanduser("~/.config/adminbot.toml")


def save_config(config):
    """Save the config to disk."""
    with open(config_path, "w") as file_descriptor:
        toml.dump(config, file_descriptor)


if not os.path.exists(config_path):
    save_config(default_config)
    print("Please adjust the configuration file at '~/.config/adminbot.toml'")
    sys.exit(1)
else:
    config = toml.load(config_path)

__all__ = ["config"]
