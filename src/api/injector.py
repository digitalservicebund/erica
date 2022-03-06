from opyoid import Module, Injector

from src.application.FreischaltCode.FreischaltCodeApplicationModule import FreischaltCodeApplicationModule
from src.infrastructure.sqlalchemy.repositories.RepositoriesModule import RepositoriesModule

injector = Injector([
    RepositoriesModule(),
    FreischaltCodeApplicationModule()
])
