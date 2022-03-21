from abc import ABC

from erica.domain.erica_request.erica_request import EricaRequest
from erica.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface


class EricaRequestRepositoryInterface(BaseRepositoryInterface[EricaRequest], ABC):
    pass
