from erica.request_processing.erica_input.v2.erica_input import ErrorRequestQueue, ResponseGetFromQueue, \
    ResponseGetSendEstFromQueue, ResponseGetTaxNumberValidityFromQueue, \
    ResponseGetUnlockCodeRequestAndActivationFromQueue, ResponseGetUnlockCodeRevocationFromQueue

response_model_post_to_queue = {
    201: {"description": "Job was successfully submitted to the queue and the job id was returned."},
    422: {"model": ErrorRequestQueue, "description": "Job could not be submitted to the queue."}}

response_model_get_est_validation_from_queue = {
    200: {"model": ResponseGetFromQueue,
          "description": "Job status of an est validation was successfully retrieved from the queue."},
    500: {"model": ErrorRequestQueue, "description": "Job status could not be retrieved from the queue."}}

response_model_get_send_est_from_queue = {
    200: {"model": ResponseGetSendEstFromQueue,
          "description": "Job status of a sent est was successfully retrieved from the queue."},
    500: {"model": ErrorRequestQueue, "description": "Job status could not be retrieved from the queue."}}

response_model_get_tax_number_validity_from_queue = {
    200: {"model": ResponseGetTaxNumberValidityFromQueue,
          "description": "Job status of a tax number validity was successfully retrieved from the queue."},
    500: {"model": ErrorRequestQueue, "description": "Job status could not be retrieved from the queue."}}

response_model_get_unlock_code_request_from_queue = {
    200: {"model": ResponseGetUnlockCodeRequestAndActivationFromQueue,
          "description": "Job status of an unlock code request was successfully retrieved from the queue."},
    500: {"model": ErrorRequestQueue, "description": "Job status could not be retrieved from the queue."}}

response_model_get_unlock_code_activation_from_queue = {
    200: {"model": ResponseGetUnlockCodeRequestAndActivationFromQueue,
          "description": "Job status of an unlock code activation was successfully retrieved from the queue."},
    500: {"model": ErrorRequestQueue, "description": "Job status could not be retrieved from the queue."}}

response_model_get_unlock_code_revocation_from_queue = {
    200: {"model": ResponseGetUnlockCodeRevocationFromQueue,
          "description": "Job status of an unlock code revocation was successfully retrieved from the queue."},
    500: {"model": ErrorRequestQueue, "description": "Job status could not be retrieved from the queue."}}
