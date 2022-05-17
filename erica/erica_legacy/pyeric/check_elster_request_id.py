from functools import lru_cache

from erica.erica_legacy.elster_xml import elster_xml_generator
from erica.erica_legacy.elster_xml.xml_parsing.erica_xml_parsing import remove_declaration_and_namespace
from erica.erica_legacy.pyeric.pyeric_controller import PermitListingPyericProcessController

SPECIAL_TESTMERKER_IDNR = ['04452397687',
                           '02259674819',
                           '04452317681',
                           '09952417688',
                           '03352417692',
                           '03352419681',
                           '03352417981',
                           '03392417683',
                           '03352917681',
                           '03359417681']

NEW_REQUEST_ID_SINCE_LAST_CACHE_INVALIDATION = []


def reset_new_request_id_list():
    global NEW_REQUEST_ID_SINCE_LAST_CACHE_INVALIDATION
    NEW_REQUEST_ID_SINCE_LAST_CACHE_INVALIDATION = []


def add_new_request_id_to_cache_list(request_id):
    global NEW_REQUEST_ID_SINCE_LAST_CACHE_INVALIDATION
    NEW_REQUEST_ID_SINCE_LAST_CACHE_INVALIDATION.append(request_id)


def get_vast_list_from_xml(xml):
    simple_xml = remove_declaration_and_namespace(xml)
    return {antrag.find('.//AntragsID').text: antrag.find('.//DateninhaberIdNr').text for antrag in simple_xml.findall('.//Antrag')}


@lru_cache
def get_list_vast_requests(pyeric_controller):
    xml = elster_xml_generator.generate_full_vast_list_xml()
    result = pyeric_controller(xml=xml).get_eric_response()
    vast_request_list = get_vast_list_from_xml(result.server_response)
    reset_new_request_id_list()
    return vast_request_list


def tax_id_number_is_test_id_number(tax_id_number):
    return tax_id_number in SPECIAL_TESTMERKER_IDNR


def request_needs_testmerker(request_id):
    if request_id in NEW_REQUEST_ID_SINCE_LAST_CACHE_INVALIDATION:
        get_list_vast_requests.cache_clear()
    return tax_id_number_is_test_id_number(get_list_vast_requests(PermitListingPyericProcessController).get(request_id))