import logging

import sentry_sdk
from huey import RedisHuey

from erica.config import get_settings


huey = RedisHuey('erica-huey-queue', url=get_settings().queue_url, immediate=get_settings().use_immediate_worker)


@huey.on_startup()
def init_sentry():
    try:
        sentry_sdk.init(
            dsn=get_settings().sentry_dsn_worker,
            environment=get_settings().env_name,
            traces_sample_rate=1.0,
        )
    except Exception as e:
        # pass silently if the Sentry integration failed
        logging.getLogger().warn(f"Sentry integration failed to load: {e}")
        pass


@huey.pre_execute()
def start_sentry_transaction(task):
    task.sentry_txn = sentry_sdk.start_transaction(op="huey task", name=task.name)
    sentry_sdk.set_tag("huey.task_id", task.id)


@huey.post_execute()
def finish_sentry_transaction(task, task_value, exc):
    task.sentry_txn.finish()
