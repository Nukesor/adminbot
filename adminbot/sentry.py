"""Simple wrapper around sentry that allows for lazy initilization."""

import traceback

import sentry_sdk
from sentry_sdk import configure_scope

from adminbot.config import config


class Sentry:
    """Sentry wrapper class that allows this app to work without a sentry token.

    If no token is specified in the config, the messages used for logging
    are simply not called.
    """

    initialized = False

    def __init__(self):
        """Construct new sentry wrapper."""
        if config["logging"]["sentry_enabled"]:
            self.initialized = True
            sentry_sdk.init(config["logging"]["sentry_token"])

    def captureMessage(self, *args, **kwargs):
        """Capture message with sentry."""
        if not self.initialized:
            return

        with configure_scope() as scope:
            scope.set_tag("bot", "adminbot")
            sentry_sdk.captureMessage(*args, **kwargs)

    def captureException(self, *args, **kwargs):
        """Capture exception with sentry."""
        if not self.initialized:
            return

        with configure_scope() as scope:
            scope.set_tag("bot", "adminbot")
            sentry_sdk.captureException(*args, **kwargs)


sentry = Sentry()


def handle_exceptions(func):
    """Generic sentry exception handler."""

    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except Exception as e:
            if config["logging"]["debug"]:
                traceback.print_exc()

            sentry.captureException(e)

    return wrapper
