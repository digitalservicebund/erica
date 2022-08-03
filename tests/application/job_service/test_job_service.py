from datetime import datetime
from unittest.mock import Mock, MagicMock, call
from uuid import UUID

import pytest
from freezegun import freeze_time
from sqlalchemy.orm import Session

from erica.application.job_service.job_service import JobService
from erica.domain.shared.base_domain_model import BasePayload
from erica.domain.shared.erica_request import RequestType
from erica.domain.erica_request.erica_request import EricaRequest
from erica.erica_legacy.request_processing.requests_controller import CheckTaxNumberRequestController
from erica.erica_shared.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository


class MockEricaRequestRepository(EricaRequestRepository, list):

    def __init__(self, db_connection: Session = None):
        self.DatabaseEntity = None
        self.DomainModel = None

    def create(self, model):
        self.append(model)
        model.id = "1234"
        return model

    def get(self, skip: int = 0, limit: int = 100):
        return self

    def get_by_id(self, request_id):
        return [entity for entity in self if entity.id == request_id][0]

    def update(self, model_id, model):
        for entity, index in enumerate(self):
            if entity.id == model_id:
                self[index] = model
        return model

    def delete(self, request_id):
        for entity, index in enumerate(self):
            if entity.id == request_id:
                self.pop(index)


class MockRequestController(CheckTaxNumberRequestController):
    call_list = []

    @classmethod
    def process(cls, *args, **kwargs):
        cls.call_list.append({'args': [*args], 'kwargs': {**kwargs}})


class PickableMock(Mock):

    def __reduce__(self):
        return Mock, ()


class MockDto(BasePayload):
    name: str
    friend: str




class TestJobServiceQueue:

    @freeze_time("2001-01-03 08:22:00")
    @pytest.mark.freeze_uuids
    def test_if_input_data_provided_then_add_request_to_repository(self):
        mock_job = PickableMock()
        service = JobService(job_repository=MockEricaRequestRepository(),
                             request_controller=MockRequestController, payload_type=MockDto, job_method=mock_job)
        input_data = MockDto.parse_obj({'name': 'Batman', 'friend': 'Joker'})

        service.add_to_queue(input_data, "steuerlotse", job_type=RequestType.freischalt_code_activate)

        assert service.repository[0] == EricaRequest(
            id="1234",
            request_id="00000000-0000-0000-0000-000000000000",
            payload=input_data,
            created_at=None,
            updated_at=None,
            creator_id="steuerlotse",
            type=RequestType.freischalt_code_activate
        )

    @pytest.mark.freeze_uuids
    def test_if_input_data_provided_then_call_job_method_with_correct_params(self):
        mock_job = PickableMock()
        service = JobService(job_repository=MockEricaRequestRepository(),
                             request_controller=MockRequestController, payload_type=MockDto, job_method=mock_job)
        input_data = MockDto.parse_obj({'name': 'Batman', 'friend': 'Joker'})

        service.add_to_queue(input_data, "steuerlotse", job_type=RequestType.freischalt_code_activate)

        mock_call = mock_job.mock_calls[0]
        assert mock_call.args[0] == UUID('00000000-0000-0000-0000-000000000000')


class TestJobServiceRun:

    def test_if_input_data_provided_then_call_init_of_request_controller_with_correct_data(self):
        controller_instance = MagicMock()
        mock_request_controller = MagicMock(return_value=controller_instance)
        service = JobService(job_repository=MockEricaRequestRepository(),
                             request_controller=mock_request_controller, payload_type=MockDto, job_method=MagicMock())
        input_data = MockDto.parse_obj({'name': 'Batman', 'friend': 'Joker'})

        service.apply_to_elster(input_data)

        assert mock_request_controller.mock_calls == [call(input_data, False)]

    def test_if_input_data_provided_then_call_process_with_input_data(self):
        controller_instance = MagicMock()
        mock_request_controller = MagicMock(return_value=controller_instance)
        service = JobService(job_repository=MockEricaRequestRepository(),
                             request_controller=mock_request_controller, payload_type=MockDto, job_method=MagicMock())
        input_data = MockDto.parse_obj({'name': 'Batman', 'friend': 'Joker'})
        request_entity = EricaRequest(
            id="1234",
            request_id="00000000-0000-0000-0000-000000000000",
            payload=input_data,
            created_at=datetime.now().__str__(),
            updated_at=datetime.now().__str__(),
            creator_id="api",
            type=RequestType.freischalt_code_activate
        )

        service.apply_to_elster(request_entity)

        assert controller_instance.process.call_count == 1
