import sys

from redis import Redis
from rq import Connection, Worker, Queue


def run_worker():
    with Connection(Redis('localhost', 6379)):
        qs = map(Queue, sys.argv[1:]) or [Queue('dongle')]
        worker_dongle = Worker(qs)
        worker_dongle.work(with_scheduler=True)


if __name__ == '__main__':
    run_worker()
