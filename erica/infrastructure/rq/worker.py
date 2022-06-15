import sys

from redis import Redis
from rq import Connection, Worker, Queue
from sentry_sdk.integrations.rq import RqIntegration

from erica.config import get_settings
import sentry_sdk

from erica.exception_handler import retry_exception_handler


def run_worker():
    if get_settings().sentry_dsn_worker:
        sentry_sdk.init(
            get_settings().sentry_dsn_worker,
            integrations=[RqIntegration()],
            environment=get_settings().env_name)

    with Connection(Redis.from_url(get_settings().queue_url,
                                   health_check_interval=10,
                                   socket_connect_timeout=5,
                                   socket_keepalive=True,
                                   retry_on_timeout=True)):
        qs = map(Queue, sys.argv[1:]) if sys.argv[1:] else Queue(get_settings().default_queue)
        worker = Worker(qs, exception_handlers=[retry_exception_handler])
        worker.work(with_scheduler=True)


if __name__ == '__main__':
    run_worker()
