import base64

from erica.elster_xml.common.basic_xml import construct_basic_xml_object_representation
from erica.elster_xml.common.transfer_header import add_transfer_header
from erica.elster_xml.grundsteuer.elster_data_representation import get_elster_grundsteuer_data
from erica.elster_xml.grundsteuer.xml_converter import convert_to_grundsteuer_xml
from erica.elster_xml.transfer_header_fields import get_grundsteuer_th_fields
from erica.pyeric.pyeric_controller import GrundsteuerPyericProcessController
from erica.pyeric.pyeric_response import PyericResponse
from erica.request_processing.requests_controller import TransferTicketRequestController


class GrundsteuerRequestController(TransferTicketRequestController):
    _PYERIC_CONTROLLER = GrundsteuerPyericProcessController

    def _is_testmerker_used(self):
        return True

    def generate_full_xml(self, use_testmerker):
        elster_data_representation = get_elster_grundsteuer_data(self.input_data)
        xml_without_th = construct_basic_xml_object_representation('F', "1121", elster_data_representation, "TICKET")
        grundsteuer_xml = convert_to_grundsteuer_xml(xml_without_th)
        complete_xml = add_transfer_header(grundsteuer_xml, get_grundsteuer_th_fields(self._is_testmerker_used()))
        return complete_xml

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response['pdf'] = base64.b64encode(pyeric_response.pdf)
        return response


