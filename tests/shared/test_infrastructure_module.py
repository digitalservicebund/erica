import pytest
from opyoid import Injector

from erica.shared.infrastructure_module import InfrastructureModule
from erica.shared.sqlalchemy.database import DatabaseSessionProvider
from erica.shared.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository


class TestInfrastructureModule:

    @pytest.mark.usefixtures('fake_db_connection_in_settings')
    def test_if_used_to_inject_erica_req_repository_then_db_connection_correct_injected(self):
        injector = Injector([InfrastructureModule()])
        erica_request_repository = injector.inject(EricaRequestRepository)

        assert erica_request_repository.db_connection.bind.url == DatabaseSessionProvider().get().bind.url