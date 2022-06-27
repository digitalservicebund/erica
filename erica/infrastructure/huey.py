from huey import RedisHuey

from erica.config import get_settings


huey = RedisHuey('erica-huey-queue', url=get_settings().queue_url, immediate=get_settings().use_immediate_worker)
