import re
from typing import Union

import discord


def get_current_time_string(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get the current time as a string with a given format
    Args:
        format_str (str): The format string
    Returns:
        str: The current time as a string
    """
    return discord.utils.utcnow().strftime(format_str)


def get_id_from_text(text: str) -> Union[int, None]:
    """
    Get a discord id from a string
    Args:
        text (str): The text
    Returns:
        Union[int, None]: The id or None
    """
    for numeric_string in re.findall('[0-9]+', re.sub(" +", " ", text).strip()):
        if len(numeric_string) > 15:
            return int(numeric_string)
    return None
