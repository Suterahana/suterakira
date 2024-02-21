from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import View, Button as ButtonView

if TYPE_CHECKING:
    from discord_bot.interactions_handlers.main_interactions_handlers.help_menu_interactions_handler import \
        HelpMenuInteractionsHandler


def get_back_view(interactions_handler: 'HelpMenuInteractionsHandler', add_close_button: bool = False) -> View:
    """
    Generates and returns the view for the back button
    Args:
        interactions_handler (BaseInteractionsHandler): The interactions handler for the help menu
        add_close_button (bool): Whether to add a close button to the view
    Returns:
        View: The view
    """
    view = View(timeout=300)

    back_button = ButtonView(label="Back", style=ButtonStyle.gray, custom_id="back")
    back_button.callback = interactions_handler.handle_go_back
    view.add_item(back_button)

    if add_close_button:
        close_button = ButtonView(label="Close", emoji='🗑', style=ButtonStyle.red, custom_id="close")
        close_button.callback = interactions_handler.handle_cancel
        view.add_item(close_button)

    view.on_timeout = interactions_handler.on_timeout
    return view
