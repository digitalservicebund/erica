from enum import Enum
from typing import Optional, List

from erica.application.base_dto import BaseDto


class JobState(Enum):
    PROCESSING = "Processing"
    FAILURE = "Failure"
    SUCCESS = "Success"


class ResponseBaseDto(BaseDto):
    process_status: JobState
    result: Optional[BaseDto]
    error_code: Optional[str]
    errorMessage: Optional[str]


class ResponseErrorDto(BaseDto):
    error_code: str
    errorMessage: str


class ResultTransferPdfResponseDto(BaseDto):
    transferticket: str
    pdf: str


class ResultValidationErrorResponseDto(BaseDto):
    validation_errors: List[str]
