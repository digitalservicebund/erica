import unittest
from ctypes import c_int
from unittest.mock import patch, MagicMock, mock_open

import pytest

from erica.erica_legacy.config import get_settings
from tests.erica_legacy.utils import gen_random_key, missing_cert, missing_pyeric_lib
from erica.erica_legacy.pyeric.eric import EricWrapper, EricDruckParameterT, EricVerschluesselungsParameterT, EricResponse, \
    get_eric_wrapper
from erica.erica_legacy.pyeric.eric_errors import EricProcessNotSuccessful, EricNullReturnedError, EricGlobalError

TEST_CERTIFICATE_PATH = 'erica/erica_legacy/instances/blueprint/cert.pfx'


@pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGetEricWrapper(unittest.TestCase):
    def test_calls_initialise(self):
        with patch('erica.erica_legacy.pyeric.eric.EricWrapper.initialise') as init_fun, \
                patch('erica.erica_legacy.pyeric.eric.EricWrapper.shutdown'), \
                patch('builtins.open', mock_open()):
            with get_eric_wrapper():
                # Test the context manager
                pass

            init_fun.assert_called_once()

    def test_calls_shutdown(self):
        with patch('erica.erica_legacy.pyeric.eric.EricWrapper.initialise'), \
             patch('erica.erica_legacy.pyeric.eric.EricWrapper.shutdown') as shutdown_fun, \
                patch('builtins.open', mock_open()):
            with get_eric_wrapper():
                # Test the context manager
                pass

            shutdown_fun.assert_called_once()

""" 

injector = Injector([InfrastructureModule(), RqModule()])


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

    def __init__(self, repository: EricaAuftragRepository = injector.inject(EricaAuftragRepository)) -> None:
        super().__init__()
        self.freischaltcode_repository = repository

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
        background_worker = injector.inject(BackgroundJobInterface)

        background_worker.enqueue(activate_freischalt_code,
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


"""