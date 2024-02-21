from clients.discord_service import DiscordClient
from discord_bot.events import *

print(f"## RUNNING IN {settings.ENV_NAME.upper()} ENVIRONMENT ##")

DiscordClient.run_client()
