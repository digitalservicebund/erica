import datetime
import uuid
from unittest.mock import MagicMock, call
from uuid import uuid4, UUID
import pytest
import pytest_pgsql
from erica.domain.shared.erica_request import RequestType
from erica.domain.shared.status import Status
from erica.domain.erica_request.erica_request import EricaRequest
from erica.erica_shared.sqlalchemy.erica_request_schema import EricaRequestSchema
from erica.erica_shared.sqlalchemy.repositories.base_repository import EntityNotFoundError
from erica.erica_shared.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository
from tests.erica_shared.sqlalechemy.repositories.mock_repositories import MockDomainModel, MockSchema


class MockEricaRequestRepository(
    EricaRequestRepository
):
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.DatabaseEntity = MockSchema
        self.DomainModel = MockDomainModel


@pytest.fixture
def transactional_erica_postgresql_db(postgresql_db):
    if not postgresql_db.has_table(EricaRequestSchema.__tablename__):
        postgresql_db.create_table(EricaRequestSchema)
    yield postgresql_db


@pytest.fixture
def transactional_erica_request_session(transactional_erica_postgresql_db):
    yield transactional_erica_postgresql_db.session


class TestEricaRepositoryCreate:

    @pytest_pgsql.freeze_time(datetime.datetime(2001, 1, 3, 8, 22, 0, tzinfo=datetime.timezone.utc))
    def test_if_create_object_then_set_timestamps_to_now(self, transactional_erica_postgresql_db):
        request_id = uuid4()
        mock_object = EricaRequest(request_id=request_id,
                                   payload={'endboss': 'Melkor'},
                                   creator_id="api",
                                   type=RequestType.freischalt_code_request,
                                   status=Status.new)

        EricaRequestRepository(db_connection=transactional_erica_postgresql_db.session).create(mock_object)

        found_entity = transactional_erica_postgresql_db.session.query(EricaRequestSchema).filter(EricaRequestSchema.request_id == request_id).first()

        assert found_entity.created_at.timestamp() == datetime.datetime.utcnow().timestamp()
        assert found_entity.updated_at.timestamp() == datetime.datetime.utcnow().timestamp()


class TestEricaRepositoryGetByJobId:

    def test_if_entity_in_database_then_return_domain_representation(self, transactional_session_with_mock_schema):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        request_id = uuid4()
        mock_object.request_id = request_id
        schema_object = MockSchema(**mock_object.dict())
        transactional_session_with_mock_schema.add(schema_object)
        transactional_session_with_mock_schema.commit()

        found_entity = MockEricaRequestRepository(db_connection=transactional_session_with_mock_schema).get_by_job_request_id(request_id)

        assert found_entity == mock_object

    @pytest.mark.usefixtures('fake_db_connection_in_settings')
    def test_if_entity_not_in_database_then_raise_exception(self, transactional_session_with_mock_schema):
        request_id = uuid4()

        with pytest.raises(EntityNotFoundError):
            MockEricaRequestRepository(db_connection=transactional_session_with_mock_schema).get_by_job_request_id(request_id)


