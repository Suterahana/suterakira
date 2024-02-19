from discord.ext import commands
import discord

import settings


class DiscordClient:
    client = None

    @staticmethod
    def get_client() -> commands.Bot:
        if not DiscordClient.client:
            DiscordClient.client = commands.Bot(intents=discord.Intents.all(),
                                                command_prefix='/')
        return DiscordClient.client

    @staticmethod
    def run_client():
        DiscordClient.get_client().run(token=settings.DISCORD_BOT_TOKEN)
