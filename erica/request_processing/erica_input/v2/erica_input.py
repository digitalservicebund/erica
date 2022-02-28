from typing import  Union
from pydantic import BaseModel
from erica.request_processing.erica_input.v1.erica_input import EstData, UnlockCodeRequestData, \
    UnlockCodeActivationData, UnlockCodeRevocationData
from enum import Enum


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