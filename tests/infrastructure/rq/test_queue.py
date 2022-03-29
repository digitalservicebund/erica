import pytest
from redis import Redis
from rq import Queue

from erica.config import get_settings
from erica.infrastructure.rq.queue import get_queue, QueueNotAvailableError


class TestQueue:

    def test_if_queue_name_not_allowed_then_raise_error(self):
        with pytest.raises(QueueNotAvailableError):
            get_queue("NOT_ALLOWED_NAME")

    def test_if_no_queue_name_then_return_dongle_queue_with_correct_connection(self):
        expected_queue = Queue("dongle", connection=Redis(get_settings().queue_host, get_settings().queue_port))

        returned_queue = get_queue()

        assert returned_queue == expected_queue


    def test_if_queue_name_dongle_allowed_then_return_dongle_queue_with_correct_connection(self):
        expected_queue = Queue("dongle", connection=Redis(get_settings().queue_host, get_settings().queue_port))

        returned_queue = get_queue("dongle")

        assert returned_queue == expected_queue

    def test_if_queue_name_cert_allowed_then_return_cert_queue_with_correct_connection(self):
        expected_queue = Queue("cert", connection=Redis(get_settings().queue_host, get_settings().queue_port))

        returned_queue = get_queue("cert")

        assert returned_queue == expected_queue

    def test_if_queue_name_common_allowed_then_return_common_queue_with_correct_connection(self):
        expected_queue = Queue("common", connection=Redis(get_settings().queue_host, get_settings().queue_port))

        returned_queue = get_queue("common")

        assert returned_queue == expected_queue

