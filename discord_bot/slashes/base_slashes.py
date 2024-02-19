import traceback
from typing import Union, Any

import discord

import cached_items
from constants import LogType
from utils.custom_logger import InfoLogger, ErrorLogger


class BaseSlashes:

    def __new__(cls, *args, **kwargs):
        if cls is BaseSlashes:
            raise TypeError("BaseSlashes class may not be instantiated.")
        return object.__new__(cls)

    def __init__(self, interaction: discord.Interaction) -> None:
        """
        Base class for slash command handlers.
        Args:
            interaction (discord.Interaction): The interaction object
        """
        self.interaction: discord.Interaction = interaction
        self.guild: discord.Guild = interaction.guild
        self.channel: Union[discord.TextChannel, discord.DMChannel] = interaction.channel
        self.user: discord.User = interaction.user
        self.is_dm = not interaction.guild
        self.member: discord.Member = interaction.guild.get_member(self.user.id) if not self.is_dm else None
        self.interaction_data: dict = interaction.data

        self.command_name: str = interaction.command.qualified_name
        from .main_slashes.base_main_slashes import MainSlashes
        if isinstance(self, MainSlashes):
            self.command_name = self.command_name.split(" ", 1)[1]
            command_type_permissions = cached_items.main_commands_permissions
        else:
            raise NotImplementedError("Command type not handled while determining permissions.")
        self.command_user_permissions: list = command_type_permissions.get(self.command_name, {}).get("member", [])
        self.command_bot_permissions: list = command_type_permissions.get(self.command_name, {}).get("bot", [])

        self.info_logger = InfoLogger(component=self.__class__.__name__)
        self.error_logger = ErrorLogger(component=self.__class__.__name__)

    async def log_command(self) -> None:
        """
        Log the command handler call.
        Returns:
            None
        """
        try:
            from .main_slashes.base_main_slashes import MainSlashes
            handler_name = self.interaction.command.qualified_name
            self.info_logger.log(f"Slash handler for `{handler_name}` called by user: {self.user} ({self.user.id})."
                                 + f" Channel: {self.channel} ({self.channel.id})." if self.channel else ""
                                 + f" Guild: {self.guild} ({self.guild.id})." if self.guild else "",
                                 log_to_discord=False,
                                 log_type=LogType.SLASH_COMMAND_RECEIVED,
                                 extras={"interaction_data": self.interaction_data,
                                         "command_name": handler_name,
                                         "guild_id": self.guild.id if self.guild else None,
                                         "user_id": self.user.id})
        except Exception as e:
            print(f"Error while logging slash command handler: {e}\n{traceback.format_exc()}")

    async def check_permissions(self) -> tuple[list[str], list[str]]:
        """
        Check if the user and bot have the required permissions to fully execute the command.
        Returns:
            tuple[list[str], list[str]]: Missing user permissions and missing bot permissions
        """
        missing_user_perms = []
        missing_bot_perms = []
        if self.is_dm:
            return missing_user_perms, missing_bot_perms
        if self.command_user_permissions:
            if not self.member:
                return missing_user_perms, missing_bot_perms
            for perm in self.command_user_permissions:
                if not getattr(self.member.guild_permissions, perm):
                    missing_user_perms.append(perm)
        if self.command_bot_permissions:
            for perm in self.command_bot_permissions:
                if not getattr(self.guild.me.guild_permissions, perm):
                    missing_bot_perms.append(perm)
        return missing_user_perms, missing_bot_perms

    async def preprocess_and_validate(self, guild_only: bool = False, **kwargs) -> bool:
        """
        Preprocess and validate the command.
        Args:
            guild_only (bool): Whether the command can only be used in a server
            **kwargs: Additional arguments
        Returns:
            bool: Whether the command call is valid
        """
        if guild_only and not self.guild:
            await self.return_error_message(message="This command can only be used in a server.")
            return False

        missing_user_perms, missing_bot_perms = await self.check_permissions()
        if missing_user_perms or missing_bot_perms:
            error_message = "Please ensure that:"
            if missing_user_perms:
                user_perms = ', '.join(["**" + missing_user_perm.replace('_', ' ').title() + "**"
                                        for missing_user_perm in missing_user_perms])
                error_message += f"\n• You have the following permissions:" \
                                 f" {user_perms}"
            if missing_bot_perms:
                bot_perms = ', '.join(["**" + missing_bot_perm.replace('_', ' ').title() + "**"
                                       for missing_bot_perm in missing_bot_perms])
                error_message += f"\n• I have the following permissions:" \
                                 f" {bot_perms}"
            await self.return_error_message(message=error_message)
            return False

        await self.log_command()

        return True

    async def return_error_message(self, message: str = None) -> Any:
        """
        Return an error message to the user.
        Args:
            message (str): The error message
        Returns:
            Any
        """
        if not message:
            message = "An error occurred while processing your command. " \
                      "We've been informed of the issue and we'll get to fixing it ASAP."
        try:
            if not self.interaction.response.is_done():  # noqa
                return await self.interaction.response.send_message(message, ephemeral=True,  # noqa
                                                                    delete_after=10)
            else:
                return await self.interaction.followup.send(message, ephemral=True, delete_after=10)
        except:
            return await self.channel.send(message, delete_after=5)

    def send_as_ephemeral(self, make_visible: bool = True) -> bool:
        """
        Check if the response should be sent as ephemeral.
        Args:
            make_visible (bool): Method caller preference to make the response visible or not
             if no overriding conditions are met
        Returns:
            bool: Whether the response should be sent as ephemeral
        """
        if self.is_dm:
            return False
        if not self.channel.permissions_for(self.guild.me).embed_links:
            return True
        return not make_visible
