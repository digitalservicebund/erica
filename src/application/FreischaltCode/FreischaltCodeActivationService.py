import datetime
from abc import abstractmethod, ABCMeta
from uuid import uuid4

from opyoid import Injector, Module
from rq import Retry

from src.application.EricRequestProcessing.erica_input.v1.erica_input import UnlockCodeActivationData
from src.application.EricRequestProcessing.requests_controller import UnlockCodeActivationRequestController
from src.application.EricaAuftrag.EricaAuftrag import EricaAuftragDto
from src.application.FreischaltCode.FreischaltCode import FreischaltCodeActivateDto
from src.application.FreischaltCode.Jobs.jobs import request_freischalt_code
from src.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from src.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from src.domain.FreischaltCode.FreischaltCode import FreischaltCodeActivatePayload
from src.domain.Shared.EricaAuftrag import AuftragType
from src.infrastructure.InfrastructureModule import InfrastructureModule
from src.infrastructure.rq.RqModule import RqModule
from src.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepository

injector = Injector([InfrastructureModule(), RqModule()])


class FreischaltCodeActivationServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def freischalt_code_bei_elster_aktivieren_queued(self,
                                                     freischaltcode_dto: FreischaltCodeActivateDto) -> EricaAuftragDto:
        pass

    @abstractmethod
    def freischalt_code_bei_elster_aktivieren(self, freischaltcode_dto: FreischaltCodeActivateDto,
                                              include_elster_responses: bool):
        pass


class FreischaltCodeActivationService(FreischaltCodeActivationServiceInterface):
    freischaltcode_repository: EricaAuftragRepository

    def __init__(self, repository: EricaAuftragRepository = injector.inject(EricaAuftragRepository)) -> None:
        super().__init__()
        self.freischaltcode_repository = repository

    async def freischalt_code_bei_elster_aktivieren_queued(self, freischaltcode_dto: FreischaltCodeActivateDto) -> EricaAuftragDto:
        job_id = uuid4()
        freischaltcode = EricaAuftrag(job_id=job_id,
                                      payload=FreischaltCodeActivatePayload.parse_obj(freischaltcode_dto),
                                      created_at=datetime.datetime.now().__str__(),
                                      updated_at=datetime.datetime.now().__str__(),
                                      creator_id="api",
                                      type=AuftragType.freischalt_code_activate
                                      )

        created = self.freischaltcode_repository.create(freischaltcode)
        background_worker = injector.inject(BackgroundJobInterface)

        background_worker.enqueue(request_freischalt_code,
                                  created.id,
                                  retry=Retry(max=3, interval=1),
                                  job_id=job_id.__str__()
                                  )

        return EricaAuftragDto.parse_obj(created)

    async def freischalt_code_bei_elster_aktivieren(self, freischaltcode_dto: FreischaltCodeActivateDto,
                                                    include_elster_responses: bool = False):
        request = UnlockCodeActivationRequestController(UnlockCodeActivationData.parse_obj(
            {"idnr": freischaltcode_dto.tax_ident, "unlock_code": freischaltcode_dto.freischalt_code,
             "elster_request_id": freischaltcode_dto.elster_request_id}),
            include_elster_responses)
        return request.process()


class FreischaltCodeActivationServiceModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeActivationServiceInterface, to_class=FreischaltCodeActivationService)
