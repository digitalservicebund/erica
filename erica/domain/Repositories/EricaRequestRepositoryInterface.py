from abc import ABC

from erica.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from erica.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface


class EricaRequestRepositoryInterface(BaseRepositoryInterface[EricaAuftrag], ABC):
    pass
