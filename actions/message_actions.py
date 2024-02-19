from typing import List, Sequence, Union

import discord

from constants import Colour, LogType
from utils.custom_logger import InfoLogger
from utils.exceptions import MessageSendingException
from utils.helpers.typehinting_helpers import MESSAGEABLE_DISCORD_OBJECT


async def send_message(channel: MESSAGEABLE_DISCORD_OBJECT,
                       content: str = None,
                       embed: discord.Embed = None,
                       embeds: Sequence[discord.Embed] = None,
                       view: discord.ui.View = None,
                       file: discord.File = None,
                       files: Sequence[discord.File] = None,
                       reply_to: discord.Message = None,
                       delete_after: int = None,
                       log_action: bool = False) -> discord.Message:
    """
    Send a message to a messageable channel
    Args:
        channel (discord.abc.Messageable): The channel to send the message to
        content (str): The content of the message
        embed (discord.Embed): The embed to send with the message
        embeds (List[discord.Embed]): The embeds to send with the message (if embed is provided then this is ignored)
        view (discord.ui.View): The view to send with the message
        file (discord.File): The file to send with the message
        files (List): The files to send with the message (if file is provided then this is ignored)
        reply_to (discord.Message): The message to reply to
        delete_after (int): The time to wait in seconds before deleting the message
        log_action (bool): Whether to log the message being sent and its destination
    Returns:
        discord.Message: The message that was sent
    Raises:
        MessageSendingException: If the message could not be sent for any reason
    """
    if embed:
        embeds = [embed]
    elif not embeds:
        embeds = []
    if file:
        files = [file]
    elif not files:
        files = []
    if reply_to:
        reference = reply_to.to_reference(fail_if_not_exists=False)
    else:
        reference = None

    try:
        if isinstance(channel, discord.User) or isinstance(channel, discord.Member):
            channel = channel.dm_channel or await channel.create_dm()

        message = await channel.send(content=content, embeds=embeds, view=view, files=files, reference=reference,
                                     delete_after=delete_after)
    except Exception as e:
        raise MessageSendingException(message=f"Could not send message: {e}",
                                      original_exception=e,
                                      target_channel=channel)
    else:
        if log_action:
            InfoLogger(component="SEND_MESSAGE").log(
                message=(f"Sent message to {channel} ({channel.id}) "
                         f"{f'in guild {channel.guild} ({channel.guild.id}) ' if getattr(channel, 'guild') else ''} "
                         f"with content: '{content}' "
                         f"and embeds: {len(embeds)} "
                         f"and files: {len(files)}."),
                log_type=LogType.MESSAGE_SENT,
                extras={"guild_id": channel.guild.id if getattr(channel, 'guild') else None,
                        "channel_id": channel.id,
                        "user_id": channel.id if isinstance(channel, discord.DMChannel) else None}
            )

    return message


async def send_quick_embed_message(channel: MESSAGEABLE_DISCORD_OBJECT,
                                   message_content: str = None,
                                   title: str = None,
                                   description: str = None,
                                   color: Union[discord.Color, int] = Colour.WHITE,
                                   field_value_pairs: Sequence[dict] = None,
                                   thumbnail: str = None,
                                   image: str = None,
                                   footer: str = None,
                                   footer_icon: str = None,
                                   delete_after: int = None,
                                   log_action: bool = False) -> discord.Message:
    """
    Send a quick embed message to a messageable channel
    Args:
        channel (discord.abc.Messageable): The channel to send the message to
        message_content (str): The content of the message
        title (str): The title of the embed
        description (str): The description of the embed
        color (Union[discord.Color, int]): The color of the embed
        field_value_pairs (List[dict]): A list of dictionaries containing the field name and value
        thumbnail (str): The URL of the thumbnail
        image (str): The URL of the image
        footer (str): The footer text
        footer_icon (str): The URL of the footer icon
        delete_after (int): The time to wait in seconds before deleting the message
        log_action (bool): Whether to log the message being sent and its destination
    Returns:
        discord.Message: The message that was sent
    Raises:
        MessageSendingException: If the message could not be sent for any reason
    """
    embed = discord.Embed(title=title, description=description, color=color)
    if field_value_pairs:
        for field_value_pair in field_value_pairs:
            embed.add_field(name=field_value_pair.get('name'), value=field_value_pair.get('value'), inline=False)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)
    if footer:
        embed.set_footer(text=footer, icon_url=footer_icon)

    return await send_message(channel=channel, content=message_content, embed=embed, delete_after=delete_after,
                              log_action=log_action)
