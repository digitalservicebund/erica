from erica.request_processing.erica_input.v2.erica_input import ErrorRequestQueue, SuccessResponseGetFromQueue, \
    SuccessResponseGetSendEstFromQueue, SuccessResponseGetTaxNumberValidityFromQueue, \
    SuccessResponseGetUnlockCodeRequestAndActivationFromQueue, SuccessResponseGetUnlockCodeRevocationFromQueue

model_error_request_queue = {"model": ErrorRequestQueue,
                             "description": "Job status could not be retrieved from the queue."}

response_model_post_to_queue = {
    201: {"description": "Job was successfully submitted to the queue and the job id was returned."},
    422: {"model": ErrorRequestQueue, "description": "Job could not be submitted to the queue."}}

response_model_get_est_validation_from_queue = {
    200: {"model": SuccessResponseGetFromQueue,
          "description": "Job status of an est validation was successfully retrieved from the queue."},
    500: model_error_request_queue}

response_model_get_send_est_from_queue = {
    200: {"model": SuccessResponseGetSendEstFromQueue,
          "description": "Job status of a sent est was successfully retrieved from the queue."},
    500: model_error_request_queue}

response_model_get_tax_number_validity_from_queue = {
    200: {"model": SuccessResponseGetTaxNumberValidityFromQueue,
          "description": "Job status of a tax number validity was successfully retrieved from the queue."},
    500: model_error_request_queue}

response_model_get_unlock_code_request_from_queue = {
    200: {"model": SuccessResponseGetUnlockCodeRequestAndActivationFromQueue,
          "description": "Job status of an unlock code request was successfully retrieved from the queue."},
    500: model_error_request_queue}

response_model_get_unlock_code_activation_from_queue = {
    200: {"model": SuccessResponseGetUnlockCodeRequestAndActivationFromQueue,
          "description": "Job status of an unlock code activation was successfully retrieved from the queue."},
    500: model_error_request_queue}

response_model_get_unlock_code_revocation_from_queue = {
    200: {"model": SuccessResponseGetUnlockCodeRevocationFromQueue,
          "description": "Job status of an unlock code revocation was successfully retrieved from the queue."},
    500: model_error_request_queue}
