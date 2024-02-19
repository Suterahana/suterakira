import asyncio
import io
from pathlib import Path

import discord

import settings
from clients import discord_client
from constants import LogType
from settings import DISCORD_LOGGING_CHANNEL_ID
from utils.embed_factory.general_embeds import get_discord_log_embed
from utils.helpers.file_helpers import get_path_to_file
from utils.helpers.string_helpers import get_current_time_string


class Logger:
    def __init__(self,
                 component: str = None,
                 log_to_file_default: bool = True,
                 log_to_discord_default: bool = True,
                 **kwargs):
        """
        Base logger class
        Args:
            component (str): The component name
            log_to_file_default (bool): Whether to log to file by default if not specified
            log_to_discord_default (bool): Whether to log to discord by default if not specified
            **kwargs: Additional keyword arguments
        """
        self.component = component or "Unspecified Component"
        self.log_to_file_default = log_to_file_default
        self.log_to_discord_default = log_to_discord_default

        self.logging_directory = get_path_to_file(['logs', f'{settings.ENV}'])
        self._make_logging_directory()
        self.default_log_type = LogType.GENERAL

    def log(self,
            message: str,
            log_type: str = None,
            log_to_file: bool = None,
            log_to_discord: bool = None,
            extras: dict = None) -> None:
        """
        Log a message
        Args:
            message (str): The message to log
            log_type (LogType): The type of log
            log_to_file (bool): Whether to log to file
            log_to_discord (bool): Whether to log to discord
            extras (dict): Additional information to log
        Returns:
            None
        """
        log_type = log_type or self.default_log_type
        log_to_file = log_to_file if log_to_file is not None else self.log_to_file_default
        log_to_discord = log_to_discord if log_to_discord is not None else self.log_to_discord_default
        extras = extras or {}
        extras.update({'component': self.component})

        asyncio.get_event_loop().create_task(
            self._log(message=message, log_type=log_type, log_to_file=log_to_file,
                      log_to_discord=log_to_discord, extras=extras)
        )

    async def _log(self,
                   message: str,
                   log_type: str,
                   log_to_file: bool,
                   log_to_discord: bool,
                   extras: dict) -> None:
        """
        Log a message asynchronously. Separation of log and _log is to allow for non-async contexts to use log and
        also for logging in general to be non-blocking
        Args:
            message (str): The message to log
            log_type (LogType): The type of log
            log_to_file (bool): Whether to log to file
            log_to_discord (bool): Whether to log to discord
            extras (dict): Additional information to log
        Returns:
            None
        """
        event_loop = asyncio.get_event_loop()
        await event_loop.run_in_executor(None, self._log_to_console,
                                         message, log_type, extras)
        if log_to_file:
            await event_loop.run_in_executor(None, self._log_to_file,
                                             message, log_type, extras)
        if log_to_discord:
            await event_loop.run_in_executor(None, self._log_to_discord,
                                             message, log_type, extras)

    async def _log_to_console(self, message: str, log_type: str, extras: dict = None) -> None:  # noqa
        """
        Log a message to console
        Args:
            message (str): The message to log
            log_type (LogType): The type of log
            extras (dict): Additional information to log
        Returns:
            None
        """
        extras_str = ' '.join([f'[{key}={value}]' for key, value in extras.items()])
        print(f"{get_current_time_string()}  [{log_type}] - {message}\n\tExtras: {extras_str}")

    async def _log_to_file(self, message: str, log_type: str, extras: dict = None) -> None:
        """
        Log a message to file
        Args:
            message (str): The message to log
            log_type (LogType): The type of log
            extras (dict): Additional information to log
        Returns:
            None
        """
        try:
            extras_str = ' '.join([f'[{key}={value}]' for key, value in extras.items()])
            with open(self._get_logging_file_path(), 'a+', encoding='utf-8') as logging_file:
                logging_file.write(
                    f"{get_current_time_string()} [{log_type}] {message} - {extras_str}\n"
                )
        except Exception as e:
            await self._log_to_console(message=f"Error while logging to file: {e}",
                                       log_type=LogType.ERROR)

    async def _log_to_discord(self, message: str, log_type: str, extras: dict = None) -> None:  # noqa
        """
        Log a message to discord
        Args:
            message (str): The message to log
            log_type (LogType): The type of log
            extras (dict): Additional information to log
        Returns:
            None
        """
        log_channel = discord_client.get_channel(DISCORD_LOGGING_CHANNEL_ID)
        if len(message) > 4000:
            buf = io.BytesIO(str.encode(f"{get_current_time_string()} [{log_type}]\n{message}"))
            await log_channel.send(content=f"{log_type} - message too long..",
                                   file=discord.File(buf, filename=f'log_{log_type}_{get_current_time_string()}.txt'),)
        else:
            log_embed = get_discord_log_embed(message=message, log_type=log_type, extras=extras)
            await log_channel.send(embed=log_embed)

    def _make_logging_directory(self) -> None:
        """
        Make the logging directory if it doesn't exist
        """
        Path(self.logging_directory).mkdir(parents=True, exist_ok=True)

    def _get_logging_file_path(self):
        return get_path_to_file([self.logging_directory, f'{get_current_time_string("%Y.%m.%d")}.txt'])


class InfoLogger(Logger):
    def __init__(self, **kwargs):
        """
        Info logger class
        Args:
            **kwargs: Additional keyword arguments
        """
        super().__init__(log_to_file_default=True, log_to_discord_default=False, **kwargs)
        self.default_log_type = LogType.INFO


class ErrorLogger(Logger):
    def __init__(self, **kwargs):
        """
        Error logger class
        Args:
            **kwargs: Additional keyword arguments
        """
        super().__init__(log_to_file_default=True, log_to_discord_default=True, **kwargs)
        self.default_log_type = LogType.ERROR


class DMLogger(Logger):
    def __init__(self, **kwargs):
        """
        DM logger class
        Args:
            **kwargs: Additional keyword arguments
        """
        super().__init__(log_to_file_default=True, log_to_discord_default=True, **kwargs)
        self.default_log_type = LogType.DM_RECEIVED

    async def log_dm(self, message: discord.Message) -> None:
        """
        Log a message received on DMs with details
        Args:
            message (discord.Message): The message received
        Returns:
            None
        """
        media_list = ""
        if message.attachments:
            media_list += "**Attachments**:\n"
            for attachment in message.attachments:
                media_list += f"[{attachment.content_type}] ({attachment.filename}) {attachment.url}\n"
        if message.stickers:
            media_list += "**Stickers**:\n"
            for sticker in message.stickers:
                media_list += f"[sticker] ({sticker.name}) {sticker.url}"
        message_content = "> " + message.content.strip().replace("\n", "\n> ")
        self.log(message=f"Received message on DMs from {message.author} ({message.author.id})\n"
                         f"{message_content}\n{media_list}")
