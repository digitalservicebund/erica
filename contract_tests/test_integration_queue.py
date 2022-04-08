import json
import os
import uuid
from datetime import date
from decimal import Decimal
from time import sleep

import pytest
import requests


ERICA_TESTING_URL = os.environ.get("ERICA_TESTING_URL", "http://localhost:8080/")


@pytest.fixture()
def full_est_data():
    est_payload = {
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

    return build_request_data(est_payload)


@pytest.fixture()
def full_grundsteuer_data():
    grundsteuer_payload = {'freitext': '', 'grundstueck': {'steuernummer': '2181508150', 'typ': 'einfamilienhaus', 'innerhalb_einer_gemeinde': True, 'bodenrichtwert': '41,99', 'flurstueck': [], 'adresse': {'strasse': 'Madeupstr', 'hausnummer': '22', 'hausnummerzusatz': 'b', 'plz': '33333', 'ort': 'Bielefeld', 'bundesland': 'BE'}}, 'gebaeude': {'ab1949': {'is_ab1949': False}, 'kernsaniert': {'is_kernsaniert': False}, 'abbruchverpflichtung': {'has_abbruchverpflichtung': False}, 'weitere_wohnraeume': {'has_weitere_wohnraeume': False}, 'garagen': {'has_garagen': False}, 'wohnflaechen': [42]}, 'eigentuemer': {'person': [{'steuer_id': {'steuer_id': '04452317681'}, 'anteil': {'zaehler': 1, 'nenner': 1}, 'persoenlicheAngaben': {'anrede': 'frau', 'name': 'Granger', 'vorname': 'Hermione'}, 'adresse': {'plz': '7777', 'ort': 'London'}}]}}
    return build_request_data(grundsteuer_payload)


@pytest.fixture()
def full_unlock_code_request_data():
    payload = {'tax_id_number': "04531972802",
               'date_of_birth': date(1957, 7, 14),
            }

    return build_request_data(payload)


@pytest.fixture()
def full_unlock_code_activation_data():
    payload = {'tax_id_number': "04531972802",
               'freischalt_code': "42",
               'elster_request_id': 'CORRECT'
            }

    return build_request_data(payload)


@pytest.fixture()
def full_unlock_code_revocation_data():
    payload = {'tax_id_number': "04531972802",
               'elster_request_id': 'CORRECT',
            }

    return build_request_data(payload)


@pytest.fixture()
def tax_number_validity_data():
    payload = {'state_abbreviation': "BY",
               'tax_number': "04531972802",
            }

    return build_request_data(payload)


def build_request_data(payload):
    return {
        'payload': payload,
        'clientIdentifier': 'ContractTests'
    }


class TestV2Ping:

    def test_if_get_from_ping_then_return_pong(self):
        response = requests.get(ERICA_TESTING_URL + "v2/ping")
        assert response.text == '"pong"'


class TestV2UnlockCodeRequest:
    endpoint = "v2/fsc/request"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self, full_unlock_code_request_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_request_data, default=str))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] + "/" + location[1] + "/" + location[2] == self.endpoint
        assert is_valid_uuid(location[3])

    def test_if_post_without_full_data_then_return_422(self, full_unlock_code_request_data):
        request_payload = full_unlock_code_request_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=str))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self, full_unlock_code_request_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_request_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        sleep(4)
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)

        assert response.status_code == 200
        assert response.json()["processStatus"] == "Failure"
        assert "result" in response.json()
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self):
        response = requests.post(ERICA_TESTING_URL + "v2/fsc/activation",
                                 data=json.dumps(create_unlock_code_activation(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_non_existing_request_then_return_404_and_response_with_error_code_and_message(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422


class TestV2UnlockCodeActivation:
    endpoint = "v2/fsc/activation"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self, full_unlock_code_activation_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_activation_data, default=str))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] + "/" + location[1] + "/" + location[2] == self.endpoint
        assert is_valid_uuid(location[3])

    def test_if_post_without_full_data_then_return_422(self, full_unlock_code_activation_data):
        request_payload = full_unlock_code_activation_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=str))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self, full_unlock_code_activation_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_activation_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        sleep(4)
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)

        assert response.status_code == 200
        assert response.json()["processStatus"] == "Failure"
        assert "result" in response.json()
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self):
        response = requests.post(ERICA_TESTING_URL + "v2/fsc/request",
                                 data=json.dumps(create_unlock_code_request(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_non_existing_request_then_return_404_and_response_with_error_code_and_message(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422


class TestV2UnlockCodeRevocation:
    endpoint = "v2/fsc/revocation"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self, full_unlock_code_revocation_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_revocation_data, default=str))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] + "/" + location[1] + "/" + location[2] == self.endpoint
        assert is_valid_uuid(location[3])

    def test_if_post_without_full_data_then_return_422(self, full_unlock_code_revocation_data):
        request_payload = full_unlock_code_revocation_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=str))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self, full_unlock_code_revocation_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_revocation_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        sleep(4)
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)

        assert response.status_code == 200
        assert response.json()["processStatus"] == "Failure"
        assert "result" in response.json()
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self):
        response = requests.post(ERICA_TESTING_URL + "v2/fsc/activation",
                                 data=json.dumps(create_unlock_code_activation(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_non_existing_request_then_return_404_and_response_with_error_code_and_message(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422


class TestV2TaxNumberValidity:
    endpoint = "v2/tax_number_validity"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self, tax_number_validity_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(tax_number_validity_data, default=str))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] + "/" + location[1] == self.endpoint
        assert is_valid_uuid(location[2])

    def test_if_post_without_full_data_then_return_422(self, tax_number_validity_data):
        request_payload = tax_number_validity_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=str))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self, tax_number_validity_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(tax_number_validity_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]
        sleep(4)
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)

        assert response.status_code == 200
        assert response.json()["processStatus"] == "Success"
        assert "result" in response.json()
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self):
        response = requests.post(ERICA_TESTING_URL + "v2/fsc/activation",
                                 data=json.dumps(create_unlock_code_activation(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_non_existing_request_then_return_404_and_response_with_error_code_and_message(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422


class TestV2TaxOffices:
    endpoint = "v2/tax_offices"

    def test_if_get_from_tax_office_list_then_return_tax_offices_json(self):
        with open("erica/infrastructure/static/tax_offices.json", "r") as response_file:
            response_content = json.load(response_file)
        response = requests.get(ERICA_TESTING_URL + self.endpoint)
        assert response.status_code == 200
        assert response.json() == response_content


class TestV2SendEst:
    endpoint = "v2/ests"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self, full_est_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_est_data, default=str))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] + "/" + location[1] == self.endpoint
        assert is_valid_uuid(location[2])

    def test_if_post_without_full_data_then_return_422(self, full_est_data):
        request_payload = full_est_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=str))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self, full_est_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_est_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]
        sleep(4)
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)

        assert response.status_code == 200
        assert response.json()["processStatus"] == "Success"
        assert "result" in response.json()
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self):
        response = requests.post(ERICA_TESTING_URL + "v2/fsc/activation",
                                 data=json.dumps(create_unlock_code_activation(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_non_existing_request_then_return_404_and_response_with_error_code_and_message(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422


class TestV2GrundsteuerRequest:
    endpoint = "v2/grundsteuer"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_send_grundsteuer(), default=json_default))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] + "/" + location[1] == self.endpoint
        assert is_valid_uuid(location[2])

    def test_if_post_without_clientidentifier_then_return_422(self):
        request = create_send_grundsteuer()
        request.clientIdentifier = None
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request, default=json_default))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self):
        request = create_send_grundsteuer()
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request, default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 200
        assert "processStatus" in response.json()
        assert "result" in response.json()
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self):
        response = requests.post(ERICA_TESTING_URL + "v2/fsc/activation",
                                 data=json.dumps(create_unlock_code_activation(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_non_existing_request_then_return_404_entity_not_found(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "errorCode" in response.json()
        assert "errorMessage" in response.json()

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422

def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def generate_uuid():
    return uuid.uuid4()


def json_default(value):
    if isinstance(value, date):
        return value.isoformat()
    else:
        return value.__dict__