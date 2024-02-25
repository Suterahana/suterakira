import traceback
import discord
from constants import LogType
from ..base_interactions_handler import BaseInteractionsHandler
from utils.custom_logger import ErrorLogger
from utils.decorators import interaction_handler


class BaseModal(discord.ui.Modal, title="Form"):

    def __init__(self, interactions_handler: BaseInteractionsHandler, **kwargs):
        """
        Base class for modals. All modals should inherit from this class.
        Args:
            interactions_handler (BaseInteractionsHandler): The interaction handler that triggered the modal
            kwargs: Additional keyword arguments
        """
        super().__init__(**kwargs)
        self.interactions_handler = interactions_handler
        self.modal_name = self.__class__.__name__
        self.error_logger = ErrorLogger(component=self.modal_name)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Check if the interaction is from the same user that triggered the modal as a default behavior.
        Args:
            interaction (discord.Interaction): The interaction to check
        Returns:
            bool: Whether the check passed
        """
        return self.interactions_handler.source_interaction.user.id == interaction.user.id

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        """
        Default error handler for modals.
        Args:
            interaction (discord.Interaction): The interaction that triggered the modal
            error (Exception): The error that occurred
        """
        await interaction.response.send_message("An error occurred while processing your input."  # noqa
                                                " We're working on fixing it.", ephemeral=True)
        self.error_logger.log(message=f"An error occurred while processing {self.modal_name} modal input: "
                                      f"{error}\n{traceback.format_exc()}",
                              log_type=LogType.ERROR,
                              extras={"guild_id": self.interactions_handler.source_interaction.guild.id
                                      if self.interactions_handler.source_interaction.guild else None,
                                      "user_id": interaction.user.id})

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Handler for the submit event. This method should be overridden by the inheriting class.
        Args:
            interaction (discord.Interaction): The interaction that triggered the modal
        """
        raise NotImplementedError


class ConfirmationModal(BaseModal, title="Confirm"):
    confirm_input = discord.ui.TextInput(
        label="This action cannot be reverted.",
        max_length=100,
        min_length=1,
        required=True,
        placeholder="Type \"CONFIRM\" to confirm.",
        style=discord.TextStyle.short
    )

    def __init__(self, callback: callable, callback_params: dict, **kwargs):
        """
        Generic modal for confirming actions.
        Args:
            callback (Callable): The callback to be executed if the action is confirmed
            callback_params (dict): The parameters to be passed to the callback
            kwargs: Additional keyword arguments
        """
        super().__init__(**kwargs)
        self.callback = callback
        self.callback_params = callback_params

    @interaction_handler
    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Handler for the submit event.
        Args:
            interaction (discord.Interaction): The interaction that triggered the modal
        Returns:
            None
        """
        if self.confirm_input.value.lower() != "confirm":
            return await interaction.response.send_message("Action not confirmed.", ephemeral=True)  # noqa
        await self.callback(interaction, **self.callback_params)
