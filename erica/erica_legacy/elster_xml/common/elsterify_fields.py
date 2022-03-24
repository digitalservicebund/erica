from datetime import date
from typing import Union

from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_eigentuemer import Anrede
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_grundstueck import Grundstuecksart


def elsterify_anrede(anrede_input: Anrede):
    """ Converts input Anrede enum to Elster's Anrede enum """
    anrede_mapping = {
        Anrede.no_anrede: '01',
        Anrede.herr: '02',
        Anrede.frau: '03',
    }
    return anrede_mapping[anrede_input]


def elsterify_grundstuecksart(grundstuecksart_input: Grundstuecksart):
    grundstuecksart_mapping = {
        Grundstuecksart.baureif: 1,
        Grundstuecksart.abweichende_entwicklung: 1,
        Grundstuecksart.einfamilienhaus: 2,
        Grundstuecksart.zweifamilienhaus: 3,
        Grundstuecksart.wohnungseigentum: 5,
    }
    return grundstuecksart_mapping[grundstuecksart_input]


def elsterify_date(date_input: Union[date, None]):
    """ Converts input date to Elster's date format """
    if not date_input:
        return None
    return date_input.strftime("%d.%m.%Y")
