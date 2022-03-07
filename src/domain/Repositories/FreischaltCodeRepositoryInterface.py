from abc import ABC

from src.domain.FreischaltCode.FreischaltCode import FreischaltCode
from src.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface


class FreischaltCodeRepositoryInterface(BaseRepositoryInterface[FreischaltCode], ABC):
    pass
