from abc import ABC

from src.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from src.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface


class EricaAuftragRepositoryInterface(BaseRepositoryInterface[EricaAuftrag], ABC):
    pass
