import json
import logging
import os
import time
import uuid
from datetime import date
from decimal import Decimal
from time import sleep

import pytest
import requests

ERICA_TESTING_URL = os.environ.get("ERICA_TESTING_URL", "http://localhost:8000")


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
def est_data_with_validation_errors():
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

            'iban': 'DE35133713370000012345',
            'account_holder': 'person_b',

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
    grundsteuer_payload = {
        "grundstueck": {
            "typ": "einfamilienhaus",
            "adresse": {
                "strasse": "GST Strasse",
                "hausnummer": "2",
                "hausnummerzusatz": "GST",
                "zusatzangaben": "GST Zusatzangaben",
                "plz": "12345",
                "ort": "GST Ort",
                "bundesland": "BB"
            },
            "steuernummer": "09841275756757579",
            "innerhalbEinerGemeinde": "true",
            "bodenrichtwert": "123,00",
            "flurstueck": [
                {
                    "angaben": {
                        "grundbuchblattnummer": "1",
                        "gemarkung": "2"
                    },
                    "flur": {
                        "flur": "1",
                        "flurstueckZaehler": "23",
                        "flurstueckNenner": "45",
                        "wirtschaftlicheEinheitZaehler": "67.1000",
                        "wirtschaftlicheEinheitNenner": "89"
                    },
                    "groesseQm": "1234"
                },
                {
                    "angaben": {
                        "grundbuchblattnummer": "2",
                        "gemarkung": "3"
                    },
                    "flur": {
                        "flur": "2",
                        "flurstueckZaehler": "34",
                        "flurstueckNenner": "56",
                        "wirtschaftlicheEinheitZaehler": "78.0000",
                        "wirtschaftlicheEinheitNenner": "90"
                    },
                    "groesseQm": "12345"
                }
            ]
        },
        "gebaeude": {
            "ab1949": {
                "isAb1949": "true"
            },
            "baujahr": {
                "baujahr": "2000"
            },
            "kernsaniert": {
                "isKernsaniert": "true"
            },
            "kernsanierungsjahr": {
                "kernsanierungsjahr": "2001"
            },
            "abbruchverpflichtung": {
                "hasAbbruchverpflichtung": "true"
            },
            "abbruchverpflichtungsjahr": {
                "abbruchverpflichtungsjahr": "2032"
            },
            "wohnflaechen": [
                "100"
            ],
            "weitereWohnraeume": {
                "hasWeitereWohnraeume": "true"
            },
            "weitereWohnraeumeDetails": {
                "anzahl": "2",
                "flaeche": "200"
            },
            "garagen": {
                "hasGaragen": "true"
            },
            "garagenAnzahl": {
                "anzahlGaragen": "3"
            }
        },
        "eigentuemer": {
            "person": [
                {
                    "persoenlicheAngaben": {
                        "anrede": "frau",
                        "titel": "1 Titel",
                        "vorname": "1 Vorname",
                        "name": "1 Name",
                        "geburtsdatum": "1980-01-31"
                    },
                    "adresse": {
                        "strasse": "1 Strasse",
                        "hausnummer": "1",
                        "hausnummerzusatz": "Hausnummer",
                        "plz": "12345",
                        "ort": "1 Ort"
                    },
                    "telefonnummer": "111111",
                    "steuerId": "04452397687",
                    "anteil": {
                        "zaehler": "1",
                        "nenner": "2"
                    }
                },
                {
                    "persoenlicheAngaben": {
                        "anrede": "herr",
                        "titel": "2 Titel",
                        "vorname": "2 Vorname",
                        "name": "2 Name",
                        "geburtsdatum": "1990-02-02"
                    },
                    "adresse": {
                        "strasse": "2 Strasse",
                        "hausnummer": "2",
                        "hausnummerzusatz": "Hausnummer",
                        "plz": "12345",
                        "ort": "2 Ort"
                    },
                    "telefonnummer": "222222",
                    "steuerId": "03352417692",
                    "vertreter": {
                        "name": {
                            "anrede": "herr",
                            "titel": "VERT Titel",
                            "vorname": "VERT Vorname",
                            "name": "VERT Name"
                        },
                        "adresse": {
                            "strasse": "VERT Strasse",
                            "hausnummer": "3",
                            "hausnummerzusatz": "VERT",
                            "plz": "12345",
                            "ort": "VERT Ort"
                        },
                        "telefonnummer": "333333"
                    },
                    "anteil": {
                        "zaehler": "3",
                        "nenner": "4"
                    }
                }
            ],
            "verheiratet": "false",
            "bruchteilsgemeinschaft": {
                "name": "BTG Name",
                "adresse": {
                    "strasse": "BTG Strasse",
                    "hausnummer": "1",
                    "hausnummerzusatz": "BTG",
                    "plz": "12345",
                    "ort": "BTG Ort"
                }
            },
            "empfangsbevollmaechtigter": {
                "name": {
                    "anrede": "no_anrede",
                    "titel": "EMP Titel",
                    "vorname": "EMP Vorname",
                    "name": "EMP Name"
                },
                "adresse": {
                    "postfach": "654321",
                    "plz": "12345",
                    "ort": "EMP Ort"
                },
                "telefonnummer": "12345"
            }
        }
    }
    return build_request_data(grundsteuer_payload)


