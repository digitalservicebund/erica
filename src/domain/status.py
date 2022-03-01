import pydantic.types


class Status(pydantic.types.Enum):
    new = 0
    scheduled = 1
    processing = 2
    failed = 3
    success = 4
