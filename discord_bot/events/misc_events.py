import sys
import traceback

from clients import discord_client
from constants import LogType
from utils.custom_logger import ErrorLogger


@discord_client.event
async def on_error(event, *args, **kwargs):
    """
    Uncaught exceptions handler
    Args:
        event (str): The event name
        args (tuple): The event args
        kwargs (dict): The event kwargs
    Returns:
        None
    """
    error_text = f"event= {event}\n" \
                 f"args= {args}\n" \
                 f"kwargs= {kwargs}\n" \
                 f"exception_info= {sys.exc_info()}\n" \
                 f"traceback=\n {traceback.format_exc()}"

    ErrorLogger(component="ON_ERROR").log(message=error_text, log_type=LogType.ERROR)
