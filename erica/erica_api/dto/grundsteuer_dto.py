from typing import Optional, Union

from erica.erica_api.dto.response_dto import ResponseBaseDto, ResultTransferPdfResponseDto, \
    ResultValidationErrorResponseDto
from erica.erica_api.dto.grundsteuer_input_eigentuemer import Eigentuemer

from erica.erica_api.dto.base_dto import CamelCaseModel
from erica.erica_api.dto.grundsteuer_input_gebaeude import Gebaeude
from erica.erica_api.dto.grundsteuer_input_grundstueck import Grundstueck

from abc import ABC
from erica.erica_shared.model.base_domain_model import BasePayload


# Input

class GrundsteuerPayload(BasePayload, ABC, CamelCaseModel):
    grundstueck: Grundstueck
    gebaeude: Optional[Gebaeude]
    eigentuemer: Eigentuemer
    freitext: Optional[str]


class GrundsteuerDto(CamelCaseModel):
    payload: GrundsteuerPayload
    client_identifier: str


# Output

class GrundsteuerResponseDto(ResponseBaseDto):
    result: Optional[Union[ResultTransferPdfResponseDto, ResultValidationErrorResponseDto]]