class TestEricaRepositoryUpdateByJobId:

    def test_if_entity_in_database_then_return_updated_domain_representation(self, transactional_session_with_mock_schema):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session_with_mock_schema.add(schema_object)
        transactional_session_with_mock_schema.commit()
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        updated_entity = MockEricaRequestRepository(db_connection=transactional_session_with_mock_schema).update_by_job_request_id(schema_object.request_id, updated_object)

        assert updated_entity == updated_object

    def test_if_entity_in_database_then_update_in_database(self, transactional_session_with_mock_schema):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session_with_mock_schema.add(schema_object)
        transactional_session_with_mock_schema.commit()
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        MockEricaRequestRepository(db_connection=transactional_session_with_mock_schema).update_by_job_request_id(schema_object.request_id, updated_object)

        updated_entry_in_db = transactional_session_with_mock_schema.query(MockSchema).filter(MockSchema.request_id == schema_object.request_id).first()
        assert updated_entry_in_db.request_id == schema_object.request_id
        assert updated_entry_in_db.payload == {'endboss': 'Sauron'}

    def test_if_entity_not_in_database_then_raise_error(self, transactional_session_with_mock_schema):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        with pytest.raises(EntityNotFoundError):
            MockEricaRequestRepository(db_connection=transactional_session_with_mock_schema).update_by_job_request_id(schema_object.request_id, updated_object)

    def test_if_update_object_then_set_only_updated_at_timestamp(self, transactional_erica_postgresql_db):
        with transactional_erica_postgresql_db.time.freeze('December 31st 1999 11:59:59 PM') as freezer:
            request_id = uuid4()
            mock_object = EricaRequest(request_id=request_id,
                                       payload={'endboss': 'Melkor'},
                                       creator_id="api",
                                       type=RequestType.freischalt_code_request,
                                       status=Status.new)
            created_object = EricaRequestRepository(db_connection=transactional_erica_postgresql_db.session).create(mock_object)
            found_entity_before_update = transactional_erica_postgresql_db.session.query(EricaRequestSchema).filter(EricaRequestSchema.request_id == request_id).first()
            before_update_created_at_timestamp = found_entity_before_update.created_at
            before_update_updated_at_timestamp = found_entity_before_update.updated_at
            created_object.payload = {'endboss': 'Sauron'}

            freezer.tick()

            EricaRequestRepository(db_connection=transactional_erica_postgresql_db.session).update_by_job_request_id(request_id, created_object)

            found_entity = transactional_erica_postgresql_db.session.query(EricaRequestSchema).filter(EricaRequestSchema.request_id==request_id).first()

        assert found_entity.created_at == before_update_created_at_timestamp
        assert found_entity.updated_at > before_update_updated_at_timestamp

    @pytest.mark.freeze_uuids
    def test_if_only_request_id_changed_then_only_call_update_with_changed_attributes(self, transactional_session_with_mock_schema):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session_with_mock_schema.add(schema_object)
        transactional_session_with_mock_schema.commit()
        updated_object = MockDomainModel(request_id=uuid4(),
                                         payload={'endboss': 'Melkor'})

        # We need a mock object to be able to intercept the call to the update function
        repo = MockEricaRequestRepository(db_connection=transactional_session_with_mock_schema)
        update_mock = MagicMock()
        mocked_get_by_job_request_id = MagicMock(side_effect=lambda request_id: MagicMock(
            first=MagicMock(return_value=MockEricaRequestRepository(db_connection=transactional_session_with_mock_schema)._get_by_job_request_id(request_id).first()),
            update=update_mock))
        repo._get_by_job_request_id = mocked_get_by_job_request_id

        repo.update_by_job_request_id(mock_object.request_id, updated_object)

        assert update_mock.mock_calls == [call({'request_id': UUID('00000000-0000-0000-0000-000000000000')})]


class TestEricaRepositoryDeleteByJobId:

    def test_if_entity_in_database_then_delete_from_database(self, transactional_session_with_mock_schema):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session_with_mock_schema.add(schema_object)
        transactional_session_with_mock_schema.commit()

        MockEricaRequestRepository(db_connection=transactional_session_with_mock_schema).delete_by_job_request_id(schema_object.request_id)

        not_found_entry = transactional_session_with_mock_schema.query(MockSchema).filter(MockSchema.request_id == schema_object.request_id).first()
        assert not_found_entry is None

    def test_if_entity_not_in_database_then_raise_error(self, transactional_session_with_mock_schema):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())

        with pytest.raises(EntityNotFoundError):
            MockEricaRequestRepository(db_connection=transactional_session_with_mock_schema).delete_by_job_request_id(schema_object.request_id)


