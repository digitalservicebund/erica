from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_eigentuemer import Eigentuemer
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_gebaeude import Gebaeude
from erica.erica_legacy.request_processing.erica_input.v2.possibly_aliased_input import PossiblyAliasedInput


class GrundsteuerData(PossiblyAliasedInput):
    gebaeude: Gebaeude
    eigentuemer: Eigentuemer


class GrundsteuerWithTtl(PossiblyAliasedInput):
    ttlInMinutes: int
    payload: GrundsteuerData
