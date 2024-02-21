import asyncio

import discord

from clients import discord_client, worker_manager_service
from components.command_permissions_component import CommandPermissionsComponent
from constants import LogType
from utils.custom_logger import InfoLogger


@discord_client.event
async def on_ready() -> None:
    """
    Called when the bot is online and ready - initial setup and data loading
    Returns:
        None
    """

    if getattr(on_ready, '_was_run', False):
        return

    on_ready._was_run = True

    info_logger = InfoLogger(component="ON_READY_EVENT")
    info_logger.log("Bot is up. Setting up...", log_to_discord=True,
                    log_type=LogType.INFO)

    # load data
    CommandPermissionsComponent.load_permissions()

    # load cogs
    from discord_bot.slashes import blueprint
    await blueprint.add_cogs()

    # set bot status
    await discord_client.change_presence(activity=discord.Game(f'Singularity | /help'))

    # add & start workers
    await worker_manager_service.register_workers()
    asyncio.get_event_loop().create_task(worker_manager_service.run())

    info_logger.log("Bot is ready.", log_to_discord=True, log_type=LogType.INFO)
