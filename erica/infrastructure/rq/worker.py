import sys

from redis import Redis
from rq import Connection, Worker, Queue

from erica.config import get_settings


def run_worker():
    with Connection(Redis(get_settings().queue_host, get_settings().queue_port)):
        qs = map(Queue, sys.argv[1:]) or [Queue(get_settings().default_queues)]
        worker = Worker(qs)
        worker.work(with_scheduler=True)


if __name__ == '__main__':
    run_worker()
