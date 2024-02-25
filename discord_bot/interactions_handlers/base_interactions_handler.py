import discord

from utils.custom_logger import InfoLogger, ErrorLogger
from constants import LogType


class BaseInteractionsHandler:

    def __init__(self, source_interaction: discord.Interaction):
        """
        Base class for interaction handlers. All interaction handlers should inherit from this class.
        Args:
            source_interaction (discord.Interaction): The interaction that triggered the handler
        """
        self.source_interaction: discord.Interaction = source_interaction
        self.guild = getattr(source_interaction, "guild", None)
        self.channel = source_interaction.channel
        self.source_interaction_user = source_interaction.user
        self.source_interaction_member = self.guild.get_member(self.source_interaction_user.id) \
            if self.guild else None
        self.info_logger = InfoLogger(component=self.__class__.__name__)
        self.error_logger = ErrorLogger(component=self.__class__.__name__)

    def __new__(cls, *args, **kwargs):
        if cls is BaseInteractionsHandler:
            raise TypeError("BaseInteractionsHandler class may not be instantiated.")
        return object.__new__(cls)

    async def on_timeout(self) -> None:
        """
        Base view timeout handler.
        Returns:
            None
        """
        self.info_logger.log(f"View timeout not handled. Handler class: {self.__class__.__name__}",
                             log_type=LogType.MINOR_WARNING, log_to_discord=True)


class NumberedListInteractions:
    """
    Interaction handlers that handle numbered lists should inherit from this class.
    """

    async def handle_selection(self, interaction: discord.Interaction):
        """
        Handler for number list interactions. This method should be overridden by the inheriting class.
        Args:
            interaction (discord.Interaction): The interaction that triggered the handler
        """
        raise NotImplemented

    async def handle_cancel(self, interaction: discord.Interaction):
        """
        Handler for number list interactions. This method should be overridden by the inheriting class if used.
        Args:
            interaction (discord.Interaction): The interaction that triggered the handler
        """
        raise NotImplemented


class PagedNavigationInteractions:
    """
    Interaction handlers that handle paged navigation should inherit from this class.
    """

    async def handle_next(self, interaction: discord.Interaction) -> None:
        """
        Handler for moving to the next page. This method should be overridden by the inheriting class.
        Args:
            interaction (discord.Interaction): The interaction that triggered the handler
        Returns:
            None
        """
        raise NotImplemented

    async def handle_previous(self, interaction: discord.Interaction):
        """
        Handler for moving to the previous page. This method should be overridden by the inheriting class.
        Args:
            interaction (discord.Interaction): The interaction that triggered the handler
        Returns:
            None
        """
        raise NotImplemented

    async def handle_cancel(self, interaction: discord.Interaction):
        """
        Handler for cancelling the view. This method should be overridden by the inheriting class if needed.
        Args:
            interaction (discord.Interaction): The interaction that triggered the handler
        Returns:
            None
        """
        raise NotImplemented

    async def handle_go_back(self, interaction: discord.Interaction):
        """
        Handler for moving back to the previous view if applicable. This method should be overridden by the inheriting
        class if needed.
        Args:
            interaction (discord.Interaction): The interaction that triggered the handler
        Returns:
            None
        """
        raise NotImplemented
