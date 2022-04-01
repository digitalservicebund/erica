from redis import Redis
from rq import Queue, Connection

from erica.erica_legacy.config import get_settings

_ALLOWED_QUEUE_NAMES = ['dongle', 'cert', 'common']


class QueueNotAvailableError(Exception):
    """Raised in case an unexpected queue name was provided"""


def get_queue(queue_name='dongle'):
    if queue_name not in _ALLOWED_QUEUE_NAMES:
        raise QueueNotAvailableError
    with Connection(Redis.from_url(get_settings().queue_url)):
        return Queue(queue_name)
