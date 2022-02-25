import base64

from erica.pyeric.pyeric_response import PyericResponse
from erica.request_processing.requests_controller import TransferTicketRequestController


class GrundsteuerRequestController(TransferTicketRequestController):
    def _is_testmerker_used(self):
        return True

    def generate_full_xml(self, use_testmerker):
        pass  # TODO

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response['pdf'] = base64.b64encode(pyeric_response.pdf)
        return response

    def process(self):
        """
        Processing the request_data will extract information from the data, perform necessary operations with the
        data and return the correct json result
        """
        # TODO
        xml = self.generate_full_xml(self._is_testmerker_used())

        return {"request": "successful"}
