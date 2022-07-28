import os
import sys
from xml.etree.ElementTree import Element

from erica.erica_legacy.elster_xml import elster_xml_generator
from erica.erica_legacy.elster_xml.xml_parsing.erica_xml_parsing import remove_declaration_and_namespace, \
    get_elements_from_xml_element, get_elements_text_from_xml_element
from erica.erica_legacy.pyeric.eric_errors import EricProcessNotSuccessful
from erica.erica_legacy.pyeric.pyeric_controller import PermitListingPyericProcessController


def get_idnr_status_list():
    xml = elster_xml_generator.generate_full_vast_list_xml()

    try:
        result = PermitListingPyericProcessController(xml=xml).get_eric_response()
    except EricProcessNotSuccessful as e:
        print("Error occurred")
        print(e.generate_error_response(True))
        return

    xml = remove_declaration_and_namespace(result.server_response)
    datenteil_xml = xml.find('.//DatenTeil')
    return datenteil_xml


def get_status_of_idnr(idnr, xml: Element):
    antraege = get_elements_from_xml_element(xml, "Antrag")

    matching_antraege = []
    for antrag in antraege:
        antrag_idnrs = get_elements_text_from_xml_element(antrag, "DateninhaberIdNr")
        if (antrag_idnrs[0] == idnr):
            matching_antraege.append(antrag)

    for matching_antrag in matching_antraege:
        print(elster_xml_generator._pretty(matching_antrag))


if __name__ == "__main__":
    os.chdir('../')  # Change the working directory to be able to find the eric binaries
    requested_idnr = sys.argv[1] if len(sys.argv) > 1 else None
    permit_list = get_idnr_status_list()
    if requested_idnr:
        get_status_of_idnr(requested_idnr, permit_list)
    else:
        print(elster_xml_generator._pretty(permit_list))
