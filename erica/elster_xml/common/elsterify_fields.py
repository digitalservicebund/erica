from datetime import date
from typing import Union

from erica.request_processing.erica_input.v2.grundsteuer_input import Anrede


def elsterify_anrede(anrede_input: Anrede):
    """ Converts input Anrede enum to Elster's Anrede enum """
    anrede_mapping = {
        Anrede.no_anrede: '01',
        Anrede.herr: '02',
        Anrede.frau: '03',
    }
    return anrede_mapping[anrede_input]


def elsterify_date(date_input: Union[date, None]):
    """ Converts input date to Elster's date format """
    if not date_input:
        return None
    return date_input.strftime("%d.%m.%Y")
