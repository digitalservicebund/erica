from redis import Redis
from rq import Queue, Connection

from erica.erica_legacy.config import get_settings

with Connection(Redis(get_settings().queue_host, get_settings().queue_port)):
    dongle_queue = Queue('dongle')
    cert_queue = Queue('cert')
    common_queue = Queue('common')
