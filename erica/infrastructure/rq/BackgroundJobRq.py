from rq import Queue

from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from erica.infrastructure.rq.queue import dongle_queue


class BackgroundJobRq(BackgroundJobInterface):
    __queue: Queue

    def __init__(self, queue: Queue = dongle_queue):
        self.__queue = queue

    def scheduled_enqueue(self):
        pass

    def get_enqueued_job_by_id(self):
        pass

    def list_all_jobs(self):
        pass

    def enqueue(self, f, *args, **kwargs):

        (f, timeout, description, result_ttl, ttl, failure_ttl,
         depends_on, job_id, at_front, meta, retry, on_success,
         on_failure, pipeline, args, kwargs) = Queue.parse_args(f, *args, **kwargs)

        self.__queue.enqueue(
            f=f, args=args, kwargs=kwargs, timeout=timeout,
            result_ttl=result_ttl, ttl=ttl, failure_ttl=failure_ttl,
            description=description, depends_on=depends_on, job_id=job_id,
            at_front=at_front, meta=meta, retry=retry, on_success=on_success, on_failure=on_failure,
            pipeline=pipeline)
