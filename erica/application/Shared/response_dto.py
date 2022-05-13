from enum import Enum
from typing import Optional

from erica.application.base_dto import BaseDto


class JobState(Enum):
    PROCESSING = "Processing"
    FAILURE = "Failure"
    SUCCESS = "Success"


class ResponseBaseDto(BaseDto):
    processStatus: JobState
    result: Optional[BaseDto]
    errorCode: Optional[str]
    errorMessage: Optional[str]


class ResponseErrorDto(BaseDto):
    errorCode: str
    errorMessage: str


class ResultTransferPdfResponseDto(BaseDto):
    transferticket: str
    pdf: str
