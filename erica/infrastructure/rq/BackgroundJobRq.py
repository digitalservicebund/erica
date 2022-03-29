from rq import Queue
from rq.job import Job

from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from erica.infrastructure.rq.get_queue import get_queue


class BackgroundJobRq(BackgroundJobInterface):
    __queue: Queue

    def __init__(self, queue: Queue = get_queue('dongle')):
        self.__queue = queue

    def scheduled_enqueue(self):
        pass

    def get_enqueued_job_by_id(self, job_id):
        return self.__queue.fetch_job(job_id)

    def list_all_jobs(self):
        return self.__queue

    def enqueue(self, f, *args, **kwargs) -> Job:

        (f, timeout, description, result_ttl, ttl, failure_ttl,
         depends_on, job_id, at_front, meta, retry, on_success,
         on_failure, pipeline, args, kwargs) = Queue.parse_args(f, *args, **kwargs)

        return self.__queue.enqueue(
            f=f, args=args, kwargs=kwargs, timeout=timeout,
            result_ttl=result_ttl, ttl=ttl, failure_ttl=failure_ttl,
            description=description, depends_on=depends_on, job_id=job_id,
            at_front=at_front, meta=meta, retry=retry, on_success=on_success, on_failure=on_failure,
            pipeline=pipeline)
