import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List

from erica.erica_legacy.elster_xml.common.elsterify_fields import elsterify_grundstuecksart, \
    elsterify_wirtschaftliche_einheit_zaehler
from erica.application.grundsteuer.grundsteuer_input_grundstueck  import Adresse, Grundstueck, \
    Flurstueck, Grundstuecksart


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
        self.E7401125 = adresse.hausnummer
        self.E7401126 = adresse.hausnummerzusatz
        self.E7401131 = adresse.zusatzangaben
        self.E7401121 = adresse.plz
        self.E7401122 = adresse.ort


@dataclass
class EAngGrundstuecksart:
    E7401322: int

    def __init__(self, typ: Grundstuecksart):
        self.E7401322 = elsterify_grundstuecksart(typ)


@dataclass
class EMehrereGemeinden:
    E7401190: int

    def __init__(self):
        self.E7401190 = 1


@dataclass
class EFlurstueck:
    E7401141: str
    E7401142: Optional[str]  # TODO determine if mandatory
    E7401143: str
    E7401144: int
    E7401145: Optional[str]
    E7411001: int
    E7410702: str
    E7410703: int
    E7410704: int  # Enthalten in der/den in Anlage Grundstück, Zeile 4 angegebenen Fläche(n) des (Teil-)Grundstücks

    def __init__(self, flurstueck: Flurstueck):
        self.E7401141 = flurstueck.angaben.gemarkung
        self.E7401142 = flurstueck.angaben.grundbuchblattnummer
        self.E7401143 = flurstueck.flur.flur
        self.E7401144 = flurstueck.flur.flurstueck_zaehler
        self.E7401145 = flurstueck.flur.flurstueck_nenner
        self.E7411001 = flurstueck.groesse_qm
        self.E7410702 = elsterify_wirtschaftliche_einheit_zaehler(flurstueck.flur.wirtschaftliche_einheit_zaehler)
        self.E7410703 = flurstueck.flur.wirtschaftliche_einheit_nenner
        self.E7410704 = 1  # "erste Flaeche"


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
class EEntwZust:
    E7403051: int

    def __init__(self, abweichende_entwicklung: str):
        if abweichende_entwicklung == "bauerwartungsland":
            self.E7403051 = 1
        elif abweichende_entwicklung == "rohbauland":
            self.E7403051 = 2


@dataclass
class EAngGrund:
    Ang_Flaeche: EAngFlaeche
    Entw_Zust: Optional[EEntwZust]

    def __init__(self, grundstueck: Grundstueck):
        self.Ang_Flaeche = EAngFlaeche(grundstueck)
        if grundstueck.abweichende_entwicklung:
            self.Entw_Zust = EEntwZust(grundstueck.abweichende_entwicklung)
        else:
            self.Entw_Zust = None