@pytest.fixture()
def grundsteuer_data_with_validation_errors():
    grundsteuer_payload = {
        "grundstueck": {
            "typ": "baureif",
            "adresse": {
                "strasse": "GST Strasse",
                "hausnummer": "2",
                "hausnummerzusatz": "GST",
                "zusatzangaben": "GST Zusatzangaben",
                "plz": "12345",
                "ort": "GST Ort",
                "bundesland": "BB"
            },
            "steuernummer": "09841275756757579",
            "innerhalbEinerGemeinde": "true",
            "bodenrichtwert": "123,00",
            "flurstueck": [
                {
                    "angaben": {
                        "grundbuchblattnummer": "1",
                        "gemarkung": "2"
                    },
                    "flur": {
                        "flur": "1",
                        "flurstueckZaehler": "23",
                        "flurstueckNenner": "45",
                        "wirtschaftlicheEinheitZaehler": "67.1000",
                        "wirtschaftlicheEinheitNenner": "89"
                    },
                    "groesseQm": "1234"
                }
            ]
        },
        "eigentuemer": {
            "person": [
                {
                    "persoenlicheAngaben": {
                        "anrede": "frau",
                        "titel": "1 Titel",
                        "vorname": "1 Vorname",
                        "name": "1 Name",
                        "geburtsdatum": "1980-01-31"
                    },
                    "adresse": {
                        # ILLEGAL TO HAND STRASSE + POSTFACH
                        "postfach": "123456",
                        "strasse": "1 Strasse",
                        "hausnummer": "1",
                        "hausnummerzusatz": "Hausnummer",
                        "plz": "12345",
                        "ort": "1 Ort"
                    },
                    "telefonnummer": "111111",
                    "steuerId": "04452397687",
                    "anteil": {
                        "zaehler": "1",
                        "nenner": "2"
                    }
                }
            ],
        }
    }
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
        response = requests.get(ERICA_TESTING_URL + "/v2/ping")
        assert response.text == '"pong"'


