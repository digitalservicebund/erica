import base64

from erica.config import get_settings
from erica.worker.elster_xml.common.electronic_steuernummer import generate_electronic_steuernummer
from erica.worker.elster_xml.elster_xml_generator import get_belege_xml, generate_vorsatz_without_tax_number, \
    generate_vorsatz_with_tax_number
from erica.worker.elster_xml.xml_parsing.elster_specifics_xml_parsing import get_antrag_id_from_xml, \
    get_transferticket_from_xml, get_address_from_xml, get_relevant_beleg_ids
from erica.worker.pyeric.eric_errors import InvalidBufaNumberError
from erica.worker.pyeric.pyeric_response import PyericResponse
from erica.worker.elster_xml import est_mapping, elster_xml_generator

from erica.worker.elster_xml.xml_parsing.erica_xml_parsing import get_elements_text_from_xml

from erica.worker.pyeric.pyeric_controller import EstPyericProcessController, \
    EstValidationPyericProcessController, \
    UnlockCodeActivationPyericProcessController, UnlockCodeRequestPyericProcessController, \
    UnlockCodeRevocationPyericProcessController, \
    DecryptBelegePyericController, BelegIdRequestPyericProcessController, \
    BelegRequestPyericProcessController, CheckTaxNumberPyericController
from erica.worker.pyeric.check_elster_request_id import add_new_request_id_to_cache_list, \
    request_needs_testmerker, tax_id_number_is_test_id_number
from erica.worker.request_processing.eric_mapper import EstEricMapping, UnlockCodeRequestEricMapper
from erica.worker.request_processing.erica_input.v1.erica_input import UnlockCodeRequestData, EstData


class EricaRequestController(object):
    """
    Generic class to handle any request to the eric api. That is processing the input data,
    performing the needed procedures and generating the response. Any request should inherit from this function.
    """

    _PYERIC_CONTROLLER = None

    def __init__(self, input_data, include_elster_responses: bool = False):
        self.input_data = input_data
        self.include_elster_responses: bool = include_elster_responses

    def process(self):
        """
        Processing the request_data will extract information from the data, perform necessary operations with the
        data and return the correct json result
        """
        xml = self.generate_full_xml(self._is_testmerker_used())

        pyeric_controller = self._PYERIC_CONTROLLER(xml)
        pyeric_response = pyeric_controller.get_eric_response()

        return self.generate_json(pyeric_response)

    def generate_full_xml(self, use_testmerker):
        raise NotImplementedError

    def _is_testmerker_used(self):
        return tax_id_number_is_test_id_number(self.input_data.tax_id_number)

    def generate_json(self, pyeric_response: PyericResponse):
        response = {}
        if self.include_elster_responses:
            response['eric_response'] = pyeric_response.eric_response
            response['server_response'] = pyeric_response.server_response
        return response


class TransferticketRequestController(EricaRequestController):

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        if pyeric_response.server_response:
            response['transferticket'] = get_transferticket_from_xml(pyeric_response.server_response)
        return response


class EstValidationRequestController(TransferticketRequestController):
    _PYERIC_CONTROLLER = EstValidationPyericProcessController

    def __init__(self, input_data: EstData, include_elster_responses: bool = False):
        super().__init__(input_data, include_elster_responses)

    def _is_testmerker_used(self):
        return tax_id_number_is_test_id_number(self.input_data.est_data.person_a_idnr)

    def process(self):
        # Translate our form data structure into the fields from
        # the Elster specification (see `Jahresdokumentation_10_2021.xml`)
        est_with_eric_mapping = EstEricMapping.parse_obj(self.input_data.est_data)
        fields = est_mapping.check_and_generate_entries(est_with_eric_mapping.__dict__)

        common_vorsatz_args = (
            self.input_data.meta_data.year,
            self.input_data.est_data.person_a_idnr,
            self.input_data.est_data.person_b_idnr,
            self.input_data.est_data.person_a_first_name,
            self.input_data.est_data.person_a_last_name,
            self.input_data.est_data.person_a_street,
            self.input_data.est_data.person_a_street_number,
            self.input_data.est_data.person_a_plz,
            self.input_data.est_data.person_a_town
        )
        if self.input_data.est_data.submission_without_tax_nr:
            empfaenger = self.input_data.est_data.bufa_nr
            vorsatz = generate_vorsatz_without_tax_number(*common_vorsatz_args)
        else:
            electronic_steuernummer = generate_electronic_steuernummer(
                self.input_data.est_data.steuernummer,
                self.input_data.est_data.bundesland,
                use_testmerker=self._is_testmerker_used())
            vorsatz = generate_vorsatz_with_tax_number(electronic_steuernummer, *common_vorsatz_args)
            empfaenger = electronic_steuernummer[:4]

        xml = elster_xml_generator.generate_full_est_xml(fields, vorsatz, self.input_data.meta_data.year, empfaenger,
                                                         use_testmerker=self._is_testmerker_used())

        pyeric_controller = self._PYERIC_CONTROLLER(xml, self.input_data.meta_data.year)
        pyeric_response = pyeric_controller.get_eric_response()

        return self.generate_json(pyeric_response)


class EstRequestController(EstValidationRequestController):
    _PYERIC_CONTROLLER = EstPyericProcessController

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response['pdf'] = (base64.b64encode(pyeric_response.pdf)).decode('utf-8')
        return response


