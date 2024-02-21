from discord.ext import commands
import discord

import settings


class DiscordClient:
    """
    A simple class to manage the discord client.
    """
    client = None

    @staticmethod
    def get_client() -> commands.Bot:
        """
        Get the discord client if it exists, otherwise create it and return it.
        Returns:
            commands.Bot: the discord client
        """
        if not DiscordClient.client:
            intents = discord.Intents.default()
            intents.message_content = True
            DiscordClient.client = commands.Bot(intents=intents,
                                                command_prefix='/')
        return DiscordClient.client

    @staticmethod
    def run_client() -> None:
        """
        Run the discord client.
        Returns:
            None
        """
        DiscordClient.get_client().run(token=settings.DISCORD_BOT_TOKEN)
