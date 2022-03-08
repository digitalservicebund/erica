import base64

from lib.pyeric.pyeric_controller import GrundsteuerPyericProcessController
from lib.pyeric.pyeric_response import PyericResponse
from src.application.EricRequestProcessing.requests_controller import TransferTicketRequestController
from src.domain.ElsterXml.common.transfer_header import add_transfer_header
from src.domain.ElsterXml.common.xml_conversion import convert_object_to_xml
from src.domain.ElsterXml.grundsteuer.elster_data_representation import get_full_grundsteuer_data_representation
from src.domain.ElsterXml.transfer_header_fields import get_grundsteuer_th_fields


class GrundsteuerRequestController(TransferTicketRequestController):
    _PYERIC_CONTROLLER = GrundsteuerPyericProcessController

    def _is_testmerker_used(self):
        # TODO revisit this
        return True

    def generate_full_xml(self, use_testmerker):
        """ Constructs the complete XML for the grundsteuer use case. """
        grundsteuer_data_representation = get_full_grundsteuer_data_representation(self.input_data)
        grundsteuer_xml_without_th = convert_object_to_xml(grundsteuer_data_representation)
        complete_xml = add_transfer_header(grundsteuer_xml_without_th,
                                           get_grundsteuer_th_fields(use_testmerker))
        return complete_xml

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response['pdf'] = base64.b64encode(pyeric_response.pdf)
        return response
