import datetime
from abc import abstractmethod, ABCMeta
from uuid import UUID, uuid4

from opyoid import Injector, Module
from rq import Retry

from src.application.EricRequestProcessing.erica_input.v1.erica_input import UnlockCodeRequestData
from src.application.EricRequestProcessing.requests_controller import UnlockCodeRequestController
from src.application.FreischaltCode.FreischaltCode import FreischaltCodeCreateDto, FreischaltCodeDto
from src.application.FreischaltCode.Jobs.jobs import request_freischalt_code
from src.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from src.domain.FreischaltCode.FreischaltCode import FreischaltCode
from src.infrastructure.InfrastructureModule import InfrastructureModule
from src.infrastructure.rq.RqModule import RqModule
from src.infrastructure.sqlalchemy.repositories.FreischaltCodeRepository import FreischaltCodeRepository

injector = Injector([InfrastructureModule(), RqModule()])


class FreischaltCodeServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_queued_to_elster(self, freischaltcode_dto: FreischaltCodeCreateDto) -> FreischaltCodeDto:
        pass

    @abstractmethod
    def send_to_elster(self, freischaltcode_dto: FreischaltCodeCreateDto, include_elster_responses: bool):
        pass

    @abstractmethod
    def get_status(self, tax_ident: UUID):
        pass


class FreischaltCodeService(FreischaltCodeServiceInterface):
    freischaltcode_repository: FreischaltCodeRepository

    def __init__(self, repository: FreischaltCodeRepository = injector.inject(FreischaltCodeRepository)) -> None:
        super().__init__()
        self.freischaltcode_repository = repository

    async def send_queued_to_elster(self, freischaltcode_dto: FreischaltCodeCreateDto) -> FreischaltCodeDto:
        job_id = uuid4()
        freischaltcode = FreischaltCode(tax_ident=freischaltcode_dto.tax_ident,
                                        job_id=job_id,
                                        date_of_birth=freischaltcode_dto.date_of_birth,
                                        created_at=datetime.datetime.now().__str__(),
                                        updated_at=datetime.datetime.now().__str__(),
                                        creator_id="api"
                                        )

        created = self.freischaltcode_repository.create(freischaltcode)
        background_worker = injector.inject(BackgroundJobInterface)

        background_worker.enqueue(request_freischalt_code,
                                  created.id,
                                  retry=Retry(max=3, interval=1),
                                  job_id=job_id.__str__()
                                  )

        return FreischaltCodeDto.parse_obj(created)

    async def send_to_elster(self, freischaltcode_dto: FreischaltCodeCreateDto, include_elster_responses: bool = False):
        request = UnlockCodeRequestController(UnlockCodeRequestData.parse_obj(
            {"idnr": freischaltcode_dto.tax_ident, "dob": freischaltcode_dto.date_of_birth}), include_elster_responses)
        return request.process()

    def get_status(self, tax_ident: UUID):
        return self.freischaltcode_repository.get_by_id(tax_ident)


class FreischaltCodeServiceModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeServiceInterface, to_class=FreischaltCodeService)
