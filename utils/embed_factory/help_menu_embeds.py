import discord

from clients import discord_client
from constants import Colour, HelpMenuType
from settings import SUPPORT_SERVER_INVITE


def get_general_help_embed() -> discord.Embed:
    """
    Get the general help embed (AKA main help menu)
    Returns:
        discord.Embed: The embed
    """
    embed = discord.Embed(colour=Colour.PRIMARY_ACCENT,
                          description="I have listed my most popular commands below. "
                                      "Click on each section to see the full commands list.\n‎")
    embed.set_thumbnail(url=discord_client.user.avatar.with_size(128).url if discord_client.user.avatar else None)
    embed.set_author(name=discord_client.user.name)

    embed.add_field(name="Main commands", value=f"• **/help** • **/support** • **/example command**\n‎",
                    inline=False)

    embed.add_field(name="Join our support server", value=f"{SUPPORT_SERVER_INVITE}\n", inline=False)
    # embed.add_field(name="Support the project", value=f"{SUPPORT_ME_LINK}\n", inline=False)

    embed.set_footer(text="General Help Menu",
                     icon_url=discord_client.user.avatar.with_size(128).url if discord_client.user.avatar else None)

    return embed


def get_help_embed_for_menu(menu_type: str) -> discord.Embed:
    """
    Get the help embed for a specific menu type (command category)
    Args:
        menu_type (str): The menu type
    Returns:
        discord.Embed: The embed
    """
    if menu_type == HelpMenuType.MAIN:
        from discord_bot.slashes.blueprint.main_blueprints import cog
    else:
        raise Exception(f"Invalid menu type: {menu_type}")

    embed = discord.Embed(colour=Colour.PRIMARY_ACCENT,
                          description=f"Full list of {menu_type} commands.\n‎")
    embed.set_thumbnail(url=discord_client.user.avatar.with_size(128).url if discord_client.user.avatar else None)
    embed.set_author(name=f"{menu_type} Commands")

    for command in list(cog.walk_app_commands()):
        if isinstance(cog, discord.app_commands.Group):
            continue
        if not command.extras.get('unlisted') and not command.extras.get('is_alias'):
            embed.add_field(name=f"{command.qualified_name}", value=f"{command.description}", inline=True)
        if len(embed.fields) == 25:
            break

    embed.set_footer(text="Commands List",
                     icon_url=discord_client.user.avatar.with_size(128).url if discord_client.user.avatar else None)

    return embed
