import os

import click

from erica.worker.elster_xml import elster_xml_generator
from erica.worker.elster_xml.xml_parsing.erica_xml_parsing import remove_declaration_and_namespace
from erica.worker.pyeric.eric_errors import EricProcessNotSuccessful
from erica.worker.pyeric.pyeric_controller import PermitListingPyericProcessController


def _get_eric_response_datenteil(xml):
    try:
        result = PermitListingPyericProcessController(xml=xml).get_eric_response()
    except EricProcessNotSuccessful as e:
        print("Error occurred")
        print(e.generate_error_response(True))
        return

    xml = remove_declaration_and_namespace(result.server_response)
    return xml.find('.//DatenTeil')


@click.command()
@click.option('--idnr')
@click.option('--status', multiple=True)
@click.option('--start_date')
@click.option('--end_date')
def get_idnr_status_list(idnr=None, status=None, start_date=None, end_date=None):
    xml = elster_xml_generator.generate_full_vast_list_xml(specific_idnr=idnr, specific_status=status,start_date=start_date, end_date=end_date)
    permit_list = _get_eric_response_datenteil(xml)
    if permit_list:
        print(elster_xml_generator._pretty(permit_list))
    else:
        print("No list returned")


if __name__ == "__main__":
    os.chdir('../')  # Change the working directory to be able to find the eric binaries
    get_idnr_status_list()
