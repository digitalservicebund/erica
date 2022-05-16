from typing import Optional, Union

from erica.application.Shared.response_dto import ResponseBaseDto, ResultTransferPdfResponseDto, \
    ResultValidationErrorResponseDto
from erica.application.grundsteuer.grundsteuer_input_eigentuemer import Eigentuemer

from erica.application.grundsteuer.camel_case_input import CamelCaseInput
from erica.application.grundsteuer.grundsteuer_input_gebaeude import Gebaeude
from erica.application.grundsteuer.grundsteuer_input_grundstueck import Grundstueck

from abc import ABC
from erica.domain.Shared.BaseDomainModel import BasePayload


# Input

class GrundsteuerPayload(BasePayload, ABC, CamelCaseInput):
    grundstueck: Grundstueck
    gebaeude: Optional[Gebaeude]
    eigentuemer: Eigentuemer
    freitext: Optional[str]


class GrundsteuerDto(CamelCaseInput):
    payload: GrundsteuerPayload
    client_identifier: str


# Output

class GrundsteuerResponseDto(ResponseBaseDto):
    result: Optional[Union[ResultTransferPdfResponseDto, ResultValidationErrorResponseDto]]
