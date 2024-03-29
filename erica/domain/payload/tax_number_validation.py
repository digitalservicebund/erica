from abc import ABC
from enum import Enum

from erica.domain.model.base_domain_model import BasePayload


class StateAbbreviation(str, Enum):
    bw = "bw"
    by = "by"
    be = "be"
    bb = "bb"
    hb = "hb"
    hh = "hh"
    he = "he"
    mv = "mv"
    nd = "nd"
    nw = "nw"
    rp = "rp"
    sl = "sl"
    sn = "sn"
    st = "st"
    sh = "sh"
    th = "th"

    # To find the correct values case insensitively
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.lower() == value.lower():
                return member


class CheckTaxNumberPayload(BasePayload, ABC):
    state_abbreviation: StateAbbreviation
    tax_number: str
