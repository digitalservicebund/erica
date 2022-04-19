from redis import Redis
from rq import Queue, Connection

from erica.config import get_settings

_ALLOWED_QUEUE_NAMES = ['dongle', 'cert', 'common']


class QueueNotAvailableError(Exception):
    """Raised in case an unexpected queue name was provided"""


def get_queue(queue_name='dongle'):
    if queue_name not in _ALLOWED_QUEUE_NAMES:
        raise QueueNotAvailableError
    with Connection(Redis.from_url(get_settings().queue_url,
                                   health_check_interval=10,
                                   socket_connect_timeout=5,
                                   socket_keepalive=True,
                                   retry_on_timeout=True,
                                   socket_keepalive_options={
                                    "socket.TCP_KEEPIDLE":120,
                                    "socket.TCP_KEEPCNT":2,
                                    "socket.TCP_KEEPINTVL":30
                                   })):
        return Queue(queue_name)
