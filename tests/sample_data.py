import copy

from erica.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerData, Vertreter


def get_sample_vertreter_dict(complete=True):
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
    adresse = {
        "postfach": "32263",
        "plz": "98765",
        "ort": "Godric's Hollow",
        "strasse": "Diagon Alley",
        "hausnummer": 4,
        "hausnummerzusatz": "b",
        "zusatzangaben": "Secret"
    } if complete else {
        "plz": "98765",
        "ort": "Godric's Hollow",
    }
    telefonnummer = {
        "telefonnummer": {
            "telefonnummer": "32168"
        }
    } if complete else {}

    return copy.deepcopy({**{
        "name": name,
        "adresse": adresse,
    }, **telefonnummer})


def get_single_person_dict(complete=True, with_vertreter=True):
    vertreter = {"vertreter": get_sample_vertreter_dict(complete)} if with_vertreter else {}
    name = {
        "name": {
            "anrede": "frau",
            "titel": "Dr",
            "name": "Granger",
            "vorname": "Hermine",
        }} if complete else {
        "name": {
            "anrede": "frau",
            "name": "Granger",
            "vorname": "Hermine",
        }
    }
    adresse = {
        "adresse": {
            "strasse": "Grimmauld place",
            "hausnummer": 12,
            "hausnummerzusatz": "a",
            "zusatzangaben": "Secret House",
            "plz": "77777",
            "ort": "London",
        }} if complete else {
        "adresse": {
            "plz": "77777",
            "ort": "London",
        },
    }
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


def create_grundsteuer(complete=True):
    valid_sample_data_single_with_vertreter = {
        "eigentuemer": {
            "person": [
                get_single_person_dict(complete=complete)
            ],
        }}
    return GrundsteuerData.parse_obj(valid_sample_data_single_with_vertreter)
