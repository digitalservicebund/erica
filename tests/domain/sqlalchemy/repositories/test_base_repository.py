from abc import ABC
from unittest.mock import MagicMock, call
from uuid import uuid4, UUID

import pytest
from domain.sqlalchemy.repositories.mock_repositories import MockDomainModel, MockSchema

from erica.domain.repositories.base_repository_interface import BaseRepositoryInterface
from erica.domain.sqlalchemy.repositories.base_repository import BaseRepository, EntityNotFoundError


class MockBaseRepository(
    BaseRepository[MockDomainModel, MockSchema],
    BaseRepositoryInterface,
    ABC
):
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.DatabaseEntity = MockSchema
        self.DomainModel = MockDomainModel


class TestBaseRepositoryCreate:

    def test_if_entity_of_type_domain_model_as_input_then_entity_with_correct_data_in_database(self, setup_database):
        repository = MockBaseRepository(db_connection=setup_database)

        repository.create(MockDomainModel(payload={'endboss': 'Melkor'}))

        assert len(setup_database.query(MockSchema).all()) == 1
        assert isinstance(setup_database.query(MockSchema).all()[0], MockSchema)

    def test_if_entity_of_type_domain_model_as_input_then_entity_of_schema_type_is_in_database(self, setup_database):
        repository = MockBaseRepository(db_connection=setup_database)

        repository.create(MockDomainModel(payload={'endboss': 'Melkor'}))

        assert isinstance(setup_database.query(MockSchema).all()[0], MockSchema)

    def test_if_entity_of_type_domain_model_as_input_then_return_schema_type(self, setup_database):
        repository = MockBaseRepository(db_connection=setup_database)

        returned_value = repository.create(MockDomainModel(payload={'endboss': 'Melkor'}))

        assert isinstance(returned_value, MockDomainModel)


class TestBaseRepositoryGet:

    def test_if_entity_of_type_domain_model_as_input_then_return_list_with_schema_repr_of_entities(self, setup_database):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        list_of_schema_object = [MockSchema(**mock_object.dict()), MockSchema(**mock_object.dict()), MockSchema(**mock_object.dict())]

        setup_database.add(list_of_schema_object[0])
        setup_database.add(list_of_schema_object[1])
        setup_database.add(list_of_schema_object[2])
        setup_database.commit()

        found_entities = MockBaseRepository(db_connection=setup_database).get()

        assert found_entities == list_of_schema_object

    def test_if_table_is_empty_then_return_empty_list(self, setup_database):
        found_entities = MockBaseRepository(db_connection=setup_database).get()

        assert found_entities == []


class TestBaseRepositoryGetById:

    def test_if_entity_in_database_then_return_domain_representation(self, setup_database):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        setup_database.add(schema_object)
        setup_database.commit()

        found_entity = MockBaseRepository(db_connection=setup_database).get_by_id(schema_object.id)

        assert found_entity == mock_object

    def test_if_entity_not_in_database_then_raise_exception(self, setup_database):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        mock_object.request_id = uuid4()
        schema_object = MockSchema(**mock_object.dict())

        with pytest.raises(EntityNotFoundError):
            MockBaseRepository(db_connection=setup_database).get_by_id(schema_object.id)


class TestBaseRepositoryUpdate:

    def test_if_entity_in_database_then_return_updated_domain_representation(self, setup_database):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        setup_database.add(schema_object)
        setup_database.commit()
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        updated_entity = MockBaseRepository(db_connection=setup_database).update(schema_object.id, updated_object)

        assert updated_entity == updated_object

    def test_if_entity_in_database_then_update_in_database(self, setup_database):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        setup_database.add(schema_object)
        setup_database.commit()
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        MockBaseRepository(db_connection=setup_database).update(schema_object.id, updated_object)

        updated_entry_in_db = setup_database.query(MockSchema).filter(MockSchema.id == schema_object.id).first()
        assert updated_entry_in_db.id == schema_object.id
        assert updated_entry_in_db.payload == {'endboss': 'Sauron'}

    def test_if_entity_not_in_database_then_raise_error(self, setup_database):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        updated_object = MockDomainModel(payload={'endboss': 'Sauron'})

        with pytest.raises(EntityNotFoundError):
            MockBaseRepository(db_connection=setup_database).update(schema_object.id, updated_object)

    @pytest.mark.freeze_uuids
    def test_if_only_request_id_changed_then_only_call_update_with_changed_attributes(self, setup_database):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        setup_database.add(schema_object)
        setup_database.commit()

        updated_object = MockDomainModel(request_id=uuid4(),
                                         payload={'endboss': 'Melkor'})

        # We need a mock object to be able to intercept the call to the update function
        repo = MockBaseRepository(db_connection=setup_database)
        update_mock = MagicMock()
        mocked_get_by_id = MagicMock(side_effect=lambda request_id: MagicMock(
            first=MagicMock(return_value=MockBaseRepository(db_connection=setup_database)._get_by_id(request_id).first()),
            update=update_mock))
        repo._get_by_id = mocked_get_by_id

        repo.update(schema_object.id, updated_object)

        assert update_mock.mock_calls == [call({'request_id': UUID('00000000-0000-0000-0000-000000000000')})]


class TestBaseRepositoryDelete:

    def test_if_entity_in_database_then_delete_from_database(self, setup_database):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())
        setup_database.add(schema_object)
        setup_database.commit()

        MockBaseRepository(db_connection=setup_database).delete(schema_object.id)

        assert len(setup_database.query(MockSchema).all()) == 0

    def test_if_entity_not_in_database_then_raise_error(self, setup_database):
        mock_object = MockDomainModel(payload={'endboss': 'Melkor'})
        schema_object = MockSchema(**mock_object.dict())

        with pytest.raises(EntityNotFoundError):
            MockBaseRepository(db_connection=setup_database).delete(schema_object.id)

