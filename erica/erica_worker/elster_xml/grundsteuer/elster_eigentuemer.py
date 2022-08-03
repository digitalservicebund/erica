from dataclasses import dataclass
from typing import Optional

from erica.erica_worker.elster_xml.common.elsterify_fields import elsterify_anrede, elsterify_date, \
    elsterify_eigentumsverhaeltnis
from erica.erica_api.dto.grundsteuer_input_eigentuemer import Anteil, Vertreter, \
    Person, Eigentuemer as EigentuemerInput


@dataclass
class EAnteil:
    E7404570: str
    E7404571: str

    def __init__(self, input_data: Anteil):
        self.E7404570 = input_data.zaehler
        self.E7404571 = input_data.nenner


@dataclass
class EGesetzlicherVertreter:
    E7415101: str
    E7415102: Optional[str]
    E7415201: str
    E7415301: str
    E7415401: str
    E7415501: Optional[int]
    E7415502: Optional[str]
    E7415601: str
    E7415602: Optional[str]
    E7415603: str
    E7415604: Optional[str]

    def __init__(self, input_data: Vertreter):
        self.E7415101 = elsterify_anrede(input_data.name.anrede)
        self.E7415102 = input_data.name.titel
        self.E7415201 = input_data.name.vorname
        self.E7415301 = input_data.name.name
        self.E7415401 = input_data.adresse.strasse
        self.E7415501 = input_data.adresse.hausnummer
        self.E7415502 = input_data.adresse.hausnummerzusatz
        self.E7415601 = input_data.adresse.plz
        self.E7415602 = input_data.adresse.postfach
        self.E7415603 = input_data.adresse.ort
        self.E7415604 = input_data.telefonnummer


@dataclass
class EPersonData:
    Beteiligter: int
    E7404510: str
    E7404514: Optional[str]
    E7404518: Optional[str]
    E7404513: str
    E7404511: str
    E7404524: str
    E7404525: Optional[str]
    E7404526: Optional[str]
    E7404540: str
    E7404527: Optional[str]
    E7404522: str
    E7414601: Optional[str]
    E7404519: str
    Anteil: EAnteil
    Ges_Vertreter: Optional[EGesetzlicherVertreter]

    def __init__(self, input_data: Person, person_index: int):
        self.Beteiligter = person_index + 1
        self.E7404510 = elsterify_anrede(input_data.persoenliche_angaben.anrede)
        self.E7404514 = input_data.persoenliche_angaben.titel
        self.E7404518 = elsterify_date(input_data.persoenliche_angaben.geburtsdatum)
        self.E7404513 = input_data.persoenliche_angaben.vorname
        self.E7404511 = input_data.persoenliche_angaben.name
        self.E7404524 = input_data.adresse.strasse
        self.E7404525 = input_data.adresse.hausnummer
        self.E7404526 = input_data.adresse.hausnummerzusatz
        self.E7404540 = input_data.adresse.plz
        self.E7404527 = input_data.adresse.postfach
        self.E7404522 = input_data.adresse.ort
        self.E7414601 = input_data.telefonnummer

        self.E7404519 = input_data.steuer_id
        self.Anteil = EAnteil(input_data.anteil)

        # input_data.vertreter might not be set -> handle specifically
        if input_data.vertreter:
            self.Ges_Vertreter = EGesetzlicherVertreter(input_data.vertreter)
        else:
            self.Ges_Vertreter = None


@dataclass
class EEigentumsverh:
    E7401340: str

    def __init__(self, input_data: EigentuemerInput):
        self.E7401340 = elsterify_eigentumsverhaeltnis(input_data)


@dataclass
class EEmpfangsbevollmaechtigter:
    E7404610: str
    E7404614: Optional[str]
    E7404613: str
    E7404611: str
    E7404624: Optional[str]
    E7404625: Optional[str]
    E7404626: Optional[str]
    E7404640: str
    E7404627: Optional[str]
    E7404622: str
    E7412201: Optional[str]
    E7412901: Optional[int]

    def __init__(self, eigentuemer: EigentuemerInput):
        empfangsbevollmaechtigter = eigentuemer.empfangsbevollmaechtigter
        self.E7404610 = elsterify_anrede(empfangsbevollmaechtigter.name.anrede)
        self.E7404614 = empfangsbevollmaechtigter.name.titel
        self.E7404613 = empfangsbevollmaechtigter.name.vorname
        self.E7404611 = empfangsbevollmaechtigter.name.name
        self.E7404624 = empfangsbevollmaechtigter.adresse.strasse
        self.E7404625 = empfangsbevollmaechtigter.adresse.hausnummer
        self.E7404626 = empfangsbevollmaechtigter.adresse.hausnummerzusatz
        self.E7404640 = empfangsbevollmaechtigter.adresse.plz
        self.E7404627 = empfangsbevollmaechtigter.adresse.postfach
        self.E7404622 = empfangsbevollmaechtigter.adresse.ort
        self.E7412201 = empfangsbevollmaechtigter.telefonnummer

        if elsterify_eigentumsverhaeltnis(eigentuemer) == "6":  # Bruchteilsgemeinschaft
            self.E7412901 = 1
        else:
            self.E7412901 = None
