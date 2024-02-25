import discord

from clients import discord_client


@discord_client.event
async def on_interaction(interaction: discord.Interaction) -> None:
    """
    Interaction events handler
    Args:
        interaction (discord.Interaction): The interaction object
    Returns:
        None
    """
    if not interaction.message or interaction.message.author.id != discord_client.user.id:
        return
