import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ["ERICA_ENV"] = 'testing'

import pytest_asyncio
import pytest
from opyoid import Injector
from datetime import date

from erica.api.ApiModule import ApiModule
from erica.application.EricaRequest.EricaRequestService import EricaRequestServiceInterface
from erica.erica_legacy.config import get_settings
from erica.infrastructure.sqlalchemy.database import run_migrations
from tests.infrastructure.sqlalechemy.repositories.mock_repositories import MockSchema

from erica.erica_legacy.request_processing.erica_input.v1.erica_input import FormDataEst


@pytest.fixture
def standard_est_input_data():
    return FormDataEst(
        submission_without_tax_nr=True,
        bufa_nr='9198',
        bundesland='BY',
        familienstand='married',
        familienstand_date=date(2000, 1, 31),

        person_a_idnr='04452397687',
        person_a_dob=date(1950, 8, 16),
        person_a_first_name='Manfred',
        person_a_last_name='Mustername',
        person_a_street='Steuerweg',
        person_a_street_number=42,
        person_a_plz=20354,
        person_a_town='Hamburg',
        person_a_religion='none',

        person_b_idnr='02293417683',
        person_b_dob=date(1951, 2, 25),
        person_b_first_name='Gerta',
        person_b_last_name='Mustername',
        person_b_same_address=True,
        person_b_religion='rk',

        iban='DE35133713370000012345',
        account_holder='person_a',

        confirm_complete_correct=True,
        confirm_send=True
    )


@pytest.fixture()
def fake_db_connection_in_settings(database_uri):
    postgresql_url = database_uri
    original_db_url = get_settings().database_url
    get_settings().database_url = postgresql_url

    yield postgresql_url

    get_settings().database_url = original_db_url


@pytest.fixture
def transactional_session_with_mock_schema(transacted_postgresql_db):
    if not transacted_postgresql_db.has_table(MockSchema.__tablename__):
        transacted_postgresql_db.create_table(MockSchema)

    yield transacted_postgresql_db.session

    transacted_postgresql_db.reset_db()


@pytest_asyncio.fixture()
async def async_fake_db_connection_with_erica_table_in_settings(database_uri):
    postgresql_url = database_uri
    original_db_url = get_settings().database_url
    get_settings().database_url = postgresql_url
    run_migrations()

    yield postgresql_url

    repository = Injector([ApiModule()]).inject(EricaRequestServiceInterface)
    entities = repository.erica_request_repository.get()

    for entity in entities:
        repository.erica_request_repository.db_connection.delete(entity)
    get_settings().database_url = original_db_url
