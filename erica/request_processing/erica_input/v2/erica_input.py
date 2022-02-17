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
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None


class PayloadGetSendEstFromQueue(BaseModel):
    transfer_ticket: str
    pdf: str


class ResponseGetSendEstFromQueue(ResponseGetFromQueue):
    payload: PayloadGetSendEstFromQueue


class PayloadGetTaxNumberValidityFromQueue(BaseModel):
    is_valid: bool


class ResponseGetTaxNumberValidityFromQueue(ResponseGetFromQueue):
    payload: PayloadGetTaxNumberValidityFromQueue


class PayloadTransferTicketAndIdnr(BaseModel):
    transfer_ticket: str
    idnr: str


class PayloadGetUnlockCodeRequestAndActivationFromQueue(PayloadTransferTicketAndIdnr):
    elster_request_id: str


class ResponseGetUnlockCodeRequestAndActivationFromQueue(ResponseGetFromQueue):
    payload: PayloadGetUnlockCodeRequestAndActivationFromQueue


class ResponseGetUnlockCodeRevocationFromQueue(ResponseGetFromQueue):
    payload: PayloadTransferTicketAndIdnr
