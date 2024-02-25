from clients import discord_client
from .general_main_blueprints import GeneralMainBlueprints


class MainSlashesCog(GeneralMainBlueprints):
    pass


cog = MainSlashesCog()


async def add_cogs():
    await discord_client.add_cog(cog)
