import base64
import unittest
from datetime import date
from unittest.mock import patch, MagicMock, call

import pytest

from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeActivatePayload, FreischaltCodeRevocatePayload
from erica.domain.tax_number_validation.check_tax_number import CheckTaxNumberPayload
from erica.erica_legacy.pyeric.eric_errors import InvalidBufaNumberError
from erica.erica_legacy.pyeric.pyeric_response import PyericResponse
from erica.erica_legacy.request_processing.eric_mapper import EstEricMapping, UnlockCodeRequestEricMapper
from erica.erica_legacy.request_processing.erica_input.v1.erica_input import UnlockCodeRequestData, \
    UnlockCodeActivationData, \
    UnlockCodeRevocationData, GetAddressData
from erica.erica_legacy.request_processing.requests_controller import UnlockCodeRequestController, \
    UnlockCodeActivationRequestController, EstRequestController, EstValidationRequestController, \
    UnlockCodeRevocationRequestController, GetAddressRequestController, \
    GetBelegeRequestController, CheckTaxNumberRequestController
from tests.erica_legacy.utils import create_est, missing_cert, missing_pyeric_lib, replace_text_in_xml, \
    replace_subtree_in_xml, TEST_EST_VERANLAGUNGSJAHR
from tests.utils import read_text_from_sample


class TestEstValidationRequestProcess(unittest.TestCase):

    def test_pyeric_controller_is_initialised_with_correct_arguments(self):
        est_validation_request = EstValidationRequestController(create_est(correct_form_data=True))

        xml = '<xml></xml>'

        with patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.__init__',
                   MagicMock(return_value=None)) \
                as pyeric_controller_init, \
                patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.erica_legacy.elster_xml.est_mapping.check_and_generate_entries'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.EstValidationRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.'
                      'generate_full_est_xml', MagicMock(return_value=xml)):
            est_validation_request.process()

            pyeric_controller_init.assert_called_with(xml, TEST_EST_VERANLAGUNGSJAHR)

    def test_pyeric_get_eric_response_is_called(self):
        est_validation_request = EstValidationRequestController(create_est(correct_form_data=True))

        xml = '<xml></xml>'

        with patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.__init__',
                   MagicMock(return_value=None)), \
                patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response') \
                        as pyeric_controller_get_response, \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.EstValidationRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.'
                      'generate_full_est_xml', MagicMock(return_value=xml)):
            est_validation_request.process()

            pyeric_controller_get_response.assert_called()


class TestEstRequestInit(unittest.TestCase):

    def test_if_no_include_param_given_then_set_include_false(self):
        created_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=False)

        self.assertFalse(created_request.include_elster_responses)

    def test_if_include_param_true_then_set_include_true(self):
        created_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=True)

        self.assertTrue(created_request.include_elster_responses)


