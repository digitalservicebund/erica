from dataclasses import dataclass


@dataclass
class EEmpfaenger:
    xml_only_text: str
    xml_attr_id: str

    def __init__(self, empfaenger_text, empfaenger_id):
        self.xml_only_text = empfaenger_text
        self.xml_attr_id = empfaenger_id


@dataclass
class ENutzdatenHeader:
    NutzdatenTicket: str
    Empfaenger: EEmpfaenger
    xml_attr_version: str

    def __init__(self, empfaenger_id, empfaenger_text, nutzdaten_ticket):
        self.NutzdatenTicket = nutzdaten_ticket
        self.Empfaenger = EEmpfaenger(empfaenger_text, empfaenger_id=empfaenger_id)
        self.xml_attr_version = "11"  # TODO make this param


@dataclass
class ENutzdaten:
    pass


@dataclass
class ENutzdatenblock:
    NutzdatenHeader: ENutzdatenHeader
    Nutzdaten: ENutzdaten

    def __init__(self, empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_ticket):
        self.NutzdatenHeader = ENutzdatenHeader(empfaenger_id, empfaenger_text, nutzdaten_ticket)
        self.Nutzdaten = nutzdaten_object


@dataclass
class EDatenTeil:
    Nutzdatenblock: ENutzdatenblock

    def __init__(self, empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_ticket):
        self.Nutzdatenblock = ENutzdatenblock(empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_ticket)


@dataclass
class EElster:
    DatenTeil: EDatenTeil
    xml_attr_xmlns: str

    def __init__(self, empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_ticket):
        self.DatenTeil = EDatenTeil(empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_ticket)
        self.xml_attr_xmlns = "http://www.elster.de/elsterxml/schema/v11"


@dataclass
class EXml:
    Elster: EElster

    def __init__(self, empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_ticket):
        self.Elster = EElster(empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_ticket)


def construct_basic_xml_object_representation(empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_ticket):
    return EXml(empfaenger_id, empfaenger_text, nutzdaten_object, nutzdaten_ticket)
