import json
import uuid
from unittest.mock import MagicMock, Mock, patch

import pytest

from erica.api.v2.endpoints.fsc import request_fsc, get_request_fsc_job, activate_fsc, get_fsc_activation_job
from erica.api.v2.responses.model import JobState
from erica.application.EricaAuftrag.EricaAuftrag import EricaAuftragDto
from erica.application.JobService.job_service import JobService
from erica.domain.Shared.EricaAuftrag import RequestType
from erica.domain.Shared.Status import Status
from erica.domain.erica_request.erica_request import EricaRequest
from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError
from tests.application.job_service.test_job_service import MockEricaRequestRepository, MockRequestController, MockDto, \
    PickableMock
from tests.utils import create_unlock_code_request, \
    create_unlock_code_activation


@pytest.mark.asyncio
@pytest.mark.parametrize("method, data",
                         [(request_fsc, create_unlock_code_request()), (activate_fsc, create_unlock_code_activation())])
async def test_if_create_fsc_request_returns_location(method, data):
    request_id = uuid.uuid4()
    job_service = JobService(job_repository=MockEricaRequestRepository(), background_worker=MagicMock(),
                             request_controller=MockRequestController, payload_type=MockDto, job_method=PickableMock())
    job_service.add_to_queue = Mock(
        return_value=EricaAuftragDto(type=RequestType.freischalt_code_request, status=Status.new, payload="{}",
                                     job_id=request_id))
    with patch("erica.api.v2.endpoints.fsc.get_job_service", MagicMock(return_value=job_service)):
        response = await method(data)
        assert response == "request/" + str(request_id)


@pytest.mark.asyncio
@pytest.mark.parametrize("method", [get_request_fsc_job, get_fsc_activation_job])
async def test_if_get_fsc_request_job_returns_success_status(method):
    job_id = uuid.uuid4()
    idnr = "test_idnr"
    elster_request_id = "test_elster_request_id"
    transfer_ticket = "test_transfer_ticket"
    erica_request = EricaRequest(type=RequestType.freischalt_code_request, status=Status.success,
                                 payload={"idnr": idnr},
                                 result={"elster_request_id": elster_request_id,
                                         "transfer_ticket": transfer_ticket},
                                 job_id=job_id, creator_id="test")
    with patch("erica.api.v2.endpoints.fsc.get_erica_request", MagicMock()) as mock_get_request:
        mock_get_request.return_value = erica_request
        response = await method(job_id)
        assert response.processStatus == JobState.SUCCESS
        assert response.result.idnr == idnr
        assert response.result.elster_request_id == elster_request_id
        assert response.result.transfer_ticket == transfer_ticket
        assert response.errorCode is None
        assert response.errorMessage is None


@pytest.mark.asyncio
@pytest.mark.parametrize("method", [get_request_fsc_job, get_fsc_activation_job])
async def test_if_get_fsc_request_job_returns_failure_status(method):
    job_id = uuid.uuid4()
    error_code = "1"
    error_message = "wingardium leviosa"

    erica_request = EricaRequest(type=RequestType.freischalt_code_request, status=Status.failed,
                                 error_code=error_code,
                                 error_message=error_message,
                                 job_id=job_id, creator_id="test")
    with patch("erica.api.v2.endpoints.fsc.get_erica_request", MagicMock()) as mock_get_request:
        mock_get_request.return_value = erica_request
        response = await method(job_id)
        assert response.processStatus == JobState.FAILURE
        assert response.errorCode == error_code
        assert response.errorMessage == error_message
        assert response.result is None


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [Status.new, Status.scheduled, Status.processing])
@pytest.mark.parametrize("method", [get_request_fsc_job, get_fsc_activation_job])
async def test_if_get_fsc_request_job_returns_processing_status(status, method):
    job_id = uuid.uuid4()
    erica_request = EricaRequest(type=RequestType.freischalt_code_request, status=status,
                                 job_id=job_id, creator_id="test")
    with patch("erica.api.v2.endpoints.fsc.get_erica_request", MagicMock()) as mock_get_request:
        mock_get_request.return_value = erica_request
        response = await method(job_id)
        assert response.processStatus == JobState.PROCESSING
        assert response.result is None
        assert response.errorCode is None
        assert response.errorMessage is None


@pytest.mark.asyncio
@pytest.mark.parametrize("method", [get_request_fsc_job, get_fsc_activation_job])
async def test_if_get_fsc_request_job_returns_not_found(method):
    request_id = uuid.uuid4()
    with patch("erica.api.v2.endpoints.fsc.get_erica_request", MagicMock()) as mock_get_request:
        mock_get_request.side_effect = EntityNotFoundError
        response = await method(request_id)
        body = json.loads(response.body)
        assert body['errorCode'] == -1
        assert body['errorMessage'] == "Raised in case an entity could not be found in the database"
