from dataclasses import dataclass


@dataclass
class ENutzdaten:
    """ Subclass this for each Use Case """
    pass


@dataclass
class EEmpfaenger:
    xml_only_text: str
    xml_attr_id: str

    def __init__(self, empfaenger_id, empfaenger_text):
        self.xml_only_text = empfaenger_text
        self.xml_attr_id = empfaenger_id


@dataclass
class ENutzdatenHeader:
    NutzdatenTicket: str
    Empfaenger: EEmpfaenger
    xml_attr_version: str

    def __init__(self, empfaenger_id, empfaenger_text, nutzdaten_header_version, nutzdaten_ticket):
        self.NutzdatenTicket = nutzdaten_ticket
        self.Empfaenger = EEmpfaenger(empfaenger_id, empfaenger_text)
        self.xml_attr_version = nutzdaten_header_version


@dataclass
class ENutzdatenblock:
    NutzdatenHeader: ENutzdatenHeader
    Nutzdaten: ENutzdaten

    def __init__(self, empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_header_version, nutzdaten_ticket):
        self.NutzdatenHeader = ENutzdatenHeader(empfaenger_id, empfaenger_text, nutzdaten_header_version,
                                                nutzdaten_ticket)
        self.Nutzdaten = nutzdaten_object


@dataclass
class EDatenTeil:
    Nutzdatenblock: ENutzdatenblock

    def __init__(self, empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_header_version, nutzdaten_ticket):
        self.Nutzdatenblock = ENutzdatenblock(empfaenger_id, empfaenger_text, nutzdaten_object,
                                              nutzdaten_header_version, nutzdaten_ticket)


@dataclass
class EElster:
    DatenTeil: EDatenTeil
    xml_attr_xmlns: str

    def __init__(self, empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_header_version, nutzdaten_ticket):
        self.DatenTeil = EDatenTeil(empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_header_version,
                                    nutzdaten_ticket)
        self.xml_attr_xmlns = "http://www.elster.de/elsterxml/schema/v11"


@dataclass
class EXml:
    Elster: EElster

    def __init__(self, empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_header_version, nutzdaten_ticket):
        self.Elster = EElster(empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_header_version,
                              nutzdaten_ticket)


def construct_basic_xml_data_representation(empfaenger_id: str, empfaenger_text: str, nutzdaten_object: ENutzdaten,
                                            nutzdaten_header_version: str, nutzdaten_ticket: str = "1"):
    """
    Returns the complete data representation of a valid Elster XML.

    :param empfaenger_id: ID of the Empfaenger - "F" in most cases
    :param empfaenger_text: specifics of the Empfaenger - the bufa_nr in most cases
    :param nutzdaten_object: a subclass of ENutzdaten including the use case specific
    Nutzdaten part of the xml data representation
    :param nutzdaten_header_version: The version of the NutzdatenHeader to use
    :param nutzdaten_ticket: The ID of the Nutzdatenticket. Irrelevant in cases
    with only one data item within the complete XML
    """
    return EXml(empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_header_version, nutzdaten_ticket)
