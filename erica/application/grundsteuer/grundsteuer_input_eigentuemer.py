from datetime import date
from enum import Enum
from typing import Optional, List

from pydantic import validator
from erica.application.grundsteuer.camel_case_input import CamelCaseInput


class Anrede(str, Enum):
    no_anrede = 'no_anrede'
    herr = 'herr'
    frau = 'frau'


class Name(CamelCaseInput):
    anrede: Anrede
    titel: Optional[str]
    name: str
    vorname: str


class PersoenlicheAngaben(Name):
    geburtsdatum: Optional[date]


class Adresse(CamelCaseInput):
    strasse: Optional[str]
    hausnummer: Optional[str]
    hausnummerzusatz: Optional[str]
    postfach: Optional[str]
    plz: str
    ort: str


class Vertreter(CamelCaseInput):
    name: Name
    adresse: Adresse
    telefonnummer: Optional[str]


class Anteil(CamelCaseInput):
    zaehler: str
    nenner: str


class Person(CamelCaseInput):
    persoenlicheAngaben: PersoenlicheAngaben
    adresse: Adresse
    telefonnummer: Optional[str]
    steuer_id: Optional[str]
    vertreter: Optional[Vertreter]
    anteil: Anteil


class Bruchteilsgemeinschaft(CamelCaseInput):
    name: str
    adresse: Adresse


class Empfangsbevollmaechtigter(CamelCaseInput):
    name: Name
    adresse: Adresse
    telefonnummer: Optional[str]


class Eigentuemer(CamelCaseInput):
    person: List[Person]
    verheiratet: Optional[bool]
    bruchteilsgemeinschaft: Optional[Bruchteilsgemeinschaft]
    empfangsbevollmaechtigter: Optional[Empfangsbevollmaechtigter]

    @validator("verheiratet", always=True)
    def must_be_set_only_if_two_persons(cls, v, values):
        if values.get('person') and len(values.get('person')) == 2 and v is None:
            raise ValueError('has to be set if two persons')
        if values.get('person') and len(values.get('person')) != 2 and v is not None:
            raise ValueError('must not be set if other than two persons')
        return v