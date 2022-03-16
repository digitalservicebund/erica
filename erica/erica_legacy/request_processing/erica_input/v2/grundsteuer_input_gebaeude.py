from typing import Optional

from pydantic import root_validator

from erica.erica_legacy.request_processing.erica_input.v2.possibly_aliased_input import PossiblyAliasedInput


class Ab1949(PossiblyAliasedInput):
    is_ab1949: bool


class Baujahr(PossiblyAliasedInput):
    baujahr: str


class Kernsaniert(PossiblyAliasedInput):
    is_kernsaniert: bool


class Kernsanierungsjahr(PossiblyAliasedInput):
    kernsanierungsjahr: str


class Abbruchverpflichtung(PossiblyAliasedInput):
    has_abbruchverpflichtung: bool


class Abbruchverpflichtungsjahr(PossiblyAliasedInput):
    abbruchverpflichtungsjahr: str


class Wohnflaeche(PossiblyAliasedInput):
    wohnflaeche: int


class Wohnflaechen(PossiblyAliasedInput):
    wohnflaeche1: int
    wohnflaeche2: int


class WeitereWohnraeume(PossiblyAliasedInput):
    has_weitere_wohnraeume: bool


class WeitereWohnraeumeDetails(PossiblyAliasedInput):
    anzahl: int
    flaeche: int


class Garagen(PossiblyAliasedInput):
    has_garagen: bool


class GaragenAnzahl(PossiblyAliasedInput):
    anzahl_garagen: int


class Gebaeude(PossiblyAliasedInput):
    ab1949: Ab1949
    baujahr: Optional[Baujahr]
    kernsaniert: Kernsaniert
    kernsanierungsjahr: Optional[Kernsanierungsjahr]
    abbruchverpflichtung: Abbruchverpflichtung
    abbruchverpflichtungsjahr: Optional[Abbruchverpflichtungsjahr]
    wohnflaeche: Optional[Wohnflaeche]
    wohnflaechen: Optional[Wohnflaechen]
    weitere_wohnraeume: WeitereWohnraeume
    weitere_wohnraeume_details: Optional[WeitereWohnraeumeDetails]
    garagen: Garagen
    garagen_anzahl: Optional[GaragenAnzahl]

    @root_validator
    def baujahr_must_be_present_if_ab_1949(cls, values):
        field_name = "baujahr"
        v = values.get(field_name)
        if values.get("ab1949").is_ab1949 is True and not v:
            raise ValueError(f"{field_name} has to be set if is_ab1949")
        return values

    @root_validator
    def kernsanierungsjahr_must_be_present_if_kernsaniert(cls, values):
        field_name = "kernsanierungsjahr"
        v = values.get(field_name)
        if values.get('kernsaniert').is_kernsaniert is True and not v:
            raise ValueError(f"{field_name} has to be set if is_kernsaniert")
        return values

    @root_validator
    def abbruchverpflichtungsjahr_must_be_present_if_has_abbruchverpflichtung(cls, values):
        field_name = "abbruchverpflichtungsjahr"
        v = values.get(field_name)
        if values.get("abbruchverpflichtung").has_abbruchverpflichtung is True and not v:
            raise ValueError(f"{field_name} has to be set if has_abbruchverpflichtung")
        return values

    @root_validator
    def weitere_wohnraeume_details_must_be_present_if_has_weitere_wohnraeume(cls, values):
        field_name = "weitere_wohnraeume_details"
        v = values.get(field_name)
        if values.get("weitere_wohnraeume").has_weitere_wohnraeume is True and not v:
            raise ValueError(f"{field_name} has to be set if has_weitere_wohnraeume")
        return values

    @root_validator
    def garagen_anzahl_must_be_present_if_has_garagen(cls, values):
        field_name = "garagen_anzahl"
        v = values.get(field_name)
        if values.get("garagen").has_garagen is True and not v:
            raise ValueError(f"{field_name} has to be set if has_garagen")
        return values

    @root_validator
    def must_contain_exactly_one_of_wohnflaechen_wohnflaeche(cls, values):
        if bool(values.get("wohnflaeche")) == bool(values.get('wohnflaechen')):
            raise ValueError('exactly one of wohnflaeche and wohnflaeche must be present')
        return values