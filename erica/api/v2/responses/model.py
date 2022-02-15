from erica.request_processing.erica_input.v2.erica_input import ErrorRequestQueue, ResponseGetFromQueue

response_model_post_to_queue = {
    201: {"description": "Job was successfully submitted to the queue and the job id was returned."},
    422: {"model": ErrorRequestQueue, "description": "Job could not be submitted to the queue."}}

response_model_get_from_queue = {
    200: {"model": ResponseGetFromQueue, "description": "Job status was successfully retrieved from the queue."},
    500: {"model": ErrorRequestQueue, "description": "Job status could not be retrieved from the queue."}}
