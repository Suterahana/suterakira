import settings
from constants import Colour, HelpMenuType
from utils.decorators import slash_command
from ..main_slashes.base_main_slashes import MainSlashes
from ...interactions_handlers.main_interactions_handlers.help_menu_interactions_handler import \
    HelpMenuInteractionsHandler


class GeneralMainSlashes(MainSlashes):

    @slash_command
    async def support(self):
        """
        /support
        Get the support server invite link
        """

        if not await self.preprocess_and_validate():
            return

        from utils.embed_factory.general_embeds import get_quick_embed
        await self.interaction.response.send_message(  # noqa
            embed=get_quick_embed(text=f"[Click here]({settings.SUPPORT_SERVER_INVITE}) to join the support server.",
                                  color=Colour.SUCCESS),
            ephemeral=True
        )

    @slash_command
    async def help(self, menu: HelpMenuType.values_as_enum() = None, make_visible: bool = False):
        """
        /help
        Show the help menu
        """

        if not await self.preprocess_and_validate():
            return

        # since we only have the main commands for now
        menu = HelpMenuType.values_as_enum().Main if not menu else menu  # noqa

        interactions_handler = HelpMenuInteractionsHandler(interaction=self.interaction,
                                                           selected_menu=menu)

        embed, view = interactions_handler.get_embed_and_view()

        await self.interaction.response.send_message(embed=embed,  # noqa
                                                     view=view,
                                                     ephemeral=self.send_as_ephemeral(make_visible=make_visible))
