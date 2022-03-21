import datetime
from abc import abstractmethod, ABCMeta
from typing import Type, Callable
from uuid import uuid4

from rq import Retry

from erica.application.EricRequestProcessing.requests_controller import EricaRequestController
from erica.application.EricaAuftrag.EricaAuftrag import EricaAuftragDto
from erica.application.FreischaltCode.FreischaltCode import BaseDto
from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from erica.domain.Repositories.EricaRequestRepositoryInterface import EricaRequestRepositoryInterface
from erica.domain.Shared.EricaAuftrag import RequestType

from erica.domain.erica_request.erica_request import EricaRequest


class JobServiceInterface():
    __metaclass__ = ABCMeta
    payload_type: Type[BaseDto]
    repository: EricaRequestRepositoryInterface

    @abstractmethod
    def add_to_queue(self, payload_dto: BaseDto, job_type: RequestType) -> EricaAuftragDto:
        pass

    @abstractmethod
    def apply_to_elster(self, request_entity: EricaRequest, include_elster_responses: bool):
        pass


class JobService(JobServiceInterface):

    def __init__(self,
                 job_repository: EricaRequestRepositoryInterface,
                 background_worker: BackgroundJobInterface,
                 payload_type: Type[BaseDto],
                 request_controller: Type[EricaRequestController],
                 job_method: Callable) -> None:
        super().__init__()

        self.repository = job_repository
        self.background_worker = background_worker
        self.payload_type = payload_type
        self.request_controller = request_controller
        self.job_method = job_method

    def add_to_queue(self, payload_dto: BaseDto, job_type: RequestType) -> EricaAuftragDto:
        request_entity = EricaRequest(job_id=uuid4(),
                                      payload=self.payload_type.parse_obj(payload_dto),
                                      created_at=datetime.datetime.now(),
                                      updated_at=datetime.datetime.now(),
                                      creator_id="api",
                                      type=job_type
                                      )

        created = self.repository.create(request_entity)

        self.background_worker.enqueue(
            created.id,
            f=self.job_method,
            retry=Retry(max=3, interval=1),
            job_id=request_entity.job_id.__str__(),
        )

        return EricaAuftragDto.parse_obj(created)

    async def apply_to_elster(self, payload_data, include_elster_responses: bool = False):
        controller = self.request_controller(payload_data, include_elster_responses) # TODO check if we can directly inject the class
        return controller.process()
