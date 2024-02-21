import os
from datetime import datetime

import psutil

from actions.message_actions import send_quick_embed_message
from clients import discord_client
from constants import SuterakiraEnum, Colour
from utils.helpers.string_helpers import get_id_from_text


class OwnerCommandsHandler:
    class OwnerCommand(SuterakiraEnum):
        HELP = "help"
        USAGE = 'usage'
        GUILD_LEAVE = 'guild leave'
        GUILD_INFO = 'guild info'
        STATS = 'stats'

        # MIGRATIONS
        SYNC_SLASHES = 'sync slashes'

    def __init__(self, message):
        """
        Wrapper for handling owner commands triggered via messages
        Args:
            message (discord.Message): The message that triggered the command
        """
        self.message = message
        self.message_content_lowered = message.content.lower()[2:]
        self.channel = message.channel
        self.client = discord_client

    async def handle(self) -> None:
        """
        Handles the owner command
        Returns:
            None
        """
        if self.message_content_lowered == self.OwnerCommand.HELP:
            return await self.handle_command_help()
        elif self.message_content_lowered == self.OwnerCommand.USAGE:
            return await self.handle_command_usage()
        elif self.message_content_lowered.startswith(self.OwnerCommand.GUILD_LEAVE):
            return await self.handle_command_guild_leave()
        elif self.message_content_lowered.startswith(self.OwnerCommand.GUILD_INFO):
            return await self.handle_command_guild_info()
        elif self.message_content_lowered == self.OwnerCommand.STATS:
            return await self.handle_command_stats()
        elif self.message_content_lowered == self.OwnerCommand.SYNC_SLASHES:
            return await self.handle_command_sync_slashes()

    async def handle_command_help(self) -> None:
        """
        Returns the list of owner commands
        Returns:
            None
        """
        commands_list = '**' + '**\n**'.join(self.OwnerCommand.as_list()) + '**'
        await send_quick_embed_message(channel=self.channel,
                                       description=f"Owner commands:\n{commands_list}")

    async def handle_command_usage(self) -> None:
        """
        Returns a summary of resource usage
        Returns:
            None
        """
        memory_amount_usage = round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2, 2)
        memory_percent_usage = round(psutil.virtual_memory().percent, 2)
        memory_usage = f"Memory usage = {memory_amount_usage} MB ({memory_percent_usage}%)"

        disk_amount_usage = round(psutil.disk_usage(os.sep).used / 1024 ** 2, 2)
        disk_percent_usage = round(psutil.disk_usage(os.sep).percent, 2)
        disk_usage = f"Disk usage = {disk_amount_usage} MB ({disk_percent_usage}%)"

        cpu_usage = f"CPU usage = {round(psutil.cpu_percent(), 2)}%"

        await send_quick_embed_message(channel=self.channel,
                                       title="🚀 Usage",
                                       description=f"{memory_usage}\n{disk_usage}\n{cpu_usage}",
                                       color=Colour.SYSTEM)

    async def handle_command_guild_leave(self) -> None:
        """
        Leaves a guild
        Returns:
            None
        """
        guild_id = get_id_from_text(self.message.content)
        if not guild_id or not (guild := discord_client.get_guild(guild_id)):
            await send_quick_embed_message(channel=self.channel, description="Invalid ID or guild not found.")
            return
        guild_name = guild.name
        await guild.leave()
        await send_quick_embed_message(channel=self.channel, description=f"Left guild `{guild_name}` ({guild_id}).")

    async def handle_command_guild_info(self) -> None:
        """
        Returns detailed information about a guild
        Returns:
            None
        """
        guild_id = get_id_from_text(self.message.content)
        if not guild_id or not (guild := discord_client.get_guild(guild_id)):
            await send_quick_embed_message(channel=self.channel, description="Invalid ID or guild not found.")
            return
        member_count = guild.member_count
        bot_count = len([member for member in guild.members if member.bot])
        owner_other_guild_count = len([guild_ for guild_ in self.client.guilds
                                       if guild_.owner.id == guild.owner.id and guild_.id != guild.id])
        await send_quick_embed_message(
            channel=self.channel,
            description=f"**{guild}** ({guild.id})\n\n"
            f"**Member count**: {guild.member_count}.\n"
            f"**Owned by** {guild.owner} ({guild.owner.id}).\n" +
            (f"**Bot is in** {owner_other_guild_count} other guilds they own.\n" if owner_other_guild_count else "") +
            f"**Created at** <t:{int(datetime.timestamp(guild.created_at))}:f>.\n"
            f"**Joined at** <t:{int(datetime.timestamp(guild.me.joined_at))}:f>.\n"
            f"**Human count** = {len([member for member in guild.members if not member.bot])}.\n"
            f"**Bot count** = {bot_count}.\n"
            f"**Bot Percentage** = {round(bot_count * 100 / member_count, 2)}%\n"
            f"**Admin status**: {guild.me.guild_permissions.administrator}.\n")

    async def handle_command_stats(self):
        member_ids = []
        bot_ids = []
        channel_count = 0
        for guild in self.client.guilds:
            for user in guild.members:
                member_ids.append(user.id)
                if user.bot:
                    bot_ids.append(user.id)
            channel_count += len(guild.channels)
        total_member_count = len(member_ids)
        total_bot_count = len(bot_ids)
        unique_user_count = len(set(member_ids))
        unique_bot_count = len(set(bot_ids))
        total_human_percentage = round((total_member_count - total_bot_count) * 100 / total_member_count, 2)
        total_bot_percentage = round(100 - total_human_percentage, 2)
        unique_human_percentage = round((unique_user_count - unique_bot_count) * 100 / unique_user_count, 2)
        unique_bot_percentage = round(100 - unique_human_percentage, 2)
        await send_quick_embed_message(
            channel=self.channel,
            description=f"**Bot Stats**\n"
                        f"**Guild count** = {len(self.client.guilds)}\n"
                        f"**Total channel count** = {channel_count}\n"
                        f"**Total member count** = {total_member_count}\n"
                        f"  **-of which are bots** = {total_bot_count}\n"
                        f"**Unique user count** = {unique_user_count}\n"
                        f"  **-of which are bots** = {unique_bot_count}\n"
                        f"**Total human/bot ratio** = {total_human_percentage}% humans,"
                        f" {total_bot_percentage}% bots\n"
                        f"**Unique user/bot ratio** = {unique_human_percentage}% humans,"
                        f" {unique_bot_percentage}% bots"
        )

    async def handle_command_sync_slashes(self) -> None:
        """
        Syncs the slash commands
        Returns:
            None
        """
        if 'guild' in self.message_content_lowered:
            await discord_client.tree.sync(guild=self.channel.guild)
        else:
            await discord_client.tree.sync()
        await send_quick_embed_message(channel=self.channel, description="Slashes sync requested")

    @staticmethod
    def _get_option_value_pairs(message_content: str, options_keep_digit_values_as_str: list = None) -> dict:
        """
        Parses the message content for option-value pairs from owner commands
        Args:
            message_content (str): The message content of the command
            options_keep_digit_values_as_str (list): A list of option names to keep their values
             as strings if they are digits
        Returns:
            dict: The option-value pairs
        """
        if options_keep_digit_values_as_str is None:
            options_keep_digit_values_as_str = []
        pairs = {}
        idx = 0
        while idx < len(message_content):
            if message_content[idx] != '-':
                idx += 1
                continue
            elif (idx + 1) < len(message_content) and message_content[idx + 1] != ' ':
                idx += 1
                option_name = ''
                while idx < len(message_content) and message_content[idx] != ' ':
                    option_name += message_content[idx]
                    idx += 1
                while message_content[idx] == ' ' and idx < len(message_content):
                    idx += 1
                option_value = ''
                while idx < len(message_content) and message_content[idx] not in ['-', ' ']:
                    option_value += message_content[idx]
                    idx += 1
                if option_value.isdigit() and option_name not in options_keep_digit_values_as_str:
                    option_value = int(option_value)
                if option_value == '':
                    option_value = True
                pairs[option_name] = option_value

        return pairs