class UnlockCodeRequestController(TransferticketRequestController):
    _PYERIC_CONTROLLER = UnlockCodeRequestPyericProcessController

    def __init__(self, input_data: UnlockCodeRequestData, include_elster_responses: bool = False):
        super().__init__(input_data, include_elster_responses)

    def process(self):
        json_response = super().process()
        add_new_request_id_to_cache_list(json_response.get('elster_request_id'))
        return json_response

    def generate_full_xml(self, use_testmerker):
        return elster_xml_generator.generate_full_vast_request_xml(
            UnlockCodeRequestEricMapper.parse_obj(self.input_data).__dict__,
            use_testmerker=use_testmerker)

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)

        response["elster_request_id"] = get_antrag_id_from_xml(pyeric_response.server_response)
        response["idnr"] = self.input_data.tax_id_number

        return response


class UnlockCodeActivationRequestController(TransferticketRequestController):
    _PYERIC_CONTROLLER = UnlockCodeActivationPyericProcessController

    def _is_testmerker_used(self):
        if self.input_data.tax_id_number:
            return tax_id_number_is_test_id_number(self.input_data.tax_id_number)
        else:
            return request_needs_testmerker(self.input_data.elster_request_id)

    def generate_full_xml(self, use_testmerker):
        return elster_xml_generator.generate_full_vast_activation_xml(self.input_data.__dict__,
                                                                      use_testmerker=use_testmerker)

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response["elster_request_id"] = get_antrag_id_from_xml(pyeric_response.server_response)
        response["idnr"] = self.input_data.tax_id_number
        return response


class UnlockCodeRevocationRequestController(TransferticketRequestController):
    _PYERIC_CONTROLLER = UnlockCodeRevocationPyericProcessController

    def _is_testmerker_used(self):
        if self.input_data.tax_id_number:
            return tax_id_number_is_test_id_number(self.input_data.tax_id_number)
        else:
            return request_needs_testmerker(self.input_data.elster_request_id)

    def generate_full_xml(self, use_testmerker):
        return elster_xml_generator.generate_full_vast_revocation_xml(self.input_data.__dict__,
                                                                      use_testmerker=use_testmerker)

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response["elster_request_id"] = get_antrag_id_from_xml(pyeric_response.server_response)
        return response


class CheckTaxNumberRequestController(EricaRequestController):
    """This handles any request that wants to check if a tax number is valid"""

    def process(self):
        try:
            full_tax_number = CheckTaxNumberRequestController._generate_tax_number(
                self.input_data.state_abbreviation.upper(), self.input_data.tax_number)
        except InvalidBufaNumberError:
            return CheckTaxNumberRequestController.generate_json(False)
        result = CheckTaxNumberPyericController.get_eric_response(full_tax_number)
        return CheckTaxNumberRequestController.generate_json(result)

    @staticmethod
    def _generate_tax_number(state_abbreviation, tax_number):
        return generate_electronic_steuernummer(
            tax_number,
            state_abbreviation,
            use_testmerker=get_settings().use_testmerker)

    @staticmethod
    def generate_json(valid):
        response = {}
        response['is_valid'] = valid

        return response


class GetBelegeRequestController(EricaRequestController):
    """This serves as an abstract class to implement all request controllers that request belege.
    Override the following constants in the subclasses."""
    _BELEG_ID_REQUEST_PYERIC_CONTROLLER = BelegIdRequestPyericProcessController
    _BELEG_REQUEST_PYERIC_CONTROLLER = BelegRequestPyericProcessController
    _NEEDED_BELEG_ART = None

    def process(self):
        beleg_ids = self._request_beleg_ids()
        encrypted_belege = self._request_encrypted_belege(beleg_ids)
        belege_xml = self._request_decrypted_belege(encrypted_belege)

        response_xml = PyericResponse('', belege_xml)
        return self.generate_json(response_xml)

    def _request_beleg_ids(self):
        get_beleg_id_xml = elster_xml_generator.generate_full_vast_beleg_ids_request_xml(
            self.input_data.__dict__,
            use_testmerker=self._is_testmerker_used())
        pyeric_response = self._BELEG_ID_REQUEST_PYERIC_CONTROLLER(get_beleg_id_xml).get_eric_response()
        return get_relevant_beleg_ids(pyeric_response.server_response, self._NEEDED_BELEG_ART)

    def _request_encrypted_belege(self, beleg_ids):
        user_data = {'idnr': self.input_data.tax_id_number}
        get_beleg_xml = elster_xml_generator.generate_full_vast_beleg_request_xml(user_data, beleg_ids)
        pyeric_response = self._BELEG_REQUEST_PYERIC_CONTROLLER(get_beleg_xml).get_eric_response()

        encrypted_belege_xml = pyeric_response.server_response
        return get_elements_text_from_xml(encrypted_belege_xml, 'Datenpaket')

    def _request_decrypted_belege(self, encrypted_belege):
        decrypted_belege = DecryptBelegePyericController().get_decrypted_belege(encrypted_belege)
        return get_belege_xml(decrypted_belege)


class GetAddressRequestController(GetBelegeRequestController):
    _NEEDED_BELEG_ART = ['VaSt_Pers1']

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response['address'] = get_address_from_xml(pyeric_response.server_response)
        return response
