from datetime import timedelta
from unittest.mock import MagicMock, call, patch
from uuid import uuid4

import pytest
from freezegun import freeze_time

from erica.erica_worker.jobs.job import perform_job
from erica.erica_shared.model.erica_request import Status
from erica.erica_worker.pyeric.eric_errors import EricProcessNotSuccessful, EricGlobalValidationError, \
    EricTransferError, EricAlreadyRequestedError
from erica.erica_shared.sqlalchemy.repositories.base_repository import EntityNotFoundError


class TestJob:

    def test_if_service_raises_not_raisable_error_then_job_does_not_raise_error(self):
        mock_apply_to_elster = MagicMock(side_effect=EricProcessNotSuccessful(3))
        mock_service = MagicMock(apply_to_elster=mock_apply_to_elster)
        perform_job(request_id=uuid4(), repository=MagicMock(), service=mock_service,
                              payload_type=MagicMock(), logger=MagicMock())

    def test_if_service_raises_error_then_log_error_in_warning_logger(self):
        mock_apply_to_elster = MagicMock(side_effect=EricProcessNotSuccessful(610201215))
        mock_service = MagicMock(apply_to_elster=mock_apply_to_elster)
        warning_logger = MagicMock()
        logger = MagicMock(warning=warning_logger)

        perform_job(request_id=uuid4(), repository=MagicMock(), service=mock_service,
                              payload_type=MagicMock(), logger=logger)

        assert any("Job failed" in logged_msg[1][0] for logged_msg in warning_logger.mock_calls)

    def test_if_service_raises_transfer_error_then_log_error_with_elster_error_code_in_warning_logger(self):
        mock_apply_to_elster = MagicMock(side_effect=EricTransferError(
            610101210, b'<xml/>', b'<xml/>', {'TH_RES_CODE': "0", 'TH_ERR_MSG': "A message - do you copy?", 'NDH_ERR_XML': "<xml/>"}))
        mock_service = MagicMock(apply_to_elster=mock_apply_to_elster)
        warning_logger = MagicMock()
        logger = MagicMock(warning=warning_logger)

        with patch("erica.erica_worker.jobs.job.get_error_codes_from_server_err_msg", MagicMock(return_value="1234")):
            perform_job(request_id=uuid4(), repository=MagicMock(), service=mock_service,
                        payload_type=MagicMock(), logger=logger)

        assert any("Job failed" in logged_msg[1][0] for logged_msg in warning_logger.mock_calls)
        assert any("1234" in logged_msg[1][0] for logged_msg in warning_logger.mock_calls)

    def test_if_service_raises_special_transfer_error_then_log_error_without_elster_error_code_in_warning_logger(self):
        mock_apply_to_elster = MagicMock(side_effect=EricAlreadyRequestedError(
            b'<xml/>', b'<xml/>', {'TH_RES_CODE': "0", 'TH_ERR_MSG': "A message - do you copy?", 'NDH_ERR_XML': "<xml/>"}))
        mock_service = MagicMock(apply_to_elster=mock_apply_to_elster)
        warning_logger = MagicMock()
        logger = MagicMock(warning=warning_logger)

        with patch("erica.erica_worker.jobs.job.get_error_codes_from_server_err_msg", MagicMock(return_value="1234")):
            perform_job(request_id=uuid4(), repository=MagicMock(), service=mock_service,
                        payload_type=MagicMock(), logger=logger)

        assert any("Job failed" in logged_msg[1][0] for logged_msg in warning_logger.mock_calls)
        assert any("1234" not in logged_msg[1][0] for logged_msg in warning_logger.mock_calls)

    def test_if_service_raises_error_then_update_entity_in_database_with_correct_values(self):
        mock_entity = MagicMock(id="R2-D2", request_id="C3PO")
        mock_get_by_job_request_id = MagicMock(return_value=mock_entity)
        mock_update = MagicMock()
        mock_repository = MagicMock(get_by_job_request_id=mock_get_by_job_request_id, update=mock_update)
        mock_service = MagicMock(apply_to_elster=MagicMock(side_effect=EricTransferError(
            eric_response=f"<xml>Eric Response</xml>".encode(),
            server_response=f"<xml>Server Response</xml>".encode())))

        perform_job(request_id=uuid4(), repository=mock_repository, service=mock_service,
                              payload_type=MagicMock(), logger=MagicMock())

        assert mock_entity.error_code == EricProcessNotSuccessful().generate_error_response().get('message')
        assert mock_entity.error_message == EricProcessNotSuccessful().generate_error_response().get('message')
        assert mock_entity.result is None
        assert mock_entity.status == Status.failed
        assert mock_update.mock_calls == [call(mock_entity.id, mock_entity)]

    def test_if_service_raises_error_with_validation_problems_then_update_entity_in_database_with_correct_values(self):
        validation_problems = "These are not the Ericas you are looking for"
        mock_entity = MagicMock(id="R2-D2", request_id="C3PO")
        mock_get_by_job_request_id = MagicMock(return_value=mock_entity)
        mock_update = MagicMock()
        mock_repository = MagicMock(get_by_job_request_id=mock_get_by_job_request_id, update=mock_update)
        mock_service = MagicMock(apply_to_elster=MagicMock(side_effect=EricGlobalValidationError(
            eric_response=f"<xml><Text>{validation_problems}</Text></xml>".encode())))

        perform_job(request_id=uuid4(), repository=mock_repository, service=mock_service,
                              payload_type=MagicMock(), logger=MagicMock())

        assert mock_entity.error_code == EricProcessNotSuccessful().generate_error_response().get('message')
        assert mock_entity.error_message == EricProcessNotSuccessful().generate_error_response().get('message')
        assert mock_entity.result == {'validation_errors': [validation_problems]}
        assert mock_entity.status == Status.failed
        assert mock_update.mock_calls == [call(mock_entity.id, mock_entity)]

    @freeze_time("Jan 3th, 1892", auto_tick_seconds=15)
    def test_if_service_raises_error_then_log_runtime_of_job(self):
        mock_apply_to_elster = MagicMock(side_effect=EricProcessNotSuccessful(610201215))
        mock_service = MagicMock(apply_to_elster=mock_apply_to_elster)
        info_logger = MagicMock()
        logger = MagicMock(info=info_logger)

        perform_job(request_id=uuid4(), repository=MagicMock(), service=mock_service,
                              payload_type=MagicMock(), logger=logger)

        assert any("Job running time" in logged_msg[1][0] for logged_msg in info_logger.mock_calls)
        assert any(f"{timedelta(seconds=15)}" in logged_msg[1][0] for logged_msg in info_logger.mock_calls)

    def test_if_entity_not_found_then_raise_error(self):
        mock_get_by_job_request_id = MagicMock(side_effect=EntityNotFoundError)
        mock_repository = MagicMock(get_by_job_request_id=mock_get_by_job_request_id)

        with pytest.raises(EntityNotFoundError):
            perform_job(request_id=uuid4(), repository=mock_repository, service=MagicMock(),
                              payload_type=MagicMock(), logger=MagicMock())

    def test_if_entity_not_found_then_log_error_in_warning_logger(self):
        mock_get_by_job_request_id = MagicMock(side_effect=EntityNotFoundError)
        mock_repository = MagicMock(get_by_job_request_id=mock_get_by_job_request_id)
        warning_logger = MagicMock()
        logger = MagicMock(warning=warning_logger)
        request_id = uuid4()

        with pytest.raises(EntityNotFoundError):
            perform_job(request_id=request_id, repository=mock_repository, service=MagicMock(),
                              payload_type=MagicMock(), logger=logger)

        assert any(f"{request_id}" in logged_msg[1][0] for logged_msg in warning_logger.mock_calls)
        assert any("Entity not found" in logged_msg[1][0] for logged_msg in warning_logger.mock_calls)

    def test_if_entity_exists_then_log_start_of_job_in_info_logger(self):
        info_logger = MagicMock()
        logger = MagicMock(info=info_logger)

        perform_job(request_id=uuid4(), repository=MagicMock(), service=MagicMock(), payload_type=MagicMock(),
                          logger=logger)

        assert any("Job started" in logged_msg[1][0] for logged_msg in info_logger.mock_calls)

    def test_if_entity_exists_then_call_service_with_parsed_entity_payload_and_include_elster_response_true(self):
        mock_entity = MagicMock(id="R2-D2", request_id="C3PO")
        mock_repository = MagicMock(get_by_job_request_id=MagicMock(return_value=mock_entity))
        payload_type_parse_obj = MagicMock()
        mock_apply_to_elster = MagicMock()
        service = MagicMock(apply_to_elster=mock_apply_to_elster)

        perform_job(request_id=uuid4(), repository=mock_repository, service=service,
                          payload_type=MagicMock(parse_obj=payload_type_parse_obj), logger=MagicMock())

        assert mock_apply_to_elster.mock_calls[0] == call(payload_type_parse_obj(mock_entity), True)

    def test_if_job_ran_successful_then_update_entity_in_database_with_correct_values(self):
        mock_entity = MagicMock(id="R2-D2", request_id="C3PO")
        mock_get_by_job_request_id = MagicMock(return_value=mock_entity)
        mock_update = MagicMock()
        mock_repository = MagicMock(get_by_job_request_id=mock_get_by_job_request_id, update=mock_update)
        mock_result = {'msg': "These are not the mocks you are looking for"}
        service = MagicMock(apply_to_elster=MagicMock(return_value=mock_result))

        perform_job(request_id=uuid4(), repository=mock_repository, service=service, payload_type=MagicMock(),
                          logger=MagicMock())

        assert mock_entity.result == {**mock_result}
        assert mock_entity.status == Status.success
        assert mock_update.mock_calls == [call(mock_entity.id, mock_entity)]

    def test_if_job_ran_successful_then_ids_type_and_payload_of_entity_not_changed(self):
        original_id = "R2-D2"
        original_request_id = "C3P0"
        original_type = "droid"
        mock_entity = MagicMock(id=original_id, request_id=original_request_id, type=original_type)
        mock_get_by_job_request_id = MagicMock(return_value=mock_entity)
        mock_update = MagicMock()
        mock_repository = MagicMock(get_by_job_request_id=mock_get_by_job_request_id, update=mock_update)
        mock_result = {'msg': "These are not the mocks you are looking for"}
        service = MagicMock(apply_to_elster=MagicMock(return_value=mock_result))

        perform_job(request_id=uuid4(), repository=mock_repository, service=service, payload_type=MagicMock(),
                          logger=MagicMock())

        assert mock_entity.id == original_id
        assert mock_entity.request_id == original_request_id
        assert mock_entity.type == original_type

    def test_if_job_ran_successful_then_log_completion_message(self):
        warning_logger = MagicMock()
        logger = MagicMock(warning=warning_logger)

        perform_job(request_id=uuid4(), repository=MagicMock(), service=MagicMock(), payload_type=MagicMock(),
                          logger=logger)

        assert any("Job finished" in logged_msg[1][0] for logged_msg in warning_logger.mock_calls)

    @freeze_time("Jan 3th, 1892", auto_tick_seconds=15)
    def test_if_job_ran_successful_then_log_runtime_of_job(self):
        info_logger = MagicMock()
        logger = MagicMock(info=info_logger)

        perform_job(request_id=uuid4(), repository=MagicMock(), service=MagicMock(), payload_type=MagicMock(),
                          logger=logger)

        assert any("Job running time" in logged_msg[1][0] for logged_msg in info_logger.mock_calls)
        assert any(f"{timedelta(seconds=15)}" in logged_msg[1][0] for logged_msg in info_logger.mock_calls)