class TestEstRequestProcess(unittest.TestCase):

    def test_check_and_generate_entries_is_called_with_eric_mapped_object(self):
        eric_mapped_object = EstEricMapping.parse_obj(create_est(correct_form_data=True).est_data)
        with patch('erica.erica_legacy.request_processing.eric_mapper', MagicMock(return_value=eric_mapped_object)), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.est_mapping.check_and_generate_entries') as generate_entries, \
                patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.erica_legacy.request_processing.requests_controller.EstRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_est_xml'):
            EstRequestController(create_est(correct_form_data=True)).process()

        assert generate_entries.mock_calls == [call(eric_mapped_object.__dict__)]

    def test_pyeric_controller_is_initialised_with_correct_arguments(self):
        est_request = EstRequestController(create_est(correct_form_data=True))

        xml = '<xml></xml>'

        with patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.__init__',
                   MagicMock(return_value=None)) \
                as pyeric_controller_init, \
                patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.erica_legacy.request_processing.requests_controller.EstRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.'
                      'generate_full_est_xml', MagicMock(return_value=xml)):
            est_request.process()

            pyeric_controller_init.assert_called_with(xml, TEST_EST_VERANLAGUNGSJAHR)

    def test_pyeric_get_eric_response_is_called(self):
        est_request = EstRequestController(create_est(correct_form_data=True))

        xml = '<xml></xml>'

        with patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.__init__',
                   MagicMock(return_value=None)), \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response') as pyeric_get_response, \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.est_mapping.check_and_generate_entries'), \
                patch('erica.erica_legacy.request_processing.requests_controller.EstRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.'
                      'generate_full_est_xml', MagicMock(return_value=xml)):
            est_request.process()

            pyeric_get_response.assert_called()

    def test_if_use_testmerker_env_false_and_test_idnr_then_create_xml_is_called_with_use_testmerker_set_true(self):
        correct_est = create_est(correct_form_data=True)
        correct_est.est_data.person_a_idnr = '04452397687'

        with patch('erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_est_xml') as generate_xml_fun, \
                patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.erica_legacy.request_processing.requests_controller.EstRequestController.generate_json'):
            est_request = EstRequestController(correct_est)
            est_request.process()

            self.assertTrue(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_use_testmerker_env_false_and_not_test_idnr_then_create_xml_is_called_with_use_testmerker_set_false(
            self):
        correct_est = create_est(correct_form_data=True)
        correct_est.est_data.person_a_idnr = '19327675747'

        with patch('erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_est_xml') as generate_xml_fun, \
                patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.erica_legacy.request_processing.requests_controller.EstRequestController.generate_json'):
            est_request = EstRequestController(correct_est)
            est_request.process()

            self.assertFalse(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_submission_without_tax_nr_then_generate_vorsatz_without_tax_nr_is_called(self):
        empfaenger = '9198'
        correct_est = create_est(correct_form_data=True, with_tax_number=False)
        correct_est.est_data.bufa_nr = empfaenger

        with patch(
                'erica.erica_legacy.request_processing.requests_controller.generate_vorsatz_without_tax_number') as generate_vorsatz_without_tax_number, \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_est_xml') as generate_xml_fun, \
                patch('erica.erica_legacy.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.erica_legacy.request_processing.requests_controller.EstRequestController.generate_json'):
            est_request = EstRequestController(correct_est)
            est_request.process()

            generate_vorsatz_without_tax_number.assert_called()
            self.assertEqual(empfaenger, generate_xml_fun.call_args.args[-1])  # empfaenger should be the last args

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_full_form_then_return_not_none_response(self):
        est_request = EstRequestController(create_est(correct_form_data=True))

        response = est_request.process()

        self.assertIsNotNone(response)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_submission_without_tax_nr_then_return_not_none_response(self):
        est_request = EstRequestController(create_est(correct_form_data=True, with_tax_number=False))

        response = est_request.process()

        self.assertIsNotNone(response)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_full_form_and_include_elster_responses_then_return_response_only_with_correct_keys(self):
        expected_keys = ['transferticket', 'pdf', 'eric_response', 'server_response']

        est_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=True)

        response = est_request.process()

        self.assertEqual(set(expected_keys), set(response.keys()))

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_full_form_and_not_include_elster_responses_then_return_response_with_correct_keys(self):
        expected_keys = ['transferticket', 'pdf']

        est_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=False)

        response = est_request.process()

        self.assertEqual(expected_keys, list(response.keys()))


class TestEstRequestGenerateJson(unittest.TestCase):

    def setUp(self):
        self.expected_transferticket = 'J-KLAPAUCIUS'
        self.pdf_bytes = b"Our lives begin the day we become silent about things that matter"
        self.expected_pdf = base64.b64encode(self.pdf_bytes).decode('utf-8')
        self.expected_eric_response = "We are now faced with the fact that tomorrow is today."
        response_with_correct_transferticket = replace_text_in_xml(
            read_text_from_sample('sample_est_response_server.xml'),
            'TransferTicket', self.expected_transferticket)
        self.expected_server_response = response_with_correct_transferticket

    def test_if_id_given_and_include_true_then_return_json_with_correct_info(self):
        expected_output = {
            'transferticket': self.expected_transferticket,
            'pdf': self.expected_pdf,
            'eric_response': self.expected_eric_response,
            'server_response': self.expected_server_response
        }
        est_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=True)
        pyeric_response = PyericResponse(self.expected_eric_response,
                                         self.expected_server_response,
                                         self.pdf_bytes)
        actual_response = est_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_id_given_and_include_false_then_return_json_with_correct_info(self):
        expected_output = {
            'transferticket': self.expected_transferticket,
            'pdf': self.expected_pdf
        }
        est_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=False)
        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response,
                                         self.pdf_bytes)

        actual_response = est_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)


class TestUnlockCodeRequestInit(unittest.TestCase):

    def test_if_idnr_given_then_set_idnr_as_attribute_correctly(self):
        expected_idnr = "09952417688"
        created_request = UnlockCodeRequestController(UnlockCodeRequestData(idnr=expected_idnr, dob=date(1969, 7, 20)))

        self.assertEqual(expected_idnr, created_request.input_data.tax_id_number)

    def test_if_no_include_param_given_then_set_include_false(self):
        created_request = UnlockCodeRequestController(UnlockCodeRequestData(idnr="09952417688", dob=date(1969, 7, 20)))

        self.assertFalse(created_request.include_elster_responses)

    def test_if_include_param_true_then_set_include_true(self):
        created_request = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr="09952417688",
            dob=date(1969, 7, 20)),
            include_elster_responses=True)
        self.assertTrue(created_request.include_elster_responses)


