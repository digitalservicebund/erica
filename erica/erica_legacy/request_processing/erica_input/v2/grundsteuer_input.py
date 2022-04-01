from typing import Optional

from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_eigentuemer import Eigentuemer
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_gebaeude import Gebaeude
from erica.erica_legacy.request_processing.erica_input.v2.camel_case_input import CamelCaseInput
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_grundstueck import Grundstueck

from abc import ABC
from erica.domain.Shared.BaseDomainModel import BasePayload


class GrundsteuerData(BasePayload, ABC, CamelCaseInput):
    grundstueck: Grundstueck
    gebaeude: Optional[Gebaeude]
    eigentuemer: Eigentuemer
    freitext: Optional[str]


class GrundsteuerWithTtl(CamelCaseInput):
    ttlInMinutes: int
    payload: GrundsteuerData

class GrundsteuerDto(CamelCaseInput):    
    payload: GrundsteuerData
    clientIdentifier: str