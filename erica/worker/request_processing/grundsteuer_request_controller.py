import base64

from erica.config import get_settings
from erica.worker.pyeric.check_elster_request_id import tax_id_number_is_test_id_number
from erica.worker.pyeric.pyeric_controller import GrundsteuerPyericProcessController
from erica.worker.pyeric.pyeric_response import PyericResponse
from erica.worker.elster_xml.common.transfer_header import add_transfer_header
from erica.worker.elster_xml.common.xml_conversion import convert_object_to_xml
from erica.worker.elster_xml.grundsteuer.elster_data_representation import get_full_grundsteuer_data_representation
from erica.worker.elster_xml.transfer_header_fields import get_grundsteuer_th_fields
from erica.worker.request_processing.requests_controller import TransferticketRequestController


class GrundsteuerRequestController(TransferticketRequestController):
    _PYERIC_CONTROLLER = GrundsteuerPyericProcessController

    def _is_testmerker_used(self):
        if len(self.input_data.eigentuemer.person) >= 1 and self.input_data.eigentuemer.person[0].steuer_id:
            return tax_id_number_is_test_id_number(self.input_data.eigentuemer.person[0].steuer_id)
        return get_settings().use_testmerker

    def generate_full_xml(self, use_testmerker):
        """ Constructs the complete XML for the grundsteuer use case. """
        grundsteuer_data_representation = get_full_grundsteuer_data_representation(self.input_data)
        grundsteuer_xml_without_th = convert_object_to_xml(grundsteuer_data_representation)
        complete_xml = add_transfer_header(grundsteuer_xml_without_th,
                                           get_grundsteuer_th_fields(use_testmerker))
        return complete_xml

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response['pdf'] = base64.b64encode(pyeric_response.pdf).decode('utf-8')
        return response
