from enum import Enum


class AuftragType(int, Enum):
    freischalt_code_beantragen = 0
    freischalt_code_activate = 1
    freischalt_code_revocate = 2
