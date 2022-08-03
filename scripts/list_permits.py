import os
import sys

from erica.erica_worker.elster_xml import elster_xml_generator
from erica.erica_worker.elster_xml.xml_parsing.erica_xml_parsing import remove_declaration_and_namespace
from erica.erica_worker.pyeric.eric_errors import EricProcessNotSuccessful
from erica.erica_worker.pyeric.pyeric_controller import PermitListingPyericProcessController


def _get_eric_response_datenteil(xml):
    try:
        result = PermitListingPyericProcessController(xml=xml).get_eric_response()
    except EricProcessNotSuccessful as e:
        print("Error occurred")
        print(e.generate_error_response(True))
        return

    xml = remove_declaration_and_namespace(result.server_response)
    return xml.find('.//DatenTeil')


def get_idnr_status_list():
    xml = elster_xml_generator.generate_full_vast_list_xml()
    return _get_eric_response_datenteil(xml)


def get_status_of_idnr(idnr):
    xml = elster_xml_generator.generate_full_vast_list_xml(specific_idnr=idnr)
    return _get_eric_response_datenteil(xml)


if __name__ == "__main__":
    os.chdir('../')  # Change the working directory to be able to find the eric binaries
    requested_idnr = sys.argv[1] if len(sys.argv) > 1 else None
    if requested_idnr:
        permit_list = get_status_of_idnr(requested_idnr)
    else:
        permit_list = get_idnr_status_list()
    if permit_list:
        print(elster_xml_generator._pretty(permit_list))
    else:
        print("No list returned")
