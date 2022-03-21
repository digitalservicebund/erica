import re
from dataclasses import dataclass
from typing import Optional

from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_grundstueck import Adresse


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
    E7401124: Optional[str]  # strasse
    E7401125: Optional[str]  # hausnummer
    E7401126: Optional[str]  # hausnummerzusatz
    E7401131: Optional[str]  # zusatzangaben
    E7401121: Optional[str]  # plz
    E7401122: Optional[str]  # oret

    def __init__(self, adresse: Adresse):
        self.E7401124 = adresse.strasse

        hausnummer = Hausnummer(adresse.hausnummer)
        self.E7401125 = hausnummer.nummer
        self.E7401126 = hausnummer.zusatz

        self.E7401131 = adresse.zusatzangaben
        self.E7401121 = adresse.plz
        self.E7401122 = adresse.ort
