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
