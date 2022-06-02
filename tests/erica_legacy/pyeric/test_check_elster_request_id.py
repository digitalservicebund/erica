from unittest.mock import MagicMock, patch, call

import pytest

from erica.erica_legacy.pyeric.pyeric_response import PyericResponse
from erica.erica_legacy.pyeric.check_elster_request_id import get_vast_list_from_xml, get_list_vast_requests, \
    NEW_REQUEST_ID_SINCE_LAST_CACHE_INVALIDATION, add_new_request_id_to_cache_list, request_needs_testmerker, \
    reset_new_request_id_list
from tests.erica_legacy.utils import missing_pyeric_lib
from tests.utils import read_text_from_sample


class TestGetVastListFromXml:

    def test_if_entries_in_xml_then_return_correct_dict(self):
        input_xml = read_text_from_sample('sample_vast_list.xml')
        expected_dict = {
            'br1652dntwz6wg1md87hc6055aij0nev': '02293417683',
            'br1226cnpymxm35hf0ptmsmc2nqpv9y9': '03392417683',
        }

        actual_dict = get_vast_list_from_xml(input_xml)

        assert actual_dict == expected_dict

    def test_if_no_entries_in_xml_then_return_empty_dict(self):
        input_xml = read_text_from_sample('sample_vast_list_empty.xml')
        expected_dict = {}

        actual_dict = get_vast_list_from_xml(input_xml)

        assert actual_dict == expected_dict


class MockPyericController(MagicMock):

    @staticmethod
    def get_eric_response():

        return PyericResponse(eric_response="", server_response=read_text_from_sample('sample_vast_list.xml'))


class TestListVastRequests:

    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_cache_is_invalidated_then_call_pyeric_controller(self):
        get_list_vast_requests.cache_clear()
        mock_pyeric_controller = MockPyericController()

        get_list_vast_requests(mock_pyeric_controller)

        assert mock_pyeric_controller.call_count == 1

    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_function_is_called_more_then_once_then_do_not_call_pyeric_controller_again(self):
        get_list_vast_requests.cache_clear()
        mock_pyeric_controller = MockPyericController()

        get_list_vast_requests(mock_pyeric_controller)
        get_list_vast_requests(mock_pyeric_controller)
        get_list_vast_requests(mock_pyeric_controller)

        assert mock_pyeric_controller.call_count == 1

    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_function_is_called_more_then_once_and_cache_invalid_then_call_pyeric_controller_again(self):
        get_list_vast_requests.cache_clear()
        mock_pyeric_controller = MockPyericController()

        get_list_vast_requests(mock_pyeric_controller)
        get_list_vast_requests(mock_pyeric_controller)

        get_list_vast_requests.cache_clear()

        get_list_vast_requests(mock_pyeric_controller)

        assert mock_pyeric_controller.call_count == 2


class TestRequestNeedsTestmerker:

    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_idnr_in_list_then_cache_invalidated(self):
        idnr = "1234"
        add_new_request_id_to_cache_list(idnr)
        with patch('erica.erica_legacy.pyeric.check_elster_request_id.get_list_vast_requests') as get_list_vast_requests_mock:

            request_needs_testmerker(idnr)

        assert call.cache_clear() in get_list_vast_requests_mock.mock_calls

    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_idnr_not_in_list_then_cache_not_invalidated(self):
        idnr = "1234"
        reset_new_request_id_list()
        with patch('erica.erica_legacy.pyeric.check_elster_request_id.get_list_vast_requests') as get_list_vast_requests_mock:

            request_needs_testmerker(idnr)

        assert call.cache_clear() not in get_list_vast_requests_mock.mock_calls
