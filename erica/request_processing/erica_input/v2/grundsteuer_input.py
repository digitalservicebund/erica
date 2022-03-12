from datetime import date
from enum import Enum
from typing import List, Optional

from humps import camelize
from pydantic import BaseModel, validator, root_validator


class PossiblyAliasedInput(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Ab1949(PossiblyAliasedInput):
    is_ab1949: bool


class Baujahr(PossiblyAliasedInput):
    baujahr: Optional[str]


class Kernsaniert(PossiblyAliasedInput):
    is_kernsaniert: bool


class Kernsanierungsjahr(PossiblyAliasedInput):
    kernsanierungsjahr: Optional[str]


class Abbruchverpflichtung(PossiblyAliasedInput):
    has_abbruchverpflichtung: bool


class Abbruchverpflichtungsjahr(PossiblyAliasedInput):
    abbruchverpflichtungsjahr: Optional[str]


class Wohnflaeche(PossiblyAliasedInput):
    wohnflaeche: Optional[int]


class Wohnflaechen(PossiblyAliasedInput):
    wohnflaeche1: Optional[int]
    wohnflaeche2: Optional[int]


class WeitereWohnraeume(PossiblyAliasedInput):
    has_weitere_wohnraeume: bool


class WeitereWohnraeumeFlaeche(PossiblyAliasedInput):
    flaeche: Optional[str]


class Garagen(PossiblyAliasedInput):
    has_garagen: bool


class GaragenAnzahl(PossiblyAliasedInput):
    anzahl_garagen: Optional[int]


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
    weitere_wohnraeume_flaeche: Optional[WeitereWohnraeumeFlaeche]
    garagen: Garagen
    garagen_anzahl: Optional[GaragenAnzahl]

    @root_validator
    def baujahr_must_be_present_if_ab_1949(cls, values):
        v = values.get("baujahr")
        if values.get("ab1949").is_ab1949 is True and (not v or not v.baujahr):
            raise ValueError('has to be set if is_ab1949')
        return values

    @root_validator
    def kernsanierungsjahr_must_be_present_if_kernsaniert(cls, values):
        v = values.get("kernsanierungsjahr")
        if values.get('kernsaniert').is_kernsaniert is True and (not v or not v.kernsanierungsjahr):
            raise ValueError('has to be set if is_kernsaniert')
        return values

    @root_validator
    def abbruchverpflichtungsjahr_must_be_present_if_has_abbruchverpflichtung(cls, values):
        v = values.get("abbruchverpflichtungsjahr")
        if values.get("abbruchverpflichtung").has_abbruchverpflichtung is True and (
                    not v or not v.abbruchverpflichtungsjahr):
            raise ValueError("has to be set if has_abbruchverpflichtung")
        return values

    @root_validator
    def weitere_wohnraeume_flaeche_must_be_present_if_has_weitere_wohnraeume(cls, values):
        v = values.get("weitere_wohnraeume_flaeche")
        if values.get("weitere_wohnraeume").has_weitere_wohnraeume is True and (
                not v or not v.flaeche):
            raise ValueError("has to be set if has_weitere_wohnraeume")
        return values

    @root_validator
    def garagen_anzahl_must_be_present_if_has_garagen(cls, values):
        v = values.get("garagen_anzahl")
        if values.get("garagen").has_garagen is True and (
                not v or not v.anzahl_garagen):
            raise ValueError("has to be set if has_garagen")
        return values

    @root_validator
    def must_contain_exactly_one_of_wohnflaechen_wohnflaeche(cls, values):
        if bool(values.get("wohnflaeche")) == bool(values.get('wohnflaechen')):
            raise ValueError('exactly one of wohnflaeche and wohnflaeche must be present')
        return values


class Anrede(str, Enum):
    no_anrede = 'no_anrede'
    herr = 'herr'
    frau = 'frau'


class Name(PossiblyAliasedInput):
    anrede: Anrede
    titel: Optional[str]
    name: str
    vorname: str


class PersoenlicheAngaben(Name):
    geburtsdatum: Optional[date]


class Adresse(PossiblyAliasedInput):
    strasse: Optional[str]
    hausnummer: Optional[str]
    hausnummerzusatz: Optional[str]
    postfach: Optional[str]
    plz: str
    ort: str


class Telefonnummer(PossiblyAliasedInput):
    telefonnummer: str


class SteuerId(PossiblyAliasedInput):
    steuer_id: str


class Vertreter(PossiblyAliasedInput):
    name: Name
    adresse: Adresse
    telefonnummer: Optional[Telefonnummer]


class Anteil(PossiblyAliasedInput):
    zaehler: str
    nenner: str


class Verheiratet(PossiblyAliasedInput):
    are_verheiratet: bool


class Person(PossiblyAliasedInput):
    persoenlicheAngaben: PersoenlicheAngaben
    adresse: Adresse
    telefonnummer: Optional[Telefonnummer]
    steuer_id: Optional[SteuerId]
    vertreter: Optional[Vertreter]
    anteil: Anteil


class Empfangsbevollmaechtigter(PossiblyAliasedInput):
    name: Name
    adresse: Adresse
    telefonnummer: Optional[Telefonnummer]


class Eigentuemer(PossiblyAliasedInput):
    person: List[Person]
    verheiratet: Optional[Verheiratet]
    empfangsbevollmaechtigter: Optional[Empfangsbevollmaechtigter]

    @validator("verheiratet", always=True)
    def must_be_set_only_if_two_persons(cls, v, values):
        if values.get('person') and len(values.get('person')) == 2 and not v:
            raise ValueError('has to be set if two persons')
        if values.get('person') and len(values.get('person')) != 2 and v:
            raise ValueError('must not be set if other than two persons')
        return v


class GrundsteuerData(PossiblyAliasedInput):
    eigentuemer: Eigentuemer


class GrundsteuerWithTtl(PossiblyAliasedInput):
    ttlInMinutes: int
    payload: GrundsteuerData
