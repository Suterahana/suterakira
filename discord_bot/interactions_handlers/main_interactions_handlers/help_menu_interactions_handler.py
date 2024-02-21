import discord
from constants import Colour, HelpMenuType

from .base_main_interactions_handler import MainInteractionsHandler
from utils.decorators import interaction_handler
from utils.view_factory.general_views import get_back_view
from utils.view_factory.help_menu_views import get_general_help_view
from utils.embed_factory.help_menu_embeds import get_general_help_embed, get_help_embed_for_menu
from utils.embed_factory.general_embeds import get_quick_embed


class HelpMenuInteractionsHandler(MainInteractionsHandler):

    def __init__(self, interaction: discord.Interaction, selected_menu: HelpMenuType.values_as_enum() = None,
                 allow_navigation: bool = True):
        """
        Interaction handler for the help menu.
        Args:
            interaction (discord.Interaction): The interaction that triggered the help menu
            selected_menu (HelpMenuType.values_as_enum()): The selected menu
            allow_navigation (bool): Whether to allow navigation in the help menu from its initial state
        """
        super().__init__(interaction)
        self._selected_menu = selected_menu.value if selected_menu else None
        self.allow_navigation = allow_navigation

    @interaction_handler
    async def handle_main_menu(self, interaction: discord.Interaction) -> None:
        """
        Handles moving to 'main commands' help menu
        Args:
            interaction (discord.Interaction): The interaction that triggered the help menu
        Returns:
            None
        """
        if self.source_interaction.user.id != interaction.user.id:
            return await interaction.response.defer()  # noqa
        await interaction.response.defer()  # noqa
        self._selected_menu = HelpMenuType.MAIN
        await self.refresh_message()

    @interaction_handler
    async def handle_cancel(self, interaction: discord.Interaction):
        """
        Handles cancelling/closing the help menu
        Args:
            interaction (discord.Interaction): The interaction that triggered the help menu
        Returns:
            None
        """
        if self.source_interaction.user.id != interaction.user.id:
            if not (self.guild and self.guild.get_member(interaction.user.id).guild_permissions.manage_messages):
                return await interaction.response.defer()  # noqa
        await interaction.response.defer()  # noqa
        await self.source_interaction.edit_original_response(embed=get_quick_embed("Help menu closed",
                                                                                   color=Colour.PRIMARY_ACCENT),
                                                             view=None)

    @interaction_handler
    async def handle_go_back(self, interaction: discord.Interaction):
        """
        Handles going back to the main/general help menu
        Args:
            interaction (discord.Interaction): The interaction that triggered the help menu
        Returns:
            None
        """
        if self.source_interaction.user.id != interaction.user.id:
            return await interaction.response.defer()  # noqa
        await interaction.response.defer()  # noqa
        self._selected_menu = None
        await self.refresh_message()

    async def refresh_message(self, no_views=False) -> None:
        """
        Refreshes the message after any change in the handler attributes and state
        Args:
            no_views (bool): Whether to remove the views from the message
        Returns:
            None
        """
        embed, views = self.get_embed_and_view()
        await self.source_interaction.edit_original_response(
            embed=embed,
            view=views if not no_views and self.allow_navigation else None
        )

    def get_embed_and_view(self) -> tuple[discord.Embed, discord.ui.View]:
        """
        Generates and returns the embed and views for the help menu in the current state
        Returns:
            tuple[discord.Embed, discord.ui.View]: The embed and views for the help menu
        """
        if self._selected_menu:
            embed = get_help_embed_for_menu(menu_type=self._selected_menu)
            views = get_back_view(interactions_handler=self,
                                  add_close_button=True)
        else:
            embed = get_general_help_embed()
            views = get_general_help_view(interactions_handler=self)

        return embed, views

    async def on_timeout(self) -> None:
        await self.refresh_message(no_views=True)
