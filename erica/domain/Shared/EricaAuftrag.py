from enum import Enum


class RequestType(int, Enum):
    freischalt_code_request = 0
    freischalt_code_activate = 1
    freischalt_code_revocate = 2
    check_tax_number = 3
    send_est = 4
