from datetime import date
from typing import Optional

from pydantic import BaseModel, root_validator, validator

from erica.worker.request_processing.erica_input.v1.erica_input import AccountHolder, Stmind

STANDARD_DATE_FORMAT = '%d.%m.%Y'


class EstEricMapping(Stmind):
    steuernummer: Optional[str]
    submission_without_tax_nr: Optional[bool]
    bufa_nr: Optional[str]
    bundesland: str
    iban: str
    account_holder: AccountHolder

    telephone_number: Optional[str]

    familienstand: str  # potentially enum
    familienstand_date: Optional[str]
    familienstand_married_lived_separated: Optional[bool]
    familienstand_married_lived_separated_since: Optional[date]
    familienstand_widowed_lived_separated: Optional[bool]
    familienstand_widowed_lived_separated_since: Optional[date]

    person_a_idnr: str
    person_a_dob: str
    person_a_last_name: str
    person_a_first_name: str
    person_a_religion: str
    person_a_street: str
    person_a_street_number: str
    person_a_street_number_ext: Optional[str]
    person_a_address_ext: Optional[str]
    person_a_plz: str
    person_a_town: str

    person_a_pauschbetrag_disability_degree: Optional[int]
    person_a_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad: Optional[bool]
    person_a_pauschbetrag_has_merkzeichen_g_ag: Optional[bool]
    person_a_fahrtkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad: Optional[bool]
    person_a_fahrtkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80: Optional[bool]

    person_b_same_address: Optional[bool]
    person_b_idnr: Optional[str]
    person_b_dob: Optional[str]
    person_b_last_name: Optional[str]
    person_b_first_name: Optional[str]
    person_b_religion: Optional[str]
    person_b_street: Optional[str]
    person_b_street_number: Optional[str]
    person_b_street_number_ext: Optional[str]
    person_b_address_ext: Optional[str]
    person_b_plz: Optional[str]
    person_b_town: Optional[str]

    person_b_pauschbetrag_disability_degree: Optional[int]
    person_b_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad: Optional[bool]
    person_b_pauschbetrag_has_merkzeichen_g_ag: Optional[bool]
    person_b_fahrtkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad: Optional[bool]
    person_b_fahrtkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80: Optional[bool]

    @root_validator(pre=True)
    def set_pauschbetrag_disability_degrees(cls, values):
        if values.get('person_a_requests_pauschbetrag'):
            values['person_a_pauschbetrag_disability_degree'] = values.get('person_a_disability_degree')

        if values.get('person_b_requests_pauschbetrag'):
            values['person_b_pauschbetrag_disability_degree'] = values.get('person_b_disability_degree')

        return values

    @root_validator(pre=True)
    def set_person_a_merkzeichen_bl_tbl_h_pflegegrad(cls, values):
        merkzeichen_values = [
            values.get('person_a_has_pflegegrad'),
            values.get('person_a_has_merkzeichen_bl'),
            values.get('person_a_has_merkzeichen_tbl'),
            values.get('person_a_has_merkzeichen_h')
        ]
        if any(merkzeichen_values) and values.get('person_a_requests_pauschbetrag'):
            values['person_a_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad'] = True
        return values

    @root_validator(pre=True)
    def set_person_a_merkzeichen_g_ag(cls, values):
        merkzeichen_values = [
            values.get('person_a_has_merkzeichen_g'),
            values.get('person_a_has_merkzeichen_ag')
        ]
        if any(merkzeichen_values) and values.get('person_a_requests_pauschbetrag'):
            values['person_a_pauschbetrag_has_merkzeichen_g_ag'] = True
        return values

    @root_validator(pre=True)
    def set_person_a_fahrtkostenpauschale(cls, values):
        merkzeichen_for_higher_fahrtkostenpauschale = [
            values.get('person_a_has_pflegegrad'),
            values.get('person_a_has_merkzeichen_bl'),
            values.get('person_a_has_merkzeichen_tbl'),
            values.get('person_a_has_merkzeichen_tbl'),
            values.get('person_a_has_merkzeichen_h'),
            values.get('person_a_has_merkzeichen_ag')
        ]
        if values.get('person_a_requests_fahrtkostenpauschale'):
            if any(merkzeichen_for_higher_fahrtkostenpauschale):
                values['person_a_fahrtkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad'] = True
            elif values.get('person_a_disability_degree') >= 80 or (
                    values.get('person_a_has_merkzeichen_g') and values.get('person_a_disability_degree') >= 70):
                values['person_a_fahrtkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80'] = True
        return values

    @root_validator(pre=True)
    def set_person_b_merkzeichen_bl_tbl_h_pflegegrad(cls, values):
        merkzeichen_values = [
            values.get('person_b_has_pflegegrad'),
            values.get('person_b_has_merkzeichen_bl'),
            values.get('person_b_has_merkzeichen_tbl'),
            values.get('person_b_has_merkzeichen_h')
        ]
        if any(merkzeichen_values) and values.get('person_b_requests_pauschbetrag'):
            values['person_b_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad'] = True
        return values

    @root_validator(pre=True)
    def set_person_b_merkzeichen_g_ag(cls, values):
        merkzeichen_values = [
            values.get('person_b_has_merkzeichen_g'),
            values.get('person_b_has_merkzeichen_ag')
        ]
        if any(merkzeichen_values) and values.get('person_b_requests_pauschbetrag'):
            values['person_b_pauschbetrag_has_merkzeichen_g_ag'] = True
        return values

    @root_validator(pre=True)
    def set_person_b_fahrtkostenpauschale(cls, values):
        merkzeichen_for_higher_fahrtkostenpauschale = [
            values.get('person_b_has_pflegegrad'),
            values.get('person_b_has_merkzeichen_bl'),
            values.get('person_b_has_merkzeichen_tbl'),
            values.get('person_b_has_merkzeichen_tbl'),
            values.get('person_b_has_merkzeichen_h'),
            values.get('person_b_has_merkzeichen_ag')
        ]
        if values.get('person_b_requests_fahrtkostenpauschale'):
            if any(merkzeichen_for_higher_fahrtkostenpauschale):
                values['person_b_fahrtkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad'] = True
            elif values.get('person_b_disability_degree') >= 80 or (
                    values.get('person_b_has_merkzeichen_g') and values.get('person_b_disability_degree') >= 70):
                values['person_b_fahrtkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80'] = True
        return values

    @validator('person_a_dob', 'person_b_dob', 'familienstand_date', pre=True)
    def convert_datetime_to_d_m_y(cls, v):
        return v.strftime(STANDARD_DATE_FORMAT) if v else None

    @validator('person_a_pauschbetrag_disability_degree', 'person_b_pauschbetrag_disability_degree')
    def set_disability_degree_only_if_above_20(cls, v):
        return None if v and v < 20 else v


class UnlockCodeRequestEricMapper(BaseModel):
    tax_id_number: str
    date_of_birth: str
    tax_year: Optional[str]

    @validator('date_of_birth', pre=True)
    def convert_datetime_to_y_m_d(cls, v):
        return v.strftime('%Y-%m-%d') if v else None
