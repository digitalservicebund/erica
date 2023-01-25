from erica.worker.elster_xml import elster_xml_generator
from erica.worker.elster_xml.xml_parsing.erica_xml_parsing import remove_declaration_and_namespace
from erica.worker.huey import huey
from erica.worker.pyeric.eric_errors import EricProcessNotSuccessful
from erica.worker.pyeric.pyeric_controller import PermitListingPyericProcessController


@huey.task(expires=480)
def get_idnr_status_list_with_huey(idnr=None, status=None, start_date=None, end_date=None, show_xml=False):
    return get_idnr_status_list(idnr, status, start_date, end_date, show_xml)


def get_idnr_status_list(idnr=None, status=None, start_date=None, end_date=None, show_xml=False):
    xml = elster_xml_generator.generate_full_vast_list_xml(specific_idnr=idnr, specific_status=status,start_date=start_date, end_date=end_date)
    printable_result = ""
    if show_xml:
        printable_result += f"{xml}\n---------------"
    permit_list = _get_eric_response_datenteil(xml)
    if permit_list:
        printable_result += f"\n{elster_xml_generator._pretty(permit_list)}"
    else:
        printable_result += "No list returned"

    return printable_result


def _get_eric_response_datenteil(xml):
    try:
        result = PermitListingPyericProcessController(xml=xml).get_eric_response()
    except EricProcessNotSuccessful as e:
        print("Error occurred")
        print(e.generate_error_response(True))
        return

    xml = remove_declaration_and_namespace(result.server_response)
    return xml.find('.//DatenTeil')