import discord

import settings
from actions.message_actions import send_message
from clients import discord_client
from extensions.owner_code_executor import execute_owner_code_snippet
from extensions.owner_commands import OwnerCommandsHandler
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

    if message.author.id in settings.BOT_OWNER_IDS:
        if message.content.startswith(settings.OWNER_COMMAND_PREFIX):
            return await (OwnerCommandsHandler(message=message)).handle()
        elif message.content.startswith("execute"):
            return await execute_owner_code_snippet(message)

    if isinstance(message.channel, discord.DMChannel):
        await DMLogger(component="ON_MESSAGE").log_dm(message=message)
        await send_message(content="BeepBoop", channel=message.channel)
        return
    return
