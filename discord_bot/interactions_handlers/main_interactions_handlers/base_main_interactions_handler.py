import discord

from ..base_interactions_handler import BaseInteractionsHandler


class MainInteractionsHandler(BaseInteractionsHandler):

    def __init__(self, source_interaction: discord.Interaction):
        """
        Base class for user interactions handlers. Should be inherited by all user interactions handlers.
        Args:
            source_interaction (discord.Interaction): The interaction that triggered the handler
        """
        super().__init__(source_interaction=source_interaction)
        self.guild = source_interaction.guild or None
        self.user = source_interaction.user
        self.member = self.guild.get_member(self.source_interaction.user.id) if self.guild else None
        self.is_dm = not self.guild

    def __new__(cls, *args, **kwargs):
        if cls is MainInteractionsHandler:
            raise TypeError("MainInteractionsHandler class may not be instantiated.")
        return object.__new__(cls)

    async def on_timeout(self) -> None:
        """
        Called when the view times out to remove the view from the message.
         Should be overridden by subclasses if needed.
        Returns:
            None
        """
        try:
            await self.source_interaction.edit_original_response(view=None)
        except discord.NotFound:
            pass