class TestV2UnlockCodeRequest:
    endpoint = "/v2/fsc/request"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self, full_unlock_code_request_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_request_data, default=str))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert "/" + location[0] + "/" + location[1] + "/" + location[2] == self.endpoint
        assert is_valid_uuid(location[3])

    def test_if_post_without_full_data_then_return_422(self, full_unlock_code_request_data):
        request_payload = full_unlock_code_request_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=str))
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self,
                                                                                      full_unlock_code_request_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_request_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = poll(endpoint=ERICA_TESTING_URL + self.endpoint + "/" + uuid, expected_process_status="Failure")

        assert response.status_code == 200
        logging.getLogger().info(f"Response: {response.json()}")
        assert response.json()["processStatus"] == "Failure"
        assert response.json()["result"] is None
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self,
                                                                                                full_unlock_code_activation_data):
        response = requests.post(ERICA_TESTING_URL + "/v2/fsc/activation",
                                 data=json.dumps(full_unlock_code_activation_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)

        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_non_existing_request_then_return_404_and_response_with_error_code_and_message(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None


class TestV2UnlockCodeActivation:
    endpoint = "/v2/fsc/activation"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self,
                                                                                 full_unlock_code_activation_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_activation_data, default=str))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert "/" + location[0] + "/" + location[1] + "/" + location[2] == self.endpoint
        assert is_valid_uuid(location[3])

    def test_if_post_without_full_data_then_return_422(self, full_unlock_code_activation_data):
        request_payload = full_unlock_code_activation_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=str))
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self,
                                                                                      full_unlock_code_activation_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_activation_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = poll(endpoint=ERICA_TESTING_URL + self.endpoint + "/" + uuid, expected_process_status="Failure")

        assert response.status_code == 200
        logging.getLogger().info(f"Response: {response.json()}")
        assert response.json()["processStatus"] == "Failure"
        assert response.json()["result"] is None
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self,
                                                                                                full_unlock_code_request_data):
        response = requests.post(ERICA_TESTING_URL + "/v2/fsc/request",
                                 data=json.dumps(full_unlock_code_request_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_non_existing_request_then_return_404_and_response_with_error_code_and_message(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None


class TestV2UnlockCodeRevocation:
    endpoint = "/v2/fsc/revocation"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self,
                                                                                 full_unlock_code_revocation_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_revocation_data, default=str))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert "/" + location[0] + "/" + location[1] + "/" + location[2] == self.endpoint
        assert is_valid_uuid(location[3])

    def test_if_post_without_full_data_then_return_422(self, full_unlock_code_revocation_data):
        request_payload = full_unlock_code_revocation_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=str))
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self,
                                                                                      full_unlock_code_revocation_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_unlock_code_revocation_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = poll(endpoint=ERICA_TESTING_URL + self.endpoint + "/" + uuid, expected_process_status="Failure")

        assert response.status_code == 200
        logging.getLogger().info(f"Response: {response.json()}")
        assert response.json()["processStatus"] == "Failure"
        assert response.json()["result"] is None
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self,
                                                                                                full_unlock_code_activation_data):
        response = requests.post(ERICA_TESTING_URL + "/v2/fsc/activation",
                                 data=json.dumps(full_unlock_code_activation_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_non_existing_request_then_return_404_and_response_with_error_code_and_message(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None


class TestV2TaxNumberValidity:
    endpoint = "/v2/tax_number_validity"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self, tax_number_validity_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(tax_number_validity_data, default=str))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert "/" + location[0] + "/" + location[1] == self.endpoint
        assert is_valid_uuid(location[2])

    def test_if_post_without_full_data_then_return_422(self, tax_number_validity_data):
        request_payload = tax_number_validity_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=str))
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self, tax_number_validity_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(tax_number_validity_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]
        response = poll(endpoint=ERICA_TESTING_URL + self.endpoint + "/" + uuid, expected_process_status="Success")

        assert response.status_code == 200
        logging.getLogger().info(f"Response: {response.json()}")
        assert response.json()["processStatus"] == "Success"
        assert response.json()["result"] is not None
        assert response.json()["result"]["isValid"] is False
        assert response.json()["errorCode"] is None
        assert response.json()["errorMessage"] is None

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self,
                                                                                                full_unlock_code_activation_data):
        response = requests.post(ERICA_TESTING_URL + "/v2/fsc/activation",
                                 data=json.dumps(full_unlock_code_activation_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_non_existing_request_then_return_404_and_response_with_error_code_and_message(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None


class TestV2TaxOffices:
    endpoint = "/v2/tax_offices"

    def test_if_get_from_tax_office_list_then_return_tax_offices_json(self):
        with open("erica/infrastructure/static/tax_offices.json", "r") as response_file:
            response_content = json.load(response_file)
        response = requests.get(ERICA_TESTING_URL + self.endpoint)
        assert response.status_code == 200
        assert response.json() == response_content


class TestV2SendEst:
    endpoint = "/v2/ests"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self, full_est_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_est_data, default=str))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert "/" + location[0] + "/" + location[1] == self.endpoint
        assert is_valid_uuid(location[2])

    def test_if_post_without_full_data_then_return_422(self, full_est_data):
        request_payload = full_est_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=str))
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self, full_est_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_est_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]
        response = poll(endpoint=ERICA_TESTING_URL + self.endpoint + "/" + uuid, expected_process_status="Success")

        assert response.status_code == 200
        logging.getLogger().info(f"Response: {response.json()}")
        assert response.json()["processStatus"] == "Success"
        assert response.json()["result"] is not None
        assert response.json()["result"]["pdf"] is not None
        assert response.json()["result"]["transferticket"] is not None
        assert response.json()["errorCode"] is None
        assert response.json()["errorMessage"] is None

    def test_if_get_existing_request_with_validation_errors_then_return_200_and_response_with_correct_params(self, est_data_with_validation_errors):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(est_data_with_validation_errors, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]
        response = poll(endpoint=ERICA_TESTING_URL + self.endpoint + "/" + uuid, expected_process_status="Failure")

        assert response.status_code == 200
        logging.getLogger().info(f"Response: {response.json()}")
        assert response.json()["processStatus"] == "Failure"
        assert response.json()["result"] is not None
        assert response.json()["result"]["validationErrors"] is not None
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self,
                                                                                                full_unlock_code_activation_data):
        response = requests.post(ERICA_TESTING_URL + "/v2/fsc/activation",
                                 data=json.dumps(full_unlock_code_activation_data, default=str))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_non_existing_request_then_return_404_and_response_with_error_code_and_message(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None


class TestV2GrundsteuerRequest:
    endpoint = "/v2/grundsteuer"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self, full_grundsteuer_data):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(full_grundsteuer_data, default=json_default))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert "/" + location[0] + "/" + location[1] == self.endpoint
        assert is_valid_uuid(location[2])

    def test_if_post_without_clientidentifier_then_return_422(self, full_grundsteuer_data):
        request_payload = full_grundsteuer_data
        request_payload.pop('clientIdentifier', None)
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=json_default))
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self, full_grundsteuer_data):
        request = full_grundsteuer_data
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request, default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]

        response = poll(endpoint=ERICA_TESTING_URL + self.endpoint + "/" + uuid, expected_process_status="Success")

        assert response.status_code == 200
        logging.getLogger().info(f"Response: {response.json()}")
        assert response.json()["processStatus"] == "Success"
        assert response.json()["result"] is not None
        assert response.json()["result"]["pdf"] is not None
        assert response.json()["result"]["transferticket"] is not None
        assert response.json()["errorCode"] is None
        assert response.json()["errorMessage"] is None

    def test_if_get_existing_request_with_validation_errors_then_return_200_and_response_with_correct_params(self, grundsteuer_data_with_validation_errors):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(grundsteuer_data_with_validation_errors, default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]

        response = poll(endpoint=ERICA_TESTING_URL + self.endpoint + "/" + uuid, expected_process_status="Failure")

        assert response.status_code == 200
        logging.getLogger().info(f"Response: {response.json()}")
        assert response.json()["processStatus"] == "Failure"
        assert response.json()["result"] is not None
        assert response.json()["result"]["validationErrors"] is not None
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_existing_request_with_wrong_request_type_then_return_404_wrong_request_type(self,
                                                                                                full_unlock_code_activation_data):
        response = requests.post(ERICA_TESTING_URL + "/v2/fsc/activation",
                                 data=json.dumps(full_unlock_code_activation_data, default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[3]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_non_existing_request_then_return_404_entity_not_found(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + str(generate_uuid()))
        assert response.status_code == 404
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None

    def test_if_get_request_with_invalid_uuid_then_return_422(self):
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + "INVALID_UUID")
        assert response.status_code == 422
        assert "result" not in response.json()
        assert response.json()["errorCode"] is not None
        assert response.json()["errorMessage"] is not None


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


def poll(endpoint, expected_process_status, timeout=30, step=0.5):

    start_time = time.perf_counter()
    while time.perf_counter()- start_time < timeout:
        response = requests.get(endpoint)
        if response.status_code == 200 and response.json()['processStatus'] == expected_process_status:
            return response
        sleep(step)

    raise RuntimeError(f"Timeout reached while polling endpoint: {endpoint}")

