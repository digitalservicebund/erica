import base64

from erica.elster_xml.common.transfer_header import add_transfer_header
from erica.elster_xml.grundsteuer.elster_data_representation import get_full_grundsteuer_data_representation
from erica.elster_xml.common.xml_conversion import convert_object_to_xml
from erica.elster_xml.transfer_header_fields import get_grundsteuer_th_fields
from erica.pyeric.pyeric_controller import GrundsteuerPyericProcessController
from erica.pyeric.pyeric_response import PyericResponse
from erica.request_processing.requests_controller import TransferTicketRequestController


class GrundsteuerRequestController(TransferTicketRequestController):
    _PYERIC_CONTROLLER = GrundsteuerPyericProcessController

    def _is_testmerker_used(self):
        return True

    def generate_full_xml(self, use_testmerker):
        grundsteuer_data_representation = get_full_grundsteuer_data_representation(self.input_data)
        grundsteuer_xml_without_th = convert_object_to_xml(grundsteuer_data_representation)
        complete_xml = add_transfer_header(grundsteuer_xml_without_th,
                                           get_grundsteuer_th_fields(self._is_testmerker_used()))
        return complete_xml

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response['pdf'] = base64.b64encode(pyeric_response.pdf)
        return response
