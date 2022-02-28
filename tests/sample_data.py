from erica.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerData


def create_grundsteuer():
    valid_sample_data_single_with_vertreter = {
        "eigentuemer": {
            "person": [
                {
                    "name": {
                        "anrede": "frau",
                        "titel": "Dr",
                        "name": "Granger",
                        "vorname": "Hermine",
                    },
                    "adresse": {
                        "strasse": "Grimmauld place",
                        "hausnummer": "12",
                        "zusatzangaben": "Secret House",
                        "plz": "77777",
                        "ort": "London",
                    },
                    "telefonnummer": {
                        "telefonnummer": "123",
                    },
                    "steuer_id": {
                        "steuer_id": "04452317681",
                    },
                    "vertreter": {
                        "name": {
                            "anrede": "no_anrede",
                            "name": "Shacklebolt",
                            "vorname": "Kingsley",
                        },
                        "adresse": {
                            "postfach": "32263",
                            "plz": "98765",
                            "ort": "Godric's Hollow",
                        },
                    },
                    "anteil": {
                        "zaehler": 1,
                        "nenner": 1,
                    },
                },
            ],
        }}
    return GrundsteuerData.parse_obj(valid_sample_data_single_with_vertreter)
