from erica.application.Shared.response_dto import JobState
from erica.domain.Shared.Status import Status


def map_status(status: Status):
    """
    Mapper from internal rq job state to API job state.
            Parameters:
                    status (Status): the internal rq job state.
            Returns:
                    (JobState): the corresponding API job state.
    """
    switcher = {
        Status.new: JobState.PROCESSING,
        Status.scheduled: JobState.PROCESSING,
        Status.processing: JobState.PROCESSING,
        Status.failed: JobState.FAILURE,
        Status.success: JobState.SUCCESS
    }
    return switcher.get(status)
