import sys

from redis import Redis
from rq import Connection, Worker, Queue

from erica.config import get_settings


def run_worker():
    with Connection(Redis(get_settings().queue_host, get_settings().queue_port)):
        print(map(Queue, sys.argv[1:]) if sys.argv[1:] else Queue(get_settings().default_queues))
        qs = map(Queue, sys.argv[1:]) if sys.argv[1:] else Queue(get_settings().default_queues)
        worker = Worker(qs)
        worker.work(with_scheduler=True)


if __name__ == '__main__':
    run_worker()