class TestUnlockCodeRequestProcess(unittest.TestCase):

    def setUp(self):
        self.unlock_request_with_valid_input = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr="19327675747",
            dob=date(1985, 1, 1)))

        self.unlock_request_with_valid_input_with_test_idnr = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr='04452397687',
            dob=date(1985, 1, 1)))

    def test_pyeric_controller_is_initialised_with_correct_arguments(self):
        xml = '<xml></xml>'

        with patch('erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.__init__',
                   MagicMock(return_value=None)) \
                as pyeric_controller_init, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.'
                      'generate_full_vast_request_xml', MagicMock(return_value=xml)):
            self.unlock_request_with_valid_input.process()

            pyeric_controller_init.assert_called_with(xml)

    def test_pyeric_get_eric_response_is_called(self):
        xml = '<xml></xml>'

        with patch('erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.__init__',
                   MagicMock(return_value=None)), \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.get_eric_response') \
                        as pyeric_controller_get_response, \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.'
                      'generate_full_vast_request_xml', MagicMock(return_value=xml)):
            self.unlock_request_with_valid_input.process()

            pyeric_controller_get_response.assert_called()

    def test_if_test_idnr_then_create_xml_is_called_with_use_testmerker_set_true(self):
        with patch(
                'erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_request_xml') as generate_xml_fun, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeRequestController.generate_json'):
            self.unlock_request_with_valid_input_with_test_idnr.process()

            self.assertTrue(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_not_test_idnr_then_create_xml_is_called_with_use_testmerker_set_false(self):
        with patch(
                'erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_request_xml') as generate_xml_fun, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeRequestController.generate_json'):
            self.unlock_request_with_valid_input.process()

            self.assertFalse(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_processed_called_then_elster_request_id_added_to_cache_list(self):
        elster_request_id = "1234"
        with patch('erica.erica_legacy.request_processing.requests_controller.TransferticketRequestController.process', MagicMock(return_value={'elster_request_id': elster_request_id})),\
            patch('erica.erica_legacy.request_processing.requests_controller.add_new_request_id_to_cache_list') as add_to_cache_list:
            self.unlock_request_with_valid_input.process()

            add_to_cache_list.assert_called_once_with(elster_request_id)


class TestUnlockCodeRequestGenerateFullXml(unittest.TestCase):

    def test_if_dob_date_given_then_call_generate_full_xml_with_unlock_code_eric_mapping(self):
        unlock_code_eric_mapping = UnlockCodeRequestEricMapper(tax_id_number="09952417688", date_of_birth=date(1969, 7, 20), tax_year="2021")

        created_request = UnlockCodeRequestController(UnlockCodeRequestData(idnr="09952417688", dob=date(1969, 7, 20)))

        with patch(
                'erica.erica_legacy.request_processing.requests_controller.elster_xml_generator.generate_full_vast_request_xml') as generate_full_xml:
            created_request.generate_full_xml(use_testmerker=True)

        assert generate_full_xml.mock_calls == [call(unlock_code_eric_mapping.__dict__, use_testmerker=True)]


class TestUnlockCodeRequestGenerateJson(unittest.TestCase):

    def setUp(self):
        self.expected_request_id = 'J-KLAPAUCIUS'
        self.expected_transferticket = 'Transferiato'
        self.expected_idnr = "123456789"
        self.expected_eric_response = "We are now faced with the fact that tomorrow is today."
        response_with_correct_transferticket = replace_text_in_xml(
            read_text_from_sample('sample_vast_request_response.xml'),
            'TransferTicket', self.expected_transferticket)
        self.expected_server_response = response_with_correct_transferticket

    def test_if_id_given_and_include_true_then_return_json_with_correct_info(self):
        expected_output = {
            'transferticket': self.expected_transferticket,
            'elster_request_id': self.expected_request_id,
            'idnr': self.expected_idnr,
            'eric_response': self.expected_eric_response,
            'server_response': self.expected_server_response
        }
        unlock_code_request = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr=self.expected_idnr,
            dob=date(1985, 1, 1)), include_elster_responses=True)

        with patch('erica.erica_legacy.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_id_given_and_include_false_then_return_json_with_correct_info(self):
        expected_output = {
            'transferticket': self.expected_transferticket,
            'elster_request_id': self.expected_request_id,
            'idnr': self.expected_idnr,
        }
        unlock_code_request = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr=self.expected_idnr,
            dob=date(1985, 1, 1)), include_elster_responses=False)

        with patch('erica.erica_legacy.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
            actual_response = unlock_code_request.generate_json(pyeric_response)

            self.assertEqual(expected_output, actual_response)

    def test_if_eric_process_successful_then_return_correct_elster_request_id(self):
        unlock_code_request = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr=self.expected_idnr,
            dob=date(1985, 1, 1)), include_elster_responses=False)
        expected_elster_request_id = "PizzaAndApplePie"

        successful_server_response = replace_text_in_xml(read_text_from_sample('sample_vast_request_response.xml', 'r'),
                                                         "AntragsID", expected_elster_request_id)

        pyeric_response = PyericResponse('eric_response', successful_server_response)
        actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_elster_request_id, actual_response['elster_request_id'])

    def test_if_eric_process_successful_then_return_correct_transferticket(self):
        unlock_code_request = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr=self.expected_idnr,
            dob=date(1985, 1, 1)), include_elster_responses=False)
        expected_transferticket = "PizzaAndNutCake"

        successful_server_response = replace_text_in_xml(read_text_from_sample('sample_vast_request_response.xml', 'r'),
                                                         "TransferTicket", expected_transferticket)

        pyeric_response = PyericResponse('eric_response', successful_server_response)
        actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_transferticket, actual_response['transferticket'])


