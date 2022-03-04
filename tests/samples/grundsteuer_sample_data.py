import copy
import datetime

from erica.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerData


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


def get_grundsteuer_sample_data(complete=True, only_postfach=False, only_strasse=False):
    valid_sample_data_single_with_vertreter = {
        "eigentuemer": {
            "person": [
                get_sample_single_person_dict(complete=complete, only_postfach=only_postfach, only_strasse=only_strasse)
            ],
        }}
    return GrundsteuerData.parse_obj(valid_sample_data_single_with_vertreter)
