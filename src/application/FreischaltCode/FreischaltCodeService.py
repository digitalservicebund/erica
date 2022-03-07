import asyncio
import datetime
from abc import abstractmethod, ABCMeta
from uuid import UUID, uuid4

from opyoid import Injector, Module
from rq import Retry

from src.application.FreischaltCode.FreischaltCode import FreischaltCodeCreateDto, FreischaltCodeDto
from src.application.FreischaltCode.Jobs.jobs import send_freischalt_code
from src.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from src.domain.FreischaltCode.FreischaltCode import FreischaltCode
from src.infrastructure.rq.RqModule import RqModule
from src.infrastructure.sqlalchemy.repositories.RepositoriesModule import RepositoriesModule
from src.infrastructure.sqlalchemy.repositories.FreischaltCodeRepository import FreischaltCodeRepository

injector = Injector([RepositoriesModule(), RqModule()])


class FreischaltCodeServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_scheduled_to_elster(self, freischaltcode_dto: FreischaltCodeCreateDto) -> FreischaltCodeDto:
        pass

    @abstractmethod
    def send_to_elster(self, freischaltcode_dto: FreischaltCodeCreateDto):
        pass

    @abstractmethod
    def get_status(self, tax_ident: UUID):
        pass


class FreischaltCodeService(FreischaltCodeServiceInterface):
    freischaltcode_repository: FreischaltCodeRepository

    def __init__(self, repository: FreischaltCodeRepository = injector.inject(FreischaltCodeRepository)) -> None:
        super().__init__()
        self.freischaltcode_repository = repository

    async def send_scheduled_to_elster(self, freischaltcode_dto: FreischaltCodeCreateDto) -> FreischaltCodeDto:
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

        background_worker.enqueue(send_freischalt_code,
                                  created.id,
                                  retry=Retry(max=3, interval=60),
                                  job_id=job_id.__str__()
                                  )

        return FreischaltCodeDto.parse_obj(created)

    async def send_to_elster(self, freischaltcode_dto: FreischaltCodeCreateDto):
        await asyncio.sleep(1)
        pass

    def get_status(self, tax_ident: UUID):
        return self.freischaltcode_repository.get_by_id(tax_ident)


class ApplicationFreischaltCodeModule(Module):
    def configure(self) -> None:
        self.install(ApplicationFreischaltCodeModule())
        self.bind(FreischaltCodeService)
