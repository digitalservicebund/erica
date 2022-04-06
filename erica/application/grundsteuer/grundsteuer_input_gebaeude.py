from typing import Optional, List

from pydantic import validator

from erica.application.grundsteuer.camel_case_input import CamelCaseInput


class Ab1949(CamelCaseInput):
    is_ab1949: bool


class Baujahr(CamelCaseInput):
    baujahr: str


class Kernsaniert(CamelCaseInput):
    is_kernsaniert: bool


class Kernsanierungsjahr(CamelCaseInput):
    kernsanierungsjahr: str


class Abbruchverpflichtung(CamelCaseInput):
    has_abbruchverpflichtung: bool


class Abbruchverpflichtungsjahr(CamelCaseInput):
    abbruchverpflichtungsjahr: str


class WeitereWohnraeume(CamelCaseInput):
    has_weitere_wohnraeume: bool


class WeitereWohnraeumeDetails(CamelCaseInput):
    anzahl: int
    flaeche: int


class Garagen(CamelCaseInput):
    has_garagen: bool


class GaragenAnzahl(CamelCaseInput):
    anzahl_garagen: int


class Gebaeude(CamelCaseInput):
    ab1949: Ab1949
    baujahr: Optional[Baujahr]
    kernsaniert: Kernsaniert
    kernsanierungsjahr: Optional[Kernsanierungsjahr]
    abbruchverpflichtung: Abbruchverpflichtung
    abbruchverpflichtungsjahr: Optional[Abbruchverpflichtungsjahr]
    wohnflaechen: List[int]
    weitere_wohnraeume: WeitereWohnraeume
    weitere_wohnraeume_details: Optional[WeitereWohnraeumeDetails]
    garagen: Garagen
    garagen_anzahl: Optional[GaragenAnzahl]

    @validator("baujahr", always=True)
    def baujahr_must_be_present_if_ab_1949(cls, v, values):
        if values.get("ab1949").is_ab1949 is True and not v:
            raise ValueError("has to be set if is_ab1949")
        return v

    @validator("kernsanierungsjahr", always=True)
    def kernsanierungsjahr_must_be_present_if_kernsaniert(cls, v, values):
        if values.get('kernsaniert').is_kernsaniert is True and not v:
            raise ValueError("has to be set if is_kernsaniert")
        return v

    @validator("abbruchverpflichtungsjahr", always=True)
    def abbruchverpflichtungsjahr_must_be_present_if_has_abbruchverpflichtung(cls, v, values):
        if values.get("abbruchverpflichtung").has_abbruchverpflichtung is True and not v:
            raise ValueError("has to be set if has_abbruchverpflichtung")
        return v

    @validator("weitere_wohnraeume_details", always=True)
    def weitere_wohnraeume_details_must_be_present_if_has_weitere_wohnraeume(cls, v, values):
        if values.get("weitere_wohnraeume").has_weitere_wohnraeume is True and not v:
            raise ValueError("has to be set if has_weitere_wohnraeume")
        return v

    @validator("garagen_anzahl", always=True)
    def garagen_anzahl_must_be_present_if_has_garagen(cls, v, values):
        if values.get("garagen").has_garagen is True and not v:
            raise ValueError("has to be set if has_garagen")
        return v

