import copy
import datetime

from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerData
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_gebaeude import Gebaeude


class SampleGebaeude:
    def __init__(self):
        self.dict = {
            "ab1949": {
                "is_ab1949": False,
            },
            "kernsaniert": {
                "is_kernsaniert": False,
            },
            "abbruchverpflichtung": {
                "has_abbruchverpflichtung": False,
            },
            "weitere_wohnraeume": {
                "has_weitere_wohnraeume": False,
            },
            "garagen": {
                "has_garagen": False,
            },
        }

    def with_baujahr(self, baujahr=None):
        self.dict["ab1949"]["is_ab1949"] = True
        if baujahr:
            self.dict["baujahr"] = {"baujahr": baujahr}
        return self

    def with_kernsanierung(self, kernsanierungsjahr=None):
        self.dict["kernsaniert"]["is_kernsaniert"] = True
        if kernsanierungsjahr:
            self.dict["kernsanierungsjahr"] = {"kernsanierungsjahr": kernsanierungsjahr}
        return self

    def with_abbruchverpflichtung(self, abbruchverpflichtungsjahr=None):
        self.dict["abbruchverpflichtung"]["has_abbruchverpflichtung"] = True
        if abbruchverpflichtungsjahr:
            self.dict["abbruchverpflichtungsjahr"] = {"abbruchverpflichtungsjahr": abbruchverpflichtungsjahr}
        return self

    def with_wohnflaeche(self, wohnflaeche):
        self.dict["wohnflaeche"] = {"wohnflaeche": wohnflaeche}
        return self

    def with_wohnflaechen(self, wohnflaeche1, wohnflaeche2):
        self.dict["wohnflaechen"] = {"wohnflaeche1": wohnflaeche1, "wohnflaeche2": wohnflaeche2}
        return self

    def with_weitere_wohnraeume(self, flaeche=0, anzahl=0):
        self.dict["weitere_wohnraeume"]["has_weitere_wohnraeume"] = True
        if anzahl > 0:
            self.dict["weitere_wohnraeume_details"] = {"anzahl": anzahl, "flaeche": flaeche}
        return self

    def with_garagen(self, anzahl_garagen=None):
        self.dict["garagen"]["has_garagen"] = True
        if anzahl_garagen:
            self.dict["garagen_anzahl"] = {"anzahl_garagen": anzahl_garagen}
        return self

    def build(self):
        return {
            **self.dict
        }

    def parse(self):
        return Gebaeude.parse_obj(self.build())


def get_sample_adresse_eigentuemer(complete=True, only_postfach=False, only_strasse=False):
    if only_strasse:
        return {
            "strasse": "Grimmauld place",
            "hausnummer": "12",
            "hausnummerzusatz": "a",
            "plz": "77777",
            "ort": "London",
        }
    if only_postfach:
        return {
            "postfach": "11111",
            "plz": "77777",
            "ort": "London",
        }
    if complete:
        return {
            "strasse": "Grimmauld place",
            "hausnummer": "12",
            "hausnummerzusatz": "a",
            "postfach": "11111",
            "plz": "77777",
            "ort": "London",
        }

    return {
        "plz": "77777",
        "ort": "London",
    }


def get_sample_adresse_vertreter(complete=True, only_postfach=False, only_strasse=False):
    if only_strasse:
        return {
            "plz": "98765",
            "ort": "Godric's Hollow",
            "strasse": "Diagon Alley",
            "hausnummer": "04",
            "hausnummerzusatz": "b",
        }

    if only_postfach:
        return {
            "postfach": "32263",
            "plz": "98765",
            "ort": "Godric's Hollow"
        }
    if complete:
        return {
            "postfach": "32263",
            "plz": "98765",
            "ort": "Godric's Hollow",
            "strasse": "Diagon Alley",
            "hausnummer": "04",
            "hausnummerzusatz": "b",
        }
    return {
        "plz": "98765",
        "ort": "Godric's Hollow"
    }


