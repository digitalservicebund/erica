import copy
from unittest.mock import Mock

import pytest
from fakeredis import FakeStrictRedis
from rq import Queue

from erica.infrastructure.rq.BackgroundJobRq import BackgroundJobRq


@pytest.fixture()
def async_fake_redis_queue():
    return Queue("test", connection=FakeStrictRedis())


@pytest.fixture()
def sync_fake_redis_queue():
    return Queue(is_async=False, connection=FakeStrictRedis())


@pytest.fixture()
def mocked_queue():
    class MockQueue(Queue, list):
        call_list = []

        @classmethod
        def enqueue(cls, *args, **kwargs):
            cls.call_list.append([*args, {**kwargs}])

    return MockQueue


class PickableMock(Mock):

    def __reduce__(self):
        return Mock, ()


class TestBackgroundJobRqEnqueue:

    def test_if_enqueue_job_then_job_is_queued(self, async_fake_redis_queue):
        fake_job = PickableMock()
        background_job_rq = BackgroundJobRq(queue=async_fake_redis_queue)

        job = background_job_rq.enqueue(fake_job)

        assert job.is_queued

    def test_if_job_enqueued_then_job_function_is_called(self, sync_fake_redis_queue):
        fake_job = PickableMock()
        background_job_rq = BackgroundJobRq(queue=sync_fake_redis_queue)

        job = background_job_rq.enqueue(fake_job)

        assert len(fake_job.mock_calls) == 1
        assert job.is_finished

    def test_if_job_enqueued_with_arguments_then_queue_is_called_with_arguments(self, mocked_queue):
        fake_job = PickableMock()
        args = [1939, "First Batman comic"]
        input_kwargs = {'job_timeout': None, 'description': 'description', 'result_ttl': 12, 'ttl': 12,
                        'failure_ttl': 12, 'depends_on': Mock, 'job_id': 12, 'at_front': 12, 'meta': Mock,
                        'retry': Mock, 'on_success': Mock, 'on_failure': Mock, 'pipeline': Mock}
        additional_kwargs = {'author': 'Bill Finger and Bob Kane'}
        expected_kwargs = copy.deepcopy(input_kwargs)
        expected_kwargs['timeout'] = expected_kwargs.pop('job_timeout')
        background_job_rq = BackgroundJobRq(queue=mocked_queue)

        background_job_rq.enqueue(fake_job, *args, **input_kwargs, **additional_kwargs)

        assert background_job_rq._BackgroundJobRq__queue.call_list == [[{'f': fake_job, 'args': tuple(args), **expected_kwargs, 'kwargs': {**additional_kwargs}}]]


class TestTestBackgroundJobRqGetJobById:

    def test_if_job_added_to_queue_then_job_is_found(self, sync_fake_redis_queue):
        fake_job = PickableMock()
        job = sync_fake_redis_queue.enqueue(fake_job)
        job_id = job.id

        found_job = BackgroundJobRq(sync_fake_redis_queue).get_enqueued_job_by_id(job_id)

        assert found_job == job

    def test_if_job_not_on_queue_then_return_none(self, sync_fake_redis_queue):
        found_job = BackgroundJobRq(sync_fake_redis_queue).get_enqueued_job_by_id("INVALID_ID")

        assert found_job is None