class TestUnlockCodeActivationProcess(unittest.TestCase):
    def setUp(self):
        self.known_real_idnr = '19327675747'

        self.unlock_activation_with_valid_input = UnlockCodeActivationRequestController(UnlockCodeActivationData(
            idnr=self.known_real_idnr,
            unlock_code='1985-T67D-K89O',
            elster_request_id='42'))

        self.unlock_activation_with_valid_input_with_test_idnr = UnlockCodeActivationRequestController(
            UnlockCodeActivationData(
                idnr='04452397687',
                unlock_code='1985-T67D-K89O',
                elster_request_id='42'))

        self.unlock_activation_with_unknown_idnr = UnlockCodeActivationRequestController(UnlockCodeActivationData(
            idnr="123456789",
            unlock_code='1985-T67D-K89O',
            elster_request_id='42'))

        self.unlock_activation_without_idnr = UnlockCodeActivationRequestController(FreischaltCodeActivatePayload(
            freischalt_code='1985-T67D-K89O',
            elster_request_id='42'))

    def test_pyeric_controller_is_initialised_with_correct_argument(self):
        xml = '<xml></xml>'

        with patch('erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.__init__',
                   MagicMock(return_value=None)) \
                as pyeric_controller_init, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeActivationRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.'
                      'generate_full_vast_activation_xml', MagicMock(return_value=xml)):
            self.unlock_activation_with_valid_input.process()

            pyeric_controller_init.assert_called_with(xml)

    def test_pyeric_get_eric_response_is_called(self):
        xml = '<xml></xml>'

        with patch('erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.__init__',
                   MagicMock(return_value=None)), \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response') \
                        as pyeric_controller_get_response, \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeActivationRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_activation_xml',
                      MagicMock(return_value=xml)):
            self.unlock_activation_with_valid_input.process()

            pyeric_controller_get_response.assert_called()

    def test_if_test_idnr_then_create_xml_is_called_with_use_testmerker_set_true(self):
        with patch(
                'erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_activation_xml') as generate_xml_fun, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeActivationRequestController.generate_json'):
            self.unlock_activation_with_valid_input_with_test_idnr.process()

            self.assertTrue(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_not_test_idnr_then_create_xml_is_called_with_use_testmerker_set_false(self):
        with patch(
                'erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_activation_xml') as generate_xml_fun, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeActivationRequestController.generate_json'):
            self.unlock_activation_with_valid_input.process()

            self.assertFalse(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_idnr_and_request_needs_test_merker_then_create_xml_is_called_with_true(self):
        with patch(
                'erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_activation_xml') as generate_xml_fun, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeActivationRequestController.generate_json'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.request_needs_testmerker', MagicMock(return_value=True)):
            self.unlock_activation_without_idnr.process()

            self.assertTrue(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_idnr_and_request_needs_test_merker_then_create_xml_is_called_with_false(self):
        with patch(
                'erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_activation_xml') as generate_xml_fun, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeActivationRequestController.generate_json'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.request_needs_testmerker', MagicMock(return_value=False)):
            self.unlock_activation_without_idnr.process()

            self.assertFalse(generate_xml_fun.call_args.kwargs['use_testmerker'])


class TestUnlockCodeActivationGenerateJson(unittest.TestCase):

    def setUp(self):
        self.expected_idnr = "123456789"
        self.expected_request_id = 'J-KLAPAUCIUS'
        self.expected_transferticket = 'Transfiguration'
        self.expected_eric_response = "We are now faced with the fact that tomorrow is today."
        response_with_correct_transferticket = replace_text_in_xml(
            read_text_from_sample('sample_vast_activation_response.xml'),
            'TransferTicket', self.expected_transferticket)
        self.expected_server_response = response_with_correct_transferticket

    def test_if_id_given_and_include_true_then_return_json_with_correct_info(self):
        expected_output = {
            'transferticket': self.expected_transferticket,
            'elster_request_id': self.expected_request_id,
            'idnr': self.expected_idnr,
            'eric_response': self.expected_eric_response,
            'server_response': self.expected_server_response
        }
        unlock_code_request = UnlockCodeActivationRequestController(UnlockCodeActivationData(
            idnr=self.expected_idnr,
            unlock_code='1985-T67D-K89O',
            elster_request_id='42'), include_elster_responses=True)

        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.erica_legacy.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_id_given_and_include_false_then_return_json_with_correct_info(self):
        expected_output = {
            'transferticket': self.expected_transferticket,
            'elster_request_id': self.expected_request_id,
            'idnr': self.expected_idnr,
        }
        unlock_code_request = UnlockCodeActivationRequestController(UnlockCodeActivationData(
            idnr=self.expected_idnr,
            unlock_code='1985-T67D-K89O',
            elster_request_id='42'), include_elster_responses=False)
        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.erica_legacy.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_eric_process_successful_then_return_correct_transferticket(self):
        expected_transferticket = "PizzaAndNutCake"
        unlock_code_activation = UnlockCodeActivationRequestController(UnlockCodeActivationData(
            idnr=self.expected_idnr,
            unlock_code='1985-T67D-K89O',
            elster_request_id='42'), include_elster_responses=False)

        successful_server_response = replace_text_in_xml(read_text_from_sample('sample_vast_activation_response.xml'),
                                                         "TransferTicket", expected_transferticket)

        pyeric_response = PyericResponse('eric_response', successful_server_response)
        actual_response = unlock_code_activation.generate_json(pyeric_response)

        self.assertEqual(expected_transferticket, actual_response['transferticket'])


class TestUnlockCodeRevocationProcess(unittest.TestCase):
    def setUp(self):
        self.known_real_idnr = '19327675747'

        self.unlock_revocation_with_valid_input = UnlockCodeRevocationRequestController(UnlockCodeRevocationData(
            idnr=self.known_real_idnr,
            elster_request_id='lookanotherrequestid'))

        self.unlock_revocation_with_valid_input_and_test_idnr = UnlockCodeRevocationRequestController(
            UnlockCodeRevocationData(
                idnr='04452397687',
                elster_request_id='lookanotherrequestid'))

        self.unlock_revocation_with_unknown_idnr = UnlockCodeRevocationRequestController(UnlockCodeRevocationData(
            idnr="123456789",
            elster_request_id='lookyetanotherrequestid'))

        self.unlock_revocation_without_idnr = UnlockCodeRevocationRequestController(FreischaltCodeRevocatePayload(
            elster_request_id='lookyetanotherrequestid'))

    def test_pyeric_controller_is_initialised_with_correct_arguments(self):
        xml = '<xml></xml>'

        with patch('erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.__init__',
                   MagicMock(return_value=None)) \
                as pyeric_controller_init, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeRevocationRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_revocation_xml',
                      MagicMock(return_value=xml)):
            self.unlock_revocation_with_valid_input.process()

            pyeric_controller_init.assert_called_with(xml)

    def test_pyeric_get_eric_response_is_called(self):
        xml = '<xml></xml>'

        with patch('erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.__init__',
                   MagicMock(return_value=None)), \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response') \
                        as pyeric_controller_get_response, \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeRevocationRequestController.generate_json'), \
                patch('erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_revocation_xml',
                      MagicMock(return_value=xml)):
            self.unlock_revocation_with_valid_input.process()

            pyeric_controller_get_response.assert_called()

    def test_if_test_idnr_then_create_xml_is_called_with_use_testmerker_set_true(self):
        with patch(
                'erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_revocation_xml') as generate_xml_fun, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeRevocationRequestController.generate_json'):
            self.unlock_revocation_with_valid_input_and_test_idnr.process()

            self.assertTrue(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_not_test_idnr_then_create_xml_is_called_with_use_testmerker_set_false(self):
        with patch(
                'erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_revocation_xml') as generate_xml_fun, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeRevocationRequestController.generate_json'):
            self.unlock_revocation_with_valid_input.process()

            self.assertFalse(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_idnr_and_request_needs_test_merker_then_create_xml_is_called_with_true(self):
        with patch(
                'erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_revocation_xml') as generate_xml_fun, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeRevocationRequestController.generate_json'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.request_needs_testmerker', MagicMock(return_value=True)):
            self.unlock_revocation_without_idnr.process()

            self.assertTrue(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_idnr_and_request_needs_test_merker_then_create_xml_is_called_with_false(self):
        with patch(
                'erica.erica_legacy.elster_xml.elster_xml_generator.generate_full_vast_revocation_xml') as generate_xml_fun, \
                patch(
                    'erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.UnlockCodeRevocationRequestController.generate_json'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.request_needs_testmerker', MagicMock(return_value=False)):
            self.unlock_revocation_without_idnr.process()

            self.assertFalse(generate_xml_fun.call_args.kwargs['use_testmerker'])


class TestUnlockCodeRevocationGenerateJson(unittest.TestCase):

    def setUp(self):
        self.expected_idnr = "123456789"
        self.expected_request_id = 'J-KLAPAUCIUS'
        self.expected_transferticket = 'The time is always right to do what is right.'
        self.expected_eric_response = "We are now faced with the fact that tomorrow is today."
        response_with_correct_transferticket = replace_text_in_xml(
            read_text_from_sample('sample_vast_revocation_response.xml'),
            'TransferTicket', self.expected_transferticket)
        self.expected_server_response = response_with_correct_transferticket

    def test_if_id_given_and_include_true_then_return_json_with_correct_info(self):
        expected_output = {
            'transferticket': self.expected_transferticket,
            'elster_request_id': self.expected_request_id,
            'eric_response': self.expected_eric_response,
            'server_response': self.expected_server_response
        }
        unlock_code_request = UnlockCodeRevocationRequestController(UnlockCodeRevocationData(
            idnr=self.expected_idnr,
            elster_request_id='lookanotherrequestid'), include_elster_responses=True)

        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.erica_legacy.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_id_given_and_include_false_then_return_json_with_correct_info(self):
        expected_output = {
            'transferticket': self.expected_transferticket,
            'elster_request_id': self.expected_request_id
        }
        unlock_code_request = UnlockCodeRevocationRequestController(UnlockCodeRevocationData(
            idnr=self.expected_idnr,
            elster_request_id='lookanotherrequestid'), include_elster_responses=False)

        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.erica_legacy.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_eric_process_successful_then_return_correct_transferticket(self):
        expected_transferticket = "PizzaAndNutCake"
        unlock_code_revocation = UnlockCodeRevocationRequestController(UnlockCodeRevocationData(idnr=self.expected_idnr,
                                                                                                elster_request_id='42'),
                                                                       include_elster_responses=False)

        successful_server_response = replace_text_in_xml(read_text_from_sample('sample_vast_revocation_response.xml'),
                                                         "TransferTicket", expected_transferticket)

        pyeric_response = PyericResponse('eric_response', successful_server_response)
        actual_response = unlock_code_revocation.generate_json(pyeric_response)

        self.assertEqual(expected_transferticket, actual_response['transferticket'])


class TestCheckTaxNumberRequestControllerProcess:

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_tax_number_is_valid_then_return_json_with_is_valid_true(self):
        state_abbreviation = "by"
        valid_tax_number = "19811310010"
        input_data = CheckTaxNumberPayload(state_abbreviation=state_abbreviation, tax_number=valid_tax_number)

        result = CheckTaxNumberRequestController(input_data).process()

        assert result == {'is_valid': True}

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_tax_number_is_invalid_then_return_json_with_is_valid_false(self):
        state_abbreviation = "by"
        invalid_tax_number = "19811310011"  # is invalid because of incorrect check sum (last digit should be 0)
        input_data = CheckTaxNumberPayload(state_abbreviation=state_abbreviation, tax_number=invalid_tax_number)

        result = CheckTaxNumberRequestController(input_data).process()

        assert result == {'is_valid': False}

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_generate_electronic_steuernummer_raises_invalid_bufa_nr_then_return_json_with_is_valid_false(self):
        state_abbreviation = "by"
        valid_tax_number = "19811310010"
        input_data = CheckTaxNumberPayload(state_abbreviation=state_abbreviation, tax_number=valid_tax_number)

        with patch('erica.erica_legacy.request_processing.requests_controller.generate_electronic_steuernummer', MagicMock(side_effect=InvalidBufaNumberError)):
            result = CheckTaxNumberRequestController(input_data).process()

        assert result == {'is_valid': False}


class TestGetBelegeRequestController(unittest.TestCase):
    def setUp(self):
        self.idnr = '04452397687'
        self.input_data = GetAddressData.parse_obj({'idnr': self.idnr})
        self.request_xml = '<Anfrage>'
        self.sample_beleg_ids = ['vg3071ovc201t97gdvyy1851qrutaheh']
        self.sample_encrypted_belege = [read_text_from_sample('sample_encrypted_beleg.xml')]

    def test_get_beleg_ids_calls_correct_pyeric_controller_with_correct_argument(self):
        with patch(
                'erica.erica_legacy.request_processing.requests_controller.BelegIdRequestPyericProcessController.__init__',
                MagicMock(return_value=None)) as pyeric_controller_mock, \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_ids_request_xml',
                    MagicMock(return_value=self.request_xml)), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.BelegIdRequestPyericProcessController.get_eric_response'), \
                patch('erica.erica_legacy.request_processing.requests_controller.get_relevant_beleg_ids'):
            GetBelegeRequestController(self.input_data)._request_beleg_ids()
            pyeric_controller_mock.assert_called_once_with(self.request_xml)

    def test_get_beleg_ids_calls_get_eric_response(self):
        with patch(
                'erica.erica_legacy.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_ids_request_xml',
                MagicMock(return_value=self.request_xml)), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.BelegIdRequestPyericProcessController.get_eric_response') as fun_get_eric_response, \
                patch('erica.erica_legacy.request_processing.requests_controller.get_relevant_beleg_ids'):
            GetBelegeRequestController(self.input_data)._request_beleg_ids()
            fun_get_eric_response.assert_called_once()

    def test_get_beleg_ids_returns_relevant_beleg_ids_from_pyeric_response_for_given_beleg_art(self):
        mocked_pyeric_response = PyericResponse('', read_text_from_sample('sample_beleg_id_response.xml'))
        with patch(
                'erica.erica_legacy.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_ids_request_xml',
                MagicMock(return_value=self.request_xml)), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.BelegIdRequestPyericProcessController.get_eric_response',
                    MagicMock(return_value=mocked_pyeric_response)):
            request_controller = GetBelegeRequestController(self.input_data)
            request_controller._NEEDED_BELEG_ART = 'VaSt_Pers1'
            returned_beleg_ids = request_controller._request_beleg_ids()
            self.assertEqual(['vg3071ovc201t97gdvyy1851qrutaheh'], returned_beleg_ids)

    def test_request_encrypted_belege_calls_correct_pyeric_controller_with_correct_argument(self):
        with patch(
                'erica.erica_legacy.request_processing.requests_controller.BelegRequestPyericProcessController.__init__',
                MagicMock(return_value=None)) as pyeric_controller_mock, \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_request_xml',
                    MagicMock(return_value=self.request_xml)), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.BelegRequestPyericProcessController.get_eric_response'), \
                patch('erica.erica_legacy.request_processing.requests_controller.get_elements_text_from_xml'):
            GetBelegeRequestController(self.input_data)._request_encrypted_belege(self.sample_beleg_ids)
            pyeric_controller_mock.assert_called_once_with(self.request_xml)

    def test_request_encrypted_belege_calls_get_eric_response(self):
        with patch(
                'erica.erica_legacy.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_request_xml',
                MagicMock(return_value=self.request_xml)), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.BelegRequestPyericProcessController.get_eric_response') as fun_get_eric_response, \
                patch('erica.erica_legacy.request_processing.requests_controller.get_elements_text_from_xml'):
            GetBelegeRequestController(self.input_data)._request_encrypted_belege(self.sample_beleg_ids)
            fun_get_eric_response.assert_called_once()

    def test_request_encrypted_belege_returns_relevant_beleg_ids_from_pyeric_response(self):
        sample_encrypted_beleg = 'SpeakFriendAndEnter'
        sample_response_with_encrypted_beleg = replace_text_in_xml(
            read_text_from_sample('sample_encrypted_beleg_response.xml'), 'Datenpaket',
            sample_encrypted_beleg)
        mocked_pyeric_response = PyericResponse('', sample_response_with_encrypted_beleg)
        with patch(
                'erica.erica_legacy.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_request_xml',
                MagicMock(return_value=self.request_xml)), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.BelegRequestPyericProcessController.get_eric_response',
                    MagicMock(return_value=mocked_pyeric_response)):
            request_controller = GetBelegeRequestController(self.input_data)
            returned_encrypted_belege = request_controller._request_encrypted_belege(self.sample_beleg_ids)
            self.assertEqual([sample_encrypted_beleg], returned_encrypted_belege)

    def test_request_decrypted_belege_calls_get_decrypted_belege_of_correct_pyeric_controller(self):
        with patch(
                'erica.erica_legacy.request_processing.requests_controller.DecryptBelegePyericController.get_decrypted_belege') as fun_get_eric_response, \
                patch('erica.erica_legacy.request_processing.requests_controller.get_belege_xml'):
            GetBelegeRequestController(self.input_data)._request_decrypted_belege(self.sample_encrypted_belege)
            fun_get_eric_response.assert_called_once_with(self.sample_encrypted_belege)

    def test_request_decrypted_belege_returns_decrypted_belege(self):
        sample_beleg_xml = read_text_from_sample('sample_decrypted_beleg_response.xml')
        with patch(
                'erica.erica_legacy.request_processing.requests_controller.DecryptBelegePyericController.get_decrypted_belege',
                MagicMock(return_value=[sample_beleg_xml])):
            request_controller = GetBelegeRequestController(self.input_data)
            returned_decrypted_belege_xml = request_controller._request_decrypted_belege(
                self.sample_encrypted_belege)
            len_of_namespace_intro = len(
                '<?xml version="1.0" encoding="ISO-8859-15" ?><VaSt_RBM xmlns="http://finkonsens.de/elster/elstervast/vastrbm/v202001" version="202001">')
            self.assertIn(sample_beleg_xml[len_of_namespace_intro], returned_decrypted_belege_xml)
            self.assertIn('<Belege', returned_decrypted_belege_xml)


