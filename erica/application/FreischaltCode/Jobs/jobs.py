import logging

from opyoid import Injector

from erica.application.FreischaltCode.FreischaltCode import FscRequestDataDto

from erica.domain.Shared.Status import Status
from erica.erica_legacy.pyeric.eric_errors import EricProcessNotSuccessful


async def request_freischalt_code(entity_id):
    from erica.api.ApiModule import ApiModule
    from erica.application.FreischaltCode.FreischaltCodeService import FreischaltCodeServiceInterface
    from erica.domain.Repositories.EricaAuftragRepositoryInterface import EricaAuftragRepositoryInterface

    injector = Injector([ApiModule()])
    repository = injector.inject(EricaAuftragRepositoryInterface)
    service = injector.inject(FreischaltCodeServiceInterface)
    entity = repository.get_by_id(entity_id)
    request = FscRequestDataDto.parse_obj(entity.payload)

    logging.getLogger().info("Try to request unlock code. For Entity Id " + entity.id.__str__(), exc_info=True)
    try:
        response = await service.freischalt_code_bei_elster_beantragen(request, True)
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
