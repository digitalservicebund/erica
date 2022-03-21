import os

import orjson
from opyoid import Provider
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from erica.infrastructure.sqlalchemy.EricaAuftragSchema import EricaAuftragSchema

DATABASE_URL = 'postgresql://postgres:postgres@localhost/db'


def orjson_serializer(obj):
    """
        Note that `orjson.dumps()` return byte array, while sqlalchemy expects string, thus `decode()` call.
    """
    return orjson.dumps(obj, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NAIVE_UTC).decode()


def orjson_deserializer(json):
    return orjson.loads(json)


uri = DATABASE_URL or os.getenv('DB_URI')
engine = create_engine(DATABASE_URL, json_serializer=orjson_serializer, json_deserializer=orjson_deserializer)
if not database_exists(engine.url):
    create_database(engine.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_migrations():
    __create_tables_if_not_exists()


def __create_tables_if_not_exists():
    # NOTE:  use Alembic for migrations (https://alembic.sqlalchemy.org/en/latest/)
    EricaAuftragSchema.metadata.create_all(bind=engine)


class DatabaseSessionProvider(Provider[Session]):
    def get(self) -> Session:
        return SessionLocal()
