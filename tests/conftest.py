import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ["ERICA_ENV"] = 'testing'

import pytest_asyncio
import pytest
from datetime import date
from opyoid import Injector
from sqlalchemy.orm import sessionmaker

from erica.api.ApiModule import ApiModule
from erica.application.erica_request.erica_request_service import EricaRequestServiceInterface, EricaRequestService
from erica.config import get_settings
from erica.erica_legacy.request_processing.erica_input.v1.erica_input import FormDataEst
from erica.infrastructure.sqlalchemy.database import get_engine, session_scope
from tests.infrastructure.sqlalechemy.repositories.mock_repositories import MockSchema


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
    original_db_url = get_settings().database_url
    get_settings().database_url = database_uri

    with session_scope():
        yield database_uri

    get_settings().database_url = original_db_url


@pytest.fixture()
def transactional_session_with_mock_schema(transacted_postgresql_db):
    if not transacted_postgresql_db.has_table(MockSchema.__tablename__):
        transacted_postgresql_db.create_table(MockSchema)

    yield transacted_postgresql_db.session

    transacted_postgresql_db.reset_db()


@pytest.fixture()
def fake_db_connection_with_erica_table_in_settings(database_uri):
    postgresql_url = database_uri
    original_db_url = get_settings().database_url
    get_settings().database_url = postgresql_url

    engine = get_engine()

    from erica.infrastructure.sqlalchemy.erica_request_schema import EricaRequestSchema
    EricaRequestSchema.metadata.create_all(bind=engine)

    # fastapi_sqlalchemy creates its sessionmaker in the middleware constructor and provides
    # no mechanism to override it, so we have to patch it here.
    session_class = sessionmaker(bind=engine)
    with unittest.mock.patch('fastapi_sqlalchemy.middleware._Session', session_class):
        # Ideally, we'd want to wrap this yield (and therefore all test code using this fixture)
        # in a `with session_scope()` block. However, this does not work. Best guess is that it's
        # something to do with how pytest-asyncio copies the run context when scheduling test
        # functions. fastapi_sqlalchemy uses a ContextVar to track the created session and that
        # somehow gets lots when the test function runs. Workaround is to wrap any database-using
        # test code in a `with session_scope()` block in the test function.
        yield postgresql_url

        with session_scope():
            erica_request_service: EricaRequestService = Injector([ApiModule()]).inject(EricaRequestServiceInterface)
            entities = erica_request_service.erica_request_repository.get()

            for entity in entities:
                erica_request_service.erica_request_repository.db_connection.delete(entity)
    get_settings().database_url = original_db_url
