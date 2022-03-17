import datetime
from abc import abstractmethod, ABCMeta
from uuid import uuid4

from rq import Retry

from erica.application.EricRequestProcessing.erica_input.v1.erica_input import UnlockCodeActivationData
from erica.application.EricRequestProcessing.requests_controller import UnlockCodeActivationRequestController
from erica.application.EricaAuftrag.EricaAuftrag import EricaAuftragDto
from erica.application.FreischaltCode.FreischaltCode import FreischaltCodeActivateDto
from erica.application.FreischaltCode.Jobs.jobs import activate_freischalt_code
from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from erica.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeActivatePayload
from erica.domain.Shared.EricaAuftrag import AuftragType
from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepository


class FreischaltCodeActivationServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def queue(self, freischaltcode_dto: FreischaltCodeActivateDto) -> EricaAuftragDto:
        pass

    @abstractmethod
    async def activate(self, freischaltcode_dto: FreischaltCodeActivateDto, include_elster_responses: bool):
        pass


class FreischaltCodeActivationService(FreischaltCodeActivationServiceInterface):
    freischaltcode_repository: EricaAuftragRepository
    background_worker: BackgroundJobInterface

    def __init__(self, freischaltcode_repository : EricaAuftragRepository, background_worker : BackgroundJobInterface) -> None:
        super().__init__()
        self.freischaltcode_repository = freischaltcode_repository
        self.background_worker = background_worker

    async def queue(self, freischaltcode_dto: FreischaltCodeActivateDto) -> EricaAuftragDto:
        job_id = uuid4()
        freischaltcode = EricaAuftrag(job_id=job_id,
                                      payload=FreischaltCodeActivatePayload.parse_obj(freischaltcode_dto),
                                      created_at=datetime.datetime.now(),
                                      updated_at=datetime.datetime.now(),
                                      creator_id="api",
                                      type=AuftragType.freischalt_code_activate
                                      )

        created = self.freischaltcode_repository.create(freischaltcode)

        self.background_worker.enqueue(activate_freischalt_code,
                                  created.id,
                                  retry=Retry(max=3, interval=1),
                                  job_id=job_id.__str__()
                                  )

        return EricaAuftragDto.parse_obj(created)

    async def activate(self, freischaltcode_dto: FreischaltCodeActivateDto,
                                                    include_elster_responses: bool = False):
        request = UnlockCodeActivationRequestController(UnlockCodeActivationData.parse_obj(
            {"idnr": freischaltcode_dto.tax_ident, "unlock_code": freischaltcode_dto.freischalt_code,
             "elster_request_id": freischaltcode_dto.elster_request_id}),
            include_elster_responses)
        return request.process()
