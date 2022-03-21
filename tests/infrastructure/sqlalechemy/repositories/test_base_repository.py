from abc import ABC
from uuid import uuid4

import pytest
from pydantic import BaseModel
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from erica.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface
from erica.infrastructure.sqlalchemy.database import engine, run_migrations
from erica.infrastructure.sqlalchemy.erica_request_schema import BaseDbSchema
from erica.infrastructure.sqlalchemy.repositories.base_repository import BaseRepository, EntityNotFoundError


class MockDomainModel(BaseModel):
    payload: dict

    class Config:
        orm_mode = True


class MockSchema(BaseDbSchema):
    __tablename__ = 'mock_schema'
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=text("gen_random_uuid()"), )
    job_id = Column(UUID(as_uuid=True))
    payload = Column(JSONB)


class MockBaseRepository(
    BaseRepository[MockDomainModel, MockSchema],
    BaseRepositoryInterface,
    ABC
):
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.DatabaseEntity = MockSchema
        self.DomainModel = MockDomainModel


@pytest.fixture
def transactional_session():
    if not database_exists(engine.url):
        create_database(engine.url)
    run_migrations()
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    yield session

    tables = MockSchema.metadata.sorted_tables
    for table in tables:
        session.execute(table.delete())
    session.commit()


class TestBaseRepositoryCreate:

    def test_if_entity_of_type_domain_model_as_input_then_entity_with_correct_data_in_database(self, transactional_session):
        repository = MockBaseRepository(db_connection=transactional_session)

        repository.create(MockDomainModel(payload={'endboss': 'Melkor'}))

        assert len(transactional_session.query(MockSchema).all()) == 1
        assert isinstance(transactional_session.query(MockSchema).all()[0], MockSchema)

    def test_if_entity_of_type_domain_model_as_input_then_entity_of_schema_type_is_in_database(self, transactional_session):
        repository = MockBaseRepository(db_connection=transactional_session)

        repository.create(MockDomainModel(payload={'endboss': 'Melkor'}))

        assert isinstance(transactional_session.query(MockSchema).all()[0], MockSchema)

    def test_if_entity_of_type_domain_model_as_input_then_return_schema_type(self, transactional_session):
        repository = MockBaseRepository(db_connection=transactional_session)

        returned_value = repository.create(MockDomainModel(payload={'endboss': 'Melkor'}))

        assert isinstance(returned_value, MockDomainModel)


class TestBaseRepositoryGet:

    def test_if_entity_of_type_domain_model_as_input_then_return_list_with_schema_repr_of_entities(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        list_of_schema_object = [MockSchema(**mock_object.dict()), MockSchema(**mock_object.dict()), MockSchema(**mock_object.dict())]

        transactional_session.add(list_of_schema_object[0])
        transactional_session.add(list_of_schema_object[1])
        transactional_session.add(list_of_schema_object[2])
        transactional_session.commit()

        found_entities = MockBaseRepository(db_connection=transactional_session).get()

        assert found_entities == list_of_schema_object

    def test_if_table_is_empty_then_return_empty_list(self, transactional_session):
        found_entities = MockBaseRepository(db_connection=transactional_session).get()

        assert found_entities == []


class TestBaseRepositoryGetById:

    def test_if_entity_in_database_then_return_domain_representation(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()

        found_entity = MockBaseRepository(db_connection=transactional_session).get_by_id(schema_object.id)

        assert found_entity == mock_object

    def test_if_entity_not_in_database_then_raise_exception(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict(), job_id=uuid4())

        with pytest.raises(EntityNotFoundError):
            MockBaseRepository(db_connection=transactional_session).get_by_id(schema_object.id)


class TestBaseRepositoryGetByJobId:

    def test_if_entity_in_database_then_return_domain_representation(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        job_id = uuid4()
        schema_object = MockSchema(**mock_object.dict(), job_id=job_id)
        transactional_session.add(schema_object)
        transactional_session.commit()

        found_entity = MockBaseRepository(db_connection=transactional_session).get_by_job_id(job_id)

        assert found_entity == mock_object

    def test_if_entity_not_in_database_then_raise_exception(self, transactional_session):
        job_id = uuid4()

        with pytest.raises(EntityNotFoundError):
            MockBaseRepository(db_connection=transactional_session).get_by_job_id(job_id)


class TestBaseRepositoryUpdate:

    def test_if_entity_in_database_then_return_updated_domain_representation(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        updated_entity = MockBaseRepository(db_connection=transactional_session).update(schema_object.id, updated_object)

        assert updated_entity == updated_object

    def test_if_entity_in_database_then_update_in_database(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        MockBaseRepository(db_connection=transactional_session).update(schema_object.id, updated_object)

        updated_entry_in_db = transactional_session.query(MockSchema).filter(MockSchema.id == schema_object.id).first()
        assert updated_entry_in_db.id == schema_object.id
        assert updated_entry_in_db.payload == {'endboss': 'Sauron'}

    def test_if_entity_not_in_database_then_raise_error(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        with pytest.raises(EntityNotFoundError):
            MockBaseRepository(db_connection=transactional_session).update(schema_object.id, updated_object)


class TestBaseRepositoryDelete:

    def test_if_entity_in_database_then_delete_from_database(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        transactional_session.add(schema_object)
        transactional_session.commit()

        MockBaseRepository(db_connection=transactional_session).delete(schema_object.id)

        assert len(transactional_session.query(MockSchema).all()) == 0

    def test_if_entity_not_in_database_then_raise_error(self, transactional_session):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())

        with pytest.raises(EntityNotFoundError):
            MockBaseRepository(db_connection=transactional_session).delete(schema_object.id)

