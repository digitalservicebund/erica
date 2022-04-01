import logging
import os
from datetime import datetime
import click
import sys
sys.path.append(os.getcwd())
from erica.config import get_settings
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository
from opyoid import Injector
from erica.infrastructure.infrastructure_module import InfrastructureModule


@click.group()
def cli():
    pass


@cli.command()
def delete_success_fail_entities():
    injector = Injector([InfrastructureModule()])
    eric_request_repo = injector.inject(EricaRequestRepository)
    entities_deleted = eric_request_repo.delete_success_fail_old_entities(
        get_settings().ttl_success_fail_entities_in_min)
    logging.getLogger().debug(
        str(entities_deleted) + " success/fail entities deleted at " + datetime.now().strftime("%H:%M:%S"),
        exc_info=True)


@cli.command()
def update_status_not_finished_entities():
    injector = Injector([InfrastructureModule()])
    erica_request_repo = injector.inject(EricaRequestRepository)
    entities_updated = erica_request_repo.update_status_not_finished_entities_to_failed(
        get_settings().ttl_not_finished_entities_in_min)
    logging.getLogger().debug(
        str(entities_updated) + " processing entities  set to failedat " + datetime.now().strftime("%H:%M:%S"),
        exc_info=True)


if __name__ == "__main__":
    cli()
