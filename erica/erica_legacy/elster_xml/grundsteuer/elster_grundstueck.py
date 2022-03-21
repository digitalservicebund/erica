import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List

from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_grundstueck import Adresse, Grundstueck, \
    Flurstueck


@dataclass
class Hausnummer:
    """
    Parses a combined hausnumer+hausnummerzusatz into separate components. The input must either be None or adhere
    to the format 1-4 digits followed by 0 or more alphanumeric characters.
    """
    nummer: Optional[str] = None
    zusatz: Optional[str] = None

    def __init__(self, combined_hausnummer: str):
        if combined_hausnummer:
            parsed = re.match(r"([0-9]{1,4})([a-zA-Z0-9]*)", combined_hausnummer).groups()
            self.nummer = parsed[0]
            self.zusatz = parsed[1] if parsed[1] else None


@dataclass
class ELage:
    E7401124: Optional[str]
    E7401125: Optional[str]
    E7401126: Optional[str]
    E7401131: Optional[str]
    E7401121: Optional[str]
    E7401122: Optional[str]

    def __init__(self, adresse: Adresse):
        self.E7401124 = adresse.strasse

        hausnummer = Hausnummer(adresse.hausnummer)
        self.E7401125 = hausnummer.nummer
        self.E7401126 = hausnummer.zusatz

        self.E7401131 = adresse.zusatzangaben
        self.E7401121 = adresse.plz
        self.E7401122 = adresse.ort


@dataclass
class EAngGrundstuecksart:
    E7401322: str

    def __init__(self, grundstueck: Grundstueck):
        self.E7401322 = grundstueck.typ


@dataclass
class EMehrereGemeinden:
    E7401190: int

    def __init__(self):
        self.E7401190 = 1


@dataclass
class EFlurstueck:
    E7401141: str
    E7401142: str
    E7401143: str
    E7401144: int
    E7401145: str
    E7411001: int
    E7410702: str
    E7410703: int
    # E7410704 TODO

    def __init__(self, flurstueck: Flurstueck):
        self.E7401141 = flurstueck.angaben.gemarkung
        self.E7401142 = flurstueck.angaben.grundbuchblattnummer
        self.E7401143 = flurstueck.flur.flur
        self.E7401144 = flurstueck.flur.flurstueck_zaehler
        self.E7401145 = flurstueck.flur.flurstueck_nenner
        self.E7411001 = flurstueck.groesse_qm
        self.E7410702 = flurstueck.flur.wirtschaftliche_einheit_zaehler
        self.E7410703 = flurstueck.flur.wirtschaftliche_einheit_nenner


@dataclass
class EGemarkungen:
    Einz: List[EFlurstueck]

    def __init__(self, flurstucke: List[Flurstueck]):
        self.Einz = []
        for flurstueck in flurstucke:
            elster_flurstueck = EFlurstueck(flurstueck)
            self.Einz.append(elster_flurstueck)


@dataclass
class EAngFlaeche:
    E7403010: int  # flaeche
    E7403011: str  # bodenrichtwert

    def __init__(self, grundstueck: Grundstueck):
        gesamtflaeche = 0
        for flurstueck in grundstueck.flurstueck:
            w_einheit_zaehler = Decimal(flurstueck.flur.wirtschaftliche_einheit_zaehler)
            w_einheit_nenner = flurstueck.flur.wirtschaftliche_einheit_nenner
            gesamtflaeche += (w_einheit_zaehler / w_einheit_nenner) * flurstueck.groesse_qm
        self.E7403010 = int(gesamtflaeche)
        self.E7403011 = grundstueck.bodenrichtwert


@dataclass
class EAngGrund:
    Ang_Flaeche: EAngFlaeche

    def __init__(self, grundstueck: Grundstueck):
        self.Ang_Flaeche = EAngFlaeche(grundstueck)
