from erica.application.FreischaltCode.FreischaltCode import FreischaltcodeRequestAndActivationResponseDto, \
    FreischaltcodeRevocationResponseDto
from erica.application.Shared.response_dto import ResponseErrorDto
from erica.application.grundsteuer.grundsteuer_dto import GrundsteuerResponseDto
from erica.application.tax_declaration.tax_declaration_dto import EstResponseDto
from erica.application.tax_number_validation.check_tax_number_dto import TaxResponseDto

model_404_error_get_from_queue = {"model": ResponseErrorDto,
                                  "description": "The requested entity is not present in the database."}

model_422_error_queue = {"model": ResponseErrorDto,
                                  "description": "Request done with invalid input payload."}

model_500_error_get_from_queue = {"model": ResponseErrorDto,
                                  "description": "Unexpected internal server error."}

base_response_get_from_queue = {
    404: model_404_error_get_from_queue,
    422: model_422_error_queue,
    500: model_500_error_get_from_queue
}

response_model_post_to_queue = {
    201: {"description": "Job was successfully submitted to the queue and the request id was returned."},
    422: model_422_error_queue,
    500: model_500_error_get_from_queue}

response_model_get_send_est_from_queue = {
    200: {"model": EstResponseDto,
          "description": "Job status of a sent est was successfully retrieved from the queue."},
    **base_response_get_from_queue}

response_model_get_send_grundsteuer_from_queue = {
    200: {"model": GrundsteuerResponseDto,
          "description": "Job status of a sent grundsteuer was successfully retrieved from the queue."},
    **base_response_get_from_queue}

response_model_get_tax_number_validity_from_queue = {
    200: {"model": TaxResponseDto,
          "description": "Job status of a tax number validity was successfully retrieved from the queue."},
    **base_response_get_from_queue}

response_model_get_unlock_code_request_from_queue = {
    200: {"model": FreischaltcodeRequestAndActivationResponseDto,
          "description": "Job status of an unlock code request was successfully retrieved from the queue."},
    **base_response_get_from_queue}

response_model_get_unlock_code_activation_from_queue = {
    200: {"model": FreischaltcodeRequestAndActivationResponseDto,
          "description": "Job status of an unlock code activation was successfully retrieved from the queue."},
    **base_response_get_from_queue}

response_model_get_unlock_code_revocation_from_queue = {
    200: {"model": FreischaltcodeRevocationResponseDto,
          "description": "Job status of an unlock code revocation was successfully retrieved from the queue."},
    **base_response_get_from_queue}
