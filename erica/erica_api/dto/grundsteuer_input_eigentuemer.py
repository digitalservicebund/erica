from datetime import date
from enum import Enum
from typing import Optional, List

from pydantic import validator
from erica.erica_api.dto.base_dto import CamelCaseModel
from erica.erica_legacy.pyeric.check_elster_request_id import tax_id_number_is_test_id_number


class Anrede(str, Enum):
    no_anrede = 'no_anrede'
    herr = 'herr'
    frau = 'frau'


class Name(CamelCaseModel):
    anrede: Anrede
    titel: Optional[str]
    name: str
    vorname: str


class PersoenlicheAngaben(Name):
    geburtsdatum: Optional[date]


class Adresse(CamelCaseModel):
    strasse: Optional[str]
    hausnummer: Optional[str]
    hausnummerzusatz: Optional[str]
    postfach: Optional[str]
    plz: str
    ort: str


class Vertreter(CamelCaseModel):
    name: Name
    adresse: Adresse
    telefonnummer: Optional[str]


class Anteil(CamelCaseModel):
    zaehler: str
    nenner: str


class Person(CamelCaseModel):
    persoenliche_angaben: PersoenlicheAngaben
    adresse: Adresse
    telefonnummer: Optional[str]
    steuer_id: Optional[str]
    vertreter: Optional[Vertreter]
    anteil: Anteil


class Bruchteilsgemeinschaft(CamelCaseModel):
    name: str
    adresse: Adresse


class Empfangsbevollmaechtigter(CamelCaseModel):
    name: Name
    adresse: Adresse
    telefonnummer: Optional[str]


class Eigentuemer(CamelCaseModel):
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

    @validator("person")
    def must_have_all_test_ids_or_no_test_ids(cls, v, values):
        if not(all([tax_id_number_is_test_id_number(person.steuer_id) for person in v]) or all([not tax_id_number_is_test_id_number(person.steuer_id) for person in v])):
            raise ValueError('all eigentuemer need to use either real or test tax id numbers')
        return v

    @validator("person")
    def must_not_be_empty(cls, v, values):
        if len(v) < 1:
            raise ValueError('at least one eigentuemer needs to be set')
        return v
