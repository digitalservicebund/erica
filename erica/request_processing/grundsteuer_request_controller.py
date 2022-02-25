import base64

from erica.elster_xml.grundsteuer.elster_data_representation import get_elster_grundsteuer_data
from erica.elster_xml.grundsteuer.xml_converter import convert_to_grundsteuer_xml
from erica.pyeric.pyeric_controller import GrundsteuerPyericProcessController
from erica.pyeric.pyeric_response import PyericResponse
from erica.request_processing.requests_controller import TransferTicketRequestController


class GrundsteuerRequestController(TransferTicketRequestController):
    _PYERIC_CONTROLLER = GrundsteuerPyericProcessController

    def _is_testmerker_used(self):
        return True

    def generate_full_xml(self, use_testmerker):
        elster_data_representation = get_elster_grundsteuer_data(self.input_data)
        return convert_to_grundsteuer_xml(elster_data_representation)

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response['pdf'] = base64.b64encode(pyeric_response.pdf)
        return response


