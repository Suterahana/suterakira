from workers.worker_manager import WorkerManagerService
from .discord_service import DiscordClient

discord_client = DiscordClient().get_client()
worker_manager_service = WorkerManagerService()
