from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_eigentuemer import Eigentuemer
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_gebaeude import Gebaeude
from erica.erica_legacy.request_processing.erica_input.v2.camel_case_input import CamelCaseInput


class GrundsteuerData(CamelCaseInput):
    gebaeude: Gebaeude
    eigentuemer: Eigentuemer


class GrundsteuerWithTtl(CamelCaseInput):
    ttlInMinutes: int
    payload: GrundsteuerData
