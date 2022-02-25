from typing import List, Optional

from pydantic import BaseModel


class Name(BaseModel):
    anrede: str
    titel: str
    name: str
    vorname: str


class Adresse(BaseModel):
    strasse: str
    hausnummer: str
    zusatzangaben: str
    postfach: str
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
    name: Name
    adresse: Adresse
    telefonnummer: Optional[Telefonnummer]
    steuer_id: Optional[SteuerId]
    vertreter: Optional[Vertreter]
    anteil: Anteil


class Eigentuemer(BaseModel):
    verheiratet: Optional[Verheiratet]
    person: List[Person]


class GrundsteuerData(BaseModel):
    eigentuemer: Eigentuemer