class TestGetAddressProcess(unittest.TestCase):
    def setUp(self):
        self.known_real_idnr = '02293417683'

        self.get_address_with_valid_input = GetAddressRequestController(GetAddressData(idnr=self.known_real_idnr))

    def test_calls_get_relevant_beleg_ids_with_correct_arguments(self):
        mock_server_response = 'server_response'
        mock_pyeric_response = PyericResponse('', mock_server_response)
        with patch(
                'erica.erica_legacy.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_ids_request_xml'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.BelegIdRequestPyericProcessController.get_eric_response',
                    MagicMock(return_value=mock_pyeric_response)), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.get_relevant_beleg_ids') as fun_get_beleg_ids, \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.GetBelegeRequestController._request_encrypted_belege'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.GetBelegeRequestController._request_decrypted_belege'), \
                patch(
                    'erica.erica_legacy.request_processing.requests_controller.GetAddressRequestController.generate_json'):
            self.get_address_with_valid_input.process()
            fun_get_beleg_ids.assert_called_once_with(mock_server_response, ['VaSt_Pers1'])


class TestGetAddressGenerateJson(unittest.TestCase):

    def setUp(self):
        self.expected_idnr = "123456789"
        self.expected_address = '<Str>Musterstraße</Str>'
        self.expected_eric_response = "We are now faced with the fact that tomorrow is today."
        response_with_correct_address = replace_subtree_in_xml(read_text_from_sample('sample_beleg_address_response.xml'),
                                                                   'AdrKette', self.expected_address)
        self.expected_server_response = response_with_correct_address

    def test_if_id_given_and_include_true_then_return_json_with_correct_info(self):
        expected_output = {
            'address': self.expected_address,
            'eric_response': self.expected_eric_response,
            'server_response': self.expected_server_response
        }
        get_address_request = GetAddressRequestController(GetAddressData(idnr=self.expected_idnr),
                                                          include_elster_responses=True)

        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.erica_legacy.request_processing.requests_controller.get_address_from_xml',
                   MagicMock(return_value=self.expected_address)):
            actual_response = get_address_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_id_given_and_include_false_then_return_json_with_correct_info(self):
        expected_output = {
            'address': self.expected_address
        }
        unlock_code_request = GetAddressRequestController(GetAddressData(idnr=self.expected_idnr),
                                                          include_elster_responses=False)

        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.erica_legacy.request_processing.requests_controller.get_address_from_xml',
                   MagicMock(return_value=self.expected_address)):
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)
