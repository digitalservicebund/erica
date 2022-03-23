import copy
import json
import os
from datetime import date
from decimal import Decimal

import pytest
import requests

from tests.erica_legacy.samples.grundsteuer_sample_data import SampleGrundsteuerData

ERICA_TESTING_URL = os.environ.get("ERICA_TESTING_URL", "http://0.0.0.0:8000")


@pytest.fixture()
def full_est_data():
    full_data = {
        'est_data': {
            'steuernummer': '19811310010',
            'submission_without_tax_nr': False,
            'bufa_nr': '9198',
            'bundesland': 'BY',
            'familienstand': 'married',
            'familienstand_date': date(2000, 1, 31),

            'person_a_idnr': '04452397687',
            'person_a_dob': date(1950, 8, 16),
            'person_a_first_name': 'Manfred',
            'person_a_last_name': 'Mustername',
            'person_a_street': 'Steuerweg',
            'person_a_street_number': 42,
            'person_a_plz': 20354,
            'person_a_town': 'Hamburg',
            'person_a_religion': 'none',
            'person_a_has_pflegegrad': False,
            'person_a_has_merkzeichen_bl': False,
            'person_a_has_merkzeichen_tbl': False,
            'person_a_has_merkzeichen_h': False,
            'person_a_has_merkzeichen_ag': False,
            'person_a_has_merkzeichen_g': False,
            'person_a_requests_pauschbetrag': False,
            'person_a_requests_fahrtkostenpauschale': False,
            'telephone_number': '01715151',

            'person_b_idnr': '02293417683',
            'person_b_dob': date(1951, 2, 25),
            'person_b_first_name': 'Gerta',
            'person_b_last_name': 'Mustername',
            'person_b_same_address': True,
            'person_b_religion': 'rk',
            'person_b_has_pflegegrad': False,
            'person_b_has_merkzeichen_bl': False,
            'person_b_has_merkzeichen_tbl': False,
            'person_b_has_merkzeichen_h': False,
            'person_b_has_merkzeichen_ag': False,
            'person_b_has_merkzeichen_g': False,
            'person_b_requests_pauschbetrag': False,
            'person_b_requests_fahrtkostenpauschale': False,

            'iban': 'DE35133713370000012345',
            'account_holder': 'person_a',

            'haushaltsnahe_entries': ["Gartenarbeiten"],
            'haushaltsnahe_summe': Decimal('500.00'),

            'handwerker_entries': ["Renovierung Badezimmer"],
            'handwerker_summe': Decimal('200.00'),
            'handwerker_lohn_etc_summe': Decimal('100.00'),

            'confirm_complete_correct': True,
            'confirm_send': True,
        },
        'meta_data': {
            'year': 2021
        }
    }

    return full_data


@pytest.fixture()
def full_grundsteuer_data():
    return SampleGrundsteuerData().build().dict()


class TestV1Ping:

    def test_if_get_from_ping_then_return_pong(self):
        response = requests.get(ERICA_TESTING_URL + "/01/ping")

        assert response.text == '"pong"'


class TestV1ValidTaxNumber:

    def test_if_get_with_valid_tax_number_and_state_then_return_true(self, full_est_data):
        valid_state = "by"
        valid_tax_number = "19811310010"

        response = requests.get(ERICA_TESTING_URL + f"/01/tax_number_validity/{valid_state}/{valid_tax_number}",)

        assert response.json() == {"is_valid": True}

    def test_if_get_with_valid_tax_number_and_state_uppercase_then_return_true(self, full_est_data):
        valid_state = "BY"
        valid_tax_number = "19811310010"

        response = requests.get(ERICA_TESTING_URL + f"/01/tax_number_validity/{valid_state}/{valid_tax_number}",)

        assert response.json() == {"is_valid": True}

    def test_if_get_with_invalid_tax_number_then_return_false(self, full_est_data):
        valid_state = "by"
        invalid_tax_number = "123"

        response = requests.get(ERICA_TESTING_URL + f"/01/tax_number_validity/{valid_state}/{invalid_tax_number}",)

        assert response.json() == {"is_valid": False}

    def test_if_get_with_invalid_state_then_return_422(self, full_est_data):
        invalid_state = "invalid"
        valid_tax_number = "19811310010"

        response = requests.get(ERICA_TESTING_URL + f"/01/tax_number_validity/{invalid_state}/{valid_tax_number}",)

        assert response.status_code == 422

    def test_if_get_without_state_then_return_404(self, full_est_data):
        valid_tax_number = "19811310010"

        response = requests.get(ERICA_TESTING_URL + f"/01/tax_number_validity/{valid_tax_number}",)

        assert response.status_code == 404

    def test_if_get_without_tax_number_then_return_404(self, full_est_data):
        valid_state = "by"

        response = requests.get(ERICA_TESTING_URL + f"/01/tax_number_validity/{valid_state}",)

        assert response.status_code == 404


