from enum import Enum
from typing import Optional, List, Literal

from pydantic import root_validator, validator, constr

from erica.application.grundsteuer.camel_case_input import CamelCaseInput


class Grundstuecksart(str, Enum):
    einfamilienhaus = "einfamilienhaus"
    zweifamilienhaus = "zweifamilienhaus"
    wohnungseigentum = "wohnungseigentum"
    baureif = "baureif"
    abweichende_entwicklung = "abweichendeEntwicklung"

    def is_bebaut(self):
        return self in [Grundstuecksart.einfamilienhaus, Grundstuecksart.zweifamilienhaus,
                        Grundstuecksart.wohnungseigentum]


class Adresse(CamelCaseInput):
    hausnummer: Optional[str]
    hausnummerzusatz: Optional[str]
    strasse: Optional[str]
    zusatzangaben: Optional[str]
    plz: Optional[str]
    ort: Optional[str]
    bundesland: str

    @validator("strasse", always=True)
    def strasse_mus_be_present_if_hausnummer_given(cls, v, values):
        if values.get("hausnummer") and not v:
            raise ValueError("has to be set if hausnummer is set")
        return v


class FlurstueckAngaben(CamelCaseInput):
    # TODO determine if this is mandatory (only in NRW?)
    grundbuchblattnummer: Optional[str]
    gemarkung: str


class Flur(CamelCaseInput):
    flur: str
    flurstueck_zaehler: int
    flurstueck_nenner: Optional[str]
    # number with 1-6 integer digits and exactly 4 fractional digits with '.' as decimal separator, e.g.90.1234
    wirtschaftliche_einheit_zaehler: Optional[constr(regex=r"^(?=.{6,11}$)(?!0\d)\d{1,6}(\.\d{4,4})$")]  # noqa: F722
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


class Flurstueck(CamelCaseInput):
    angaben: FlurstueckAngaben
    flur: Flur
    groesse_qm: int


class Grundstueck(CamelCaseInput):
    typ: Grundstuecksart
    abweichende_entwicklung: Optional[Literal["bauerwartungsland", "rohbauland"]]
    steuernummer: str
    adresse: Adresse
    innerhalb_einer_gemeinde: bool
    bodenrichtwert: constr(regex=r"^(?=.{4,9}$)(?!0\d)\d{1,6}(,\d{2,2})$")  # noqa: F722
    flurstueck: List[Flurstueck]

    @validator("adresse", always=True)
    def adresse_fields_must_be_set_if_beabut(cls, v, values):
        if "typ" in values and values["typ"] in ["einfamilienhaus", "mehrfamilienhaus", "wohnungseigentum"] and (
                not v.strasse or not v.plz or not v.ort):
            raise ValueError("strasse, plz and ort must be set if bebaut")
        return v