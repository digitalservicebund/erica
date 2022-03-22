from uuid import uuid4

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from erica.infrastructure.sqlalchemy.database import get_engine, run_migrations
from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository
from tests.infrastructure.sqlalechemy.repositories.mock_repositories import MockDomainModel, MockSchema


class MockEricaRequstRepository(
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


class TestEricaRepositoryGetByJobId:

    def test_if_entity_in_database_then_return_domain_representation(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        job_id = uuid4()
        schema_object = MockSchema(**mock_object.dict(), job_id=job_id)
        transactional_session.add(schema_object)
        transactional_session.commit()

        found_entity = MockEricaRequstRepository(db_connection=transactional_session).get_by_job_id(job_id)

        assert found_entity == mock_object

    def test_if_entity_not_in_database_then_raise_exception(self, transactional_session):
        job_id = uuid4()

        with pytest.raises(EntityNotFoundError):
            MockEricaRequstRepository(db_connection=transactional_session).get_by_job_id(job_id)


class TestEricaRepositoryUpdateByJobId:

    def test_if_entity_in_database_then_return_updated_domain_representation(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        updated_entity = MockEricaRequstRepository(db_connection=transactional_session).update_by_job_id(schema_object.job_id, updated_object)

        assert updated_entity == updated_object

    def test_if_entity_in_database_then_update_in_database(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        MockEricaRequstRepository(db_connection=transactional_session).update_by_job_id(schema_object.job_id, updated_object)

        updated_entry_in_db = transactional_session.query(MockSchema).filter(MockSchema.job_id == schema_object.job_id).first()
        assert updated_entry_in_db.job_id == schema_object.job_id
        assert updated_entry_in_db.payload == {'endboss': 'Sauron'}

    def test_if_entity_not_in_database_then_raise_error(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        with pytest.raises(EntityNotFoundError):
            MockEricaRequstRepository(db_connection=transactional_session).update_by_job_id(schema_object.job_id, updated_object)


class TestEricaRepositoryDeleteByJobId:

    def test_if_entity_in_database_then_delete_from_database(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()

        MockEricaRequstRepository(db_connection=transactional_session).delete_by_job_id(schema_object.job_id)

        not_found_entry = transactional_session.query(MockSchema).filter(MockSchema.job_id == schema_object.job_id).first()
        assert not_found_entry is None

    def test_if_entity_not_in_database_then_raise_error(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())

        with pytest.raises(EntityNotFoundError):
            MockEricaRequstRepository(db_connection=transactional_session).delete_by_job_id(schema_object.job_id)
