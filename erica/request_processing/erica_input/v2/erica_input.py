
from typing import Optional

from pydantic import BaseModel

from erica.request_processing.erica_input.v1.erica_input import EstData, UnlockCodeRequestData, \
    UnlockCodeActivationData, UnlockCodeRevocationData


class EstDataWithTtl(BaseModel):
    ttlInMinutes: int
    payload: EstData


class TaxValidity(BaseModel):
    state_abbreviation: str
    tax_number: str


class TaxValidityWithTtl(BaseModel):
    ttlInMinutes: int
    payload: TaxValidity


class FscRequestDataWithTtl(BaseModel):
    ttlInMinutes: int
    payload: UnlockCodeRequestData


class FscActivationDataWithTtl(BaseModel):
    ttlInMinutes: int
    payload: UnlockCodeActivationData


class FscRevocationDataWithTtl(BaseModel):
    ttlInMinutes: int
    payload: UnlockCodeRevocationData


class ErrorRequestQueue(BaseModel):
    errorCode: str
    errorMessage: str


class ResponseGetFromQueue(BaseModel):
    processStatus: str
    payload: Optional[str] = None
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None


