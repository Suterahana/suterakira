from typing import Union

import discord

MESSAGEABLE_DISCORD_OBJECT = Union[discord.TextChannel, discord.DMChannel, discord.User, discord.Member,
                                   discord.GroupChannel, discord.Thread, discord.ThreadMember, discord.VoiceChannel,
                                   discord.StageChannel]
