import datetime
from abc import abstractmethod, ABCMeta
from uuid import uuid4
from typing import Type

from rq import Retry

from erica.application.EricRequestProcessing.erica_input.v1.erica_input import UnlockCodeActivationData
from erica.application.EricRequestProcessing.requests_controller import EricaRequestController
from erica.application.EricaAuftrag.EricaAuftrag import EricaAuftragDto
from erica.application.FreischaltCode.FreischaltCode import BaseDto, FreischaltCodeActivateDto
from erica.application.FreischaltCode.Jobs.jobs import activate_freischalt_code
from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from erica.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeActivatePayload
from erica.domain.Shared.EricaAuftrag import AuftragType
from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepositoryInterface

class JobServiceInterface():
    __metaclass__ = ABCMeta

    @abstractmethod
    async def queue(self, payload_dto: BaseDto, job_type: AuftragType, job_method) -> EricaAuftragDto:
        pass

    @abstractmethod
    async def run(self, request_entity: EricaAuftrag, include_elster_responses: bool):
        pass

class JobService(JobServiceInterface):

    def __init__(self,
                 job_repository : EricaAuftragRepositoryInterface,
                 background_worker : BackgroundJobInterface,
                 payload_type: BaseDto,
                 request_controller: Type[EricaRequestController]) -> None:
        super().__init__()

        self.repository = job_repository
        self.background_worker = background_worker
        self.payload_type = payload_type
        self.request_controller = request_controller

    def queue(self, payload_dto: BaseDto, job_type: AuftragType, job_method) -> EricaAuftragDto:
        request_entity = EricaAuftrag(job_id=uuid4(),
                                      payload=self.payload_type.parse_obj(payload_dto),
                                      created_at=datetime.datetime.now(),
                                      updated_at=datetime.datetime.now(),
                                      creator_id="api",
                                      type=job_type
                                      )

        created = self.repository.create(request_entity)

        self.background_worker.enqueue(
            created.id,
            f=job_method,
            retry=Retry(max=3, interval=1),
            job_id=request_entity.job_id.__str__()
        )

        return EricaAuftragDto.parse_obj(created)

    def run(self, request_entity: EricaAuftrag, include_elster_responses: bool = False):
        controller = self.request_controller(request_entity.payload, include_elster_responses) # TODO check if we can directly inject the class
        return controller.process()
