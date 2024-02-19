import discord

from actions.message_actions import send_message
from clients import discord_client
from utils.custom_logger import DMLogger


@discord_client.event
async def on_message(message: discord.Message) -> None:
    """
    Message events handler
    Args:
        message (discord.Message): The message object
    Returns:
        None
    """
    if message.author == discord_client.user or message.author.bot:
        return
    if isinstance(message.channel, discord.DMChannel):
        await DMLogger(component="ON_MESSAGE").log_dm(message=message)
        await send_message(content="BeepBoop", channel=message.channel)
        return
    return
