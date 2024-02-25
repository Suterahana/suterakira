from utils.helpers.typehinting_helpers import MESSAGEABLE_DISCORD_OBJECT


class SuterakiraException(Exception):
    """
    Base exception class for all exceptions raised by the bot.
    """
    def __init__(self, message: str, original_exception: Exception = None, **kwargs):
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception

    def __str__(self) -> str:
        return self.message


class MessageSendingException(SuterakiraException):
    """
    Exception raised when the bot fails to send a message to a channel.
    """
    def __init__(self, target_channel: MESSAGEABLE_DISCORD_OBJECT = None, **kwargs):
        super().__init__(**kwargs)
        self.target_channel = target_channel

    def __str__(self) -> str:
        return f"Could not send message to {self.target_channel} ({self.target_channel.id}). Error: {self.message}"
