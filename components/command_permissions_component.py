import json
from typing import Tuple, List

import cached_items
from components.base_component import BaseComponent
from utils.helpers.file_helpers import get_path_to_file


class CommandPermissionsComponent(BaseComponent):

    def __init__(self, *args, **kwargs):
        """
        Component for handling command permissions. Command permissions are permissions required for the command to be
         executed in a guild.
        """
        super().__init__(*args, **kwargs)

    @staticmethod
    def load_permissions() -> None:
        """
        Load the permissions
        Returns:
            None
        """
        with open(get_path_to_file(["data", "commands_permissions", "main_commands.json"])) as main_commands_file:
            cached_items.main_commands_permissions = json.loads(main_commands_file.read())

    @staticmethod
    def get_permissions(command_name: str) -> Tuple[List[str], List[str]]:
        """
        Get the permissions for a command
        Args:
            command_name (str): The name of the command
        Returns:
            Tuple[List[str], List[str]]: The member permissions and bot permissions for the command

        """
        command_permissions = cached_items.main_commands_permissions.get(command_name, {"member": [], "bot": []})
        return command_permissions["member"], command_permissions["bot"]