def get_sample_adresse_empfangsbevollmaechtigter(complete=True, only_postfach=False, only_strasse=False):
    if only_strasse:
        return {
            "plz": "08642",
            "ort": "Hogsmeade",
            "strasse": "Three Brooms",
            "hausnummer": "3",
            "hausnummerzusatz": "c",
        }

    if only_postfach:
        return {
            "postfach": "34567",
            "plz": "08642",
            "ort": "Hogsmeade"
        }
    if complete:
        return {
            "postfach": "34567",
            "plz": "08642",
            "ort": "Hogsmeade",
            "strasse": "Diagon Alley",
            "hausnummer": "3",
            "hausnummerzusatz": "c",
        }
    return {
        "plz": "08642",
        "ort": "Hogsmeade"
    }


def get_sample_vertreter_dict(complete=True, only_postfach=False, only_strasse=False):
    name = {
        "anrede": "no_anrede",
        "titel": "Prof.",
        "name": "Shacklebolt",
        "vorname": "Kingsley"
    } if complete else {
        "anrede": "no_anrede",
        "name": "Shacklebolt",
        "vorname": "Kingsley",
    }
    adresse = get_sample_adresse_vertreter(complete, only_postfach, only_strasse)
    telefonnummer = {
        "telefonnummer": {
            "telefonnummer": "32168"
        }
    } if complete else {}

    return copy.deepcopy({**{
        "name": name,
        "adresse": adresse,
    }, **telefonnummer})


def get_sample_empfangsbevollmaechtigter_dict(complete=True, only_postfach=False, only_strasse=False):
    name = {
        "anrede": "frau",
        "titel": "Prof.",
        "name": "McGonagall",
        "vorname": "Minerva"
    } if complete else {
        "anrede": "frau",
        "name": "McGonagall",
        "vorname": "Minerva",
    }
    adresse = get_sample_adresse_empfangsbevollmaechtigter(complete, only_postfach, only_strasse)
    telefonnummer = {
        "telefonnummer": {
            "telefonnummer": "123-456"
        }
    } if complete else {}

    return copy.deepcopy({**{
        "name": name,
        "adresse": adresse,
    }, **telefonnummer})


def get_sample_single_person_dict(complete=True, with_vertreter=True, only_postfach=False, only_strasse=False):
    vertreter = {
        "vertreter": get_sample_vertreter_dict(complete, only_postfach, only_strasse)} if with_vertreter else {}
    name = {
        "persoenlicheAngaben": {
            "anrede": "frau",
            "titel": "Dr",
            "name": "Granger",
            "vorname": "Hermine",
            "geburtsdatum": datetime.date(1979, 9, 19)
        }} if complete else {
        "persoenlicheAngaben": {
            "anrede": "frau",
            "name": "Granger",
            "vorname": "Hermine",
        }
    }
    adresse = {"adresse": get_sample_adresse_eigentuemer(complete, only_postfach, only_strasse)}
    telefonnummer = {
        "telefonnummer": {
            "telefonnummer": "123",
        }} if complete else {}

    return copy.deepcopy({
        **{
            "steuer_id": {
                "steuer_id": "04452317681",
            },
            "anteil": {
                "zaehler": 1,
                "nenner": 1,
            },
        },
        **vertreter,
        **name,
        **adresse,
        **telefonnummer
    })


def get_grundsteuer_sample_data(complete=True, only_postfach=False, only_strasse=False, with_empfangsvollmacht=False):
    valid_gebaeude = SampleGebaeude().with_wohnflaeche(42).build()
    valid_person_data = {
        "person": [
            get_sample_single_person_dict(complete=complete, only_postfach=only_postfach, only_strasse=only_strasse)
        ],
    }
    valid_empfangsvollmacht_data = {
        "empfangsbevollmaechtigter": get_sample_empfangsbevollmaechtigter_dict(complete=complete, only_postfach=only_postfach, only_strasse=only_strasse)
    }

    valid_eigentuemer = {**valid_person_data, **valid_empfangsvollmacht_data} if with_empfangsvollmacht else valid_person_data
    valid_sample_data_single_with_vertreter = {
        "gebaeude": valid_gebaeude,
        "eigentuemer": valid_eigentuemer
    }
    return GrundsteuerData.parse_obj(valid_sample_data_single_with_vertreter)
