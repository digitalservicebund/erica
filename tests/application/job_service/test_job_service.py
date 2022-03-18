from datetime import datetime
from unittest.mock import Mock, MagicMock, call, patch

import pytest
from freezegun import freeze_time
from sqlalchemy.orm import Session

from erica.application.FreischaltCode.FreischaltCode import BaseDto
from erica.application.JobService.job_service import JobService
from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from erica.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from erica.domain.Shared.EricaAuftrag import AuftragType
from erica.erica_legacy.request_processing.requests_controller import CheckTaxNumberRequestController
from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepository


class MockEricaRequestRepository(EricaAuftragRepository, list):

    def __init__(self, db_connection: Session = None):
        self.DatabaseEntity = None
        self.DomainModel = None

    def create(self, model):
        self.append(model)
        model.id = "1234"
        return model

    def get(self, skip: int = 0, limit: int = 100):
        return self

    def get_by_id(self, entity_id):
        return [entity for entity in self if entity.id == entity_id][0]

    def update(self, model_id, model):
        for entity, index in enumerate(self):
            if entity.id == model_id:
                self[index] = model
        return model

    def delete(self, entity_id):
        for entity, index in enumerate(self):
            if entity.id == entity_id:
                self.pop(index)


class MockRequestController(CheckTaxNumberRequestController):
    call_list = []

    @classmethod
    def process(cls, *args, **kwargs):
        cls.call_list.append({'args': [*args], 'kwargs': {**kwargs}})


class PickableMock(Mock):

    def __reduce__(self):
        return Mock, ()


class MockDto(BaseDto):
    name: str
    friend: str


class MockBackgroundJob(BackgroundJobInterface, MagicMock):
    pass


class TestJobServiceQueue:

    @freeze_time("2001-01-03 08:22:00")
    @pytest.mark.freeze_uuids
    def test_if_input_data_provided_then_add_request_to_repository(self):
        mock_job = PickableMock()
        service = JobService(job_repository=MockEricaRequestRepository(), background_worker=MagicMock(),
                             request_controller=MockRequestController, payload_type=MockDto, job_method=mock_job)
        input_data = MockDto.parse_obj({'name': 'Batman', 'friend': 'Joker'})

        service.apply_queued_to_elster(input_data, job_type=AuftragType.freischalt_code_activate)

        assert service.repository[0] == EricaAuftrag(
            id="1234",
            job_id="00000000-0000-0000-0000-000000000000",
            payload=input_data,
            created_at=datetime.now().__str__(),
            updated_at=datetime.now().__str__(),
            creator_id="api",
            type=AuftragType.freischalt_code_activate
        )

    @pytest.mark.freeze_uuids
    def test_if_input_data_provided_then_add_job_to_background_job_worker_with_correct_params(self):
        mock_job = PickableMock()
        mock_bg_worker = MagicMock()
        mock_retry = MagicMock(return_value="retry")
        service = JobService(job_repository=MockEricaRequestRepository(), background_worker=mock_bg_worker,
                             request_controller=MockRequestController, payload_type=MockDto, job_method=mock_job)
        input_data = MockDto.parse_obj({'name': 'Batman', 'friend': 'Joker'})

        with patch('erica.application.JobService.job_service.Retry', mock_retry):
            # TODO we have some dependency on the Retry object inside the service which should only be part of the infrastructure I think, so we should probably remove that
            service.apply_queued_to_elster(input_data, job_type=AuftragType.freischalt_code_activate)

        assert mock_bg_worker.enqueue.mock_calls == [
            call("1234", f=mock_job, job_id="00000000-0000-0000-0000-000000000000", retry="retry")]


class TestJobServiceRun:

    def test_if_input_data_provided_then_call_init_of_request_controller_with_correct_data(self):
        mock_bg_worker = MagicMock()
        controller_instance = MagicMock()
        mock_request_controller = MagicMock(return_value=controller_instance)
        service = JobService(job_repository=MockEricaRequestRepository(), background_worker=mock_bg_worker,
                             request_controller=mock_request_controller, payload_type=MockDto, job_method=MagicMock())
        input_data = MockDto.parse_obj({'name': 'Batman', 'friend': 'Joker'})
        request_entity = EricaAuftrag(
            id="1234",
            job_id="00000000-0000-0000-0000-000000000000",
            payload=input_data,
            created_at=datetime.now().__str__(),
            updated_at=datetime.now().__str__(),
            creator_id="api",
            type=AuftragType.freischalt_code_activate
        )

        service.apply_to_elster(request_entity)

        assert mock_request_controller.mock_calls == [call(input_data, False)]

    def test_if_input_data_provided_then_call_process_with_input_data(self):
        mock_bg_worker = MagicMock()
        controller_instance = MagicMock()
        mock_request_controller = MagicMock(return_value=controller_instance)
        service = JobService(job_repository=MockEricaRequestRepository(), background_worker=mock_bg_worker,
                             request_controller=mock_request_controller, payload_type=MockDto, job_method=MagicMock())
        input_data = MockDto.parse_obj({'name': 'Batman', 'friend': 'Joker'})
        request_entity = EricaAuftrag(
            id="1234",
            job_id="00000000-0000-0000-0000-000000000000",
            payload=input_data,
            created_at=datetime.now().__str__(),
            updated_at=datetime.now().__str__(),
            creator_id="api",
            type=AuftragType.freischalt_code_activate
        )

        service.apply_to_elster(request_entity)

        assert controller_instance.process.call_count == 1
