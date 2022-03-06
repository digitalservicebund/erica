from opyoid import Injector
from pydantic import parse_obj_as

from src.domain.FreischaltCode.freischalt_code import FreischaltCode
from src.domain.Repositories.FreischaltCodeRepositoryInterface import FreischaltCodeRepositoryInterface
from src.domain.Shared.status import Status
from src.infrastructure.sqlalchemy.repositories.RepositoriesModule import RepositoriesModule

injector = Injector([RepositoriesModule()])


def send_freischalt_code(entity_id):
    repository = injector.inject(FreischaltCodeRepositoryInterface)
    entity = repository.get_by_id(entity_id)
    entity = parse_obj_as(FreischaltCode, entity )
    print(entity.__str__)
    setattr(entity, "status", Status.success)
    repository.update(entity.id, entity)
    print(entity_id)
    return
