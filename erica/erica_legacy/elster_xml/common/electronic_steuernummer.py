from erica.erica_legacy.elster_xml.est_mapping import generate_electronic_steuernummer
from erica.erica_legacy.pyeric.eric import get_eric_wrapper

BUNDESLAENDER_WITH_STEUERNUMMER = ["BE", "HB", "SH"]


def get_bufa_nr(steuernummer: str, bundesland: str):
    """
        Returns the bufa-nr for the given steuernummer/aktenzeichen and bundesland.
        :param steuernummer: steuernummer/aktenzeichen in state-specific format
        :param bundesland: bundesland identifier
     """

    electronic_steuernummer = generate_electronic_steuernummer(steuernummer, bundesland)
    bufa_nr = electronic_steuernummer[:4]
    return bufa_nr


def generate_electronic_aktenzeichen(aktenzeichen, bundesland):
    """
        Returns the elster-specific format for the given aktenzeichen and bundesland.
        :param aktenzeichen: aktenzeichen in state-specific format
        :param bundesland: bundesland identifier
     """
    
    with get_eric_wrapper() as eric_wrapper:
        return eric_wrapper.get_electronic_aktenzeichen(aktenzeichen, bundesland)
