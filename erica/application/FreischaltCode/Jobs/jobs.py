import logging

from opyoid import Injector

from lib.pyeric.eric_errors import EricProcessNotSuccessful

from erica.domain.Shared.Status import Status


async def request_freischalt_code(entity_id):
    from erica.api.ApiModule import ApiModule
    from erica.application.FreischaltCode.FreischaltCodeRequestService import FreischaltCodeRequestServiceInterface
    from erica.domain.Repositories.EricaAuftragRepositoryInterface import EricaAuftragRepositoryInterface
    from erica.application.FreischaltCode.FreischaltCode import FreischaltCodeRequestDto

    injector = Injector([ApiModule()])
    repository = injector.inject(EricaAuftragRepositoryInterface)
    service = injector.inject(FreischaltCodeRequestServiceInterface)
    entity = repository.get_by_id(entity_id)
    request = FreischaltCodeRequestDto.parse_obj(entity.payload)

    logging.getLogger().info("Try to request unlock code. For Entity Id " + entity.id.__str__(), exc_info=True)
    
    try:
        response = await service.request(request, True)
        entity.elster_request_id = response.__str__
        entity.status = Status.success
        repository.update(entity.id, entity)
    except EricProcessNotSuccessful as e:
        logging.getLogger().warn(
            "Could not request unlock code. Got Error Message: " + e.generate_error_response(True).__str__(),
            exc_info=True
        )
        raise

    logging.getLogger().info("Unlock code Request Success. For Entity Id " + entity.id.__str__(), exc_info=True)

async def activate_freischalt_code(entity_id):
    from erica.api.ApiModule import ApiModule
    from erica.application.FreischaltCode.FreischaltCodeActivationService import FreischaltCodeActivationServiceInterface
    from erica.domain.Repositories.EricaAuftragRepositoryInterface import EricaAuftragRepositoryInterface
    from erica.application.FreischaltCode.FreischaltCode import FreischaltCodeActivateDto

    injector = Injector([ApiModule()])
    repository = injector.inject(EricaAuftragRepositoryInterface)
    service = injector.inject(FreischaltCodeActivationServiceInterface)
    entity = repository.get_by_id(entity_id)
    request = FreischaltCodeActivateDto.parse_obj(entity.payload)

    logging.getLogger().info("Try to activcate unlock code. For Entity Id " + entity.id.__str__(), exc_info=True)
    
    try:
        response = await service.request(request, True)
        entity.elster_request_id = response.__str__
        entity.status = Status.success
        repository.update(entity.id, entity)
    except EricProcessNotSuccessful as e:
        logging.getLogger().warn(
            "Could not activate unlock code. Got Error Message: " + e.generate_error_response(True).__str__(),
            exc_info=True
        )
        raise

    logging.getLogger().info("Unlock code activation success. For entity id " + entity.id.__str__(), exc_info=True)