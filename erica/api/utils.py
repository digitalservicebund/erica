from uuid import UUID


def generate_error_response(errorcode=-1, errormessage="API resource not yet implemented."):
    """
    Generator of error response for the API v2.
            Parameters:
                    errorcode (int): the error code number.
                    errormessage (str): the error message.
            Returns:
                    (dict): dict with error respones object.
    """
    error_response = {"errorCode": errorcode,
                      "errorMessage": errormessage
                      }
    return error_response


def get_entity_not_found_log_message(request_id: UUID):
    return "Job with id " + str(request_id) + " not present in the queue."
