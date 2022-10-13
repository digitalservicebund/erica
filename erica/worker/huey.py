import logging
import tempfile

import sentry_sdk

from huey import RedisHuey

from erica.config import get_settings


huey = RedisHuey('erica-huey-queue', url=get_settings().queue_url, immediate=get_settings().use_immediate_worker)
eric_wrapper = None


@huey.on_startup()
def huey_init():
    init_sentry()
    eric_wrapper_init()


def init_sentry():
    try:
        sentry_sdk.init(
            dsn=get_settings().sentry_dsn_worker,
            environment=get_settings().env_name,
            # traces_sample_rate=1.0,
        )
    except Exception as e:
        # pass silently if the Sentry integration failed
        logging.getLogger().warn(f"Sentry integration failed to load: {e}")
        pass


def eric_wrapper_init():
    global eric_wrapper
    if eric_wrapper is None:
        from erica.worker.pyeric.eric import EricWrapper
        eric_wrapper = EricWrapper()
        with tempfile.TemporaryDirectory() as tmp_dir:
            eric_wrapper.initialise(log_path=tmp_dir)


def get_initialised_eric_wrapper():
    return eric_wrapper


@huey.on_shutdown()
def shutdown_eric_wrapper():
    global eric_wrapper
    eric_wrapper.shutdown()


@huey.pre_execute()
def start_sentry_transaction(task):
    task.sentry_txn = sentry_sdk.start_transaction(op="huey task", name=task.name)
    sentry_sdk.set_tag("huey.task_id", task.id)


@huey.post_execute()
def finish_sentry_transaction(task, task_value, exc):
    if exc:
        task.sentry_txn.set_status("internal_error")
    task.sentry_txn.finish()

