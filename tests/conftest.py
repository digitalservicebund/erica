import os
import sys
from datetime import date

import pytest

from erica.erica_legacy.request_processing.erica_input.v1.erica_input import FormDataEst

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ["ERICA_ENV"] = 'testing'


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