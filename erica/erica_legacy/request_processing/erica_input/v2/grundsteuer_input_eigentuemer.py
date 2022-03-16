from datetime import date
from enum import Enum
from typing import Optional, List

from pydantic import validator

from erica.erica_legacy.request_processing.erica_input.v2.possibly_aliased_input import PossiblyAliasedInput


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