"""Simple wrapper around sentry that allows for lazy initilization."""
import traceback

from raven import Client

from adminbot.config import config


class Sentry(object):
    """Sentry wrapper class that allows this app to work without a sentry token.

    If no token is specified in the config, the messages used for logging are simply not called.
    """

    initialized = False

    def __init__(self):
        """Construct new sentry wrapper."""
        if config["logging"]["sentry_enabled"]:
            self.initialized = True
            self.sentry = Client(config["logging"]["sentry_token"])

    def captureMessage(self, *args, **kwargs):
        """Capture message with sentry."""
        if self.initialized:
            if "tags" not in kwargs:
                kwargs["tags"] = {}

            # Tag it as pollbot
            kwargs["tags"]["bot"] = "pollbot"
            self.sentry.captureMessage(*args, **kwargs)

    def captureException(self, *args, **kwargs):
        """Capture exception with sentry."""
        if self.initialized:
            if "tags" not in kwargs:
                kwargs["tags"] = {}

            # Tag it as pollbot
            kwargs["tags"]["bot"] = "pollbot"
            self.sentry.captureException(*args, **kwargs)


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
