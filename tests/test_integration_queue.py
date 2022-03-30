import json
import os
import requests

from tests.utils import json_default, create_unlock_code_request, is_valid_uuid, create_unlock_code_activation, \
    generate_uuid, create_unlock_code_revocation, create_tax_number_validity, create_send_est

ERICA_TESTING_URL = os.environ.get("ERICA_TESTING_URL", "http://localhost:8000")


class TestV2Ping:

    def test_if_get_from_ping_then_return_pong(self):
        response = requests.get(ERICA_TESTING_URL + "/v2/ping")
        assert response.text == '"pong"'


class TestV2UnlockCodeRequest:
    endpoint = "/v2/fsc/request"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_unlock_code_request(), default=json_default))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] + "/" + location[1] == "fsc/request"
        assert is_valid_uuid(location[2])

    def test_if_post_without_full_data_then_return_422(self):
        request_payload = create_unlock_code_request()
        request_payload.clientIdentifier = None
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=json_default))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_unlock_code_request(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 200
        assert "processStatus" in response.json()
        assert "result" in response.json()
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
    endpoint = "/v2/fsc/activation"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_unlock_code_activation(), default=json_default))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] + "/" + location[1] == "fsc/activation"
        assert is_valid_uuid(location[2])

    def test_if_post_without_full_data_then_return_422(self):
        request_payload = create_unlock_code_activation()
        request_payload.clientIdentifier = None
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=json_default))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_unlock_code_activation(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 200
        assert "processStatus" in response.json()
        assert "result" in response.json()
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
    endpoint = "/v2/fsc/revocation"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_unlock_code_revocation(), default=json_default))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] + "/" + location[1] == "fsc/revocation"
        assert is_valid_uuid(location[2])

    def test_if_post_without_full_data_then_return_422(self):
        request_payload = create_unlock_code_revocation()
        request_payload.clientIdentifier = None
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=json_default))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_unlock_code_revocation(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[2]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 200
        assert "processStatus" in response.json()
        assert "result" in response.json()
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
    endpoint = "/v2/tax_number_validity"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_tax_number_validity(), default=json_default))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] == "tax_number_validity"
        assert is_valid_uuid(location[1])

    def test_if_post_without_full_data_then_return_422(self):
        request_payload = create_tax_number_validity()
        request_payload.clientIdentifier = None
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=json_default))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_tax_number_validity(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[1]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 200
        assert "processStatus" in response.json()
        assert "result" in response.json()
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
    endpoint = "/v2/tax_offices"

    def test_if_get_from_ping_then_return_pong(self):
        with open("../erica/infrastructure/static/tax_offices.json", "r") as response_file:
            response_content = json.load(response_file)
        response = requests.get(ERICA_TESTING_URL + self.endpoint)
        assert response.status_code == 200
        assert response.json() == response_content


class TestV2SendEst:
    endpoint = "/v2/ests"

    def test_if_post_with_full_data_then_return_201_and_location_with_valid_uuid(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_send_est(), default=json_default))
        assert response.status_code == 201
        location = response.headers['Location'].split("/")
        assert location[0] == "ests"
        assert is_valid_uuid(location[1])

    def test_if_post_without_full_data_then_return_422(self):
        request_payload = create_send_est()
        request_payload.clientIdentifier = None
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(request_payload, default=json_default))
        assert response.status_code == 422

    def test_if_get_existing_request_then_return_200_and_response_with_correct_params(self):
        response = requests.post(ERICA_TESTING_URL + self.endpoint,
                                 data=json.dumps(create_send_est(), default=json_default))
        assert response.status_code == 201
        uuid = response.headers['Location'].split("/")[1]
        response = requests.get(ERICA_TESTING_URL + self.endpoint + "/" + uuid)
        assert response.status_code == 200
        assert "processStatus" in response.json()
        assert "result" in response.json()
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
