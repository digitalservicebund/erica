from erica.config import get_settings

from huey import RedisHuey

huey = RedisHuey('erica-huey-queue', url=get_settings().queue_url, immediate=get_settings().use_immediate_worker)