class TestV1TaxOfficeList:

    def test_if_get_list_then_return_json_list_of_tax_offices(self):
        with open("erica/erica_legacy/static/tax_offices.json", "r") as response_file:
            response_content = json.load(response_file)

        response = requests.get(ERICA_TESTING_URL + f"/01/tax_offices",)

        assert response.json() == response_content


class TestV1EstValidation:

    def test_if_get_with_full_data_then_return_200(self, full_est_data):
        response = requests.get(ERICA_TESTING_URL + "/01/est_validations", data=json.dumps(full_est_data, default=str))

        assert response.status_code == 200

    def test_if_get_with_incorrect_data_then_return_422_and_correct_error(self, full_est_data):
        incorrect_data = copy.deepcopy(full_est_data)
        incorrect_data['est_data']['submission_without_tax_nr'] = True

        response = requests.get(ERICA_TESTING_URL + "/01/est_validations", data=json.dumps(incorrect_data, default=str))

        assert response.status_code == 422
        assert 'submission_without_tax_nr' in response.json()['detail'][0]['loc']


class TestV1Ests:

    def test_if_post_with_full_data_then_return_201(self, full_est_data):
        response = requests.post(ERICA_TESTING_URL + "/01/ests", data=json.dumps(full_est_data, default=str))

        assert response.status_code == 201
        assert 'pdf' in response.json()
        assert 'transfer_ticket' in response.json()

    def test_if_post_with_incorrect_data_then_return_422_and_correct_error(self, full_est_data):
        incorrect_data = copy.deepcopy(full_est_data)
        incorrect_data['est_data']['submission_without_tax_nr'] = True

        response = requests.post(ERICA_TESTING_URL + "/01/ests", data=json.dumps(incorrect_data, default=str))

        assert response.status_code == 422
        assert 'submission_without_tax_nr' in response.json()['detail'][0]['loc']


class TestV1UnlockCodeActivation:

    # We can not test an actual activation because Elster limits our requests
    def test_if_post_without_data_then_return_422(self):
        response = requests.post(ERICA_TESTING_URL + "/01/unlock_code_activations")

        assert response.status_code == 422


class TestV1UnlockCodeRequest:

    # We can not test an actual request because Elster limits our requests
    def test_if_post_without_data_then_return_422(self):
        response = requests.post(ERICA_TESTING_URL + "/01/unlock_code_requests")

        assert response.status_code == 422


class TestV1UnlockCodeRevocation:

    # We can not test an actual revocation because Elster limits our requests
    def test_if_post_without_data_then_return_422(self):
        response = requests.post(ERICA_TESTING_URL + "/01/unlock_code_revocations")

        assert response.status_code == 422


class TestV1Grundsteuer:

    def test_if_post_without_data_then_return_422(self):
        response = requests.post(ERICA_TESTING_URL + "/01/grundsteuer")

        assert response.status_code == 422

    def test_if_post_with_data_then_return_422(self, full_grundsteuer_data):
        response = requests.post(ERICA_TESTING_URL + "/01/grundsteuer",  data=json.dumps(full_grundsteuer_data, default=str))

        assert response.status_code == 422
        assert response.json()['detail']["message"] == 'ERIC_GLOBAL_PRUEF_FEHLER'


class TestV2Ping:

    def test_if_get_from_ping_then_return_pong(self):
        response = requests.get(ERICA_TESTING_URL + "/v2/ping")

        assert response.text == '"pong"'
