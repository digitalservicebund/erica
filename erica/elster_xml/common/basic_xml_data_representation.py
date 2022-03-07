from dataclasses import dataclass

""" 
    The data representation of an Elster XML. The XML is always structured similarly:
    You have a TransferHeader (which is added by ERiC later) and a DatenTeil.
    The DatenTeil consists of header information called NutzdatenHeader and the actual specific data called Nutzdaten.
    Every use case (ESt/Grundsteuer/UnlockCodeRequest) has specific fields set that should be set via 
    a subclass of ENutzdaten.
    
    The following classes model the Elster XML structure 1:1 as objects, including the exact XML tag names as object 
    attribute names. Thus, do not change an attribute name if you're not intending to change the resulting XML.
    The classes are prefixed with "E" for "Elster".
"""


@dataclass
class ENutzdaten:
    """
    Subclass this for each Use Case where you need specific Nutzdaten. E.g. Grundsteuer / ESt.
    The concrete structure you can find in the ERiC documentation under
    /common/Schnittstellenbeschreibungen/<use case path>/Schema/<use case name>.xsd
    """
    pass


@dataclass
class EEmpfaenger:
    xml_text: str
    xml_attr_id: str

    def __init__(self, empfaenger_id, empfaenger_text):
        self.xml_text = empfaenger_text
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
