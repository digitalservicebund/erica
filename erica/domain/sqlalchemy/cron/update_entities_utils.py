import logging
from datetime import datetime
from logging.config import dictConfig

import click
from opyoid import Injector

from erica.config import get_settings
from erica.domain.infrastructure_module import InfrastructureModule
from erica.domain.sqlalchemy.database import session_scope
from erica.domain.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository


@click.group()
def cli():
    pass


@cli.command()
def delete_success_fail_entities():
    injector = Injector([InfrastructureModule()])
    eric_request_repo = injector.inject(EricaRequestRepository)
    entities_deleted = eric_request_repo.delete_success_fail_old_entities(
        get_settings().ttl_finished_request_entities_in_min)
    logging.getLogger().debug(
        str(entities_deleted) + " success/fail entities deleted at " + datetime.now().strftime("%H:%M:%S"))


@cli.command()
def set_not_processed_entities_to_failed():
    injector = Injector([InfrastructureModule()])
    erica_request_repo = injector.inject(EricaRequestRepository)
    entities_updated = erica_request_repo.set_not_processed_entities_to_failed(
        get_settings().ttl_processing_request_entities_in_min)
    if entities_updated > 0:
        logging.getLogger().error(
            f"{entities_updated} new/scheduled/processing entities set to failed at {datetime.now().strftime('%H:%M:%S')}")
    else:
        logging.getLogger().info(f"No entities set to failed at {datetime.now().strftime('%H:%M:%S')}")


dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s%(levelname)s%(name)s%(message)s%(module)s%(lineno)s%(process)d%(thread)d",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
        }
    },
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "default"
        }
    },
    "root": {
        "level": logging.INFO,
        "handlers": ["stderr"]
    },
    "disable_existing_loggers": False
})

if __name__ == "__main__":
    from erica.worker.huey import init_db_session
    init_db_session()
    with session_scope():
        cli()
