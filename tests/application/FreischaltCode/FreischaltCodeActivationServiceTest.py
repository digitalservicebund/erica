import unittest
from ctypes import c_int
from unittest.mock import Mock, patch, MagicMock, mock_open
from opyoid import Module

import pytest
from erica.application.FreischaltCode.FreischaltCodeActivationService import FreischaltCodeActivationService

from erica.erica_legacy.config import get_settings
from tests.erica_legacy.utils import gen_random_key, missing_cert, missing_pyeric_lib
from erica.erica_legacy.pyeric.eric import EricWrapper, EricDruckParameterT, EricVerschluesselungsParameterT, EricResponse, \
    get_eric_wrapper
from erica.erica_legacy.pyeric.eric_errors import EricProcessNotSuccessful, EricNullReturnedError, EricGlobalError
from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepositoryInterface
from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface

TEST_CERTIFICATE_PATH = 'erica/erica_legacy/instances/blueprint/cert.pfx'


class FreischaltCodeActivationServiceTest(unittest.TestCase):
    
    def given_freischaltcode_dto_when_queue_then_entity_created_in_repository(self):
        entity = Mock()
        freischaltcode_repository_mock = Mock()
        
        entity.id
        freischaltcode_repository_mock.create.return_value = entity
        
        service = FreischaltCodeActivationService(freischaltcode_repository_mock, Mock())
        
        



@pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGetEricWrapper(unittest.TestCase):
    def test_calls_initialise(self):
        with patch('erica.erica_legacy.pyeric.eric.EricWrapper.initialise') as init_fun, \
                patch('erica.erica_legacy.pyeric.eric.EricWrapper.shutdown'), \
                patch('builtins.open', mock_open()):
            with get_eric_wrapper():
                # Test the context manager
                pass

            init_fun.assert_called_once()

    def test_calls_shutdown(self):
        with patch('erica.erica_legacy.pyeric.eric.EricWrapper.initialise'), \
             patch('erica.erica_legacy.pyeric.eric.EricWrapper.shutdown') as shutdown_fun, \
                patch('builtins.open', mock_open()):
            with get_eric_wrapper():
                # Test the context manager
                pass

            shutdown_fun.assert_called_once()