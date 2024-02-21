import inspect
import traceback
from functools import wraps

import discord
from .custom_logger import ErrorLogger, InfoLogger
from constants import LogType, Colour


def periodic_worker(name: str, initial_delay: int = 0, **kwargs_) -> callable:
    """
    Decorator for periodic workers. The decorated function must be a coroutine.
    Args:
        name (str): Name of the worker
        initial_delay (int): Initial delay before the worker starts
        **kwargs_: Additional arguments to be passed
    Returns:
        callable: The decorated function
    """
    def decorator(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError("Periodic worker must be a coroutine function.")
        func.worker_data = {
            "name": name,
            "initial_delay": initial_delay,
            "kwargs": kwargs_
        }

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def self_scheduling_worker(name: str, initial_delay: int = 0, **kwargs_) -> callable:
    """
    Decorator for self-scheduling workers. The decorated function must be a coroutine.
    Args:
        name (str): Name of the worker
        initial_delay (int): Initial delay before the worker starts
        **kwargs_: Additional arguments to be passed
    Returns:
        callable: The decorated function
    """
    def decorator(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError("Self-scheduling worker must be a coroutine function.")
        func.worker_data = {
            "name": name,
            "initial_delay": initial_delay,
            "kwargs": kwargs_
        }

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def interaction_handler(func: callable) -> callable:
    """
    Decorator for discord interaction handlers. The decorated function must be a coroutine.
    Args:
        func (callable): The decorated function
    Returns:
        callable: The wrapper function
    """
    error_logger = ErrorLogger(component="InteractionsHandler")
    info_logger = InfoLogger(component="InteractionsHandler")

    async def wrapper(*args, **kwargs):
        handler_name = func.__qualname__
        interaction = None
        for arg in args:
            if isinstance(arg, discord.Interaction):
                interaction = arg
                break
        if not interaction:
            for arg in kwargs.values():
                if isinstance(arg, discord.Interaction):
                    interaction = arg
                    break
        if not interaction:
            error_logger.log(f"Handler {handler_name} called without interaction. "
                             f"Args: {args} and kwargs: {kwargs}.")
        try:
            info_logger.log(f"Handler {handler_name} called by user: {interaction.user} ({interaction.user.id})."
                            + f" Channel: {interaction.channel} ({interaction.channel.id})."
                            if interaction.channel else ""
                            + f" Guild: {interaction.guild} ({interaction.guild.id})."
                            if interaction.guild else "",
                            log_type=LogType.INTERACTION_CALLBACK_RECEIVED,
                            extras={"interaction_data": interaction.data})
        except Exception as e:
            print(f"Error while logging interaction callback: {e}\n{traceback.format_exc()}")
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_logger.log(f"Handler {handler_name} failed. Error: {e}\n{traceback.format_exc()}")
            if not interaction.response.is_done():  # noqa
                await interaction.response.send_message(  # noqa
                    "An error occurred. We've been notified and will look into it"
                    " as soon as possible. Sorry for the inconvenience!",
                    ephemeral=True
                )
            else:
                await interaction.followup.send("An error occurred. We've been notified and will look into it"
                                                " as soon as possible. Sorry for the inconvenience!", ephemeral=True)

        if not interaction.response.is_done():  # noqa
            error_logger.log(f"Handler {handler_name} did not respond to interaction. "
                             f"Args: {args} and kwargs: {kwargs}.")

    return wrapper


def slash_command(func: callable) -> callable:
    """
    Decorator for discord slash command handlers. The decorated function must be a coroutine.
    Args:
        func: The decorated function
    Returns:
        callable: The wrapper function
    """
    error_logger = ErrorLogger(component="SlashCommandsHandler")

    async def wrapper(*args, **kwargs):
        slashes_handler = args[0]
        interaction = slashes_handler.interaction
        if not interaction:
            error_logger.log(f"Interaction not found in kwargs for {func}\n"
                             f"Passed args: {args}\n"
                             f"Passed kwargs: {kwargs}",
                             log_type=LogType.WARNING, log_to_discord=True)
            return await func(*args, **kwargs)

        try:
            return await func(*args, **kwargs)
        except Exception as e:

            error_logger.log(f"Slash handler {func} failed.\n"
                             f"Interaction data: {interaction.data}\n"
                             f"Error: {e}\n{traceback.format_exc()}",
                             log_type=LogType.ERROR)
            error_message = "An error occurred. We've been notified and will look into it as soon as possible. " \
                            "Sorry for the inconvenience!"

        if error_message:
            error_embed = discord.Embed(title="Error",
                                        description=error_message,
                                        color=Colour.ERROR)

            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(embed=error_embed,
                                                            ephemeral=True,
                                                            delete_after=10)
                else:
                    await interaction.followup.send(embed=error_embed,
                                                    ephemeral=True,
                                                    delete_after=10)
            except discord.NotFound:
                try:
                    await interaction.followup.send(embed=error_embed,
                                                    ephemeral=True,
                                                    delete_after=10)
                except Exception:
                    pass

        if not interaction.response.is_done():
            error_logger.log(f"Slash Handler {func} did not respond to interaction. "
                             f"Args: {args} and kwargs: {kwargs}.")

    return wrapper
