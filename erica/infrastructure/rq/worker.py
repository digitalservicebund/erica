import sys

from redis import Redis
from rq import Connection, Worker, Queue

from erica.config import get_settings


def run_worker():
    with Connection(Redis.from_url(get_settings().queue_url)):
        qs = map(Queue, sys.argv[1:]) if sys.argv[1:] else Queue(get_settings().default_queue)
        worker = Worker(qs)
        worker.work()


if __name__ == '__main__':
    run_worker()
