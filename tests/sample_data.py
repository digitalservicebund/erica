from erica.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerData


def create_grundsteuer():
    valid_sample_data_single = {
        "eigentuemer": {
            "person": [
                {
                    "name": {
                        "anrede": "Frau",
                        "titel": "Dr",
                        "name": "Granger",
                        "vorname": "Hermine",
                    },
                    "adresse": {
                        "strasse": "Grimmauld place",
                        "hausnummer": "12",
                        "zusatzangaben": "Secret House",
                        "postfach": "",
                        "plz": "77777",
                        "ort": "London",
                    },
                    "telefonnummer": {
                        "telefonnummer": "",
                    },
                    "steuer_id": {
                        "steuer_id": "04452317681",
                    },
                    "vertreter": {
                        "name": {
                            "anrede": "",
                            "titel": "",
                            "name": "",
                            "vorname": "",
                        },
                        "adresse": {
                            "strasse": "",
                            "hausnummer": "",
                            "zusatzangaben": "",
                            "postfach": "",
                            "plz": "",
                            "ort": "",
                        },
                        "telefonnummer": {
                            "telefonnummer": "",
                        },
                    },
                    "anteil": {
                        "zaehler": 1,
                        "nenner": 1,
                    },
                },
            ],
        }}
    return GrundsteuerData.parse_obj(valid_sample_data_single)
