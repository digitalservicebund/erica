from abc import ABC

from erica.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from erica.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface


class EricaAuftragRepositoryInterface(BaseRepositoryInterface[EricaAuftrag], ABC):
    pass
