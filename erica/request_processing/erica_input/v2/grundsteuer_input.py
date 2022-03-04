from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, validator
from pydantic.types import date


class Anrede(str, Enum):
    no_anrede = 'no_anrede'
    herr = 'herr'
    frau = 'frau'


class Name(BaseModel):
    anrede: Anrede
    titel: Optional[str]
    name: str
    vorname: str


class PersoenlicheAngaben(Name):
    geburtsdatum: Optional[date]


class Adresse(BaseModel):
    strasse: Optional[str]
    hausnummer: Optional[int]
    hausnummerzusatz: Optional[str]
    zusatzangaben: Optional[str]
    postfach: Optional[str]
    plz: str
    ort: str


class Telefonnummer(BaseModel):
    telefonnummer: str


class SteuerId(BaseModel):
    steuer_id: str


class Vertreter(BaseModel):
    name: Name
    adresse: Adresse
    telefonnummer: Optional[Telefonnummer]


class Anteil(BaseModel):
    zaehler: str
    nenner: str


class Verheiratet(BaseModel):
    are_verheiratet: bool


class Person(BaseModel):
    persoenlicheAngaben: PersoenlicheAngaben
    adresse: Adresse
    telefonnummer: Optional[Telefonnummer]
    steuer_id: Optional[SteuerId]
    vertreter: Optional[Vertreter]
    anteil: Anteil


class Eigentuemer(BaseModel):
    person: List[Person]
    verheiratet: Optional[Verheiratet]

    @validator("verheiratet", always=True)
    def must_be_set_if_two_persons(cls, v, values):
        if values.get('person') and len(values.get('person')) == 2 and not v:
            raise ValueError('has to be set if two persons')
        return v


class GrundsteuerData(BaseModel):
    eigentuemer: Eigentuemer


class GrundsteuerWithTtl(BaseModel):
    ttlInMinutes: int
    payload: GrundsteuerData