class TestEricaRepositoryDeleteSuccessFail:

    @pytest.mark.parametrize("status", [Status.success, Status.failed], ids=["success", "failed"])
    def test_if_success_or_failed_entity_older_than_ttl_in_database_then_delete_from_database(self,
                                                                                              transactional_erica_postgresql_db,
                                                                                              status):
        transactional_erica_postgresql_db.session.query(EricaRequestSchema).delete()
        request_id = uuid.uuid4()
        mock_object = EricaRequest(request_id=request_id,
                                   payload={'endboss': 'Melkor'},
                                   creator_id="api",
                                   type=RequestType.freischalt_code_request,
                                   status=status,
                                   updated_at=datetime.datetime.now() - datetime.timedelta(minutes=2))
        EricaRequestRepository(db_connection=transactional_erica_postgresql_db.session).create(mock_object)

        deleted = EricaRequestRepository(
            db_connection=transactional_erica_postgresql_db.session).delete_success_fail_old_entities(1)
        assert deleted == 1
        entity_not_found = transactional_erica_postgresql_db.session.query(EricaRequestSchema).filter(
            EricaRequestSchema.request_id == request_id).first()
        assert entity_not_found is None

    @pytest.mark.parametrize("status", [Status.success, Status.failed], ids=["success", "failed"])
    def test_if_success_or_failed_entity_not_older_than_ttl_in_database_then_delete_from_database(self,
                                                                                                  transactional_erica_postgresql_db,
                                                                                                  status):
        request_id = uuid.uuid4()
        mock_object = EricaRequest(request_id=request_id,
                                   payload={'endboss': 'Melkor'},
                                   creator_id="api",
                                   type=RequestType.freischalt_code_request,
                                   status=status,
                                   updated_at=datetime.datetime.now())
        EricaRequestRepository(db_connection=transactional_erica_postgresql_db.session).create(mock_object)

        deleted = EricaRequestRepository(
            db_connection=transactional_erica_postgresql_db.session).delete_success_fail_old_entities(1)
        assert deleted == 0
        entity_found = transactional_erica_postgresql_db.session.query(EricaRequestSchema).filter(
            EricaRequestSchema.request_id == request_id).first()
        assert entity_found is not None

    @pytest.mark.parametrize("status", [Status.new, Status.scheduled, Status.processing],
                             ids=["new", "scheduled", "processing"])
    def test_if_not_success_nor_failed_entity_older_than_ttl_in_database_then_not_delete_from_database(self,
                                                                                                       transactional_erica_postgresql_db,
                                                                                                       status):
        request_id = uuid.uuid4()
        mock_object = EricaRequest(request_id=request_id,
                                   payload={'endboss': 'Melkor'},
                                   creator_id="api",
                                   type=RequestType.freischalt_code_request,
                                   status=status,
                                   updated_at=datetime.datetime.now() - datetime.timedelta(minutes=2))
        EricaRequestRepository(db_connection=transactional_erica_postgresql_db.session).create(mock_object)
        deleted = EricaRequestRepository(
            db_connection=transactional_erica_postgresql_db.session).delete_success_fail_old_entities(1)
        assert deleted == 0
        entity_found = transactional_erica_postgresql_db.session.query(EricaRequestSchema).filter(
            EricaRequestSchema.request_id == request_id).first()
        assert entity_found is not None


class TestEricaRepositoryUpdateProcessing:

    @pytest.mark.parametrize("status", [Status.new, Status.scheduled, Status.processing],
                             ids=["new", "scheduled", "processing"])
    def test_if_new_scheduled_processing_entity_older_than_ttl_in_database_then_update_to_failed(self,
                                                                                                 transactional_erica_postgresql_db,
                                                                                                 status):
        transactional_erica_postgresql_db.session.query(EricaRequestSchema).delete()
        request_id = uuid.uuid4()
        mock_object = EricaRequest(request_id=request_id,
                                   payload={'endboss': 'Melkor'},
                                   creator_id="api",
                                   type=RequestType.freischalt_code_request,
                                   status=status,
                                   updated_at=datetime.datetime.now() - datetime.timedelta(minutes=2))
        EricaRequestRepository(db_connection=transactional_erica_postgresql_db.session).create(mock_object)

        updated = EricaRequestRepository(
            db_connection=transactional_erica_postgresql_db.session).set_not_processed_entities_to_failed(1)
        assert updated == 1
        entity_found = transactional_erica_postgresql_db.session.query(EricaRequestSchema).filter(
            EricaRequestSchema.request_id == request_id).first()
        assert entity_found is not None
        assert entity_found.status == Status.failed

    @pytest.mark.parametrize("status", [Status.new, Status.scheduled, Status.processing],
                             ids=["new", "scheduled", "processing"])
    def test_if_new_scheduled_processing_entity_not_older_than_ttl_in_database_then_not_update_to_failed(self,
                                                                                                         transactional_erica_postgresql_db,
                                                                                                         status):
        request_id = uuid.uuid4()
        mock_object = EricaRequest(request_id=request_id,
                                   payload={'endboss': 'Melkor'},
                                   creator_id="api",
                                   type=RequestType.freischalt_code_request,
                                   status=status,
                                   updated_at=datetime.datetime.now())
        EricaRequestRepository(db_connection=transactional_erica_postgresql_db.session).create(mock_object)

        updated = EricaRequestRepository(
            db_connection=transactional_erica_postgresql_db.session).set_not_processed_entities_to_failed(1)
        assert updated == 0
        entity_found = transactional_erica_postgresql_db.session.query(EricaRequestSchema).filter(
            EricaRequestSchema.request_id == request_id).first()
        assert entity_found is not None
        assert entity_found.status == status
