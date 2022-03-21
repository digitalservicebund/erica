import datetime
from abc import abstractmethod, ABCMeta
from uuid import uuid4

from rq import Retry

from erica.application.EricRequestProcessing.erica_input.v1.erica_input import UnlockCodeRequestData
from erica.application.EricRequestProcessing.requests_controller import UnlockCodeRequestController
from erica.application.EricaAuftrag.EricaAuftrag import EricaAuftragDto
from erica.application.FreischaltCode.FreischaltCode import FreischaltCodeRequestDto
from erica.application.FreischaltCode.Jobs.jobs import request_freischalt_code
from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from erica.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeRequestPayload
from erica.domain.Shared.EricaAuftrag import RequestType
from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepository


class FreischaltCodeRequestServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def queue(self, reischaltcode_dto: FreischaltCodeRequestDto) -> EricaAuftragDto:
        pass

    @abstractmethod
    async def request(self, freischaltcode_dto: FreischaltCodeRequestDto, include_elster_responses: bool):
        pass


class FreischaltCodeRequestService(FreischaltCodeRequestServiceInterface):
    freischaltcode_repository: EricaAuftragRepository
    background_worker: BackgroundJobInterface

    def __init__(self, freischaltcode_repository: EricaAuftragRepository, background_worker: BackgroundJobInterface) -> None:
        super().__init__()
        self.freischaltcode_repository = freischaltcode_repository
        self.background_worker = background_worker

    async def queue(self, freischaltcode_dto: FreischaltCodeRequestDto) -> EricaAuftragDto:
        job_id = uuid4()
        freischaltcode = EricaAuftrag(job_id=job_id,
                                      payload=FreischaltCodeRequestPayload.parse_obj(freischaltcode_dto),
                                      created_at=datetime.datetime.now(),
                                      updated_at=datetime.datetime.now(),
                                      creator_id="api",
                                      type=RequestType.freischalt_code_request
                                      )

        created = self.freischaltcode_repository.create(freischaltcode)

        self.background_worker.enqueue(request_freischalt_code,
                                  created.id,
                                  retry=Retry(max=3, interval=1),
                                  job_id=job_id.__str__()
                                  )

        return EricaAuftragDto.parse_obj(created)

    async def request(self, freischaltcode_dto: FreischaltCodeRequestDto,
                                                    include_elster_responses: bool = False):
        request = UnlockCodeRequestController(UnlockCodeRequestData.parse_obj(
            {"idnr": freischaltcode_dto.idnr, "dob": freischaltcode_dto.date_of_birth}), include_elster_responses)
        return request.process()

