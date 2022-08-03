import logging
import re
from enum import Enum
from typing import Optional, List, Literal

from pydantic import root_validator, validator

from erica.erica_api.dto.base_dto import CamelCaseModel


class Grundstuecksart(str, Enum):
    einfamilienhaus = "einfamilienhaus"
    zweifamilienhaus = "zweifamilienhaus"
    wohnungseigentum = "wohnungseigentum"
    baureif = "baureif"
    abweichende_entwicklung = "abweichendeEntwicklung"

    def is_bebaut(self):
        return self in [Grundstuecksart.einfamilienhaus, Grundstuecksart.zweifamilienhaus,
                        Grundstuecksart.wohnungseigentum]


class Adresse(CamelCaseModel):
    hausnummer: Optional[str]
    hausnummerzusatz: Optional[str]
    strasse: Optional[str]
    zusatzangaben: Optional[str]
    plz: Optional[str]
    ort: Optional[str]
    bundesland: str


class FlurstueckAngaben(CamelCaseModel):
    grundbuchblattnummer: Optional[str]
    gemarkung: str


class Flur(CamelCaseModel):
    flur: Optional[str]
    flurstueck_zaehler: int
    flurstueck_nenner: Optional[str]
    wirtschaftliche_einheit_zaehler: Optional[str]
    wirtschaftliche_einheit_nenner: Optional[int]

    @root_validator
    def w_einheit_zaehler_nenner_should_be_given_together(cls, values):
        zaehler = "wirtschaftliche_einheit_zaehler"
        nenner = "wirtschaftliche_einheit_nenner"

        if zaehler in values and nenner in values:
            if bool(values[zaehler]) != bool(values[nenner]):
                raise ValueError(
                    ("either both or none of wirtschaftliche_einheit_zaehler"
                     " and wirtschaftliche_einheit_nenner should be present"))
            if not values[zaehler] and not values[nenner]:
                values[zaehler] = "1.0000"
                values[nenner] = 1
        return values

    @validator("wirtschaftliche_einheit_zaehler")
    def must_be_regex_compliant(cls, v):
        # number with 1-6 integer digits and exactly 4 fractional digits with '.' as decimal separator, e.g.90.1234
        pattern = re.compile("^(?=.{1,11}$)(?=.*[1-9].*)(?!0\d)\d{1,6}(.\d{1,4})?$")  # noqa: F722
        match = pattern.match(v)
        if match:
            return v
        else:
            logging.getLogger().warning("Invalid wirtschaftliche einheit zaehler: " + v)
            raise ValueError("Must match regex")


class Flurstueck(CamelCaseModel):
    angaben: FlurstueckAngaben
    flur: Flur
    groesse_qm: str

    @validator("groesse_qm")
    def must_be_valid_integer(cls, v):
        try:
            return int(v)
        except ValueError:
            logging.getLogger().warning("Invalid flurstueck groesse: " + v)
            raise ValueError("Must be a valid integer")


class Grundstueck(CamelCaseModel):
    typ: Grundstuecksart
    abweichende_entwicklung: Optional[Literal["bauerwartungsland", "rohbauland"]]
    steuernummer: str
    adresse: Adresse
    innerhalb_einer_gemeinde: bool
    bodenrichtwert: str
    flurstueck: List[Flurstueck]

    @validator("adresse", always=True)
    def adresse_fields_must_be_set_if_bebaut(cls, v, values):
        if "typ" in values and values["typ"] in ["einfamilienhaus", "mehrfamilienhaus", "wohnungseigentum"] and (
                not v.strasse or not v.plz or not v.ort):
            raise ValueError("strasse, plz and ort must be set if bebaut")
        return v

    @validator("bodenrichtwert")
    def must_be_regex_compliant(cls, v):
        pattern = re.compile("^(?=.{4,9}$)(?!0\d)\d{1,6}(,\d{2,2})$")  # noqa: F722
        match = pattern.match(v)
        if match:
            return v
        else:
            logging.getLogger().warning("Invalid bodenrichtwert: " + v)
            raise ValueError("Must match regex")
