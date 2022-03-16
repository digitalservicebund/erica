from redis import Redis
from rq import Queue, Connection

with Connection(Redis('localhost', 6379)):
    dongle_queue = Queue('dongle')
    cert_queue = Queue('cert')
    common_queue = Queue('common')
