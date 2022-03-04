from datetime import date

from erica.request_processing.erica_input.v2.grundsteuer_input import Anrede


def elsterify_anrede(anrede_input: Anrede):
    """ Converts input Anrede enum to Elster's Anrede enum """
    anrede_mapping = {
        Anrede.no_anrede: '01',
        Anrede.herr: '02',
        Anrede.frau: '03',
    }
    return anrede_mapping[anrede_input]


def elsterify_date(date_input: date):
    """ Converts input date to Elster's date format """
    return date_input.strftime("%d.%m.%Y")
