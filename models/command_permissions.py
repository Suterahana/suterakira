
class CommandPermissions:
    def __init__(self, command_name, user_permissions, bot_permissions):
        self.command_name = command_name
        self.user_permissions = user_permissions
        self.bot_permissions = bot_permissions

    @classmethod
    def from_dict(cls, command_name, data):
        return cls(command_name, data.get("member", []), data.get("bot", []))
