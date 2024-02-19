from enum import Enum
from typing import List, Type, Any


class SuterakiraEnum:
    @classmethod
    def as_list(cls) -> List[Any]:
        """
        Returns:
             List[Any]: A list of all the values in the enum
        """
        return [value for key, value in cls.__dict__.items() if not key.startswith('_') and not key.endswith('__')]

    @classmethod
    def values_as_enum(cls) -> Type[Enum]:
        """
        Returns:
            Type[Enum]: an enum.Enum instance with the values of the current enum
        """
        return Enum(cls.__name__, {value: value for value in cls.as_list()})

    @classmethod
    def as_map(cls) -> dict[str, Any]:
        """
        Returns:
            dict: A dictionary of all the keys (names) mapped to their values in the enum
        """
        return {key: value for key, value in cls.__dict__.items() if not key.startswith('_') and not key.endswith('__')}


class Colour(SuterakiraEnum):
    PRIMACY_ACCENT = 0x402349

    RED = 0xB94D35
    GREEN = 0x8ADE87
    BLACK = 0x000000
    BROWN = 0xAC7731
    WARM_GOLD = 0xFFBF52
    HOT_ORANGE = 0xD6581A
    SILVER = 0xA8A8A8
    DEEP_BLUE = 0x364B92
    SKY_BLUE = 0x6AC8FD
    CLOUDY_PURPLE = 0x2B2D42
    BLURPLE = 0x5539CC
    WHITE = 0xFFFFFF

    # ALIASES
    ERROR = RED
    SUCCESS = GREEN
    SYSTEM = BLACK
    WARNING = BROWN
    UNFORTUNATE = HOT_ORANGE


class LogType(SuterakiraEnum):
    GENERAL = "General"
    INFO = "Info"
    ERROR = "Error"
    WARNING = "Warning"
    MINOR_WARNING = "Minor Warning"

    MESSAGE_SENT = "Message Sent"
    DM_RECEIVED = "DM Received"
    MESSAGE_DELETED = "Message Deleted"
    MESSAGE_EDITED = "Message Edited"
    REPLY_SENT = "Reply Sent"

    SLASH_COMMAND_RECEIVED = "Slash Command Received"
    INTERACTION_CALLBACK_RECEIVED = "Interaction Callback Received"


class BackgroundWorker(SuterakiraEnum):
    # PERIODIC WORKERS (run every specified interval)
    pass

    # SELF-SCHEDULING WORKERS (worker decides when to run again)
    pass


PERIODIC_WORKER_FREQUENCY = {  # mapping BackgroundWorker periodic members to frequency in seconds
}

WORKER_RETRY_ON_ERROR_DELAY = 60


class HelpMenuType(SuterakiraEnum):
    MAIN = "Main"
