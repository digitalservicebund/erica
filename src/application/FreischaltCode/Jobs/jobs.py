import logging

from opyoid import Injector

from lib.pyeric.eric_errors import EricProcessNotSuccessful

from src.application.FreischaltCode.FreischaltCode import FreischaltCodeCreateDto
from src.domain.Repositories.FreischaltCodeRepositoryInterface import FreischaltCodeRepositoryInterface
from src.domain.Shared.status import Status


async def request_freischalt_code(entity_id):
    from src.api.ApiModule import ApiModule
    from src.application.FreischaltCode.FreischaltCodeService import FreischaltCodeServiceInterface

    injector = Injector([ApiModule()])
    repository = injector.inject(FreischaltCodeRepositoryInterface)
    service = injector.inject(FreischaltCodeServiceInterface)
    entity = repository.get_by_id(entity_id)
    request = FreischaltCodeCreateDto.parse_obj(entity)

    logging.getLogger().info("Try to request unlock code. For Entity Id " + entity.id.__str__(), exc_info=True)
    try:
        response = await service.send_to_elster(request, True)
        entity.elster_request_id = response.__str__
        entity.status = Status.success
        repository.update(entity.id, entity)
    except EricProcessNotSuccessful as e:
        logging.getLogger().info(
            "Could not request unlock code. Got Error Message: " + e.generate_error_response(True).__str__(),
            exc_info=True
        )
        raise

    logging.getLogger().info("Unlock code Request Success. For Entity Id " + entity.id.__str__(), exc_info=True)

    return
