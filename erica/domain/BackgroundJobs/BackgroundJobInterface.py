from abc import ABCMeta, abstractmethod


class BackgroundJobInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def enqueue(self, f, *args, **kwargs):
        pass

    @abstractmethod
    def scheduled_enqueue(self):
        pass

    @abstractmethod
    def get_enqueued_job_by_id(self, job_id):
        pass
