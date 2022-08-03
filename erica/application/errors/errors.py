from erica.domain.shared.erica_request import RequestType


class RequestTypeDoesNotMatchEndpointError(Exception):
    """ Raised in case an entity was requested that has a different type than the requested endpoint. For example you
    request /check_tax_number_validity/1234 but the request with the request_id 1234 is of type grundsteuer. """

    def __init__(self, actual_type: RequestType, requested_type: RequestType):
        self.actual_type = actual_type
        self.requested_type = requested_type
