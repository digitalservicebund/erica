from erica.worker.elster_xml.est_validation import is_valid_bufa
from erica.worker.pyeric.eric import get_eric_wrapper
from erica.worker.pyeric.eric_errors import InvalidBufaNumberError

BUNDESLAENDER_WITH_STEUERNUMMER = ["BE", "HB", "SH"]

BUNDESLAND_BUFANR_MAPPING = {
    'BW': '28', 'BY': '9', 'BE': '11', 'BB': '30', 'HB': '24', 'HH': '22', 'HE': '26', 'MV': '40', 'ND': '23',
    'NW': '5', 'RP': '27', 'SL': '10', 'SN': '32', 'ST': '31', 'SH': '21', 'TH': '41'
}

BUNDESLAENDER_WITH_PREPENDED_NUMBER = ['BB', 'HE', 'MV', 'SL', 'SN', 'ST', 'TH']


def get_bufa_nr_from_steuernummer(steuernummer: str, bundesland: str):
    """
        Returns the bufa-nr for the given steuernummer and bundesland.
        :param steuernummer: steuernummer in state-specific format
        :param bundesland: bundesland identifier
     """

    electronic_steuernummer = generate_electronic_steuernummer(steuernummer, bundesland)
    bufa_nr = electronic_steuernummer[:4]
    return bufa_nr


def get_bufa_nr_from_aktenzeichen(aktenzeichen: str, bundesland: str):
    """
        Returns the bufa-nr for the given aktenzeichen and bundesland.
        :param aktenzeichen: aktenzeichen in state-specific format
        :param bundesland: bundesland identifier
     """
    bundesschema_steuernummer = generate_electronic_aktenzeichen(aktenzeichen, bundesland)
    bufa_nr = bundesschema_steuernummer[:4]
    if not is_valid_bufa(bufa_nr):
        raise InvalidBufaNumberError(bufa_nr=bufa_nr)
    return bufa_nr


def generate_electronic_aktenzeichen(aktenzeichen, bundesland):
    """
        Returns the elster-specific format for the given aktenzeichen and bundesland.
        :param aktenzeichen: aktenzeichen in state-specific format
        :param bundesland: bundesland identifier
     """
    
    with get_eric_wrapper() as eric_wrapper:
        return eric_wrapper.get_electronic_aktenzeichen(aktenzeichen, bundesland)


def generate_electronic_steuernummer(steuernummer, bundesland, use_testmerker=False):
    """
    Generates the electronic steuernummer representation of the steuernummer specific to a federal state.
    First, we generate the "bundeseinheitliche" steuernummer and
    then the electronic unified steuernummer, by adding a 0 at the 5th position.
    The different formats can be found here: https://de.wikipedia.org/wiki/Steuernummer

    :param steuernummer: Steuernummer that is specific to one state (10-11 numbers)
    :param bundesland: The federal state the steuernummer comes from as abbreviation, such as 'BE'
    """
    raw_steuernummer = steuernummer[1:] if bundesland in BUNDESLAENDER_WITH_PREPENDED_NUMBER else steuernummer
    bundesschema_steuernummer = BUNDESLAND_BUFANR_MAPPING[bundesland] + raw_steuernummer
    # first four digits of the electronic_steuernummer represent the bufa
    bufa_nr = bundesschema_steuernummer[:4]
    if not is_valid_bufa(bufa_nr, use_testmerker):
        raise InvalidBufaNumberError(bufa_nr=bufa_nr)
    electronic_steuernummer = bufa_nr + '0' + bundesschema_steuernummer[4:]
    return electronic_steuernummer
