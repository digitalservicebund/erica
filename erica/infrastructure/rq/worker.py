import sys

from redis import Redis
from rq import Connection, Worker, Queue

from erica.config import get_settings


def run_worker():
    with Connection(Redis.from_url(get_settings().queue_url,
                                   health_check_interval=10,
                                   socket_connect_timeout=5,
                                   socket_keepalive=True,
                                   retry_on_timeout=True,
                                   socket_keepalive_options={
                                    "socket.TCP_KEEPIDLE":120,
                                    "socket.TCP_KEEPCNT":2,
                                    "socket.TCP_KEEPINTVL":30
                                   })):
        qs = map(Queue, sys.argv[1:]) if sys.argv[1:] else Queue(get_settings().default_queue)
        worker = Worker(qs)
        worker.work()


if __name__ == '__main__':
    run_worker()
