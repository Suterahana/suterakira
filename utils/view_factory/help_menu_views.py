from discord import ButtonStyle
from discord.ui import View, Button as ButtonView

from discord_bot.interactions_handlers.main_interactions_handlers.help_menu_interactions_handler import \
    HelpMenuInteractionsHandler


def get_general_help_view(interactions_handler: HelpMenuInteractionsHandler,
                          add_close_button=True) -> View:
    """
    Generates and returns the view for the general help menu
    Args:
        interactions_handler (BaseInteractionsHandler): The interactions handler for the help menu
        add_close_button (bool): Whether to add a close button to the view
    Returns:
        View: The view
    """
    view = View(timeout=300)

    general_help_button = ButtonView(label="Main Commands", style=ButtonStyle.green)
    general_help_button.callback = interactions_handler.handle_main_menu
    view.add_item(general_help_button)

    if add_close_button:
        close_button = ButtonView(label="Close", style=ButtonStyle.red, emoji="🗑")
        close_button.callback = interactions_handler.handle_cancel
        view.add_item(close_button)

    view.on_timeout = interactions_handler.on_timeout
    return view
