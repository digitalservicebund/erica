from enum import Enum
from typing import Optional, List

from erica.api.dto.base_dto import BaseDto


class JobState(Enum):
    PROCESSING = "Processing"
    FAILURE = "Failure"
    SUCCESS = "Success"


class ResponseBaseDto(BaseDto):
    process_status: JobState
    result: Optional[BaseDto]
    error_code: Optional[str]
    error_message: Optional[str]


class ResponseErrorDto(BaseDto):
    error_code: str
    error_message: str


class ResultTransferPdfResponseDto(BaseDto):
    transferticket: str
    pdf: str


class ResultValidationErrorResponseDto(BaseDto):
    validation_errors: List[str]
