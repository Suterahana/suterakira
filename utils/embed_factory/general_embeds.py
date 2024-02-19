import discord

from clients import discord_client
from constants import LogType, Colour


def get_discord_log_embed(message: str, log_type: str, extras: dict) -> discord.Embed:
    """
    Get a discord embed for logging
    Args:
        message (str): The message to log
        log_type (str): The type of log
        extras (dict): Additional information to log
    Returns:
        discord.Embed: The embed
    """
    icon_url = discord_client.user.avatar.with_size(128).url if discord_client.user.avatar else None

    if log_type == LogType.ERROR:
        color = Colour.ERROR
    elif log_type in [LogType.WARNING, LogType.MINOR_WARNING]:
        color = Colour.WARNING
    elif log_type == LogType.DM_RECEIVED:
        color = Colour.GREEN
    else:
        color = Colour.PRIMACY_ACCENT

    embed = discord.Embed(description=message, color=color,
                          timestamp=discord.utils.utcnow())
    embed.set_author(name=f'{log_type} Log')
    embed.set_footer(text="", icon_url=icon_url)
    for key, value in extras.items():
        embed.add_field(name=f"{key}", value=f"{value}", inline=False)
    return embed


def get_quick_embed(text: str, color: int = Colour.PRIMACY_ACCENT) -> discord.Embed:
    """
    Get a quick embed
    Args:
        text (str): The text to put in the embed
        color (int): The color of the embed
    Returns:
        discord.Embed: The embed
    """
    return discord.Embed(description=text, color=color)
