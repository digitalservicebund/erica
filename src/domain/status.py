from enum import Enum


class Status(int, Enum):
    new = 0
    scheduled = 1
    processing = 2
    failed = 3
    success = 4
