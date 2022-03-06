from opyoid import Module

from src.infrastructure.sqlalchemy.database import DatabaseSessionProvider, DbSession


class InfrastructureModule(Module):
    def configure(self) -> None:
        self.bind(DbSession, to_provider=DatabaseSessionProvider)
