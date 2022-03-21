import datetime
from abc import abstractmethod, ABCMeta
from uuid import uuid4

from opyoid import Injector, Module
from rq import Retry

from erica.application.EricRequestProcessing.erica_input.v1.erica_input import UnlockCodeRequestData
from erica.application.EricRequestProcessing.requests_controller import UnlockCodeRequestController
from erica.application.EricaAuftrag.EricaAuftrag import EricaAuftragDto
from erica.application.FreischaltCode.FreischaltCode import FreischaltCodeBeantragenDto
from erica.application.FreischaltCode.Jobs.jobs import request_freischalt_code
from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from erica.domain.erica_request.erica_request import EricaRequest
from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeBeantragenPayload
from erica.domain.Shared.EricaAuftrag import AuftragType
from erica.infrastructure.infrastructure_module import InfrastructureModule
from erica.infrastructure.rq.RqModule import RqModule
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository

injector = Injector([InfrastructureModule(), RqModule()])


class FreischaltCodeServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def freischalt_code_bei_elster_beantragen_queued(self,
                                                     freischaltcode_dto: FreischaltCodeBeantragenDto) -> EricaAuftragDto:
        pass

    @abstractmethod
    def freischalt_code_bei_elster_beantragen(self, freischaltcode_dto: FreischaltCodeBeantragenDto,
                                              include_elster_responses: bool):
        pass


class FreischaltCodeService(FreischaltCodeServiceInterface):
    freischaltcode_repository: EricaRequestRepository

    def __init__(self, repository: EricaRequestRepository = injector.inject(EricaRequestRepository)) -> None:
        super().__init__()
        self.freischaltcode_repository = repository

    async def freischalt_code_bei_elster_beantragen_queued(self,
                                                           freischaltcode_dto: FreischaltCodeBeantragenDto) -> EricaAuftragDto:
        job_id = uuid4()
        freischaltcode = EricaRequest(job_id=job_id,
                                      payload=FreischaltCodeBeantragenPayload.parse_obj(freischaltcode_dto),
                                      created_at=datetime.datetime.now().__str__(),
                                      updated_at=datetime.datetime.now().__str__(),
                                      creator_id="api",
                                      type=AuftragType.freischalt_code_beantragen
                                      )

        created = self.freischaltcode_repository.create(freischaltcode)
        background_worker = injector.inject(BackgroundJobInterface)

        background_worker.enqueue(request_freischalt_code,
                                  created.id,
                                  retry=Retry(max=3, interval=1),
                                  job_id=job_id.__str__()
                                  )

        return EricaAuftragDto.parse_obj(created)

    async def freischalt_code_bei_elster_beantragen(self, freischaltcode_dto: FreischaltCodeBeantragenDto,
                                                    include_elster_responses: bool = False):
        request = UnlockCodeRequestController(UnlockCodeRequestData.parse_obj(
            {"idnr": freischaltcode_dto.tax_ident, "dob": freischaltcode_dto.date_of_birth}), include_elster_responses)
        return request.process()


class FreischaltCodeServiceModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeServiceInterface, to_class=FreischaltCodeService)
