from typing import  Union
from pydantic import BaseModel

from erica.erica_legacy.request_processing.erica_input.v1.erica_input import UnlockCodeRequestData, \
    UnlockCodeActivationData, UnlockCodeRevocationData
from enum import Enum


class TaxValidity(BaseModel):
    state_abbreviation: str
    tax_number: str


class TaxValidityWithTtl(BaseModel):
    ttlInMinutes: int
    payload: TaxValidity


class ErrorRequestQueue(BaseModel):
    errorCode: str
    errorMessage: str


class Status(Enum):
    PROCESSING = "Processing"
    FAILURE = "Failure"
    SUCCESS = "Success"


class SuccessResponseGetFromQueue(BaseModel):
    processStatus: Status
    result: Union[BaseModel, None]
    errorCode: Union[str, None]
    errorMessage: Union[str, None]


class ResultGetSendEstFromQueue(BaseModel):
    transfer_ticket: str
    pdf: str


class SuccessResponseGetSendEstFromQueue(SuccessResponseGetFromQueue):
    result: ResultGetSendEstFromQueue


class ResultGetTaxNumberValidityFromQueue(BaseModel):
    is_valid: bool


class SuccessResponseGetTaxNumberValidityFromQueue(SuccessResponseGetFromQueue):
    result: ResultGetTaxNumberValidityFromQueue


class TransferTicketAndIdnr(BaseModel):
    transfer_ticket: str
    idnr: str


class ResultGetUnlockCodeRequestAndActivationFromQueue(TransferTicketAndIdnr):
    elster_request_id: str


class SuccessResponseGetUnlockCodeRequestAndActivationFromQueue(SuccessResponseGetFromQueue):
    result: ResultGetUnlockCodeRequestAndActivationFromQueue


class SuccessResponseGetUnlockCodeRevocationFromQueue(SuccessResponseGetFromQueue):
    result: TransferTicketAndIdnr
