from discord import app_commands
from discord.ext.commands import Cog

from constants import HelpMenuType
from ...main_slashes.general_main_slashes import GeneralMainSlashes


class GeneralMainBlueprints(Cog):
    SUPPORT = app_commands.command(name="support",
                                   description="Get the support server invite link",
                                   extras={"unlisted": True})
    HELP = app_commands.command(name="help",
                                description="Show the help menu",
                                extras={"unlisted": True})

    @SUPPORT
    async def support(self, interaction):
        """Get the support server invite link

        Parameters
        -----------
        interaction: Interaction
            Interaction to handle
        """

        await GeneralMainSlashes(interaction=interaction).support()

    @HELP
    @app_commands.rename(make_visible="make-visible")
    async def help(self, inter, menu: HelpMenuType.values_as_enum() = None, make_visible: bool = False):
        """Show the help menu

        Parameters
        -----------
        inter: Interaction
            Interaction to handle
        menu: HelpMenuType.values_as_enum()
           Jump to a specific menu
        make_visible: bool
            Make the menu visible to everyone
        """

        await GeneralMainSlashes(interaction=inter).help(menu=menu, make_visible=make_visible)
