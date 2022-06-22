from erica.config import get_settings

from huey import RedisHuey

huey_task = RedisHuey('erica-huey-queue', url=get_settings().queue_url, immediate=get_settings().use_immediate_worker)
