from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from unittest.mock import Mock, MagicMock, call

from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from erica.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from erica.domain.Shared.EricaAuftrag import AuftragType
from erica.erica_legacy.request_processing.requests_controller import CheckTaxNumberRequestController
from erica.application.JobService.job_service import JobService
from erica.infrastructure.sqlalchemy.repositories import EricaAuftragRepository
from erica.domain.Shared.EricaAuftrag import AuftragType


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
        return [entity for entity in self if entity.id == entity_id ][0]

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


class MockBackgroundJob(BackgroundJobInterface, list):

    def enqueue(self, f, *args, **kwargs):
        self.append({'f': f, 'args': [*args], 'kwargs': {**kwargs}})

    def scheduled_enqueue(self):
        pass

    def get_enqueued_job_by_id(self, job_id):
        pass

    def list_all_jobs(self):
        return self

class PickableMock(Mock):

     def __reduce__(self):
         return Mock, ()

class MockDto(BaseDto):
    value: str

class TestTaxNumberValidationServiceCheckTaxNumberEnqueued:

    def test_if_input_data_provided_then_add_request_to_repository(self):
        mock_job = PickableMock()
        service = JobService(job_repository= MockEricaRequestRepository(), background_worker=MockBackgroundJob, request_controller=MockRequestController, payload_type=MockDto, job_method=mock_job)
        input_data = MockDto.parse_obj({'value': 'Lord of the Rings'})
        
        service.queue(input_data, job_type=AuftragType.freischalt_code_activate, job_method=mock_job)

        assert service.repository[0] == EricaAuftrag(
            job_id="00000000-0000-0000-0000-000000000000",
            payload=input_data,
            created_at=datetime.now().__str__(),
            creator_id="api",
            type=AuftragType.check_tax_number
        )
