import datetime
from unittest.mock import MagicMock, call
from uuid import uuid4, UUID

import pytest
import pytest_pgsql
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from erica.domain.Shared.EricaAuftrag import RequestType
from erica.domain.Shared.Status import Status
from erica.domain.erica_request.erica_request import EricaRequest
from erica.infrastructure.sqlalchemy.database import get_engine, run_migrations
from erica.infrastructure.sqlalchemy.erica_request_schema import EricaRequestSchema
from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository
from tests.infrastructure.sqlalechemy.repositories.mock_repositories import MockDomainModel, MockSchema


class MockEricaRequestRepository(
    EricaRequestRepository
):
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.DatabaseEntity = MockSchema
        self.DomainModel = MockDomainModel



@pytest.fixture
def transactional_session(transacted_postgresql_db):
    transacted_postgresql_db.create_table(MockSchema)
    yield transacted_postgresql_db.session

@pytest.fixture
def transactional_erica_request_session():
    if not database_exists(get_engine().url):
        create_database(get_engine().url)
    run_migrations()
    session = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())()
    yield session

    tables = MockSchema.metadata.sorted_tables
    for table in tables:
        session.execute(table.delete())
    session.commit()


class TestEricaRepositoryCreate:

    @pytest_pgsql.freeze_time(datetime.datetime(2001, 1, 3, 8, 22, 0, tzinfo=datetime.timezone.utc))
    def test_if_create_object_then_set_timestamps_to_now(self, transacted_postgresql_db):
        transacted_postgresql_db.create_table(EricaRequestSchema)
        job_id = uuid4()
        mock_object = EricaRequest(job_id=job_id,
                                   payload={'endboss': 'Melkor'},
                                   creator_id="api",
                                   type=RequestType.freischalt_code_request,
                                   status=Status.new)

        EricaRequestRepository(db_connection=transacted_postgresql_db.session).create(mock_object)

        found_entity = transacted_postgresql_db.session.query(EricaRequestSchema).filter(EricaRequestSchema.job_id == job_id).first()

        assert found_entity.created_at.timestamp() == datetime.datetime.utcnow().timestamp()
        assert found_entity.updated_at.timestamp() == datetime.datetime.utcnow().timestamp()


class TestEricaRepositoryGetByJobId:

    def test_if_entity_in_database_then_return_domain_representation(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        job_id = uuid4()
        mock_object.job_id = job_id
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()

        found_entity = MockEricaRequestRepository(db_connection=transactional_session).get_by_job_id(job_id)

        assert found_entity == mock_object

    def test_if_entity_not_in_database_then_raise_exception(self, transactional_session):
        job_id = uuid4()

        with pytest.raises(EntityNotFoundError):
            MockEricaRequestRepository(db_connection=transactional_session).get_by_job_id(job_id)


class TestEricaRepositoryUpdateByJobId:

    def test_if_entity_in_database_then_return_updated_domain_representation(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        updated_entity = MockEricaRequestRepository(db_connection=transactional_session).update_by_job_id(schema_object.job_id, updated_object)

        assert updated_entity == updated_object

    def test_if_entity_in_database_then_update_in_database(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        MockEricaRequestRepository(db_connection=transactional_session).update_by_job_id(schema_object.job_id, updated_object)

        updated_entry_in_db = transactional_session.query(MockSchema).filter(MockSchema.job_id == schema_object.job_id).first()
        assert updated_entry_in_db.job_id == schema_object.job_id
        assert updated_entry_in_db.payload == {'endboss': 'Sauron'}

    def test_if_entity_not_in_database_then_raise_error(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        with pytest.raises(EntityNotFoundError):
            MockEricaRequestRepository(db_connection=transactional_session).update_by_job_id(schema_object.job_id, updated_object)

    def test_if_update_object_then_set_only_updated_at_timestamp(self, transactional_erica_request_session):
        job_id = uuid4()
        mock_object = EricaRequest(job_id=job_id,
                                   payload={'endboss': 'Melkor'},
                                   creator_id="api",
                                   type=RequestType.freischalt_code_request,
                                   status=Status.new)
        created_object = EricaRequestRepository(db_connection=transactional_erica_request_session).create(mock_object)
        found_entity_before_update = transactional_erica_request_session.query(EricaRequestSchema).filter(EricaRequestSchema.job_id == job_id).first()
        before_update_created_at_timestamp = found_entity_before_update.created_at
        before_update_updated_at_timestamp = found_entity_before_update.updated_at
        created_object.payload = {'endboss': 'Sauron'}

        EricaRequestRepository(db_connection=transactional_erica_request_session).update_by_job_id(job_id, created_object)

        found_entity = transactional_erica_request_session.query(EricaRequestSchema).filter(EricaRequestSchema.job_id == job_id).first()

        assert found_entity.created_at == before_update_created_at_timestamp
        assert found_entity.updated_at > before_update_updated_at_timestamp

    @pytest.mark.freeze_uuids
    def test_if_only_job_id_changed_then_only_call_update_with_changed_attributes(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()
        updated_object = MockDomainModel(job_id=uuid4(),
                                         payload={'endboss': 'Melkor'})

        # We need a mock object to be able to intercept the call to the update function
        repo = MockEricaRequestRepository(db_connection=transactional_session)
        update_mock = MagicMock()
        mocked_get_by_job_id = MagicMock(side_effect=lambda job_id: MagicMock(
            first=MagicMock(return_value=MockEricaRequestRepository(db_connection=transactional_session)._get_by_job_id(job_id).first()),
            update=update_mock))
        repo._get_by_job_id = mocked_get_by_job_id

        repo.update_by_job_id(mock_object.job_id, updated_object)

        assert update_mock.mock_calls == [call({'job_id': UUID('00000000-0000-0000-0000-000000000000')})]


class TestEricaRepositoryDeleteByJobId:

    def test_if_entity_in_database_then_delete_from_database(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()

        MockEricaRequestRepository(db_connection=transactional_session).delete_by_job_id(schema_object.job_id)

        not_found_entry = transactional_session.query(MockSchema).filter(MockSchema.job_id == schema_object.job_id).first()
        assert not_found_entry is None

    def test_if_entity_not_in_database_then_raise_error(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())

        with pytest.raises(EntityNotFoundError):
            MockEricaRequestRepository(db_connection=transactional_session).delete_by_job_id(schema_object.job_id)
