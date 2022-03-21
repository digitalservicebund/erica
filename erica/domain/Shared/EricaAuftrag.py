from enum import Enum


class RequestType(int, Enum):
    freischalt_code_request = 0
    freischalt_code_activate = 1
    freischalt_code_revocate = 2
